<template>
  <div class="chart-view">
    <!-- 标题区 -->
    <div class="chart-view__header">
      <div class="chart-view__title-group">
        <h2 class="chart-view__title">{{ title }}</h2>
        <p v-if="subtitle" class="chart-view__subtitle">{{ subtitle }}</p>
      </div>
      <div class="chart-view__meta">
        <!-- 指标切换移至 Dashboard 顶部工具栏，这里仅显示图表类型与最新日期 -->
        
        <!-- 图表类型切换 -->
        <div class="chart-type-switcher">
          <button
            v-for="chartTypeOption in chartTypes"
            :key="chartTypeOption.value"
            :class="[
              'chart-type-switcher__button',
              { 'chart-type-switcher__button--active': chartType === chartTypeOption.value }
            ]"
            @click="handleChartTypeSwitch(chartTypeOption.value)"
          >
            <span class="chart-type-switcher__icon">{{ chartTypeOption.icon }}</span>
            <span class="chart-type-switcher__label">{{ chartTypeOption.label }}</span>
          </button>
        </div>
        <span v-if="latestDate" class="chart-view__date">
          数据截至: {{ formatDate(latestDate) }}
        </span>
      </div>
    </div>

    <!-- 图表容器 -->
    <div class="chart-view__body">
      <!-- 加载状态 -->
      <div v-if="loading" class="chart-view__loading">
        <div class="chart-view__spinner"></div>
        <span class="chart-view__loading-text">图表加载中...</span>
      </div>

      <!-- 空状态 -->
      <div v-else-if="!hasData" class="chart-view__empty">
        <div class="chart-view__empty-icon">📊</div>
        <p class="chart-view__empty-text">暂无数据</p>
      </div>

      <!-- ECharts图表 -->
      <div
        v-else
        ref="chartRef"
        class="chart-view__canvas"
        :style="{ height: height }"
      ></div>
    </div>

    <!-- 图例说明 -->
    <div v-if="showLegend && hasData" class="chart-view__legend">
      <div
        v-for="(item, index) in legendItems"
        :key="index"
        class="chart-view__legend-item"
      >
        <span
          class="chart-view__legend-marker"
          :style="{ backgroundColor: item.color }"
        ></span>
        <span class="chart-view__legend-label">{{ item.name }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import { useTheme, useEChartsTheme } from '@/composables/useTheme'
import { useAppStore } from '@/stores/app'
import { useDataStore } from '@/stores/data'
import { useToast } from '@/composables/useToast'

const props = defineProps({
  // 图表标题
  title: {
    type: String,
    default: '周对比趋势'
  },
  // 副标题
  subtitle: {
    type: String,
    default: ''
  },
  // 图表数据
  chartData: {
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
    default: '400px'
  },
  // 是否显示图例
  showLegend: {
    type: Boolean,
    default: true
  }
})

// Theme
const theme = useTheme('chart')
const echartsTheme = useEChartsTheme()

// Stores
const appStore = useAppStore()
const dataStore = useDataStore()
const toast = useToast()

// Chart
const chartRef = ref(null)
let chartInstance = null

// 图表类型
const chartType = ref('bar') // bar: 柱状图, line: 折线图

// 图表类型选项
const chartTypes = [
  { value: 'bar', label: '柱状图', icon: '📊' },
  { value: 'line', label: '折线图', icon: '📈' }
]

// 指标切换：随全局 appStore.currentMetric 变化，本组件不再提供本地切换

// Computed
const currentMetric = computed(() => appStore.currentMetric)

// Computed
const hasData = computed(() => {
  return props.chartData && props.chartData.series && props.chartData.series.length > 0
})

const latestDate = computed(() => {
  return props.chartData?.latest_date || null
})

/**
 * 函数：legendItems
 * 作用：生成图例的展示项。仅改变 UI 显示文本，不改变内部语义。
 * 语义边界：内部数据仍以 code 区分（'D'/'D-7'/'D-14'），图例标签仅用于人类友好展示。
 * 返回：[{ name: '当周'|'上周'|'上上周', color: string }]
 */
const legendItems = computed(() => {
  if (!props.chartData || !props.chartData.series) return []

  // 护眼配色方案：D-14, D-7, D (从浅到深)
  const colors = [
    getComputedStyle(document.documentElement).getPropertyValue('--chart-light-gray').trim() || '#C5CAD3',
    getComputedStyle(document.documentElement).getPropertyValue('--chart-secondary-gray').trim() || '#8B95A5',
    getComputedStyle(document.documentElement).getPropertyValue('--chart-primary-blue').trim() || '#5B8DEF'
  ]

  // UI标签映射：仅用于展示，不影响内部 code 语义与计算
  const labelMap = {
    'D': '当周',
    'D-7': '上周',
    'D-14': '上上周'
  }

  return props.chartData.series.map((item, index) => ({
    name: labelMap[item.code] || item.code,
    color: colors[index % colors.length]
  }))
})

// Methods

/**
 * 函数用途：切换图表类型（柱状图/折线图）
 * 入参：type - 图表类型，'bar' 或 'line'
 * 出参：无；通过更新本地状态与重新初始化图表产生副作用
 */
const handleChartTypeSwitch = (type) => {
  if (type === chartType.value) return
  
  chartType.value = type
  
  // 重新初始化图表
  nextTick(() => {
    initChart()
  })
  
  toast.info(`已切换到${chartTypes.find(t => t.value === type)?.label}`)
}

/**
 * 函数：formatDate
 * 作用：将后端传入的日期字符串（YYYY-MM-DD）格式化为中文可读形式
 * 入参：dateStr（字符串，形如 2025-11-05）
 * 返回：格式化后的中文日期字符串（例如：2025年11月05日）
 */
function formatDate(dateStr) {
  if (!dateStr) return ''
  const [year, month, day] = dateStr.split('-')
  return `${year}年${month}月${day}日`
}

/**
 * 函数：formatNumber
 * 作用：根据当前指标类型对数值进行友好显示
 *  - 当 currentMetric 为 'premium'（保费相关）时，以“万元”为单位并取整数显示，如 123456 => 12万元
 *  - 其他指标（如单量）按千分位整数显示，如 123456 => 123,456
 * 入参：num（数字）
 * 返回：格式化后的字符串
 */
function formatNumber(num) {
  if (currentMetric.value === 'premium') {
    const wan = Math.round((num || 0) / 10000)
    return `${wan}万元`
  }
  return (num || 0).toLocaleString('zh-CN', { maximumFractionDigits: 0 })
}

/**
 * 函数：initChart
 * 作用：初始化并渲染 ECharts 图表，配置自定义 tooltip 与图例
 * 入参：无（依赖 props.chartData 内的 x_axis 与 series）
 * 返回：无
 */
function initChart() {
  if (!chartRef.value || !hasData.value) return

  // 销毁旧实例
  if (chartInstance) {
    chartInstance.dispose()
  }

  // 创建新实例
  chartInstance = echarts.init(chartRef.value)

  const { x_axis, series } = props.chartData

  // 护眼配色方案：D-14 (浅灰), D-7 (次灰), D (主蓝)
  const colors = [
    getComputedStyle(document.documentElement).getPropertyValue('--chart-light-gray').trim() || '#C5CAD3',
    getComputedStyle(document.documentElement).getPropertyValue('--chart-secondary-gray').trim() || '#8B95A5',
    getComputedStyle(document.documentElement).getPropertyValue('--chart-primary-blue').trim() || '#5B8DEF'
  ]

  const option = {
    ...echartsTheme,
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#e5e7eb',
      borderWidth: 1,
      textStyle: {
        color: '#374151',
        fontSize: 13
      },
      padding: [12, 16],
      /**
       * Tooltip 格式化器（按“星期几”显示三行对应日期的数据）
       * 规则：
       *  - 悬停到某一星期几索引 idx 时，依次展示 D-14、D-7、D 三行；每行包含：日期、数值、较7天前的变化与状态。
       *  - 不显示 D/D-7/D-14 标签，仅显示日期与计算结果。
       *  - D-14 行在 21 天窗口内无对比（缺少 D-21），显示“较7天前：— · 无对比”。
       */
      formatter: (params) => {
        const idx = params?.[0]?.dataIndex ?? 0
        const header = params?.[0]?.axisValue ?? ''

        // 取三条序列
        const s14 = series.find(s => s.code === 'D-14')
        const s7 = series.find(s => s.code === 'D-7')
        const s0 = series.find(s => s.code === 'D')

        // 颜色与标记（与系列顺序一致）：浅灰、次灰、主蓝
        const colorMap = {
          'D-14': colors[0],
          'D-7': colors[1],
          'D': colors[2]
        }

        // 状态颜色（从 CSS 变量中获取，缺省用备选）
        // 中文函数注释：用于为“变化箭头”设置颜色；当主题未定义变量时使用预设色。
        const statusColors = (() => {
          const root = document.documentElement
          const up = getComputedStyle(root).getPropertyValue('--status-success').trim() || '#52C41A'
          const down = getComputedStyle(root).getPropertyValue('--status-warning').trim() || '#F5222D'
          const neutral = getComputedStyle(root).getPropertyValue('--status-neutral').trim() || '#8B95A5'
          return { up, down, neutral }
        })()

        // 行构造方法（固定列网格布局）
        // 中文函数注释：每行采用 6 列网格固定位置：
        // 1) 色点，2) 日期，3) 当期值（主值），4) 箭头（单独一列），5) 变化值，6) 变化幅度（百分比）。
        // 数值列均使用固定列宽并居中对齐，保证各周数据视觉对齐与可比性。
        // 颜色规则遵循设计文档阈值：增长率 > +5% 用上升色；< -5% 用下降色；其余中性色。
        const buildRow = (code, currSeries, prevSeries) => {
          const date = currSeries?.dates?.[idx] || ''
          const vCurr = currSeries?.data?.[idx]
          const vPrev = prevSeries?.data?.[idx]
          const valueStr = (typeof vCurr === 'number') ? formatNumber(vCurr) : '—'

          // 箭头/颜色/变化值/变化率（紧凑信息）
          let arrow = '—'
          let color = statusColors.neutral
          let diffStr = '—'
          let pctStr = '—'
          if (prevSeries && typeof vCurr === 'number' && typeof vPrev === 'number') {
            const diff = vCurr - vPrev
            arrow = diff > 0 ? '↑' : diff < 0 ? '↓' : '—'
            diffStr = `${diff >= 0 ? '+' : ''}${formatNumber(Math.abs(diff))}`
            let pct = null
            if (vPrev !== 0) {
              pct = (diff / vPrev) * 100
              pctStr = `${diff >= 0 ? '+' : ''}${Math.abs(pct).toFixed(1)}%`
            } else {
              pctStr = '—'
            }
            if (pct !== null) {
              if (pct > 5) color = statusColors.up
              else if (pct < -5) color = statusColors.down
              else color = statusColors.neutral
            }
          }

          return `
            <div style="
              display:grid;
              grid-template-columns:12px 1fr 110px 24px 100px 100px;
              align-items:center;
              gap:10px;
              margin-bottom:8px;
            ">
              <span style="width:12px;height:12px;border-radius:50%;background:${colorMap[code]};"></span>
              <span style="color:#374151;">${date}</span>
              <span style="text-align:center;font-weight:600;">${valueStr}</span>
              <span style="text-align:center;color:${color};font-weight:600;">${arrow}</span>
              <span style="text-align:center;color:${color};font-weight:600;">${diffStr}</span>
              <span style="text-align:center;color:${color};font-weight:600;">${pctStr}</span>
            </div>
          `
        }

        // 组装三行（远→近）：D-14、D-7、D
        let result = `<div style="font-weight:600;margin-bottom:8px;">${header}</div>`
        result += buildRow('D-14', s14, null)
        result += buildRow('D-7', s7, s14)
        result += buildRow('D', s0, s7)
        return result
      }
    },
    legend: {
      show: false // 使用自定义图例
    },
    grid: {
      top: 40,
      right: 30,
      bottom: 60,
      left: 60,
      containLabel: false
    },
    xAxis: {
      type: 'category',
      data: x_axis,
      axisLine: {
        lineStyle: {
          color: '#e5e7eb'
        }
      },
      axisLabel: {
        color: '#6b7280',
        fontSize: 12,
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif'
      },
      axisTick: {
        show: false
      }
    },
    yAxis: {
      type: 'value',
      axisLine: {
        show: false
      },
      axisTick: {
        show: false
      },
      axisLabel: {
        color: '#6b7280',
        fontSize: 12,
        // 中文函数注释：Y轴标签格式化，保费以万元整数显示，其他指标千分位整数
        formatter: (value) => formatNumber(value)
      },
      splitLine: {
        lineStyle: {
          color: '#f3f4f6',
          type: 'dashed'
        }
      }
    },
    series: getSeriesOption(series, colors),
    animation: true,
    animationDuration: 1000,
    animationEasing: 'cubicOut'
  }

  chartInstance.setOption(option)
}

