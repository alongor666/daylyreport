<template>
  <div class="global-filter">
    <!-- 固定区（置顶，始终可见） -->
    <div class="global-filter__fixed">
      <!-- 条件栏（Summary Bar） -->
      <div class="global-filter__summary">
        <div class="global-filter__summary-bar">
          <span class="global-filter__icon" aria-hidden="true">🔍</span>
          <div class="global-filter__conditions" role="status" aria-live="polite">
            <template v-if="activeSummaryTags.length === 0">
              <span class="global-filter__empty-text">无筛选条件</span>
            </template>
            <template v-else>
              <!-- 显示前6个条件，用点号分隔 -->
              <template v-for="(tag, index) in visibleTags" :key="tag.key">
                <button
                  class="global-filter__tag-compact"
                  :aria-label="`移除筛选条件: ${tag.label}`"
                  @click="handleRemoveTag(tag.key)"
                  :title="`点击移除: ${tag.label}`"
                >
                  {{ tag.label }}
                </button>
                <span v-if="index < visibleTags.length - 1 || hasMoreTags" class="global-filter__separator">·</span>
              </template>
              <!-- 折叠的条件数量 -->
              <button
                v-if="hasMoreTags"
                class="global-filter__tag-more"
                :aria-label="`还有 ${hiddenTagsCount} 个筛选条件`"
                @click="toggleExpandedTags"
              >
                +{{ hiddenTagsCount }}
              </button>
            </template>
          </div>
          <div class="global-filter__summary-actions">
            <button
              v-if="activeSummaryTags.length > 0"
              class="global-filter__clear-all"
              aria-label="清空所有筛选条件"
              @click="handleClearAll"
            >
              清空
            </button>
            <button
              class="global-filter__toggle"
              :class="{ 'global-filter__toggle--open': isPanelOpen }"
              :aria-label="isPanelOpen ? '收起筛选面板' : '展开筛选面板'"
              :aria-expanded="isPanelOpen"
              @click="togglePanel"
              @keydown.f.prevent="togglePanel"
            >
              <span class="global-filter__toggle-icon" aria-hidden="true">
                {{ isPanelOpen ? '▲' : '▼' }}
              </span>
            </button>
          </div>
        </div>

        <!-- 展开的标签层叠面板 -->
        <transition name="fade">
          <div
            v-if="showExpandedTags"
            class="global-filter__expanded-tags"
            role="dialog"
            aria-label="所有筛选条件"
          >
            <button
              v-for="tag in activeSummaryTags"
              :key="tag.key"
              class="global-filter__tag"
              :aria-label="`移除筛选条件: ${tag.label}`"
              @click="handleRemoveTag(tag.key)"
            >
              <span class="global-filter__tag-text">{{ tag.label }}</span>
              <span class="global-filter__tag-close" aria-hidden="true">×</span>
            </button>
          </div>
        </transition>
      </div>

      <!-- 指标切换（独立，与筛选解耦） -->
      <div class="global-filter__metric-toggle" role="radiogroup" aria-label="选择指标类型">
        <button
          v-for="option in metricOptions"
          :key="option.value"
          class="global-filter__metric-button"
          :class="{ 'global-filter__metric-button--active': currentMetric === option.value }"
          role="radio"
          :aria-checked="currentMetric === option.value"
          :aria-label="`${option.label}指标`"
          @click="handleMetricChange(option.value)"
        >
          <span class="global-filter__metric-icon" aria-hidden="true">{{ option.icon }}</span>
          <span class="global-filter__metric-label">{{ option.label }}</span>
        </button>
      </div>
    </div>

    <!-- 可折叠筛选面板（默认收起） -->
    <transition name="panel-expand">
      <div v-if="isPanelOpen" class="global-filter__panel">
        <!-- 1. 时间与口径 -->
        <section class="global-filter__section">
          <h3 class="global-filter__section-title">时间与数据口径</h3>
          <div class="global-filter__section-content">
            <!-- 时间快捷键 -->
            <div class="global-filter__field global-filter__field--full">
              <label class="global-filter__label">时间段</label>
              <div class="global-filter__button-group" role="radiogroup" aria-label="选择时间段">
                <button
                  v-for="period in timePeriodOptions"
                  :key="period.value"
                  class="global-filter__quick-button"
                  :class="{ 'global-filter__quick-button--active': localFilters.time_range === period.value }"
                  role="radio"
                  :aria-checked="localFilters.time_range === period.value"
                  :aria-label="period.label"
                  @click="handleQuickTimeChange(period.value)"
                >
                  {{ period.label }}
                </button>
              </div>
            </div>

            <!-- 数据口径 -->
            <div class="global-filter__field">
              <label class="global-filter__label" for="caliber-select">数据口径</label>
              <select
                id="caliber-select"
                v-model="localFilters.caliber"
                class="global-filter__select"
                aria-label="选择数据口径"
              >
                <option value="exclude_endorse">不含批改</option>
                <option value="include_endorse">包含批改</option>
              </select>
            </div>
          </div>
        </section>

        <!-- 2. 组织维度 -->
        <section class="global-filter__section">
          <h3 class="global-filter__section-title">组织维度</h3>
          <div class="global-filter__section-content global-filter__grid">
            <!-- 三级机构（可能被锁定） -->
            <div class="global-filter__field">
              <label class="global-filter__label" for="org-select">
                三级机构
                <span v-if="localFilters.org_locked" class="global-filter__lock-icon" aria-label="已锁定">🔒</span>
              </label>
              <select
                id="org-select"
                v-model="localFilters.org"
                class="global-filter__select"
                :disabled="localFilters.org_locked"
                :aria-label="localFilters.org_locked ? '三级机构已锁定' : '选择三级机构'"
                @change="handleOrgChange"
              >
                <option value="">全部</option>
                <option
                  v-for="option in filterOptions['三级机构'] || []"
                  :key="option"
                  :value="option"
                >
                  {{ option }}
                </option>
              </select>
            </div>

            <!-- 团队（可能被锁定） -->
            <div class="global-filter__field">
              <label class="global-filter__label" for="team-select">
                团队
                <span v-if="localFilters.org_locked" class="global-filter__lock-icon" aria-label="已锁定">🔒</span>
              </label>
              <select
                id="team-select"
                v-model="localFilters.team"
                class="global-filter__select"
                :disabled="localFilters.org_locked || !localFilters.org"
                :aria-label="localFilters.org_locked ? '团队已锁定' : '选择团队'"
                @change="handleTeamChange"
              >
                <option value="">全部</option>
                <option
                  v-for="option in teamOptions"
                  :key="option"
                  :value="option"
                >
                  {{ option }}
                </option>
              </select>
            </div>

            <!-- 业务员 -->
            <div class="global-filter__field">
              <label class="global-filter__label" for="salesperson-select">
                业务员
                <span v-if="!isSalespersonAvailable" class="global-filter__field-hint">
                  （需先选机构）
                </span>
              </label>
              <select
                id="salesperson-select"
                v-model="localFilters.salesperson"
                class="global-filter__select"
                :disabled="!isSalespersonAvailable"
                :aria-label="isSalespersonAvailable ? '选择业务员' : '业务员选项不可用，请先选择三级机构'"
                :aria-describedby="!isSalespersonAvailable ? 'salesperson-hint' : undefined"
              >
                <option value="all">全部</option>
                <option
                  v-for="option in salespersonOptions"
                  :key="option"
                  :value="option"
                >
                  {{ option }}
                </option>
              </select>
              <span v-if="!isSalespersonAvailable" id="salesperson-hint" class="global-filter__hint">
                请先选择三级机构，再选择业务员
              </span>
            </div>
          </div>
        </section>

        <!-- 3. 业务属性 -->
        <section class="global-filter__section">
          <h3 class="global-filter__section-title">业务属性</h3>
          <div class="global-filter__section-content global-filter__grid">
            <!-- 客户类别/业务类型 -->
            <div class="global-filter__field">
              <label class="global-filter__label" for="biz-type-select">客户类别</label>
              <select
                id="biz-type-select"
                v-model="localFilters.biz_type"
                class="global-filter__select"
                aria-label="选择客户类别"
                @change="handleBizTypeChange"
              >
                <option value="all">全部</option>
                <option
                  v-for="option in filterOptions['客户类别3'] || []"
                  :key="option"
                  :value="option"
                >
                  {{ option }}
                </option>
              </select>
            </div>

            <!-- 是否新能源 -->
            <div class="global-filter__field">
              <label class="global-filter__label" for="ev-select">是否新能源</label>
              <select
                id="ev-select"
                v-model="localFilters.is_ev"
                class="global-filter__select"
                aria-label="选择是否新能源"
              >
                <option value="all">全部</option>
                <option value="yes">是</option>
                <option value="no">否</option>
              </select>
            </div>

            <!-- 险种大类 -->
            <div class="global-filter__field">
              <label class="global-filter__label" for="insurance-select">险种大类</label>
              <select
                id="insurance-select"
                v-model="localFilters.insurance_category"
                class="global-filter__select"
                aria-label="选择险种大类"
              >
                <option value="all">全部</option>
                <option
                  v-for="option in filterOptions['险别组合'] || []"
                  :key="option"
                  :value="option"
                >
                  {{ option }}
                </option>
              </select>
            </div>

            <!-- 是否续保 -->
            <div class="global-filter__field">
              <label class="global-filter__label" for="renewal-select">是否续保</label>
              <select
                id="renewal-select"
                v-model="localFilters.is_renewal"
                class="global-filter__select"
                aria-label="选择是否续保"
              >
                <option value="all">全部</option>
                <option value="new">新保</option>
                <option value="renewal">续保</option>
              </select>
            </div>

            <!-- 是否过户车 -->
            <div class="global-filter__field">
              <label class="global-filter__label" for="transfer-select">是否过户车</label>
              <select
                id="transfer-select"
                v-model="localFilters.is_transfer"
                class="global-filter__select"
                aria-label="选择是否过户车"
              >
                <option value="all">全部</option>
                <option value="yes">是</option>
                <option value="no">否</option>
              </select>
            </div>

            <!-- 是否异地车 -->
            <div class="global-filter__field">
              <label class="global-filter__label" for="nonlocal-select">是否异地车</label>
              <select
                id="nonlocal-select"
                v-model="localFilters.is_nonlocal"
                class="global-filter__select"
                aria-label="选择是否异地车"
              >
                <option value="all">全部</option>
                <option value="yes">是</option>
                <option value="no">否</option>
              </select>
            </div>

            <!-- 吨位（条件显示） -->
            <div class="global-filter__field">
              <label class="global-filter__label" for="tonnage-select">
                吨位
                <span v-if="!isTonnageAvailable" class="global-filter__field-hint">
                  （仅货车类可用）
                </span>
              </label>
              <select
                id="tonnage-select"
                v-model="localFilters.tonnage"
                class="global-filter__select"
                :disabled="!isTonnageAvailable"
                :aria-label="isTonnageAvailable ? '选择吨位' : '吨位选项不可用，仅货车类业务可选择'"
                :aria-describedby="!isTonnageAvailable ? 'tonnage-hint' : undefined"
              >
                <option value="all">全部</option>
                <option
                  v-for="option in filterOptions['吨位'] || []"
                  :key="option"
                  :value="option"
                >
                  {{ option }}
                </option>
              </select>
              <span v-if="!isTonnageAvailable" id="tonnage-hint" class="global-filter__hint">
                请选择货车类业务类型后再选择吨位
              </span>
            </div>
          </div>
        </section>

        <!-- 4. 操作区 -->
        <div class="global-filter__actions">
          <button
            class="global-filter__button global-filter__button--primary"
            :disabled="!hasPendingChanges"
            :aria-label="hasPendingChanges ? '应用筛选条件' : '没有待应用的变更'"
            @click="handleApplyFilters"
          >
            <span aria-hidden="true">✓</span> 应用筛选
          </button>
          <button
            class="global-filter__button global-filter__button--secondary"
            :aria-label="hasPendingChanges ? '重置未应用的变更' : '重置全部筛选'"
            @click="handleResetFilters"
          >
            <span aria-hidden="true">↻</span> 重置全部
          </button>
        </div>
      </div>
    </transition>

    <!-- 空结果提示 -->
    <transition name="fade">
      <div v-if="showEmptyState" class="global-filter__empty-state" role="alert">
        <div class="global-filter__empty-icon" aria-hidden="true">📊</div>
        <h3 class="global-filter__empty-title">没有匹配的数据</h3>
        <p class="global-filter__empty-text">试试减少筛选条件，或点击"清空"</p>
        <button class="global-filter__button global-filter__button--primary" @click="handleClearAll">
          清空筛选
        </button>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onBeforeUnmount } from 'vue'
