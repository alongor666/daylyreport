import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

/**
 * 筛选器状态管理
 * 管理所有筛选维度的选项和当前选中的筛选条件
 */
export const useFilterStore = defineStore('filter', () => {
  // ========== State ==========

  // 所有可用的筛选选项 (从后端获取)
  const filterOptions = ref({})

  // 当前激活的筛选条件
  // 格式: { '三级机构': '成都', '是否新能源': '是' }
  const activeFilters = ref({})

  // 筛选面板展开状态
  const panelOpen = ref(false)

  // 筛选选项加载状态
  const loading = ref(false)

  // ========== 全局筛选状态（新增） ==========
  // 时间段: day | last7d | last30d
  const timePeriod = ref('day')

  // 数据口径: exclude_correction | include_correction
  const dataScope = ref('exclude_correction')

  // 业务类型: 客户类别3（摩托车/挂车/特种车等）
  const businessType = ref('')

  // 保单号→业务员→机构/团队映射
  const policyMapping = ref({
    policy_to_staff: {},
    staff_to_info: {},
    conflicts: []
  })

  // ========== Getters ==========

  /**
   * 是否有激活的筛选条件
   */
  const hasActiveFilters = computed(() => {
    return Object.keys(activeFilters.value).length > 0
  })

  /**
   * 激活的筛选数量（含时间段、数据口径、业务类型）
   */
  const activeFiltersCount = computed(() => {
    let count = 0

    // 时间段（非默认值计数）
    if (timePeriod.value !== 'day') count++

    // 数据口径（非默认值计数）
    if (dataScope.value !== 'exclude_correction') count++

    // 业务类型
    if (businessType.value) count++

    // 其他筛选条件
    Object.values(activeFilters.value).forEach(v => {
      if (v) count++
    })

    return count
  })

  /**
   * 格式化的筛选标签列表（含时间段、数据口径、业务类型）
   * 格式: [{ key: 'timePeriod', label: '时间: 近7天' }, { key: '三级机构', label: '三级机构: 成都' }]
   */
  const filterTags = computed(() => {
    const tags = []

    // 时间段标签
    if (timePeriod.value !== 'day') {
      const labels = { last7d: '近7天', last30d: '近30天' }
      tags.push({
        key: 'timePeriod',
        label: `时间: ${labels[timePeriod.value] || timePeriod.value}`
      })
    }

    // 数据口径标签
    if (dataScope.value === 'include_correction') {
      tags.push({
        key: 'dataScope',
        label: '数据: 含批改'
      })
    }

    // 业务类型标签
    if (businessType.value) {
      tags.push({
        key: 'businessType',
        label: `业务类型: ${businessType.value}`
      })
    }

    // 其他筛选标签
    Object.entries(activeFilters.value).forEach(([key, value]) => {
      if (value) {
        tags.push({
          key,
          value,
          label: `${key}: ${value}`
        })
      }
    })

    return tags
  })

  /**
   * 获取特定维度的选项
   * @param {string} dimension - 维度名称
   */
  function getOptions(dimension) {
    return filterOptions.value[dimension] || []
  }

  /**
   * 获取团队选项 (根据选中的机构动态过滤)
   */
  const teamOptions = computed(() => {
    const selectedOrg = activeFilters.value['三级机构']
    const orgTeamMap = filterOptions.value['机构团队映射'] || {}

    if (selectedOrg && orgTeamMap[selectedOrg]) {
      return orgTeamMap[selectedOrg]
    }

    // 如果没有选择机构,返回所有团队
    return filterOptions.value['团队'] || []
  })

  // ========== Actions ==========

  /**
   * 从后端加载筛选选项
   * 注意：同时加载保单号映射，以支持基于保单号的唯一筛选
   */
  async function loadFilterOptions() {
    loading.value = true
    try {
      const [optResp, mapResp] = await Promise.all([
        axios.get('/api/filter-options'),
        axios.get('/api/policy-mapping')
      ])
      if (optResp.data.success) {
        filterOptions.value = optResp.data.data
      }
      if (mapResp.data.success) {
        policyMapping.value = mapResp.data.data
      }
    } catch (error) {
      console.error('Failed to load filter options:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  /**
   * 根据保单号解析并返回对应的业务员与机构/团队信息
   * @param {string} policyNo - 保单号
   * @returns {{ staff: string|null, org: string|null, org4: string|null, team: string|null }}
   */
  function resolveByPolicy(policyNo) {
    const staff = policyMapping.value.policy_to_staff?.[policyNo] || null
    const info = staff ? (policyMapping.value.staff_to_info?.[staff] || null) : null
    return {
      staff,
      org: info?.['三级机构'] || null,
      org4: info?.['四级机构'] || null,
      team: info?.['团队简称'] || null
    }
  }

  /**
   * 根据业务员解析并返回所属的机构/团队信息
   * 函数用途：用于“业务员”主筛选的联动，自动填充三级机构与团队简称
   * 入参：staff（字符串，业务员姓名或唯一标识）
   * 出参：{ org: string|null, org4: string|null, team: string|null }
   */
  function resolveByStaff(staff) {
    const info = policyMapping.value.staff_to_info?.[staff] || null
    return {
      org: info?.['三级机构'] || null,
      org4: info?.['四级机构'] || null,
      team: info?.['团队简称'] || null
    }
  }

  /**
   * 应用单个筛选条件
   * @param {string} key - 筛选维度
   * @param {string} value - 筛选值
   */
  function applyFilter(key, value) {
    if (value) {
      activeFilters.value[key] = value

      // 若选择保单号：自动联动设置业务员、团队、三级机构，以映射为准
      if (key === '保单号') {
        const linked = resolveByPolicy(value)
        if (linked.staff) {
          activeFilters.value['业务员'] = linked.staff
        }
        if (linked.org) {
          activeFilters.value['三级机构'] = linked.org
        }
        if (linked.team) {
          activeFilters.value['团队'] = linked.team
        } else {
          // 若映射中无团队简称，清除团队筛选以避免不一致
          delete activeFilters.value['团队']
        }
      }

      // 若选择业务员：自动联动设置团队与三级机构，以映射为准
      if (key === '业务员') {
        const linked = resolveByStaff(value)
        if (linked.org) {
          activeFilters.value['三级机构'] = linked.org
        }
        if (linked.team) {
          activeFilters.value['团队'] = linked.team
        } else {
          delete activeFilters.value['团队']
        }
      }

      // 如果修改了机构,清除团队选择
      if (key === '三级机构' && activeFilters.value['团队']) {
        const orgTeamMap = filterOptions.value['机构团队映射'] || {}
        const validTeams = orgTeamMap[value] || []

        // 如果当前选择的团队不在新机构的团队列表中,清除团队选择
        if (!validTeams.includes(activeFilters.value['团队'])) {
          delete activeFilters.value['团队']
        }
      }
    } else {
      // 如果value为空,移除该筛选
      delete activeFilters.value[key]
    }
  }

  /**
   * 移除单个筛选条件（支持时间段、数据口径、业务类型）
   * @param {string} key - 筛选维度
   */
  function removeFilter(key) {
    if (key === 'timePeriod') {
      timePeriod.value = 'day'
    } else if (key === 'dataScope') {
      dataScope.value = 'exclude_correction'
    } else if (key === 'businessType') {
      businessType.value = ''
    } else {
      delete activeFilters.value[key]
    }
  }

  /**
   * 批量应用筛选条件
   * @param {object} filters - 筛选条件对象
   */
  function applyFilters(filters) {
    activeFilters.value = { ...filters }
  }

  /**
   * 重置所有筛选条件（包括时间段、数据口径、业务类型）
   */
  function resetFilters() {
    timePeriod.value = 'day'
    dataScope.value = 'exclude_correction'
    businessType.value = ''
    activeFilters.value = {}
  }

  /**
   * 切换筛选面板展开状态
   */
  function togglePanel() {
    panelOpen.value = !panelOpen.value
  }

  /**
   * 打开筛选面板
   */
  function openPanel() {
    panelOpen.value = true
  }

  /**
   * 关闭筛选面板
   */
  function closePanel() {
    panelOpen.value = false
  }

  /**
   * 获取当前筛选条件的副本 (用于API请求)
   */
  function getActiveFilters() {
    return { ...activeFilters.value }
  }

  /**
   * 设置时间段
   * @param {string} period - 时间段 ('day' | 'last7d' | 'last30d')
   */
  function setTimePeriod(period) {
    const validPeriods = ['day', 'last7d', 'last30d']
    if (!validPeriods.includes(period)) {
      console.error('Invalid time period:', period)
      return
    }
    timePeriod.value = period
  }

  /**
   * 设置数据口径
   * @param {string} scope - 数据口径 ('exclude_correction' 或 'include_correction')
   */
  function setDataScope(scope) {
    const validScopes = ['exclude_correction', 'include_correction']
    if (!validScopes.includes(scope)) {
      console.error('Invalid data scope:', scope)
      return
    }
    dataScope.value = scope
  }

  /**
   * 设置业务类型
   * @param {string} type - 业务类型（客户类别3）
   */
  function setBusinessType(type) {
    businessType.value = type
  }

  /**
   * 获取数据口径
   */
  function getDataScope() {
    return dataScope.value
  }

  /**
   * 保存当前筛选状态快照（用于回滚）
   */
  function saveSnapshot() {
    return {
      timePeriod: timePeriod.value,
      dataScope: dataScope.value,
      businessType: businessType.value,
      activeFilters: { ...activeFilters.value }
    }
  }

  /**
   * 恢复筛选状态快照
   * @param {object} snapshot - 快照对象
   */
  function restoreSnapshot(snapshot) {
    timePeriod.value = snapshot.timePeriod
    dataScope.value = snapshot.dataScope
    businessType.value = snapshot.businessType
    activeFilters.value = { ...snapshot.activeFilters }
  }

  /**
   * 获取完整的全局筛选参数（包含时间段、数据口径、业务类型、其他筛选）
   * 用于全局筛选面板
   */
  function getAllGlobalFilters() {
    const filters = {}

    // 业务类型
    if (businessType.value) {
      filters.business_type = businessType.value
    }

    // 其他筛选条件（过滤空值）
    Object.entries(activeFilters.value).forEach(([key, value]) => {
      if (value) {
        filters[key] = value
      }
    })

    return {
      time_period: timePeriod.value,
      data_scope: dataScope.value,
      filters
    }
  }

  /**
   * 获取完整的筛选参数 (包含普通筛选和数据口径)
   * 保留此方法用于向后兼容
   */
  function getAllFilters() {
    return {
      filters: { ...activeFilters.value },
      data_scope: dataScope.value
    }
  }

  // ========== Return ==========

  return {
    // State
    filterOptions,
    activeFilters,
    panelOpen,
    loading,
    policyMapping,
    // ========== 新增状态 ==========
    timePeriod,
    dataScope,
    businessType,

    // Getters
    hasActiveFilters,
    activeFiltersCount,
    filterTags,
    teamOptions,
    getOptions,
    resolveByPolicy,
    resolveByStaff,

    // Actions
    loadFilterOptions,
    applyFilter,
    removeFilter,
    applyFilters,
    resetFilters,
    togglePanel,
    openPanel,
    closePanel,
    getActiveFilters,
    // ========== 新增 Actions ==========
    setTimePeriod,
    setDataScope,
    setBusinessType,
    getDataScope,
    getAllFilters,
    getAllGlobalFilters,
    saveSnapshot,
    restoreSnapshot
  }
})