/**
 * 函数：getSeriesOption
 * 作用：根据当前图表类型生成对应的系列配置
 * 入参：series（数据系列）, colors（颜色数组）
 * 返回：ECharts series 配置数组
 */
function getSeriesOption(series, colors) {
  const isLine = chartType.value === 'line'
  
  return series.map((item, index) => {
    const color = colors[index % colors.length]
    const isLatest = item.code === 'D'  // 判断是否为最新周期

    if (isLine) {
      // 折线图配置
      return {
        name: item.name,
        type: 'line',
        data: item.data,
        smooth: true,  // 平滑曲线
        symbol: 'circle',  // 标记点形状
        symbolSize: isLatest ? 6 : 4,  // 最新周期标记点更大
        lineStyle: {
          width: isLatest ? 3 : 2,  // 最新周期线条更粗
          color: color
        },
        itemStyle: {
          color: color
        },
        emphasis: {
          focus: 'series',
          lineStyle: {
            width: 4  // 悬停时加粗
          },
          itemStyle: {
            borderWidth: isLatest ? 3 : 2,
            borderColor: color,
            shadowBlur: 10,
            shadowColor: color
          }
        },
        // 区域填充（仅最新周期）
        areaStyle: isLatest ? {
          color: {
            type: 'linear',
            x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: color + '30' },  // 半透明
              { offset: 1, color: color + '00' }   // 完全透明
            ]
          }
        } : null
      }
    } else {
      // 柱状图配置（保持原有配置）
      return {
        name: item.name,
        type: 'bar',
        data: item.data,
        barWidth: '20%',
        itemStyle: {
          color: color,
          borderRadius: [2, 2, 0, 0]
        },
        emphasis: {
          focus: 'series',
          itemStyle: {
            shadowBlur: 10,
            shadowColor: color,
            borderWidth: isLatest ? 2 : 0,  // 最新周期强调边框
            borderColor: color
          }
        },
        // 最新周期加粗显示
        lineStyle: isLatest ? { width: 3 } : { width: 2 }
      }
    }
  })
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
  () => props.chartData,
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
.chart-view {
  background: v-bind('theme.business.value.cardBg');
  border: v-bind('theme.business.value.cardBorder');
  border-radius: v-bind('theme.radius.value.lg');
  box-shadow: v-bind('theme.business.value.cardShadow');
  padding: v-bind('theme.spacing.value.xl');
  display: flex;
  flex-direction: column;
  gap: v-bind('theme.spacing.value.lg');
}

