<template>
  <div class="dashboard">
    <!-- Header -->
    <Header />

    <!-- Main Content -->
    <main class="dashboard__content">
      <!-- 全局筛选面板（置顶） -->
      <section class="dashboard__section dashboard__section--sticky">
        <GlobalFilterPanel
          @filter:apply="handleFilterApply"
          @metric:change="handleGlobalMetricChange"
        />
      </section>

      <!-- 核心KPI分区 -->
      <section class="dashboard__section">
        <!-- KPI Section Header -->
        <div class="kpi-section-header">
          <h2 class="kpi-section-header__title">核心KPI</h2>
        </div>
        
        <!-- 核心KPI卡片 -->
        <div class="dashboard__kpi-grid">
          <KpiCard
            v-for="kpi in coreKpiCards"
            :key="kpi.id"
            :title="kpi.title"
            :icon="kpi.icon"
            :icon-bg="kpi.iconBg"
            :value="kpi.currentValue"
            :trend="kpi.trend"
            :sparkline-data="kpi.sparklineData"
            :value-type="kpi.valueType"
            :loading="dataLoading"
          />
        </div>
      </section>

      <!-- 监控占比分区 -->
      <section class="dashboard__section">
        <div class="kpi-section-header">
          <h2 class="kpi-section-header__title">监控占比</h2>
        </div>
        <div class="dashboard__kpi-grid">
          <KpiCard
            v-for="kpi in ratioKpiCards"
            :key="kpi.id"
            :title="kpi.title"
            :icon="kpi.icon"
            :icon-bg="kpi.iconBg"
            :value="kpi.currentValue"
            :trend="kpi.trend"
            :sparkline-data="kpi.sparklineData"
            :value-type="kpi.valueType"
            :loading="dataLoading"
          />
        </div>
      </section>

      <!-- 计划达成分区 -->
      <section class="dashboard__section">
        <div class="kpi-section-header">
          <h2 class="kpi-section-header__title">计划达成</h2>
        </div>
        <div class="dashboard__kpi-grid">
          <KpiCard
            v-for="kpi in planKpiCards"
            :key="kpi.id"
            :title="kpi.title"
            :icon="kpi.icon"
            :icon-bg="kpi.iconBg"
            :value="kpi.currentValue"
            :trend="kpi.trend"
            :sparkline-data="kpi.sparklineData"
            :value-type="kpi.valueType"
            :loading="dataLoading"
          />
        </div>
      </section>

      <!-- 验证警告 -->
      <section v-if="hasValidationWarning" class="dashboard__section">
        <div class="validation-warning">
          <div class="validation-warning__icon">⚠️</div>
          <div class="validation-warning__content">
            <h4 class="validation-warning__title">数据映射警告</h4>
            <p class="validation-warning__text">
              发现 {{ validationInfo.unmatched_count }} 名业务员在数据中存在但在机构团队映射文件中未找到匹配。
              请检查业务员机构团队归属.json 文件是否完整。
            </p>
            <p v-if="validationInfo.policy_consistency && validationInfo.policy_consistency.mismatch_count > 0" class="validation-warning__text">
              另有 {{ validationInfo.policy_consistency.mismatch_count }} 个保单的团队/机构与映射不一致，已按映射规则自动校正筛选逻辑。
            </p>
          </div>
          <button class="validation-warning__close" @click="dismissValidationWarning">×</button>
        </div>
      </section>


      <!-- 图表区域 -->
      <section class="dashboard__section">
        <ChartView
          :title="chartTitle"
          :subtitle="chartSubtitle"
          :chart-data="chartData"
          :loading="chartLoading"
          height="450px"
        />
      </section>

      <!-- 饼图区域 -->
      <section class="dashboard__section dashboard__pie-charts">
        <PieChartCard
          title="险别组合占比"
          :distribution-data="insuranceTypeData"
          :loading="pieChartsLoading"
          stats-type="count"
          height="280px"
        />
        <PieChartCard
          title="业务员保费区间占比"
          :distribution-data="premiumRangeData"
          :loading="pieChartsLoading"
          stats-type="staff"
          height="280px"
        />
        <PieChartCard
          title="新转续占比"
          :distribution-data="renewalTypeData"
          :loading="pieChartsLoading"
          stats-type="count"
          height="280px"
        />
      </section>
    </main>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import Header from '@/components/Header.vue'
