<template>
  <div class="pie-chart-card">
    <!-- 标题区 -->
    <div class="pie-chart-card__header">
      <h3 class="pie-chart-card__title">{{ title }}</h3>
      <span class="pie-chart-card__period">{{ periodLabel }}</span>
    </div>

    <!-- 图表容器 -->
    <div class="pie-chart-card__body">
      <!-- 加载状态 -->
      <div v-if="loading" class="pie-chart-card__loading">
        <div class="pie-chart-card__spinner"></div>
        <span class="pie-chart-card__loading-text">加载中...</span>
      </div>

      <!-- 空状态 -->
      <div v-else-if="!hasData" class="pie-chart-card__empty">
        <div class="pie-chart-card__empty-icon">📊</div>
        <p class="pie-chart-card__empty-text">暂无数据</p>
      </div>

      <!-- ECharts图表 -->
      <div
        v-else
        ref="chartRef"
        class="pie-chart-card__canvas"
        :style="{ height: height }"
      ></div>
    </div>

    <!-- 统计信息 -->
    <div v-if="hasData && !loading" class="pie-chart-card__footer">
      <div class="pie-chart-card__stat">
        <span class="pie-chart-card__stat-label">{{ statsLabel }}:</span>
        <span class="pie-chart-card__stat-value">{{ formattedTotalCount }}</span>
      </div>
      <div v-if="totalPremium > 0" class="pie-chart-card__stat">
        <span class="pie-chart-card__stat-label">保费:</span>
        <span class="pie-chart-card__stat-value">{{ formattedTotalPremium }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import { useTheme } from '@/composables/useTheme'

const props = defineProps({
  // 图表标题
  title: {
    type: String,
    required: true
  },
  // 分布数据
  distributionData: {
    type: Object,
    default: () => null
  },
  // 加载状态
  loading: {
    type: Boolean,
    default: false
  },
  // 图表高度
  height: {
    type: String,
    default: '280px'
  },
  // 护眼配色方案（可选自定义）
  colors: {
    type: Array,
    default: () => [
      '#5B8DEF', // 主蓝
      '#8B95A5', // 次灰
      '#C5CAD3', // 浅灰
      '#7CB5EC', // 浅蓝
      '#90ED7D', // 浅绿
      '#F7A35C', // 橙色
      '#8085E9', // 紫色
      '#F15C80'  // 粉色
    ]
  },
  // 统计数值类型（'count': 件数, 'staff': 人数）
  statsType: {
    type: String,
    default: 'count',
    validator: (value) => ['count', 'staff'].includes(value)
  }
})

// Theme
const theme = useTheme('chart')

// Chart
const chartRef = ref(null)
let chartInstance = null

// Computed
const hasData = computed(() => {
  return props.distributionData &&
         props.distributionData.distribution &&
         props.distributionData.distribution.length > 0
})

const periodLabel = computed(() => {
  return props.distributionData?.period_label || '当日'
})

const totalCount = computed(() => {
  const data = props.distributionData
  if (!data) return 0
  return data.total_count || data.total_staff || 0
})

const totalPremium = computed(() => {
  return props.distributionData?.total_premium || 0
})

const statsLabel = computed(() => {
  return props.statsType === 'staff' ? '业务员' : '签单量'
})

const formattedTotalCount = computed(() => {
  const count = totalCount.value
  return count.toLocaleString('zh-CN')
})

const formattedTotalPremium = computed(() => {
  const premium = totalPremium.value
  const wan = Math.round(premium / 10000)
  return `${wan.toLocaleString('zh-CN')}万元`
})

/**
 * 初始化并渲染 ECharts 饼图
 */
function initChart() {
  if (!chartRef.value || !hasData.value) return

  // 销毁旧实例
  if (chartInstance) {
    chartInstance.dispose()
  }

  // 创建新实例
  chartInstance = echarts.init(chartRef.value)

  const distribution = props.distributionData.distribution

  // 构建图表数据
  const chartData = distribution.map((item, index) => ({
    name: item.type || item.range,
    value: item.count || item.staff_count || 0,
    percentage: item.percentage || 0,
    itemStyle: {
      color: props.colors[index % props.colors.length]
    }
  }))

  const option = {
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#e5e7eb',
      borderWidth: 1,
      textStyle: {
        color: '#374151',
        fontSize: 13
      },
      padding: [12, 16],
      formatter: (params) => {
        const { name, value, percentage } = params.data
        const label = props.statsType === 'staff' ? '人' : '件'
        return `
          <div style="font-weight:600;margin-bottom:4px;">${name}</div>
          <div style="display:flex;align-items:center;gap:8px;">
            <span style="
              display:inline-block;
              width:10px;
              height:10px;
              border-radius:50%;
              background:${params.color};
            "></span>
            <span>${value.toLocaleString('zh-CN')}${label} (${percentage}%)</span>
          </div>
        `
      }
    },
    legend: {
      orient: 'horizontal',
      bottom: 0,
      left: 'center',
      textStyle: {
        color: '#6b7280',
        fontSize: 12
      },
      itemWidth: 12,
      itemHeight: 12,
      itemGap: 16,
      formatter: (name) => {
        // 图例只显示标签名称，不显示百分比值
        return `${name}`
      }
    },
    series: [
      {
        type: 'pie',
        radius: ['40%', '70%'], // 环形饼图
        center: ['50%', '45%'],
        avoidLabelOverlap: true,
        itemStyle: {
          borderRadius: 4,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: true,
          position: 'outside',
          formatter: '{d}%',
          fontSize: 12,
          color: '#374151',
          fontWeight: 600
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 14,
            fontWeight: 'bold'
          },
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.3)'
          }
        },
        labelLine: {
          show: true,
          length: 10,
          length2: 10,
          lineStyle: {
            color: '#d1d5db'
          }
        },
        data: chartData,
        animation: true,
        animationDuration: 1000,
        animationEasing: 'cubicOut'
      }
    ]
  }

  chartInstance.setOption(option)
}

