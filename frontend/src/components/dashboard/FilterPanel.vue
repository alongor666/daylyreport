<template>
  <div class="filter-panel">
    <!-- Header -->
    <div class="filter-panel__header" @click="togglePanel">
      <div class="filter-panel__title-group">
        <h3 class="filter-panel__title">
          <span class="filter-panel__icon">🔍</span>
          数据筛选
        </h3>
        <span v-if="activeFiltersCount > 0" class="filter-panel__badge">
          {{ activeFiltersCount }}
        </span>
      </div>
      <button class="filter-panel__toggle" :class="{ 'filter-panel__toggle--open': isOpen }">
        <span class="filter-panel__toggle-icon">{{ isOpen ? '▼' : '▶' }}</span>
      </button>
    </div>

    <!-- Active Filter Tags -->
    <div v-if="activeFiltersCount > 0 && !isOpen" class="filter-panel__tags">
      <div
        v-for="tag in filterTags"
        :key="tag.key"
        class="filter-panel__tag"
      >
        <span class="filter-panel__tag-text">{{ tag.label }}</span>
        <button
          class="filter-panel__tag-remove"
          @click.stop="handleRemoveFilter(tag.key)"
          title="移除筛选"
        >
          ×
        </button>
      </div>
      <button
        v-if="activeFiltersCount > 1"
        class="filter-panel__clear-all"
        @click.stop="handleResetFilters"
      >
        清空全部
      </button>
    </div>

    <!-- Filter Form (Collapsible) -->
    <transition name="filter-panel-expand">
      <div v-if="isOpen" class="filter-panel__body">
        <div class="filter-panel__grid">
          <!-- 业务员（主筛选维度） -->
          <div class="filter-panel__field">
            <label class="filter-panel__label">业务员</label>
            <select
              v-model="localFilters['业务员']"
              class="filter-panel__select"
              @change="handleFilterChange('业务员')"
            >
              <option value="">全部业务员</option>
              <option
                v-for="option in (filterOptions['业务员'] || [])"
                :key="option"
                :value="option"
              >
                {{ option }}
              </option>
            </select>
          </div>

          <!-- 三级机构 -->
          <div class="filter-panel__field">
            <label class="filter-panel__label">三级机构</label>
            <select
              v-model="localFilters['三级机构']"
              class="filter-panel__select"
              @change="handleFilterChange('三级机构')"
              :disabled="!!localFilters['业务员']"
            >
              <option value="">全部机构</option>
              <option
                v-for="option in filterOptions['三级机构']"
                :key="option"
                :value="option"
              >
                {{ option }}
              </option>
            </select>
          </div>

          <!-- 团队 (联动) -->
          <div class="filter-panel__field">
            <label class="filter-panel__label">团队</label>
            <select
              v-model="localFilters['团队']"
              class="filter-panel__select"
              @change="handleFilterChange('团队')"
              :disabled="!localFilters['三级机构'] || !!localFilters['业务员']"
            >
              <option value="">全部团队</option>
              <option
                v-for="option in teamOptions"
                :key="option"
                :value="option"
              >
                {{ option }}
              </option>
            </select>
          </div>

          <!-- 是否续保 -->
          <div class="filter-panel__field">
            <label class="filter-panel__label">是否续保</label>
            <select
              v-model="localFilters['是否续保']"
              class="filter-panel__select"
              @change="handleFilterChange('是否续保')"
            >
              <option value="">全部</option>
              <option
                v-for="option in filterOptions['是否续保']"
                :key="option"
                :value="option"
              >
                {{ option }}
              </option>
            </select>
          </div>

          <!-- 是否新能源 -->
          <div class="filter-panel__field">
            <label class="filter-panel__label">是否新能源</label>
            <select
              v-model="localFilters['是否新能源']"
              class="filter-panel__select"
              @change="handleFilterChange('是否新能源')"
            >
              <option value="">全部</option>
              <option
                v-for="option in filterOptions['是否新能源']"
                :key="option"
                :value="option"
              >
                {{ option }}
              </option>
            </select>
          </div>

          <!-- 是否过户车 -->
          <div class="filter-panel__field">
            <label class="filter-panel__label">是否过户车</label>
            <select
              v-model="localFilters['是否过户车']"
              class="filter-panel__select"
              @change="handleFilterChange('是否过户车')"
            >
              <option value="">全部</option>
              <option
                v-for="option in filterOptions['是否过户车']"
                :key="option"
                :value="option"
              >
                {{ option }}
              </option>
            </select>
          </div>

          <!-- 是否异地车 -->
          <div class="filter-panel__field">
            <label class="filter-panel__label">是否异地车</label>
            <select
              v-model="localFilters['是否异地车']"
              class="filter-panel__select"
              @change="handleFilterChange('是否异地车')"
            >
              <option value="">全部</option>
              <option
                v-for="option in (filterOptions['是否异地车'] || [])"
                :key="option"
                :value="option"
              >
                {{ option }}
              </option>
            </select>
          </div>

          <!-- 险种大类 -->
          <div class="filter-panel__field">
            <label class="filter-panel__label">险种大类</label>
            <select
              v-model="localFilters['险种大类']"
              class="filter-panel__select"
              @change="handleFilterChange('险种大类')"
            >
              <option value="">全部险种</option>
              <option
                v-for="option in filterOptions['险种大类']"
                :key="option"
                :value="option"
              >
                {{ option }}
              </option>
            </select>
          </div>

          <!-- 吨位 -->
          <div class="filter-panel__field">
            <label class="filter-panel__label">吨位</label>
            <select
              v-model="localFilters['吨位']"
              class="filter-panel__select"
              @change="handleFilterChange('吨位')"
            >
              <option value="">全部吨位</option>
              <option
                v-for="option in filterOptions['吨位']"
                :key="option"
                :value="option"
              >
                {{ option }}
              </option>
            </select>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="filter-panel__actions">
          <button
            class="filter-panel__button filter-panel__button--primary"
            @click="handleApplyFilters"
            :disabled="!hasChanges"
          >
            应用筛选
          </button>
          <button
            class="filter-panel__button filter-panel__button--secondary"
            @click="handleResetFilters"
          >
            重置
          </button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useFilterStore } from '@/stores/filter'