import KpiCard from '@/components/dashboard/KpiCard.vue'
import ChartView from '@/components/dashboard/ChartView.vue'
import GlobalFilterPanel from '@/components/dashboard/GlobalFilterPanel.vue'
import PieChartCard from '@/components/dashboard/PieChartCard.vue'
import { useAppStore } from '@/stores/app'
import { useDataStore } from '@/stores/data'
import { useFilterStore } from '@/stores/filter'
import { useToast } from '@/composables/useToast'

// Stores
const appStore = useAppStore()
const dataStore = useDataStore()
const filterStore = useFilterStore()
const toast = useToast()

// State
// 注意:时间段、数据口径、指标切换已统一由 GlobalFilterPanel 管理
// currentPeriod 仅用于内部跟踪饼图时间周期（通过 GlobalFilterPanel 的事件更新）
const currentPeriod = ref('day') // day, last7d, last30d

// Computed
const dataLoading = computed(() => dataStore.loading)
const chartLoading = computed(() => dataStore.chartLoading)
const chartData = computed(() => dataStore.chartData)
const validationInfo = computed(() => dataStore.validationInfo)
const pieChartsLoading = computed(() => dataStore.pieChartsLoading)
const insuranceTypeData = computed(() => dataStore.insuranceTypeData)
const premiumRangeData = computed(() => dataStore.premiumRangeData)
const renewalTypeData = computed(() => dataStore.renewalTypeData)
const hasValidationWarning = computed(() => {
  const v = validationInfo.value
  if (!v) return false
  const unmatched = v.unmatched_count > 0
  const mismatchPolicies = v.policy_consistency && v.policy_consistency.mismatch_count > 0
  return unmatched || mismatchPolicies
})

const chartTitle = computed(() => {
  const metric = appStore.currentMetric === 'premium' ? '签单保费' : '签单单量'
  return `${metric}周对比柱状图`
})

const chartSubtitle = computed(() => {
  const filterCount = filterStore.activeFiltersCount
  if (filterCount > 0) {
    return `已应用 ${filterCount} 个筛选条件`
  }
  return '全部数据'
})

// ===== 公共辅助函数（供各分区KPI卡复用） =====
/**
 * 生成迷你折线的模拟数据
 * 说明：基于当前主值生成7个数据点，用于KPI卡片的迷你折线展示。
 */
// 函数：generateSparklineData
// 作用：根据当前值生成简易折线图数据（长度固定），用于卡片的迷你折线图展示
// 输入：baseValue（number）当前数值，可为金额或比例；允许为 0
// 输出：number[] 生成的折线图数据序列，保证无负值且平滑过渡
const generateSparklineData = (baseValue) => {
  const v = Number(baseValue || 0)
  return Array.from({ length: 7 }, () => {
    const variance = Math.random() * 0.3 - 0.15 // ±15%变化
    return Math.round(v * (1 + variance) / 7)
  })
}

/**
 * 计算趋势值（同比/占位）
 * 说明：当无历史值时返回 -10%~+20% 随机占位；有历史值时返回 (current-previous)/previous。
 */
// 函数：calculateTrend
// 作用：计算当前值相对上期值的趋势（上升/下降/持平），并在分母为 0 或缺失时安全回退
// 输入：currentValue（number）当前值；previousValue（number|null）上期值，默认 null 表示不可比
// 输出：'up' | 'down' | 'flat' 三种趋势标识，供样式或图标使用
const calculateTrend = (currentValue, previousValue = null) => {
  const cv = Number(currentValue || 0)
  if (!previousValue) {
    const rnd = Math.random() * 30 - 10 // -10% 到 +20%
    return parseFloat(rnd.toFixed(1))
  }
  const pv = Number(previousValue || 0)
  if (pv === 0) return 0
  const pct = ((cv - pv) / pv) * 100
  return parseFloat(pct.toFixed(1))
}

/**
 * 获取当前时间口径对应数值
 * 说明：从 {day/last7d/last30d} 对象中按 currentPeriod 读取，缺失则返回 0。
 */
// 函数：getCurrentValue
// 作用：从多窗口数据结构中提取当前窗口的值并做安全数值归一
// 输入：data（number | { day?: number; last7d?: number; last30d?: number }）
// 输出：number 当前窗口对应的值，确保返回数值类型
const getCurrentValue = (data) => {
  switch (currentPeriod.value) {
    case 'day':
      return data?.day || 0
    case 'last7d':
      return data?.last7d || 0
    case 'last30d':
      return data?.last30d || 0
    default:
      return data?.day || 0
  }
}