function resizeChart() {
  if (chartInstance) {
    chartInstance.resize()
  }
}

// 防抖resize
let resizeTimer = null
function debouncedResize() {
  if (resizeTimer) clearTimeout(resizeTimer)
  resizeTimer = setTimeout(resizeChart, 300)
}

// Lifecycle
onMounted(async () => {
  await nextTick()
  if (hasData.value) {
    initChart()
  }
  window.addEventListener('resize', debouncedResize)
})

onUnmounted(() => {
  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }
  if (resizeTimer) clearTimeout(resizeTimer)
  window.removeEventListener('resize', debouncedResize)
})

// Watch
watch(
  () => props.distributionData,
  async () => {
    await nextTick()
    if (hasData.value) {
      initChart()
    }
  },
  { deep: true }
)

watch(
  () => props.loading,
  async (newVal) => {
    if (!newVal && hasData.value) {
      await nextTick()
      initChart()
    }
  }
)
</script>

<style scoped>
.pie-chart-card {
  background: v-bind('theme.business.value.cardBg');
  border: v-bind('theme.business.value.cardBorder');
  border-radius: v-bind('theme.radius.value.lg');
  box-shadow: v-bind('theme.business.value.cardShadow');
  padding: v-bind('theme.spacing.value.lg');
  display: flex;
  flex-direction: column;
  gap: v-bind('theme.spacing.value.md');
  min-height: 400px;
}

/* Header */
.pie-chart-card__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: v-bind('theme.spacing.value.md');
  padding-bottom: v-bind('theme.spacing.value.sm');
  border-bottom: v-bind('theme.business.value.divider');
}

.pie-chart-card__title {
  font-size: v-bind('theme.typography.value.base');
  font-weight: 600;
  color: v-bind('theme.colors.value.textPrimary');
  margin: 0;
}

.pie-chart-card__period {
  font-size: v-bind('theme.typography.value.xs');
  color: v-bind('theme.colors.value.textTertiary');
  padding: 3px 10px;
  background: v-bind('theme.colors.value.bgTint');
  border-radius: v-bind('theme.radius.value.sm');
}

/* Body */
.pie-chart-card__body {
  position: relative;
  flex: 1;
  min-height: 240px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.pie-chart-card__canvas {
  width: 100%;
}

/* Loading */
.pie-chart-card__loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: v-bind('theme.spacing.value.sm');
}

.pie-chart-card__spinner {
  width: 32px;
  height: 32px;
  border: 3px solid rgba(168, 85, 247, 0.1);
  border-top-color: v-bind('theme.colors.value.primary');
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.pie-chart-card__loading-text {
  font-size: v-bind('theme.typography.value.sm');
  color: v-bind('theme.colors.value.textSecondary');
}

/* Empty */
.pie-chart-card__empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: v-bind('theme.spacing.value.sm');
}

.pie-chart-card__empty-icon {
  font-size: 48px;
  opacity: 0.3;
}

.pie-chart-card__empty-text {
  font-size: v-bind('theme.typography.value.sm');
  color: v-bind('theme.colors.value.textTertiary');
  margin: 0;
}

/* Footer */
.pie-chart-card__footer {
  display: flex;
  align-items: center;
  justify-content: space-around;
  gap: v-bind('theme.spacing.value.md');
  padding-top: v-bind('theme.spacing.value.sm');
  border-top: v-bind('theme.business.value.divider');
}

.pie-chart-card__stat {
  display: flex;
  align-items: center;
  gap: 6px;
}

.pie-chart-card__stat-label {
  font-size: v-bind('theme.typography.value.xs');
  color: v-bind('theme.colors.value.textSecondary');
}

.pie-chart-card__stat-value {
  font-size: v-bind('theme.typography.value.base');
  font-weight: 600;
  color: v-bind('theme.colors.value.textPrimary');
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .pie-chart-card {
    padding: v-bind('theme.spacing.value.md');
  }

  .pie-chart-card__header {
    flex-direction: column;
    align-items: flex-start;
    gap: v-bind('theme.spacing.value.xs');
  }

  .pie-chart-card__footer {
    flex-direction: column;
    gap: v-bind('theme.spacing.value.xs');
  }
}
</style>
