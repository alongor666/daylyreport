<template>
  <header class="app-header">
    <div class="app-header__container">
      <!-- 左侧: 标题和日期 -->
      <div class="app-header__branding">
        <h1 class="app-header__title">车险签单数据分析平台</h1>
        <div class="app-header__meta">
          <span class="app-header__date">{{ displayDate }}</span>
          <span class="app-header__separator">·</span>
          <span class="app-header__version">v2.0</span>
        </div>
      </div>

      <!-- 右侧: 操作区 -->
      <div class="app-header__actions">
        <!-- 指标切换 -->
        <div class="metric-switcher">
          <button
            v-for="metric in metrics"
            :key="metric.value"
            :class="[
              'metric-switcher__button',
              { 'metric-switcher__button--active': currentMetric === metric.value }
            ]"
            @click="handleMetricSwitch(metric.value)"
          >
            <span class="metric-switcher__icon">{{ metric.icon }}</span>
            <span class="metric-switcher__label">{{ metric.label }}</span>
          </button>
        </div>

        <!-- 刷新按钮 -->
        <button
          class="refresh-button"
          :class="{ 'refresh-button--loading': isRefreshing }"
          :disabled="isRefreshing"
          @click="handleRefresh"
          title="刷新数据"
        >
          <span class="refresh-button__icon" :class="{ 'refresh-button__icon--spin': isRefreshing }">
            ↻
          </span>
          <span class="refresh-button__text">刷新</span>
        </button>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useAppStore } from '@/stores/app'
import { useDataStore } from '@/stores/data'
import { useTheme } from '@/composables/useTheme'
import { useToast } from '@/composables/useToast'

// Stores
const appStore = useAppStore()
const dataStore = useDataStore()

// Theme
const theme = useTheme('header')

// Toast
const toast = useToast()

// State
const isRefreshing = ref(false)

// 指标选项
const metrics = [
  { value: 'premium', label: '签单保费', icon: '¥' },
  { value: 'count', label: '签单单量', icon: '#' }
]

// Computed
const currentMetric = computed(() => appStore.currentMetric)
const displayDate = computed(() => appStore.formattedDisplayDate)

// Methods
const handleMetricSwitch = (metric) => {
  if (metric === currentMetric.value) return

  appStore.switchMetric(metric)

  // 刷新图表数据
  dataStore.refreshChartData().catch((error) => {
    toast.error('切换指标失败', error.message)
  })

  toast.info(`已切换到${metrics.find(m => m.value === metric)?.label}`)
}

const handleRefresh = async () => {
  if (isRefreshing.value) return

  isRefreshing.value = true

  try {
    await dataStore.refreshAllData(appStore.selectedDate)
    toast.success('数据刷新成功')
  } catch (error) {
    toast.error('数据刷新失败', error.message)
  } finally {
    isRefreshing.value = false
  }
}
</script>

<style scoped>
.app-header {
  background: v-bind('theme.business.value.cardBg');
  border-bottom: v-bind('theme.business.value.divider');
  box-shadow: v-bind('theme.business.value.cardShadow');
  backdrop-filter: blur(20px);
  position: sticky;
  top: 0;
  z-index: 100;
}

.app-header__container {
  max-width: 1400px;
  margin: 0 auto;
  padding: v-bind('theme.spacing.value.xl') v-bind('theme.spacing.value.xxl');
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: v-bind('theme.spacing.value.xl');
}

/* 左侧品牌区 */
.app-header__branding {
  display: flex;
  flex-direction: column;
  gap: v-bind('theme.spacing.value.sm');
}

.app-header__title {
  font-size: v-bind('theme.typography.value["2xl"]');
  font-weight: 700;
  color: v-bind('theme.colors.value.textPrimary');
  margin: 0;
  letter-spacing: -0.02em;
}

.app-header__meta {
  display: flex;
  align-items: center;
  gap: v-bind('theme.spacing.value.md');
  font-size: v-bind('theme.typography.value.sm');
  color: v-bind('theme.colors.value.textSecondary');
}

.app-header__separator {
  color: v-bind('theme.colors.value.border');
}

.app-header__version {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 2px 8px;
  background: v-bind('theme.colors.value.bgTint');
  color: v-bind('theme.colors.value.primary');
  border-radius: 4px;
  font-size: 11px;
  font-weight: 600;
}

/* 右侧操作区 */
.app-header__actions {
  display: flex;
  align-items: center;
  gap: v-bind('theme.spacing.value.lg');
}

/* 指标切换器 */
.metric-switcher {
  display: flex;
  gap: 4px;
  background: rgba(0, 0, 0, 0.03);
  padding: 4px;
  border-radius: v-bind('theme.radius.value.md');
}

.metric-switcher__button {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border: none;
  background: transparent;
  color: v-bind('theme.colors.value.textSecondary');
  font-size: v-bind('theme.typography.value.sm');
  font-weight: 500;
  border-radius: calc(v-bind('theme.radius.value.md') - 2px);
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  font-family: v-bind('theme.typography.value.fontFamily');
}

.metric-switcher__button:hover:not(.metric-switcher__button--active) {
  background: rgba(0, 0, 0, 0.04);
  color: v-bind('theme.colors.value.textPrimary');
}

.metric-switcher__button--active {
  background: white;
  color: v-bind('theme.colors.value.primary');
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
  font-weight: 600;
}

.metric-switcher__icon {
  font-size: 14px;
  font-weight: 700;
}

/* 刷新按钮 */
.refresh-button {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border: 1px solid v-bind('theme.colors.value.border');
  background: white;
  color: v-bind('theme.colors.value.textPrimary');
  font-size: v-bind('theme.typography.value.sm');
  font-weight: 500;
  border-radius: v-bind('theme.radius.value.md');
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  font-family: v-bind('theme.typography.value.fontFamily');
}

.refresh-button:hover:not(:disabled) {
  border-color: v-bind('theme.colors.value.primary');
  color: v-bind('theme.colors.value.primary');
  box-shadow: 0 2px 8px rgba(168, 85, 247, 0.15);
}

.refresh-button:active:not(:disabled) {
  transform: translateY(1px);
}

.refresh-button:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.refresh-button__icon {
  font-size: 18px;
  line-height: 1;
  transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.refresh-button__icon--spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .app-header__container {
    flex-direction: column;
    align-items: flex-start;
    gap: v-bind('theme.spacing.value.lg');
  }

  .app-header__title {
    font-size: v-bind('theme.typography.value.xl');
  }

  .app-header__actions {
    width: 100%;
    flex-wrap: wrap;
  }

  .metric-switcher {
    flex: 1;
  }

  .refresh-button__text {
    display: none;
  }
}
</style>