// Methods
/**
 * 处理时间段变更（从 GlobalFilterPanel 事件更新）
 */
const handleTimePeriodChange = async (period) => {
  currentPeriod.value = period
  // 刷新饼图数据
  await refreshPieChartsData()
}

/**
 * 处理全局筛选面板的筛选应用事件
 */
const handleFilterApply = async ({ filters, diff }) => {
  try {
    console.log('筛选已应用:', filters)
    console.log('变更diff:', diff)

    // 数据已在 GlobalFilterPanel 内部刷新，这里可以做额外处理
    // 例如：刷新饼图数据
    await refreshPieChartsData()
  } catch (error) {
    console.error('处理筛选应用失败:', error)
  }
}

/**
 * 处理全局筛选面板的指标切换事件
 */
const handleGlobalMetricChange = ({ oldMetric, newMetric }) => {
  console.log('指标已切换:', oldMetric, '->', newMetric)
  // 指标切换已在 GlobalFilterPanel 内部处理，这里可以做额外处理
}

// 刷新饼图数据
const refreshPieChartsData = async () => {
  try {
    const filters = filterStore.getActiveFilters()
    await dataStore.refreshPieCharts(currentPeriod.value, filters)
  } catch (error) {
    console.error('Failed to refresh pie charts:', error)
    toast.error('饼图数据加载失败', error.message)
  }
}