import { useFilterStore } from '@/stores/filter'
import { useDataStore } from '@/stores/data'
import { useAppStore } from '@/stores/app'
import { useToast } from '@/composables/useToast'

// ========== Props & Emits ==========
const emit = defineEmits([
  'filter:open',
  'filter:close',
  'filter:change',
  'filter:apply',
  'filter:reset',
  'filter:error',
  'metric:change'
])

// ========== Stores ==========
const filterStore = useFilterStore()
const dataStore = useDataStore()
const appStore = useAppStore()
const toast = useToast()

// ========== State ==========
const isPanelOpen = ref(false)
const isOrgSectionOpen = ref(false)
const showExpandedTags = ref(false)
const showEmptyState = ref(false)

// 本地筛选状态（待应用）
const localFilters = ref({
  time_range: 'last_7_days',
  caliber: 'exclude_endorse',
  biz_type: 'all',
  is_renewal: 'all',
  is_ev: 'all',
  is_transfer: 'all',
  is_nonlocal: 'all',
  insurance_category: 'all',
  tonnage: 'all',
  org_locked: false,
  org: '',
  team: '',
  salesperson: 'all',
  pending_changes: false
})

// 已应用的筛选状态
const appliedFilters = ref({ ...localFilters.value })

// 指标状态（独立）
const currentMetric = ref('premium')

