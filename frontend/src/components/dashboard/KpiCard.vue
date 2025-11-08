<template>
  <div :class="['kpi-card', { 'kpi-card--loading': loading }]">
    <!-- 加载状态 -->
    <div v-if="loading" class="kpi-card__loading">
      <div class="kpi-card__spinner"></div>
      <span class="kpi-card__loading-text">加载中...</span>
    </div>

    <!-- 正常内容 -->
    <template v-else>
      <!-- 标题和图标 -->
      <div class="kpi-card__header">
        <div class="kpi-card__icon" :style="{ background: iconBg }">
          {{ icon }}
        </div>
        <h3 class="kpi-card__title">{{ title }}</h3>
      </div>

      <!-- 主要数值(当日) -->
      <div class="kpi-card__main">
        <div class="kpi-card__value">{{ formattedMainValue }}</div>
        <div v-if="trend !== null" :class="['kpi-card__trend', trendClass]">
          <span class="kpi-card__trend-icon">{{ trendIcon }}</span>
          <span class="kpi-card__trend-value">{{ formattedTrend }}</span>
        </div>
      </div>

      <!-- 趋势图 (7天Sparkline) -->
      <div v-if="sparklineData && sparklineData.length > 0" class="kpi-card__chart">
        <div ref="chartRef" class="kpi-card__chart-canvas"></div>
      </div>

      <!-- 三口径数据 -->
      <div class="kpi-card__stats">
        <div class="kpi-card__stat">
          <span class="kpi-card__stat-label">当日</span>
          <span class="kpi-card__stat-value">{{ formattedDayValue }}</span>
        </div>
        <div class="kpi-card__stat">
          <span class="kpi-card__stat-label">近7天</span>
          <span class="kpi-card__stat-value">{{ formatted7dValue }}</span>
        </div>
        <div class="kpi-card__stat">
          <span class="kpi-card__stat-label">近30天</span>
          <span class="kpi-card__stat-value">{{ formatted30dValue }}</span>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { computed, ref, watch, onMounted, onUnmounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import { useTheme, useEChartsTheme } from '@/composables/useTheme'

const props = defineProps({
  // 标题
  title: {
    type: String,
    required: true
  },
  // 图标
  icon: {
    type: String,
    default: '📊'
  },
  // 图标背景色
  iconBg: {
    type: String,
    default: 'linear-gradient(135deg, #a855f7, #9333ea)'
  },
  // 当日数值
  dayValue: {
    type: Number,
    default: 0
  },
  // 近7天数值
  last7dValue: {
    type: Number,
    default: 0
  },
  // 近30天数值
  last30dValue: {
    type: Number,
    default: 0
  },
  // 趋势百分比 (正数为上升,负数为下降)
  trend: {
    type: Number,
    default: null
  },
  // 7天趋势数据 (用于Sparkline)
  sparklineData: {
    type: Array,
    default: () => []
  },
  // 数值格式化类型 (currency: 金额, number: 数字)
  valueType: {
    type: String,
    default: 'currency',
    validator: (value) => ['currency', 'number'].includes(value)
  },
  // 加载状态
  loading: {
    type: Boolean,
    default: false
  }
})

// Theme
const theme = useTheme('kpiCard')
const echartsTheme = useEChartsTheme()

// Chart
const chartRef = ref(null)
let chartInstance = null

// Computed
const formattedMainValue = computed(() => formatValue(props.dayValue))
const formattedDayValue = computed(() => formatValue(props.dayValue))
const formatted7dValue = computed(() => formatValue(props.last7dValue))
const formatted30dValue = computed(() => formatValue(props.last30dValue))

const formattedTrend = computed(() => {
  if (props.trend === null) return ''
  const abs = Math.abs(props.trend)
  return `${abs.toFixed(1)}%`
})

const trendClass = computed(() => {
  if (props.trend === null) return ''
  return props.trend > 0 ? 'kpi-card__trend--up' : 'kpi-card__trend--down'
})

const trendIcon = computed(() => {
  if (props.trend === null) return ''
  return props.trend > 0 ? '↑' : '↓'
})

// Methods
function formatValue(value) {
  if (props.valueType === 'currency') {
    // 金额格式化: ¥1,234,567
    return `¥${value.toLocaleString('zh-CN', { maximumFractionDigits: 0 })}`
  } else {
    // 数字格式化: 1,234
    return value.toLocaleString('zh-CN', { maximumFractionDigits: 0 })
  }
}

function initChart() {
  if (!chartRef.value || !props.sparklineData || props.sparklineData.length === 0) {
    return
  }

  // 销毁旧实例
  if (chartInstance) {
    chartInstance.dispose()
  }

  // 创建新实例
  chartInstance = echarts.init(chartRef.value)

  const option = {
    ...echartsTheme,
    grid: {
      top: 5,
      right: 5,
      bottom: 5,
      left: 5
    },
    xAxis: {
      type: 'category',
      show: false,
      data: props.sparklineData.map((_, index) => index)
    },
    yAxis: {
      type: 'value',
      show: false
    },
    series: [
      {
        type: 'line',
        data: props.sparklineData,
        smooth: true,
        symbol: 'none',
        lineStyle: {
          width: 2,
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 1,
            y2: 0,
            colorStops: [
              { offset: 0, color: '#a855f7' },
              { offset: 1, color: '#9333ea' }
            ]
          }
        },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(168, 85, 247, 0.2)' },
              { offset: 1, color: 'rgba(168, 85, 247, 0)' }
            ]
          }
        }
      }
    ],
    animation: true,
    animationDuration: 800,
    animationEasing: 'cubicOut'
  }

  chartInstance.setOption(option)
}