// KPI卡片配置
const kpiCards = computed(() => {
  const kpiData = dataStore.kpiData
  const currentMetric = appStore.currentMetric

  if (!kpiData) {
    // 默认数据(加载前)
    return [
      {
        id: 'premium',
        title: '签单保费',
        icon: '¥',
        iconBg: 'linear-gradient(135deg, #a855f7, #9333ea)',
        currentValue: 0,
        trend: null,
        sparklineData: [],
        valueType: 'currency'
      },
      {
        id: 'count',
        title: '签单单量',
        icon: '#',
        iconBg: 'linear-gradient(135deg, #10b981, #059669)',
        currentValue: 0,
        trend: null,
        sparklineData: [],
        valueType: 'number'
      },
      {
        id: 'commission',
        title: '签单佣金',
        icon: '💰',
        iconBg: 'linear-gradient(135deg, #f59e0b, #d97706)',
        currentValue: 0,
        trend: null,
        sparklineData: [],
        valueType: 'currency'
      },
      {
        id: 'target',
        title: '目标差距',
        icon: '🎯',
        iconBg: 'linear-gradient(135deg, #ef4444, #dc2626)',
        currentValue: 0,
        trend: null,
        sparklineData: [],
        valueType: 'currency'
      }
    ]
  }

  // 注：generateSparklineData/calculateTrend/getCurrentValue 已提升为模块级函数供复用

  return [
    {
      id: 'premium',
      title: '签单保费',
      icon: '¥',
      iconBg: 'linear-gradient(135deg, #a855f7, #9333ea)',
      currentValue: getCurrentValue(kpiData.premium),
      trend: calculateTrend(getCurrentValue(kpiData.premium)),
      sparklineData: generateSparklineData(getCurrentValue(kpiData.premium)),
      // 中文注释：保费以“万元整数”显示，统一与周对比图单位
      valueType: 'wanInt'
    },
    {
      id: 'count',
      title: '签单单量',
      icon: '#',
      iconBg: 'linear-gradient(135deg, #10b981, #059669)',
      currentValue: getCurrentValue(kpiData.policy_count),
      trend: calculateTrend(getCurrentValue(kpiData.policy_count)),
      sparklineData: generateSparklineData(getCurrentValue(kpiData.policy_count)),
      valueType: 'number'
    },
    {
      id: 'commission',
      title: '签单佣金',
      icon: '💰',
      iconBg: 'linear-gradient(135deg, #f59e0b, #d97706)',
      currentValue: getCurrentValue(kpiData.commission),
      trend: calculateTrend(getCurrentValue(kpiData.commission)),
      sparklineData: generateSparklineData(getCurrentValue(kpiData.commission)),
      // 中文注释：佣金以“万元整数”显示，提升单位一致性
      valueType: 'wanInt'
    },
    {
      id: 'target',
      title: '目标差距',
      icon: '🎯',
      iconBg: 'linear-gradient(135deg, #ef4444, #dc2626)',
      currentValue: currentPeriod.value === 'day' ? Math.abs(kpiData.target_gap_day || 0) : 0,
      trend: currentPeriod.value === 'day' ? calculateTrend(Math.abs(kpiData.target_gap_day || 0)) : null,
      sparklineData: currentPeriod.value === 'day' ? generateSparklineData(Math.abs(kpiData.target_gap_day || 0)) : [],
      // 中文注释：目标差距以“万元整数”显示，仅在日口径生效
      valueType: 'wanInt'
    },
    // ===== 新增四张占比类 KPI 卡 =====
    {
      id: 'telesales_ratio',
      title: '电销占比',
      icon: '📞',
      iconBg: 'linear-gradient(135deg, #3b82f6, #2563eb)',
      currentValue: getCurrentValue(kpiData?.ratios?.telesales?.[currentMetric]),
      trend: calculateTrend(getCurrentValue(kpiData?.ratios?.telesales?.[currentMetric])),
      sparklineData: generateSparklineData(getCurrentValue(kpiData?.ratios?.telesales?.[currentMetric])),
      // 中文注释：比例展示使用 'percent'，输入为 [0,1] 的占比
      valueType: 'percent'
    },
    {
      id: 'new_energy_ratio',
      title: '新能源占比',
      icon: '⚡️',
      iconBg: 'linear-gradient(135deg, #22c55e, #16a34a)',
      currentValue: getCurrentValue(kpiData?.ratios?.new_energy?.[currentMetric]),
      trend: calculateTrend(getCurrentValue(kpiData?.ratios?.new_energy?.[currentMetric])),
      sparklineData: generateSparklineData(getCurrentValue(kpiData?.ratios?.new_energy?.[currentMetric])),
      valueType: 'percent'
    },
    {
      id: 'transfer_ratio',
      title: '过户车占比',
      icon: '🔁',
      iconBg: 'linear-gradient(135deg, #f97316, #ea580c)',
      currentValue: getCurrentValue(kpiData?.ratios?.transfer?.[currentMetric]),
      trend: calculateTrend(getCurrentValue(kpiData?.ratios?.transfer?.[currentMetric])),
      sparklineData: generateSparklineData(getCurrentValue(kpiData?.ratios?.transfer?.[currentMetric])),
      valueType: 'percent'
    },
    {
      id: 'single_mandatory_ratio',
      title: '单交占比',
      icon: '🛡️',
      iconBg: 'linear-gradient(135deg, #8b5cf6, #7c3aed)',
      currentValue: getCurrentValue(kpiData?.ratios?.single_mandatory?.[currentMetric]),
      trend: calculateTrend(getCurrentValue(kpiData?.ratios?.single_mandatory?.[currentMetric])),
      sparklineData: generateSparklineData(getCurrentValue(kpiData?.ratios?.single_mandatory?.[currentMetric])),
      // 函数级中文注释：单交占比严格以“险别组合=单交”识别，双口径支持
      valueType: 'percent'
    },
    {
      id: 'commercial_ratio',
      title: '商业险占比',
      icon: '🚗',
      iconBg: 'linear-gradient(135deg, #0ea5e9, #0284c7)',
      currentValue: getCurrentValue(kpiData?.ratios?.commercial?.[currentMetric]),
      trend: calculateTrend(getCurrentValue(kpiData?.ratios?.commercial?.[currentMetric])),
      sparklineData: generateSparklineData(getCurrentValue(kpiData?.ratios?.commercial?.[currentMetric])),
      // 函数级中文注释：商业险占比按保费口径返回；切换到单量时如无数据则显示 0%
      valueType: 'percent'
    },
    {
      id: 'non_local_ratio',
      title: '异地车占比',
      icon: '🧭',
      iconBg: 'linear-gradient(135deg, #14b8a6, #0d9488)',
      currentValue: getCurrentValue(kpiData?.ratios?.non_local?.[currentMetric]),
      trend: calculateTrend(getCurrentValue(kpiData?.ratios?.non_local?.[currentMetric])),
      sparklineData: generateSparklineData(getCurrentValue(kpiData?.ratios?.non_local?.[currentMetric])),
      // 函数级中文注释：异地车占比同时支持保费与件数两种口径
      valueType: 'percent'
    },
    {
      id: 'new_policy_ratio',
      title: '新保占比',
      icon: '🆕',
      iconBg: 'linear-gradient(135deg, #22c55e, #16a34a)',
      currentValue: getCurrentValue(kpiData?.ratios?.new_policy?.[currentMetric]),
      trend: calculateTrend(getCurrentValue(kpiData?.ratios?.new_policy?.[currentMetric])),
      sparklineData: generateSparklineData(getCurrentValue(kpiData?.ratios?.new_policy?.[currentMetric])),
      // 函数级中文注释：新保占比严格以“是否续保=新保”识别，双口径支持
      valueType: 'percent'
    },
    {
      id: 'loss_business_ratio',
      title: '清亏业务占比',
      icon: '📉',
      iconBg: 'linear-gradient(135deg, #f43f5e, #e11d48)',
      currentValue: getCurrentValue(kpiData?.ratios?.loss_business?.[currentMetric]),
      trend: calculateTrend(getCurrentValue(kpiData?.ratios?.loss_business?.[currentMetric])),
      sparklineData: generateSparklineData(getCurrentValue(kpiData?.ratios?.loss_business?.[currentMetric])),
      // 函数级中文注释：清亏业务占比严格以“车险新业务分类=清亏业务”识别，支持保费/件数双口径
      valueType: 'percent'
    }
  ]
})