// ========== Constants ==========
const STORAGE_KEY_FILTER = 'insurdash.global_filter.v1'
const STORAGE_KEY_METRIC = 'insurdash.metric.v1'

// 时间段选项
const timePeriodOptions = [
  { value: 'today', label: '当日' },
  { value: 'last_7_days', label: '近7天' },
  { value: 'last_30_days', label: '近30天' }
]

// 指标选项
const metricOptions = [
  { value: 'premium', label: '保费', icon: '¥' },
  { value: 'count', label: '件数', icon: '#' }
]

// 货车类业务类型（用于判断吨位字段是否可用）
const TRUCK_TYPES = ['货车', '挂车', '特种车']

// ========== Computed ==========

// 筛选选项
const filterOptions = computed(() => filterStore.filterOptions)

// 团队选项（根据选中的机构动态过滤）
const teamOptions = computed(() => {
  const selectedOrg = localFilters.value.org
  const orgTeamMap = filterOptions.value['机构团队映射'] || {}

  if (selectedOrg && orgTeamMap[selectedOrg]) {
    return orgTeamMap[selectedOrg]
  }

  return filterOptions.value['团队'] || []
})

// 业务员选项（根据选中的三级机构和团队动态过滤）
const salespersonOptions = computed(() => {
  const selectedOrg = localFilters.value.org
  const selectedTeam = localFilters.value.team
  const staffMapping = filterStore.policyMapping?.staff_to_info || {}

  // 必须先选择三级机构
  if (!selectedOrg) {
    return []
  }

  // 过滤出符合条件的业务员
  const filteredStaff = Object.keys(staffMapping).filter(staffKey => {
    const info = staffMapping[staffKey]

    // 必须匹配选中的三级机构
    if (info['三级机构'] !== selectedOrg) {
      return false
    }

    // 如果选择了团队，必须匹配
    if (selectedTeam && info['团队简称'] !== selectedTeam) {
      return false
    }

    return true
  })

  return filteredStaff
})

// 业务员选择器是否可用
const isSalespersonAvailable = computed(() => {
  return !!localFilters.value.org
})

// 吨位字段是否可用
const isTonnageAvailable = computed(() => {
  const bizType = localFilters.value.biz_type
  return bizType !== 'all' && TRUCK_TYPES.some(type => bizType.includes(type))
})

// 是否有待应用的变更
const hasPendingChanges = computed(() => {
  return JSON.stringify(localFilters.value) !== JSON.stringify(appliedFilters.value)
})