function resizeChart() {
  if (chartInstance) {
    chartInstance.resize()
  }
}

// Lifecycle
onMounted(async () => {
  await nextTick()
  initChart()
  window.addEventListener('resize', resizeChart)
})

onUnmounted(() => {
  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }
  window.removeEventListener('resize', resizeChart)
})

// Watch
watch(
  () => props.sparklineData,
  async () => {
    await nextTick()
    initChart()
  },
  { deep: true }
)
</script>

<style scoped>
.kpi-card {
  background: v-bind('theme.business.value.cardBg');
  border: v-bind('theme.business.value.cardBorder');
  border-radius: v-bind('theme.radius.value.lg');
  box-shadow: v-bind('theme.business.value.cardShadow');
  padding: v-bind('theme.spacing.value.xl');
  display: flex;
  flex-direction: column;
  gap: v-bind('theme.spacing.value.lg');
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.kpi-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.kpi-card--loading {
  pointer-events: none;
}

/* 加载状态 */
.kpi-card__loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: v-bind('theme.spacing.value.md');
  padding: v-bind('theme.spacing.value.xxl') 0;
}

.kpi-card__spinner {
  width: 32px;
  height: 32px;
  border: 3px solid rgba(168, 85, 247, 0.1);
  border-top-color: v-bind('theme.colors.value.primary');
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.kpi-card__loading-text {
  font-size: v-bind('theme.typography.value.sm');
  color: v-bind('theme.colors.value.textSecondary');
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* 头部 */
.kpi-card__header {
  display: flex;
  align-items: center;
  gap: v-bind('theme.spacing.value.md');
}

.kpi-card__icon {
  width: 40px;
  height: 40px;
  border-radius: v-bind('theme.radius.value.md');
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  box-shadow: 0 4px 12px rgba(168, 85, 247, 0.2);
}

.kpi-card__title {
  font-size: v-bind('theme.typography.value.base');
  font-weight: 600;
  color: v-bind('theme.colors.value.textPrimary');
  margin: 0;
}

/* 主要数值 */
.kpi-card__main {
  display: flex;
  flex-direction: column;
  gap: v-bind('theme.spacing.value.sm');
}

.kpi-card__value {
  font-size: v-bind('theme.typography.value["3xl"]');
  font-weight: 700;
  color: v-bind('theme.colors.value.textPrimary');
  line-height: 1.2;
  letter-spacing: -0.02em;
}

.kpi-card__trend {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: v-bind('theme.typography.value.sm');
  font-weight: 600;
}

.kpi-card__trend--up {
  color: v-bind('theme.colors.value.success');
}

.kpi-card__trend--down {
  color: v-bind('theme.colors.value.error');
}

.kpi-card__trend-icon {
  font-size: 14px;
}

/* 趋势图 */
.kpi-card__chart {
  height: 60px;
  margin: -8px -4px;
}

.kpi-card__chart-canvas {
  width: 100%;
  height: 100%;
}

/* 统计数据 */
.kpi-card__stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: v-bind('theme.spacing.value.md');
  padding-top: v-bind('theme.spacing.value.md');
  border-top: v-bind('theme.business.value.divider');
}

.kpi-card__stat {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.kpi-card__stat-label {
  font-size: v-bind('theme.typography.value.xs');
  color: v-bind('theme.colors.value.textSecondary');
  font-weight: 500;
}

.kpi-card__stat-value {
  font-size: v-bind('theme.typography.value.base');
  font-weight: 600;
  color: v-bind('theme.colors.value.textPrimary');
}

/* 响应式 */
@media (max-width: 768px) {
  .kpi-card {
    padding: v-bind('theme.spacing.value.lg');
  }

  .kpi-card__value {
    font-size: v-bind('theme.typography.value["2xl"]');
  }

  .kpi-card__stats {
    gap: v-bind('theme.spacing.value.sm');
  }
}
</style>