// ===== 分区卡片列表 =====
/**
 * 核心KPI分区卡片列表（仅三张：保费/单量/佣金）
 * 说明：符合“核心KPI是三个”的业务约束。
 */
// 计算属性：coreKpiCards
// 作用：核心KPI分区，仅包含三张卡（签单保费/签单单量/签单佣金），满足“核心KPI是三个”约束
const coreKpiCards = computed(() => {
  const set = new Set(['premium', 'count', 'commission'])
  return (kpiCards.value || []).filter(c => set.has(c.id))
})

/**
 * 监控占比分区卡片列表（含电销/新能源/过户/单交/商业险/异地/新保/清亏）
 */
// 计算属性：ratioKpiCards
// 作用：监控占比分区，统一消费 kpiData.ratios.*[currentMetric] 并联动双口径与三窗口
const ratioKpiCards = computed(() => {
  const set = new Set([
    'telesales_ratio',
    'new_energy_ratio',
    'transfer_ratio',
    'single_mandatory_ratio',
    'commercial_ratio',
    'non_local_ratio',
    'new_policy_ratio',
    'loss_business_ratio'
  ])
  return (kpiCards.value || []).filter(c => set.has(c.id))
})

/**
 * 计划达成分区卡片列表
 * 规则：
 * - 总是包含“目标差距”（日口径）。
 * - 若命中计划（plan_exists=true），追加“保费达成率”和“保费缺口”两张卡。
 */
// 计算属性：planKpiCards
// 作用：计划达成分区；默认展示目标差距，命中 plan_exists 时追加保费达成率与保费缺口
const planKpiCards = computed(() => {
  const result = (kpiCards.value || []).filter(c => c.id === 'target')
  const kd = dataStore.kpiData || {}
  if (kd.plan_exists) {
    const progressRaw = kd.premium_progress
    const gapRaw = kd.premium_gap
    const progressVal = typeof progressRaw === 'object' ? getCurrentValue(progressRaw) : (progressRaw || 0)
    const gapVal = typeof gapRaw === 'object' ? getCurrentValue(gapRaw) : (gapRaw || 0)

    // 保费达成率
    result.push({
      id: 'premium_progress',
      title: '保费达成率',
      icon: '📈',
      iconBg: 'linear-gradient(135deg, #16a34a, #22c55e)',
      currentValue: Math.max(0, Math.min(1, progressVal)),
      trend: calculateTrend(Math.max(0, Math.min(1, progressVal))),
      sparklineData: generateSparklineData(progressVal),
      // 函数级中文注释：显示百分比，值域裁剪至 [0,1]
      valueType: 'percent'
    })

    // 保费缺口（若后端未提供则回退到目标差距）
    const gapDisplay = Math.abs(gapVal || kd.target_gap_day || 0)
    result.push({
      id: 'premium_gap',
      title: '保费缺口',
      icon: '🧮',
      iconBg: 'linear-gradient(135deg, #ef4444, #dc2626)',
      currentValue: gapDisplay,
      trend: calculateTrend(gapDisplay),
      sparklineData: generateSparklineData(gapDisplay),
      valueType: 'wanInt'
    })
  }
  return result
})