// 活跃的摘要标签（用于条件栏显示）
// 优化规则：按优先级排序，最多显示6个维度
// 优先级顺序：时间段 > 三级机构 > 客户类别(业务类型) > 是否新能源 > 险种大类 > 是否续保 > 是否过户 > 数据口径
const activeSummaryTags = computed(() => {
  const tags = []
  const filters = appliedFilters.value

  // 1. 时间段（最高优先级）
  if (filters.time_range !== 'last_7_days') {
    const period = timePeriodOptions.find(p => p.value === filters.time_range)
    if (period) {
      tags.push({ key: 'time_range', label: period.label, priority: 1 })
    }
  }

  // 2. 三级机构（第二优先级）
  if (filters.org) {
    tags.push({ key: 'org', label: filters.org, priority: 2 })
  }

  // 3. 客户类别/业务类型（第三优先级）
  if (filters.biz_type !== 'all') {
    tags.push({ key: 'biz_type', label: filters.biz_type, priority: 3 })
  }

  // 4. 是否新能源（第四优先级）
  if (filters.is_ev !== 'all') {
    const label = filters.is_ev === 'yes' ? '新能源' : '非新能源'
    tags.push({ key: 'is_ev', label, priority: 4 })
  }

  // 5. 险种大类（第五优先级）
  if (filters.insurance_category !== 'all') {
    tags.push({ key: 'insurance_category', label: filters.insurance_category, priority: 5 })
  }

  // 6. 是否续保（第六优先级）
  if (filters.is_renewal !== 'all') {
    const label = filters.is_renewal === 'new' ? '新保' : '续保'
    tags.push({ key: 'is_renewal', label, priority: 6 })
  }

  // 7. 是否过户车（第七优先级）
  if (filters.is_transfer !== 'all') {
    const label = filters.is_transfer === 'yes' ? '过户车' : '非过户车'
    tags.push({ key: 'is_transfer', label, priority: 7 })
  }

  // 8. 数据口径（第八优先级，仅当非默认时显示）
  if (filters.caliber === 'include_endorse') {
    tags.push({ key: 'caliber', label: '包含批改', priority: 8 })
  }

  // 低优先级维度（不在前8位显示）
  // 是否异地车
  if (filters.is_nonlocal !== 'all') {
    const label = filters.is_nonlocal === 'yes' ? '异地车' : '本地车'
    tags.push({ key: 'is_nonlocal', label, priority: 9 })
  }

  // 吨位
  if (filters.tonnage !== 'all') {
    tags.push({ key: 'tonnage', label: `${filters.tonnage}吨`, priority: 10 })
  }

  // 业务员
  if (filters.salesperson !== 'all') {
    tags.push({ key: 'salesperson', label: filters.salesperson, priority: 11 })
  }

  // 团队
  if (filters.team) {
    tags.push({ key: 'team', label: filters.team, priority: 12 })
  }

  // 按优先级排序
  return tags.sort((a, b) => a.priority - b.priority)
})

// 可见标签（前6个）
const visibleTags = computed(() => {
  return activeSummaryTags.value.slice(0, 6)
})

// 是否有更多标签
const hasMoreTags = computed(() => {
  return activeSummaryTags.value.length > 6
})

// 隐藏的标签数量
const hiddenTagsCount = computed(() => {
  return Math.max(0, activeSummaryTags.value.length - 6)
})

// ========== Methods ==========

/**
 * 切换面板展开/收起
 */
function togglePanel() {
  isPanelOpen.value = !isPanelOpen.value

  if (isPanelOpen.value) {
    emit('filter:open')
  } else {
    // 如果有未应用的改动，给出轻提示
    if (hasPendingChanges.value) {
      toast.info('有未应用的筛选条件')
    }
    emit('filter:close')
  }
}

/**
 * 切换展开的标签
 */
function toggleExpandedTags() {
  showExpandedTags.value = !showExpandedTags.value
}

/**
 * 移除单个标签
 */
function handleRemoveTag(key) {
  const oldValue = localFilters.value[key]

  // 重置该字段为默认值
  if (key === 'time_range') {
    localFilters.value.time_range = 'last_7_days'
  } else if (key === 'caliber') {
    localFilters.value.caliber = 'exclude_endorse'
  } else if (['biz_type', 'is_renewal', 'is_ev', 'is_transfer', 'is_nonlocal', 'insurance_category', 'tonnage', 'salesperson'].includes(key)) {
    localFilters.value[key] = 'all'
  } else {
    localFilters.value[key] = ''
  }

  emit('filter:change', { field: key, oldValue, newValue: localFilters.value[key] })

  // 标记为待应用
  localFilters.value.pending_changes = true
}

/**
 * 清空所有筛选
 */
async function handleClearAll() {
  const defaultFilters = {
    time_range: 'last_7_days',
    caliber: 'exclude_endorse',
    biz_type: 'all',
    is_renewal: 'all',
    is_ev: 'all',
    is_transfer: 'all',
    is_nonlocal: 'all',
    insurance_category: 'all',
    tonnage: 'all',
    org_locked: localFilters.value.org_locked, // 保留锁定状态
    org: localFilters.value.org_locked ? localFilters.value.org : '',
    team: localFilters.value.org_locked ? localFilters.value.team : '',
    salesperson: 'all',
    pending_changes: false
  }

  localFilters.value = { ...defaultFilters }
  appliedFilters.value = { ...defaultFilters }

  // 立即应用
  applyFiltersToStore()

  // 刷新所有图表数据
  await Promise.all([
    dataStore.refreshChartData(),
    dataStore.refreshPieCharts('last7d', {}) // 使用默认时间周期和空筛选
  ])

  // 持久化
  persistFilters()

  toast.success('已清空筛选条件')
  emit('filter:reset')

  // 关闭展开的标签
  showExpandedTags.value = false
}