import { useDataStore } from '@/stores/data'
import { useAppStore } from '@/stores/app'
import { useTheme } from '@/composables/useTheme'
import { useToast } from '@/composables/useToast'

// Stores
const filterStore = useFilterStore()
const dataStore = useDataStore()
const appStore = useAppStore()

// Theme
const theme = useTheme('filterPanel')

// Toast
const toast = useToast()

// State
const isOpen = ref(false)
const localFilters = ref({})

// Computed
const filterOptions = computed(() => filterStore.filterOptions)
const activeFiltersCount = computed(() => filterStore.activeFiltersCount)
const filterTags = computed(() => filterStore.filterTags)

const teamOptions = computed(() => {
  const selectedOrg = localFilters.value['三级机构']
  const orgTeamMap = filterOptions.value['机构团队映射'] || {}

  if (selectedOrg && orgTeamMap[selectedOrg]) {
    return orgTeamMap[selectedOrg]
  }

  return filterOptions.value['团队'] || []
})

const hasChanges = computed(() => {
  const current = filterStore.activeFilters
  const local = localFilters.value

  // 比较两个对象是否相同
  const currentKeys = Object.keys(current).sort()
  const localKeys = Object.keys(local).filter(key => local[key]).sort()

  if (currentKeys.length !== localKeys.length) return true

  return currentKeys.some(key => current[key] !== local[key])
})

// Methods
/**
 * 切换筛选面板展开/收起状态
 * 说明：点击面板头部时触发；面板展开时同步当前激活筛选到本地副本
 */
function togglePanel() {
  isOpen.value = !isOpen.value
  if (isOpen.value) {
    // 打开面板时,同步本地筛选器
    syncLocalFilters()
  }
}

/**
 * 同步本地筛选数据
 * 说明：用于将 Pinia 中的激活筛选复制到本地 `localFilters`
 */
function syncLocalFilters() {
  localFilters.value = { ...filterStore.activeFilters }
}

/**
 * 处理筛选项变更
 * 参数：key 为变更的筛选维度名称
 * 规则：
 * - 选择“三级机构”后校验并必要时清空不属于该机构的“团队”
 * - 选择“保单号”后依据映射自动填充“三级机构/团队”，同时锁定联动字段
 */
function handleFilterChange(key) {
  // 如果选择了机构,清除团队选择(如果新机构下没有该团队)
  if (key === '三级机构') {
    const selectedOrg = localFilters.value['三级机构']
    const selectedTeam = localFilters.value['团队']

    if (selectedTeam && selectedOrg) {
      const orgTeamMap = filterOptions.value['机构团队映射'] || {}
      const validTeams = orgTeamMap[selectedOrg] || []

      if (!validTeams.includes(selectedTeam)) {
        localFilters.value['团队'] = ''
      }
    }
  }

  // 若选择业务员：根据映射自动填充机构与团队，并锁定相关字段
  if (key === '业务员') {
    const staff = localFilters.value['业务员']
    if (staff) {
      const linked = filterStore.resolveByStaff(staff)
      if (linked.org) {
        localFilters.value['三级机构'] = linked.org
      }
      if (linked.team) {
        localFilters.value['团队'] = linked.team
      } else {
        localFilters.value['团队'] = ''
      }
    } else {
      // 清除联动锁定
      localFilters.value['三级机构'] = ''
      localFilters.value['团队'] = ''
    }
  }
}