/* Header */
.chart-view__header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: v-bind('theme.spacing.value.lg');
}

.chart-view__title-group {
  display: flex;
  flex-direction: column;
  gap: v-bind('theme.spacing.value.xs');
}

.chart-view__title {
  font-size: v-bind('theme.typography.value.xl');
  font-weight: 700;
  color: v-bind('theme.colors.value.textPrimary');
  margin: 0;
}

.chart-view__subtitle {
  font-size: v-bind('theme.typography.value.sm');
  color: v-bind('theme.colors.value.textSecondary');
  margin: 0;
}

.chart-view__meta {
  display: flex;
  align-items: center;
  gap: v-bind('theme.spacing.value.md');
}

.chart-view__date {
  font-size: v-bind('theme.typography.value.xs');
  color: v-bind('theme.colors.value.textTertiary');
  padding: 4px 12px;
  background: v-bind('theme.colors.value.bgTint');
  border-radius: v-bind('theme.radius.value.sm');
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
  padding: 6px 12px;
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

/* 图表类型切换器 */
.chart-type-switcher {
  display: flex;
  gap: 4px;
  background: rgba(0, 0, 0, 0.03);
  padding: 4px;
  border-radius: v-bind('theme.radius.value.md');
}

.chart-type-switcher__button {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
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

.chart-type-switcher__button:hover:not(.chart-type-switcher__button--active) {
  background: rgba(0, 0, 0, 0.04);
  color: v-bind('theme.colors.value.textPrimary');
}

.chart-type-switcher__button--active {
  background: white;
  color: v-bind('theme.colors.value.primary');
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
  font-weight: 600;
}

.chart-type-switcher__icon {
  font-size: 14px;
}

/* Body */
.chart-view__body {
  position: relative;
  min-height: 300px;
}

.chart-view__canvas {
  width: 100%;
}

/* Loading */
.chart-view__loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: v-bind('theme.spacing.value.md');
  min-height: 300px;
}

.chart-view__spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(168, 85, 247, 0.1);
  border-top-color: v-bind('theme.colors.value.primary');
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.chart-view__loading-text {
  font-size: v-bind('theme.typography.value.sm');
  color: v-bind('theme.colors.value.textSecondary');
}

/* Empty */
.chart-view__empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: v-bind('theme.spacing.value.md');
  min-height: 300px;
}

.chart-view__empty-icon {
  font-size: 64px;
  opacity: 0.3;
}

.chart-view__empty-text {
  font-size: v-bind('theme.typography.value.base');
  color: v-bind('theme.colors.value.textTertiary');
  margin: 0;
}

/* Legend */
.chart-view__legend {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: v-bind('theme.spacing.value.xl');
  padding-top: v-bind('theme.spacing.value.md');
  border-top: v-bind('theme.business.value.divider');
}

.chart-view__legend-item {
  display: flex;
  align-items: center;
  gap: v-bind('theme.spacing.value.sm');
}

.chart-view__legend-marker {
  display: inline-block;
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.chart-view__legend-label {
  font-size: v-bind('theme.typography.value.sm');
  color: v-bind('theme.colors.value.textSecondary');
  font-weight: 500;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .chart-view {
    padding: v-bind('theme.spacing.value.lg');
  }

  .chart-view__header {
    flex-direction: column;
    gap: v-bind('theme.spacing.value.md');
  }

  .chart-view__legend {
    flex-wrap: wrap;
    gap: v-bind('theme.spacing.value.md');
  }
}
</style>