/**
 * 快速时间切换（立即生效）
 */
function handleQuickTimeChange(timeRange) {
  const oldValue = localFilters.value.time_range
  localFilters.value.time_range = timeRange

  emit('filter:change', { field: 'time_range', oldValue, newValue: timeRange })

  // 立即应用
  appliedFilters.value.time_range = timeRange
  applyFiltersToStore()
  persistFilters()

  toast.info(`已切换到${timePeriodOptions.find(p => p.value === timeRange)?.label}`)
}

/**
 * 三级机构变更处理
 */
function handleOrgChange() {
  // 选择机构后，清空团队选择（需要用户重新选择匹配的团队）
  const selectedOrg = localFilters.value.org
  const selectedTeam = localFilters.value.team

  if (selectedTeam && selectedOrg) {
    const orgTeamMap = filterOptions.value['机构团队映射'] || {}
    const validTeams = orgTeamMap[selectedOrg] || []

    if (!validTeams.includes(selectedTeam)) {
      localFilters.value.team = ''
    }
  } else if (!selectedOrg) {
    // 清空机构时也清空团队
    localFilters.value.team = ''
  }

  // 清空业务员选择（因为可选业务员列表已改变）
  localFilters.value.salesperson = 'all'
}

/**
 * 团队变更处理
 */
function handleTeamChange() {
  // 团队变更后，检查当前选中的业务员是否仍在新的过滤范围内
  const currentSalesperson = localFilters.value.salesperson

  if (currentSalesperson && currentSalesperson !== 'all') {
    // 检查当前业务员是否在新的过滤列表中
    if (!salespersonOptions.value.includes(currentSalesperson)) {
      // 如果不在，清空业务员选择
      localFilters.value.salesperson = 'all'
    }
  }
}

/**
 * 业务类型变更处理
 */
function handleBizTypeChange() {
  // 如果选择的业务类型不是货车类，清空吨位选择
  if (!isTonnageAvailable.value) {
    localFilters.value.tonnage = 'all'
  }
}

/**
 * 应用筛选
 */
async function handleApplyFilters() {
  if (!hasPendingChanges.value) {
    isPanelOpen.value = false
    return
  }

  try {
    // 验证冲突条件
    const conflicts = validateFilters()
    if (conflicts.length > 0) {
      const errorMsg = conflicts.join('; ')
      toast.error('筛选条件冲突', errorMsg)
      emit('filter:error', { fields: conflicts, reason: errorMsg })
      return
    }

    // 计算 diff
    const diff = calculateDiff(appliedFilters.value, localFilters.value)

    // 应用到已应用状态
    appliedFilters.value = { ...localFilters.value }
    appliedFilters.value.pending_changes = false
    localFilters.value.pending_changes = false

    // 同步到 store
    applyFiltersToStore()

    // 刷新所有图表数据（周对比图 + 饼图）
    await Promise.all([
      dataStore.refreshChartData(),
      dataStore.refreshPieCharts(appliedFilters.value.time_range === 'today' ? 'day' :
                                  appliedFilters.value.time_range === 'last_7_days' ? 'last7d' : 'last30d',
                                  filterStore.getActiveFilters())
    ])

    // 持久化
    persistFilters()

    toast.success('筛选已应用')
    emit('filter:apply', { filters: { ...appliedFilters.value }, diff })

    isPanelOpen.value = false
  } catch (error) {
    console.error('应用筛选失败:', error)
    toast.error('应用筛选失败', error.message)
    emit('filter:error', { reason: error.message })
  }
}

/**
 * 重置筛选
 */
function handleResetFilters() {
  if (hasPendingChanges.value) {
    // 重置未应用的改动
    localFilters.value = { ...appliedFilters.value }
    toast.info('已重置未应用的改动')
  } else {
    // 重置为默认值
    handleClearAll()
  }
}

/**
 * 指标切换
 */
async function handleMetricChange(metric) {
  if (metric === currentMetric.value) return

  const oldMetric = currentMetric.value
  currentMetric.value = metric

  // 同步到 appStore
  appStore.switchMetric(metric)

  // 持久化
  persistMetric()

  // 刷新数据
  try {
    await dataStore.refreshChartData()
    toast.info(`已切换到${metric === 'premium' ? '保费' : '件数'}指标`)
    emit('metric:change', { oldMetric, newMetric: metric })
  } catch (error) {
    console.error('切换指标失败:', error)
    toast.error('切换指标失败', error.message)
  }
}

/**
 * 验证筛选条件
 */
function validateFilters() {
  const conflicts = []

  // 示例：如果业务类型是"摩托车"，吨位应该为"all"
  if (localFilters.value.biz_type !== 'all' &&
      !isTonnageAvailable.value &&
      localFilters.value.tonnage !== 'all') {
    conflicts.push('吨位仅适用于货车类业务')
  }

  return conflicts
}

/**
 * 计算 diff
 */
function calculateDiff(oldFilters, newFilters) {
  const diff = {}
  for (const key in newFilters) {
    if (oldFilters[key] !== newFilters[key]) {
      diff[key] = {
        old: oldFilters[key],
        new: newFilters[key]
      }
    }
  }
  return diff
}

/**
 * 同步筛选到 store
 */