/**
 * 应用当前筛选
 * 流程：
 * 1) 过滤空值 → 生成待应用的筛选对象
 * 2) 若包含“保单号”，依据映射补充“业务员/三级机构/团队”，并清理缺失团队场景
 * 3) 提交到 Pinia 并触发数据刷新
 */
async function handleApplyFilters() {
  if (!hasChanges.value) {
    isOpen.value = false
    return
  }

  try {
    // 过滤掉空值
    const filtersToApply = Object.fromEntries(
      Object.entries(localFilters.value).filter(([_, value]) => value)
    )

    // 若选择了业务员：依据映射补充三级机构/团队，确保一致性
    if (filtersToApply['业务员']) {
      const linked = filterStore.resolveByStaff(filtersToApply['业务员'])
      if (linked.org) {
        filtersToApply['三级机构'] = linked.org
      }
      if (linked.team) {
        filtersToApply['团队'] = linked.team
      } else {
        delete filtersToApply['团队']
      }
    }

    filterStore.applyFilters(filtersToApply)

    // 刷新图表数据
    await dataStore.refreshChartData()

    toast.success('筛选已应用')
    isOpen.value = false
  } catch (error) {
    console.error('应用筛选失败:', error)
    toast.error('应用筛选失败', error.message)
  }
}

/**
 * 重置所有筛选
 * 说明：清空本地与 Pinia 的筛选条件，并刷新图表数据
 */
function handleResetFilters() {
  localFilters.value = {}
  filterStore.resetFilters()

  // 刷新图表数据
  dataStore.refreshChartData().catch((error) => {
    console.error('刷新数据失败:', error)
  })

  toast.info('筛选已重置')
}

/**
 * 移除单个筛选标签
 * 参数：key 为要移除的筛选维度
 * 行为：更新 Pinia 后刷新图表
 */
function handleRemoveFilter(key) {
  filterStore.removeFilter(key)

  // 刷新图表数据
  dataStore.refreshChartData().catch((error) => {
    console.error('刷新数据失败:', error)
  })
}

// Lifecycle
/**
 * 组件挂载时初始化筛选选项
 * 流程：调用后端接口加载筛选选项与保单映射 → 同步到本地
 */
onMounted(async () => {
  // 加载筛选选项
  try {
    await filterStore.loadFilterOptions()
    syncLocalFilters()
  } catch (error) {
    console.error('加载筛选选项失败:', error)
    toast.error('加载筛选选项失败', error.message)
  }
})

// Watch
watch(
  () => filterStore.activeFilters,
  () => {
    if (!isOpen.value) {
      syncLocalFilters()
    }
  },
  { deep: true }
)
</script>

<style scoped>
.filter-panel {
  background: v-bind('theme.business.value.cardBg');
  border: v-bind('theme.business.value.cardBorder');
  border-radius: v-bind('theme.radius.value.lg');
  box-shadow: v-bind('theme.business.value.cardShadow');
  overflow: hidden;
}

/* Header */
.filter-panel__header {
  padding: v-bind('theme.spacing.value.lg') v-bind('theme.spacing.value.xl');
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  user-select: none;
  transition: background-color 0.2s;
}

.filter-panel__header:hover {
  background: rgba(0, 0, 0, 0.02);
}

.filter-panel__title-group {
  display: flex;
  align-items: center;
  gap: v-bind('theme.spacing.value.md');
}

.filter-panel__title {
  font-size: v-bind('theme.typography.value.lg');
  font-weight: 600;
  color: v-bind('theme.colors.value.textPrimary');
  margin: 0;
  display: flex;
  align-items: center;
  gap: v-bind('theme.spacing.value.sm');
}

.filter-panel__icon {
  font-size: 18px;
}

.filter-panel__badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 20px;
  height: 20px;
  padding: 0 6px;
  background: v-bind('theme.colors.value.primary');
  color: white;
  font-size: 11px;
  font-weight: 700;
  border-radius: 10px;
}

.filter-panel__toggle {
  background: none;
  border: none;
  padding: 8px;
  cursor: pointer;
  color: v-bind('theme.colors.value.textSecondary');
  transition: all 0.2s;
}

.filter-panel__toggle:hover {
  color: v-bind('theme.colors.value.primary');
}

