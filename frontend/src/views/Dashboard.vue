<template>
  <div class="dashboard">
    <!-- Header -->
    <Header />

    <!-- Main Content -->
    <main class="dashboard__content">
      <!-- KPI Cards Grid -->
      <section class="dashboard__section">
        <div class="dashboard__kpi-grid">
          <KpiCard
            v-for="kpi in kpiCards"
            :key="kpi.id"
            :title="kpi.title"
            :icon="kpi.icon"
            :icon-bg="kpi.iconBg"
            :day-value="kpi.dayValue"
            :last7d-value="kpi.last7dValue"
            :last30d-value="kpi.last30dValue"
            :trend="kpi.trend"
            :sparkline-data="kpi.sparklineData"
            :value-type="kpi.valueType"
            :loading="dataLoading"
          />
        </div>
      </section>

      <!-- 占位符: 后续添加图表区域 -->
      <section class="dashboard__section">
        <div class="dashboard__placeholder">
          <div class="dashboard__placeholder-icon">📊</div>
          <h3 class="dashboard__placeholder-title">图表区域</h3>
          <p class="dashboard__placeholder-text">
            ChartView 和 FilterPanel 组件将在此处展示
          </p>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import Header from '@/components/Header.vue'
import KpiCard from '@/components/dashboard/KpiCard.vue'
import { useAppStore } from '@/stores/app'
import { useDataStore } from '@/stores/data'
import { useToast } from '@/composables/useToast'

// Stores
const appStore = useAppStore()
const dataStore = useDataStore()
const toast = useToast()

// Computed
const dataLoading = computed(() => dataStore.loading)

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
        dayValue: 0,
        last7dValue: 0,
        last30dValue: 0,
        trend: null,
        sparklineData: [],
        valueType: 'currency'
      },
      {
        id: 'count',
        title: '签单单量',
        icon: '#',
        iconBg: 'linear-gradient(135deg, #10b981, #059669)',
        dayValue: 0,
        last7dValue: 0,
        last30dValue: 0,
        trend: null,
        sparklineData: [],
        valueType: 'number'
      },
      {
        id: 'commission',
        title: '签单佣金',
        icon: '💰',
        iconBg: 'linear-gradient(135deg, #f59e0b, #d97706)',
        dayValue: 0,
        last7dValue: 0,
        last30dValue: 0,
        trend: null,
        sparklineData: [],
        valueType: 'currency'
      },
      {
        id: 'target',
        title: '目标差距',
        icon: '🎯',
        iconBg: 'linear-gradient(135deg, #ef4444, #dc2626)',
        dayValue: 0,
        last7dValue: 0,
        last30dValue: 0,
        trend: null,
        sparklineData: [],
        valueType: 'currency'
      }
    ]
  }

  // 模拟7天趋势数据 (实际应该从后端获取)
  const generateSparklineData = (baseValue) => {
    // 生成7个模拟数据点
    return Array.from({ length: 7 }, (_, i) => {
      const variance = Math.random() * 0.3 - 0.15 // ±15%变化
      return Math.round(baseValue * (1 + variance) / 7)
    })
  }

  // 计算趋势 (模拟同比增长率)
  const calculateTrend = (currentValue, previousValue = null) => {
    if (!previousValue) {
      // 如果没有历史数据,生成随机趋势
      return (Math.random() * 30 - 10).toFixed(1) // -10% 到 +20%
    }
    return ((currentValue - previousValue) / previousValue * 100).toFixed(1)
  }

  return [
    {
      id: 'premium',
      title: '签单保费',
      icon: '¥',
      iconBg: 'linear-gradient(135deg, #a855f7, #9333ea)',
      dayValue: kpiData.premium?.day || 0,
      last7dValue: kpiData.premium?.last7d || 0,
      last30dValue: kpiData.premium?.last30d || 0,
      trend: parseFloat(calculateTrend(kpiData.premium?.day || 0)),
      sparklineData: generateSparklineData(kpiData.premium?.last7d || 0),
      valueType: 'currency'
    },
    {
      id: 'count',
      title: '签单单量',
      icon: '#',
      iconBg: 'linear-gradient(135deg, #10b981, #059669)',
      dayValue: kpiData.policy_count?.day || 0,
      last7dValue: kpiData.policy_count?.last7d || 0,
      last30dValue: kpiData.policy_count?.last30d || 0,
      trend: parseFloat(calculateTrend(kpiData.policy_count?.day || 0)),
      sparklineData: generateSparklineData(kpiData.policy_count?.last7d || 0),
      valueType: 'number'
    },
    {
      id: 'commission',
      title: '签单佣金',
      icon: '💰',
      iconBg: 'linear-gradient(135deg, #f59e0b, #d97706)',
      dayValue: kpiData.commission?.day || 0,
      last7dValue: kpiData.commission?.last7d || 0,
      last30dValue: kpiData.commission?.last30d || 0,
      trend: parseFloat(calculateTrend(kpiData.commission?.day || 0)),
      sparklineData: generateSparklineData(kpiData.commission?.last7d || 0),
      valueType: 'currency'
    },
    {
      id: 'target',
      title: '目标差距',
      icon: '🎯',
      iconBg: 'linear-gradient(135deg, #ef4444, #dc2626)',
      dayValue: Math.abs(kpiData.target_gap_day || 0),
      last7dValue: 0, // 目标差距通常只看当日
      last30dValue: 0,
      trend: kpiData.target_gap_day < 0 ? Math.abs(parseFloat(calculateTrend(kpiData.target_gap_day))) : -Math.abs(parseFloat(calculateTrend(kpiData.target_gap_day))),
      sparklineData: [],
      valueType: 'currency'
    }
  ]
})

// Lifecycle
onMounted(async () => {
  // 初始化: 加载KPI数据
  try {
    await dataStore.fetchKpiData()
    console.log('KPI数据加载成功', dataStore.kpiData)
  } catch (error) {
    console.error('加载KPI数据失败:', error)
    toast.error('数据加载失败', '请检查后端服务是否启动')
  }
})
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

/* KPI Grid */
.dashboard__kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--space-6);
}

/* 占位符样式 */
.dashboard__placeholder {
  background: white;
  border: 2px dashed var(--gray-300);
  border-radius: var(--radius-lg);
  padding: var(--space-8);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--space-4);
  min-height: 400px;
}

.dashboard__placeholder-icon {
  font-size: 64px;
  opacity: 0.5;
}

.dashboard__placeholder-title {
  font-size: var(--text-xl);
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.dashboard__placeholder-text {
  font-size: var(--text-base);
  color: var(--text-secondary);
  text-align: center;
  max-width: 400px;
  margin: 0;
}

/* 响应式 */
@media (max-width: 768px) {
  .dashboard__content {
    padding: var(--space-6) var(--space-4);
  }

  .dashboard__kpi-grid {
    grid-template-columns: 1fr;
    gap: var(--space-4);
  }
}
</style>