function applyFiltersToStore() {
  const filters = appliedFilters.value

  // 同步时间段
  filterStore.setTimePeriod(filters.time_range === 'today' ? 'day' :
                            filters.time_range === 'last_7_days' ? 'last7d' : 'last30d')

  // 同步数据口径
  filterStore.setDataScope(filters.caliber === 'exclude_endorse' ? 'exclude_correction' : 'include_correction')

  // 同步其他筛选条件
  const activeFilters = {}

  if (filters.biz_type !== 'all') {
    activeFilters['客户类别3'] = filters.biz_type
  }

  if (filters.is_renewal !== 'all') {
    activeFilters['是否续保'] = filters.is_renewal === 'new' ? '新保' : '续保'
  }

  if (filters.is_ev !== 'all') {
    activeFilters['是否新能源'] = filters.is_ev === 'yes' ? '是' : '否'
  }

  if (filters.is_transfer !== 'all') {
    activeFilters['是否过户车'] = filters.is_transfer === 'yes' ? '是' : '否'
  }

  if (filters.is_nonlocal !== 'all') {
    activeFilters['是否异地车'] = filters.is_nonlocal === 'yes' ? '是' : '否'
  }

  if (filters.insurance_category !== 'all') {
    activeFilters['险别组合'] = filters.insurance_category
  }

  if (filters.tonnage !== 'all') {
    activeFilters['吨位'] = filters.tonnage
  }

  if (filters.salesperson !== 'all') {
    activeFilters['业务员'] = filters.salesperson
  }

  if (filters.org) {
    activeFilters['三级机构'] = filters.org
  }

  if (filters.team) {
    activeFilters['团队'] = filters.team
  }

  filterStore.applyFilters(activeFilters)
}

/**
 * 持久化筛选状态
 */
function persistFilters() {
  try {
    localStorage.setItem(STORAGE_KEY_FILTER, JSON.stringify(appliedFilters.value))
  } catch (error) {
    console.error('持久化筛选失败:', error)
  }
}

/**
 * 持久化指标状态
 */
function persistMetric() {
  try {
    localStorage.setItem(STORAGE_KEY_METRIC, currentMetric.value)
  } catch (error) {
    console.error('持久化指标失败:', error)
  }
}

/**
 * 恢复持久化状态
 */
function restorePersistedState() {
  try {
    // 恢复筛选
    const savedFilters = localStorage.getItem(STORAGE_KEY_FILTER)
    if (savedFilters) {
      const parsed = JSON.parse(savedFilters)

      // 提示用户是否沿用
      const confirmed = confirm('是否沿用上次的筛选条件？')
      if (confirmed) {
        localFilters.value = { ...parsed }
        appliedFilters.value = { ...parsed }
        applyFiltersToStore()
      }
    }

    // 恢复指标
    const savedMetric = localStorage.getItem(STORAGE_KEY_METRIC)
    if (savedMetric) {
      currentMetric.value = savedMetric
      appStore.switchMetric(savedMetric)
    }
  } catch (error) {
    console.error('恢复持久化状态失败:', error)
  }
}

/**
 * 键盘事件处理
 */
function handleKeydown(event) {
  // F 键聚焦到展开/收起开关
  if (event.key === 'f' && !event.ctrlKey && !event.metaKey) {
    event.preventDefault()
    togglePanel()
  }

  // Esc 键关闭面板
  if (event.key === 'Escape' && isPanelOpen.value) {
    if (hasPendingChanges.value) {
      toast.info('有未应用的筛选条件')
    }
    isPanelOpen.value = false
  }
}

// ========== Lifecycle ==========

onMounted(async () => {
  // 加载筛选选项
  try {
    await filterStore.loadFilterOptions()
  } catch (error) {
    console.error('加载筛选选项失败:', error)
    toast.error('加载筛选选项失败', error.message)
  }

  // 恢复持久化状态
  restorePersistedState()

  // 监听键盘事件
  document.addEventListener('keydown', handleKeydown)
})

onBeforeUnmount(() => {
  document.removeEventListener('keydown', handleKeydown)
})

// ========== Watchers ==========

// 监听路由上下文变化（机构锁定）
watch(
  () => appStore.currentOrg,
  (newOrg) => {
    if (newOrg) {
      localFilters.value.org_locked = true
      localFilters.value.org = newOrg.name
      localFilters.value.team = newOrg.team || ''

      // 如果已应用状态不同，标记为待应用
      if (appliedFilters.value.org !== newOrg.name || appliedFilters.value.team !== newOrg.team) {
        localFilters.value.pending_changes = true
        toast.info('机构上下文已变化，请确认筛选条件')
      }
    } else {
      localFilters.value.org_locked = false
    }
  }
)
</script>

<style scoped>
/* ========== 基础样式 ========== */
.global-filter {
  background: white;
  border: 1px solid var(--gray-200);
  border-radius: var(--radius-lg);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  overflow: hidden;
  transition: box-shadow 0.2s;
}

.global-filter:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

/* ========== 固定区 ========== */
.global-filter__fixed {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-6);
  padding: var(--space-5) var(--space-6);
  border-bottom: 1px solid var(--gray-200);
  background: linear-gradient(to bottom, #fafafa 0%, #ffffff 100%);
}

/* ========== 条件栏 ========== */
.global-filter__summary {
  flex: 1;
  position: relative;
}