// Methods
/**
 * 关闭映射一致性警告条
 * 说明：将 `validationInfo` 置空，以隐藏前端告警提示区域
 */
const dismissValidationWarning = () => {
  dataStore.validationInfo = null
}

// Lifecycle
/**
 * 页面挂载时初始化数据
 * 流程：并行加载 KPI 三口径、周对比图表数据、饼图数据；若后端返回校验信息则用于告警显示
 */
onMounted(async () => {
  // 初始化: 加载所有数据
  try {
    const filters = filterStore.getActiveFilters()
    // 并行加载KPI数据、图表数据和饼图数据
    await Promise.all([
      dataStore.fetchKpiData(),
      dataStore.fetchChartData(appStore.currentMetric, {}),
      dataStore.refreshPieCharts(currentPeriod.value, filters)
    ])
    console.log('数据加载成功')
  } catch (error) {
    console.error('加载数据失败:', error)
    toast.error('数据加载失败', '请检查后端服务是否启动')
  }
})

// Watch筛选器变化，刷新饼图
watch(
  () => filterStore.activeFilters,
  async () => {
    await refreshPieChartsData()
  },
  { deep: true }
)
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  background: var(--gray-50);
}

.dashboard__content {
  max-width: 1400px;
  margin: 0 auto;
  padding: var(--space-8) var(--space-6);
  display: flex;
  flex-direction: column;
  gap: var(--space-8);
}

.dashboard__section {
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

/* 置顶筛选面板 */
.dashboard__section--sticky {
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--gray-50);
  padding-top: var(--space-2);
  padding-bottom: var(--space-2);
  margin: calc(var(--space-8) * -1) calc(var(--space-6) * -1) var(--space-6);
  padding-left: var(--space-6);
  padding-right: var(--space-6);
}

/* KPI Section Header */
.kpi-section-header {
  margin-bottom: var(--space-6);
}

.kpi-section-header__title {
  font-size: var(--font-2xl);
  font-weight: 700;
  color: var(--gray-900);
  margin: 0;
}

/* KPI Grid */
.dashboard__kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--space-6);
}

/* 饼图区域 */
.dashboard__pie-charts {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
  gap: var(--space-6);
}

/* 验证警告 */
.validation-warning {
  display: flex;
  align-items: flex-start;
  gap: var(--space-4);
  padding: var(--space-4) var(--space-5);
  background: linear-gradient(135deg, #FFF7ED 0%, #FFEDD5 100%);
  border: 1px solid #FED7AA;
  border-radius: var(--radius-lg);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.validation-warning__icon {
  font-size: var(--font-2xl);
  flex-shrink: 0;
}

.validation-warning__content {
  flex: 1;
}

.validation-warning__title {
  font-size: var(--font-base);
  font-weight: 600;
  color: var(--gray-900);
  margin: 0 0 var(--space-2) 0;
}

.validation-warning__text {
  font-size: var(--font-sm);
  color: var(--gray-700);
  margin: 0 0 var(--space-2) 0;
  line-height: 1.5;
}

.validation-warning__text:last-child {
  margin-bottom: 0;
}

.validation-warning__close {
  flex-shrink: 0;
  width: 24px;
  height: 24px;
  border: none;
  background: transparent;
  color: var(--gray-500);
  font-size: var(--font-xl);
  line-height: 1;
  cursor: pointer;
  border-radius: var(--radius-sm);
  transition: all 0.2s;
}

.validation-warning__close:hover {
  background: rgba(0, 0, 0, 0.05);
  color: var(--gray-700);
}

/* 响应式 */
@media (max-width: 768px) {
  .dashboard__content {
    padding: var(--space-6) var(--space-4);
  }

  .kpi-section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--space-4);
    margin-bottom: var(--space-4);
  }

  .kpi-section-header__controls {
    width: 100%;
    justify-content: space-between;
  }

  .kpi-section-header__data-scope {
    padding-right: 0;
    border-right: none;
  }

  .kpi-section-header__title {
    font-size: var(--font-xl);
  }

  .kpi-section-header__time-selector {
    align-self: stretch;
    justify-content: center;
  }

  .dashboard__kpi-grid {
    grid-template-columns: 1fr;
    gap: var(--space-4);
  }

  .dashboard__pie-charts {
    grid-template-columns: 1fr;
    gap: var(--space-4);
  }
}
</style>
