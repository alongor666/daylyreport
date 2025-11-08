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

  // ========== Getters ==========

  /**
   * 是否有激活的筛选条件
   */
  const hasActiveFilters = computed(() => {
    return Object.keys(activeFilters.value).length > 0
  })

  /**
   * 激活的筛选数量
   */
  const activeFiltersCount = computed(() => {
    return Object.keys(activeFilters.value).length
  })

  /**
   * 格式化的筛选标签列表
   * 格式: [{ key: '三级机构', value: '成都', label: '三级机构: 成都' }]
   */
  const filterTags = computed(() => {
    return Object.entries(activeFilters.value).map(([key, value]) => ({
      key,
      value,
      label: `${key}: ${value}`
    }))
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
   */
  async function loadFilterOptions() {
    loading.value = true
    try {
      const response = await axios.get('/api/filter-options')
      if (response.data.success) {
        filterOptions.value = response.data.data
      }
    } catch (error) {
      console.error('Failed to load filter options:', error)
      throw error
    } finally {
      loading.value = false
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
   * 移除单个筛选条件
   * @param {string} key - 筛选维度
   */
  function removeFilter(key) {
    delete activeFilters.value[key]
  }

  /**
   * 批量应用筛选条件
   * @param {object} filters - 筛选条件对象
   */
  function applyFilters(filters) {
    activeFilters.value = { ...filters }
  }

  /**
   * 重置所有筛选条件
   */
  function resetFilters() {
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

  // ========== Return ==========

  return {
    // State
    filterOptions,
    activeFilters,
    panelOpen,
    loading,

    // Getters
    hasActiveFilters,
    activeFiltersCount,
    filterTags,
    teamOptions,
    getOptions,

    // Actions
    loadFilterOptions,
    applyFilter,
    removeFilter,
    applyFilters,
    resetFilters,
    togglePanel,
    openPanel,
    closePanel,
    getActiveFilters
  }
})