.global-filter__summary-bar {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.global-filter__icon {
  font-size: var(--font-lg);
  flex-shrink: 0;
}

.global-filter__conditions {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 4px;
  flex-wrap: nowrap;
  overflow: hidden;
}

.global-filter__empty-text {
  color: var(--gray-500);
  font-size: var(--font-sm);
}

/* 紧凑型标签 - 点号分隔风格 */
.global-filter__tag-compact {
  display: inline-flex;
  align-items: center;
  padding: 0;
  background: none;
  border: none;
  font-size: var(--font-sm);
  color: var(--gray-700);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
  text-decoration: underline;
  text-decoration-color: transparent;
  text-underline-offset: 2px;
}

.global-filter__tag-compact:hover {
  color: var(--primary-600);
  text-decoration-color: var(--primary-600);
}

.global-filter__tag-compact:focus {
  outline: 2px solid var(--primary-500);
  outline-offset: 2px;
  border-radius: 2px;
}

/* 分隔符 */
.global-filter__separator {
  color: var(--gray-400);
  font-size: var(--font-sm);
  user-select: none;
  margin: 0 2px;
}

/* 更多标签按钮 */
.global-filter__tag-more {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 2px 8px;
  background: var(--primary-50);
  border: 1px solid var(--primary-200);
  border-radius: var(--radius-full);
  font-size: var(--font-xs);
  color: var(--primary-700);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
  margin-left: 2px;
}

.global-filter__tag-more:hover {
  background: var(--primary-100);
  border-color: var(--primary-300);
  color: var(--primary-800);
}

.global-filter__tag-more:focus {
  outline: 2px solid var(--primary-500);
  outline-offset: 2px;
}

/* 保留旧版标签样式用于展开面板 */
.global-filter__tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 8px 4px 12px;
  background: var(--gray-100);
  border: 1px solid var(--gray-300);
  border-radius: var(--radius-full);
  font-size: var(--font-xs);
  color: var(--gray-700);
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.global-filter__tag:hover {
  background: var(--gray-200);
  border-color: var(--gray-400);
}

.global-filter__tag:focus {
  outline: 2px solid var(--primary-500);
  outline-offset: 2px;
}

.global-filter__tag-text {
  font-weight: 500;
}

.global-filter__tag-close {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 16px;
  height: 16px;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  font-size: 14px;
  font-weight: 700;
  line-height: 1;
  transition: all 0.2s;
}

.global-filter__tag:hover .global-filter__tag-close {
  background: var(--error-500);
  color: white;
}

.global-filter__summary-actions {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.global-filter__clear-all {
  padding: 6px 12px;
  background: none;
  border: 1px solid var(--gray-300);
  border-radius: var(--radius-md);
  font-size: var(--font-xs);
  color: var(--gray-700);
  cursor: pointer;
  transition: all 0.2s;
  font-family: inherit;
}

.global-filter__clear-all:hover {
  border-color: var(--error-500);
  color: var(--error-500);
}

.global-filter__clear-all:focus {
  outline: 2px solid var(--error-500);
  outline-offset: 2px;
}

.global-filter__toggle {
  padding: 8px 12px;
  background: white;
  border: 1px solid var(--gray-300);
  border-radius: var(--radius-md);
  color: var(--gray-600);
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.global-filter__toggle:hover {
  border-color: var(--primary-400);
  color: var(--primary-600);
  background: var(--primary-50);
  box-shadow: 0 2px 4px rgba(168, 85, 247, 0.15);
}

.global-filter__toggle:focus {
  outline: 2px solid var(--primary-500);
  outline-offset: 2px;
}

.global-filter__toggle--open {
  background: var(--primary-100);
  border-color: var(--primary-500);
  color: var(--primary-700);
  box-shadow: 0 2px 6px rgba(168, 85, 247, 0.2);
}

.global-filter__toggle-icon {
  font-size: 12px;
  display: inline-block;
  transition: transform 0.2s;
}

.global-filter__toggle--open .global-filter__toggle-icon {
  transform: rotate(180deg);
}

/* 展开的标签层叠面板 */
.global-filter__expanded-tags {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  margin-top: var(--space-2);
  padding: var(--space-3);
  background: white;
  border: 1px solid var(--gray-300);
  border-radius: var(--radius-md);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 10;
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
}

/* ========== 指标切换 ========== */
.global-filter__metric-toggle {
  display: flex;
  gap: 4px;
  background: var(--gray-100);
  padding: 4px;
  border-radius: var(--radius-lg);
}

.global-filter__metric-button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border: none;
  background: transparent;
  color: var(--gray-600);
  font-size: var(--font-sm);
  font-weight: 500;
  border-radius: calc(var(--radius-lg) - 2px);
  cursor: pointer;
  transition: all 0.2s;
  font-family: inherit;
  white-space: nowrap;
}

.global-filter__metric-button:hover:not(.global-filter__metric-button--active) {
  background: rgba(255, 255, 255, 0.6);
  color: var(--gray-700);
}

.global-filter__metric-button:focus {
  outline: 2px solid var(--primary-500);
  outline-offset: 2px;
}

.global-filter__metric-button--active {
  background: white;
  color: var(--primary-600);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  font-weight: 600;
}

.global-filter__metric-icon {
  font-size: var(--font-base);
}

/* ========== 筛选面板 ========== */
.global-filter__panel {
  padding: var(--space-6);
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

.global-filter__section {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.global-filter__section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding: 0;
  background: none;
  border: none;
  cursor: pointer;
  text-align: left;
}

.global-filter__section-header:focus {
  outline: 2px solid var(--primary-500);
  outline-offset: 2px;
  border-radius: var(--radius-sm);
}

.global-filter__section-title {
  font-size: var(--font-base);
  font-weight: 700;
  color: var(--gray-800);
  margin: 0;
  letter-spacing: 0.01em;
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.global-filter__section-title::before {
  content: '';
  display: inline-block;
  width: 3px;
  height: 14px;
  background: var(--primary-500);
  border-radius: 2px;
}

.global-filter__section-toggle {
  color: var(--gray-500);
  font-size: 12px;
}

.global-filter__section-content {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.global-filter__grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--space-4);
}

.global-filter__field {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.global-filter__field--full {
  grid-column: 1 / -1;
}

.global-filter__label {
  font-size: var(--font-sm);
  font-weight: 600;
  color: var(--gray-700);
  display: flex;
  align-items: center;
  gap: var(--space-1);
}

.global-filter__lock-icon {
  font-size: var(--font-xs);
}

.global-filter__field-hint {
  font-weight: 400;
  color: var(--gray-500);
  font-size: var(--font-xs);
}

.global-filter__hint {
  font-size: var(--font-xs);
  color: var(--gray-500);
}

.global-filter__select {
  padding: 8px 12px;
  border: 1px solid var(--gray-300);
  border-radius: var(--radius-md);
  font-size: var(--font-sm);
  color: var(--gray-900);
  background: white;
  cursor: pointer;
  transition: all 0.2s;
  font-family: inherit;
}

.global-filter__select:hover:not(:disabled) {
  border-color: var(--primary-500);
}

.global-filter__select:focus {
  outline: none;
  border-color: var(--primary-500);
  box-shadow: 0 0 0 3px rgba(168, 85, 247, 0.1);
}

.global-filter__select:disabled {
  background: var(--gray-100);
  cursor: not-allowed;
  opacity: 0.6;
}

.global-filter__button-group {
  display: flex;
  gap: 4px;
  background: var(--gray-100);
  padding: 4px;
  border-radius: var(--radius-lg);
}

.global-filter__quick-button {
  flex: 1;
  padding: 8px 16px;
  border: none;
  background: transparent;
  color: var(--gray-600);
  font-size: var(--font-sm);
  font-weight: 500;
  border-radius: calc(var(--radius-lg) - 2px);
  cursor: pointer;
  transition: all 0.2s;
  font-family: inherit;
  white-space: nowrap;
}

.global-filter__quick-button:hover:not(.global-filter__quick-button--active) {
  background: rgba(255, 255, 255, 0.6);
  color: var(--gray-700);
}

.global-filter__quick-button:focus {
  outline: 2px solid var(--primary-500);
  outline-offset: 2px;
}

.global-filter__quick-button--active {
  background: white;
  color: var(--primary-600);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  font-weight: 600;
}

/* ========== 操作区 ========== */
.global-filter__actions {
  display: flex;
  gap: var(--space-3);
  justify-content: flex-start;
  padding-top: var(--space-4);
  border-top: 1px solid var(--gray-200);
}

.global-filter__button {
  padding: 10px 20px;
  border: none;
  border-radius: var(--radius-md);
  font-size: var(--font-sm);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  font-family: inherit;
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
}

.global-filter__button:focus {
  outline: 2px solid var(--primary-500);
  outline-offset: 2px;
}

.global-filter__button--primary {
  background: linear-gradient(135deg, var(--primary-600) 0%, var(--primary-700) 100%);
  color: white;
  position: relative;
  overflow: hidden;
}

.global-filter__button--primary::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.global-filter__button--primary:hover:not(:disabled)::before {
  left: 100%;
}

.global-filter__button--primary:hover:not(:disabled) {
  background: linear-gradient(135deg, var(--primary-700) 0%, var(--primary-800) 100%);
  box-shadow: 0 6px 16px rgba(168, 85, 247, 0.35);
  transform: translateY(-1px);
}

.global-filter__button--primary:active:not(:disabled) {
  transform: translateY(0);
  box-shadow: 0 2px 8px rgba(168, 85, 247, 0.25);
}

.global-filter__button--primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: var(--gray-300);
}

.global-filter__button--secondary {
  background: white;
  color: var(--gray-700);
  border: 1px solid var(--gray-300);
}

.global-filter__button--secondary:hover {
  border-color: var(--primary-500);
  color: var(--primary-600);
}

/* ========== 空结果提示 ========== */
.global-filter__empty-state {
  padding: var(--space-8);
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-4);
}

.global-filter__empty-icon {
  font-size: 48px;
}

.global-filter__empty-title {
  font-size: var(--font-lg);
  font-weight: 600;
  color: var(--gray-900);
  margin: 0;
}

.global-filter__empty-text {
  font-size: var(--font-sm);
  color: var(--gray-600);
  margin: 0;
}

/* ========== 动画 ========== */
.panel-expand-enter-active,
.panel-expand-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

.panel-expand-enter-from,
.panel-expand-leave-to {
  opacity: 0;
  max-height: 0;
}

.panel-expand-enter-to,
.panel-expand-leave-from {
  opacity: 1;
  max-height: 2000px;
}

.section-expand-enter-active,
.section-expand-leave-active {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

.section-expand-enter-from,
.section-expand-leave-to {
  opacity: 0;
  max-height: 0;
}

.section-expand-enter-to,
.section-expand-leave-from {
  opacity: 1;
  max-height: 500px;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* ========== 响应式 ========== */
@media (max-width: 768px) {
  .global-filter__fixed {
    flex-direction: column;
    align-items: stretch;
  }

  .global-filter__grid {
    grid-template-columns: 1fr;
  }

  .global-filter__actions {
    flex-direction: column;
  }

  .global-filter__button {
    width: 100%;
    justify-content: center;
  }
}

/* ========== 高对比度模式 ========== */
@media (prefers-contrast: high) {
  .global-filter__tag,
  .global-filter__select,
  .global-filter__button {
    border-width: 2px;
  }
}
</style>