.filter-panel__toggle-icon {
  display: inline-block;
  font-size: 12px;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.filter-panel__toggle--open .filter-panel__toggle-icon {
  transform: rotate(0deg);
}

/* Tags */
.filter-panel__tags {
  padding: 0 v-bind('theme.spacing.value.xl') v-bind('theme.spacing.value.lg');
  display: flex;
  align-items: center;
  gap: v-bind('theme.spacing.value.sm');
  flex-wrap: wrap;
}

.filter-panel__tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 8px 4px 12px;
  background: v-bind('theme.colors.value.bgTint');
  border: 1px solid v-bind('theme.colors.value.border');
  border-radius: v-bind('theme.radius.value.full');
  font-size: v-bind('theme.typography.value.xs');
  color: v-bind('theme.colors.value.textSecondary');
}

.filter-panel__tag-text {
  font-weight: 500;
}

.filter-panel__tag-remove {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 16px;
  height: 16px;
  background: rgba(0, 0, 0, 0.1);
  border: none;
  border-radius: 50%;
  color: v-bind('theme.colors.value.textSecondary');
  font-size: 14px;
  font-weight: 700;
  line-height: 1;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-panel__tag-remove:hover {
  background: v-bind('theme.colors.value.error');
  color: white;
}

.filter-panel__clear-all {
  padding: 4px 12px;
  background: none;
  border: 1px solid v-bind('theme.colors.value.border');
  border-radius: v-bind('theme.radius.value.full');
  font-size: v-bind('theme.typography.value.xs');
  color: v-bind('theme.colors.value.textSecondary');
  cursor: pointer;
  transition: all 0.2s;
  font-family: v-bind('theme.typography.value.fontFamily');
}

.filter-panel__clear-all:hover {
  border-color: v-bind('theme.colors.value.error');
  color: v-bind('theme.colors.value.error');
}

/* Body */
.filter-panel__body {
  padding: v-bind('theme.spacing.value.lg') v-bind('theme.spacing.value.xl');
  border-top: v-bind('theme.business.value.divider');
  display: flex;
  flex-direction: column;
  gap: v-bind('theme.spacing.value.xl');
}

.filter-panel__grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: v-bind('theme.spacing.value.lg');
}

.filter-panel__field {
  display: flex;
  flex-direction: column;
  gap: v-bind('theme.spacing.value.sm');
}

.filter-panel__label {
  font-size: v-bind('theme.typography.value.sm');
  font-weight: 600;
  color: v-bind('theme.colors.value.textPrimary');
}

.filter-panel__select {
  padding: 10px 12px;
  border: 1px solid v-bind('theme.colors.value.border');
  border-radius: v-bind('theme.radius.value.md');
  font-size: v-bind('theme.typography.value.sm');
  color: v-bind('theme.colors.value.textPrimary');
  background: white;
  cursor: pointer;
  transition: all 0.2s;
  font-family: v-bind('theme.typography.value.fontFamily');
}

.filter-panel__select:hover:not(:disabled) {
  border-color: v-bind('theme.colors.value.primary');
}

.filter-panel__select:focus {
  outline: none;
  border-color: v-bind('theme.colors.value.primary');
  box-shadow: 0 0 0 3px rgba(168, 85, 247, 0.1);
}

.filter-panel__select:disabled {
  background: v-bind('theme.colors.value.bgSecondary');
  cursor: not-allowed;
  opacity: 0.6;
}

/* Actions */
.filter-panel__actions {
  display: flex;
  gap: v-bind('theme.spacing.value.md');
  justify-content: flex-end;
}

.filter-panel__button {
  padding: 10px 24px;
  border: none;
  border-radius: v-bind('theme.radius.value.md');
  font-size: v-bind('theme.typography.value.sm');
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  font-family: v-bind('theme.typography.value.fontFamily');
}

.filter-panel__button--primary {
  background: v-bind('theme.colors.value.primary');
  color: white;
}

.filter-panel__button--primary:hover:not(:disabled) {
  background: #9333ea;
  box-shadow: 0 4px 12px rgba(168, 85, 247, 0.3);
}

.filter-panel__button--primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.filter-panel__button--secondary {
  background: white;
  color: v-bind('theme.colors.value.textSecondary');
  border: 1px solid v-bind('theme.colors.value.border');
}

.filter-panel__button--secondary:hover {
  border-color: v-bind('theme.colors.value.primary');
  color: v-bind('theme.colors.value.primary');
}

/* Transitions */
.filter-panel-expand-enter-active,
.filter-panel-expand-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

.filter-panel-expand-enter-from,
.filter-panel-expand-leave-to {
  opacity: 0;
  max-height: 0;
}

.filter-panel-expand-enter-to,
.filter-panel-expand-leave-from {
  opacity: 1;
  max-height: 1000px;
}

/* Responsive */
@media (max-width: 768px) {
  .filter-panel__grid {
    grid-template-columns: 1fr;
    gap: v-bind('theme.spacing.value.md');
  }

  .filter-panel__actions {
    flex-direction: column;
  }

  .filter-panel__button {
    width: 100%;
  }
}
</style>
