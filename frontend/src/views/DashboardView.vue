<template>
  <div class="dashboard">
    <header class="dashboard__header">
      <div class="dashboard__titles">
        <h1 class="dashboard__title">车险签单数据分析仪表板</h1>
        <p class="dashboard__subtitle">掌握核心指标与团队表现</p>
      </div>
      <div class="dashboard__actions">
        <div class="dashboard__date">最新数据日期：{{ latestDateLabel }}</div>
        <div class="dashboard__metric-switcher" role="group" aria-label="指标切换">
          <button
            v-for="metric in metricOptions"
            :key="metric.value"
            type="button"
            class="dashboard__metric-button"
            :class="{ 'dashboard__metric-button--active': appStore.currentMetric === metric.value }"
            @click="handleMetricSwitch(metric.value)"
          >
            {{ metric.label }}
          </button>
        </div>
        <div class="dashboard__buttons">
          <button type="button" class="dashboard__button" @click="handleRefresh" :disabled="dataStore.refreshing">
            {{ dataStore.refreshing ? '刷新中…' : '刷新数据' }}
          </button>
          <button type="button" class="dashboard__button dashboard__button--secondary" @click="filterStore.togglePanel()">
            {{ filterStore.hasActiveFilters ? '修改筛选' : '筛选' }}
          </button>
        </div>
      </div>
    </header>

    <section class="dashboard__filters" v-if="filterStore.hasActiveFilters">
      <h2 class="dashboard__section-title">已选条件</h2>
      <ul class="dashboard__chips">
        <li v-for="(value, key) in filterStore.activeFilters" :key="key" class="dashboard__chip">
          <span class="dashboard__chip-label">{{ key }}：</span>
          <span>{{ value }}</span>
        </li>
      </ul>
    </section>

    <section class="dashboard__kpi-grid">
      <KpiCard
        v-for="card in kpiCards"
        :key="card.title"
        v-bind="card"
      />
    </section>

    <section class="dashboard__chart">
      <ChartView :option="chartOption" :loading="dataStore.chartLoading">
        <template #title>
          <h2 class="dashboard__section-title">{{ currentMetricLabel }}趋势对比</h2>
        </template>
        <template #meta>
          <span class="dashboard__chart-meta">最近三周日度表现</span>
        </template>
      </ChartView>
    </section>

    <FilterPanel
      :options="filterOptions"
      :team-mapping="filterStore.teamMapping"
      :active-filters="filterStore.activeFilters"
      :loading="filterStore.loading"
      :is-open="filterStore.panelOpen"
      :dimensions="filterStore.orderedDimensions"
      @apply="handleApplyFilters"
      @reset="handleResetFilters"
      @toggle="filterStore.togglePanel()"
    />
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue';
import type { EChartsOption } from 'echarts';
import ChartView from '@/components/dashboard/ChartView.vue';
import FilterPanel from '@/components/dashboard/FilterPanel.vue';
import KpiCard from '@/components/dashboard/KpiCard.vue';
import { useAppStore } from '@/stores/app';
import { useDataStore } from '@/stores/data';
import { useFilterStore } from '@/stores/filter';
import { useToast } from '@/composables/useToast';
import type { MetricKey } from '@/types/api';

const appStore = useAppStore();
const dataStore = useDataStore();
const filterStore = useFilterStore();
const toast = useToast();

const metricOptions: Array<{ label: string; value: MetricKey }> = [
  { label: '总保费', value: 'premium' },
  { label: '保单数量', value: 'policy_count' }
];

const filterOptions = computed(() => filterStore.filterOptions);

const latestDateLabel = computed(() => appStore.latestDate ?? '—');

const currentMetricLabel = computed(() => {
  const current = metricOptions.find((item) => item.value === appStore.currentMetric);
  return current ? current.label : '指标';
});

const chartOption = computed<EChartsOption | null>(() => {
  const payload = dataStore.chartData;
  if (!payload) return null;

  const rootStyles = typeof window !== 'undefined' ? getComputedStyle(document.documentElement) : null;
  const primary = rootStyles?.getPropertyValue('--primary-600').trim() || '#9333ea';
  const secondary = rootStyles?.getPropertyValue('--primary-100').trim() || '#e9d5ff';
  const neutral = rootStyles?.getPropertyValue('--gray-500').trim() || '#6b7280';

  return {
    color: [primary, secondary, neutral],
    tooltip: {
      trigger: 'axis',
      backgroundColor: rootStyles?.getPropertyValue('--surface-elevated').trim() || '#ffffff'
    },
    legend: {
      bottom: 0,
      textStyle: {
        color: rootStyles?.getPropertyValue('--text-secondary').trim() || '#6b7280'
      }
    },
    grid: {
      top: 36,
      left: 32,
      right: 16,
      bottom: 64
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: payload.x_axis,
      axisLine: { lineStyle: { color: rootStyles?.getPropertyValue('--gray-300').trim() || '#d1d5db' } },
      axisLabel: { color: rootStyles?.getPropertyValue('--text-secondary').trim() || '#6b7280' }
    },
    yAxis: {
      type: 'value',
      axisLine: { show: false },
      splitLine: { lineStyle: { color: rootStyles?.getPropertyValue('--gray-100').trim() || '#f3f4f6' } },
      axisLabel: { color: rootStyles?.getPropertyValue('--text-secondary').trim() || '#6b7280' }
    },
    series: payload.series.map((series) => ({
      name: series.name,
      type: 'line',
      smooth: true,
      showSymbol: false,
      emphasis: { focus: 'series' },
      data: series.data,
      areaStyle: { opacity: 0.08 }
    }))
  };
});

const kpiCards = computed(() => {
  const summary = dataStore.kpiSummary;
  const chartSeries = dataStore.chartData?.series?.[0]?.data ?? null;
  if (!summary) return [];

  const trendFromAverage = (value: number, total: number) => {
    if (!total) return null;
    const average = total / 7;
    if (!average) return null;
    return ((value - average) / average) * 100;
  };

  return [
    {
      title: '总保费',
      value: summary.premium.day,
      unit: 'currency',
      trend: trendFromAverage(summary.premium.day, summary.premium.last7d),
      sparklineData: chartSeries,
      description: `近7天累计 ${formatCurrency(summary.premium.last7d)}`,
      targetGap: summary.target_gap_day ?? null,
      icon: '💰'
    },
    {
      title: '保单数量',
      value: summary.policy_count.day,
      unit: 'number',
      trend: trendFromAverage(summary.policy_count.day, summary.policy_count.last7d),
      sparklineData: appStore.currentMetric === 'policy_count' ? chartSeries : null,
      description: `近7天累计 ${formatNumber(summary.policy_count.last7d)}`,
      targetGap: null,
      icon: '📄'
    },
    {
      title: '手续费收入',
      value: summary.commission.day,
      unit: 'currency',
      trend: trendFromAverage(summary.commission.day, summary.commission.last7d),
      sparklineData: null,
      description: `近30天累计 ${formatCurrency(summary.commission.last30d)}`,
      targetGap: null,
      icon: '📈'
    }
  ];
});

function formatCurrency(value: number) {
  return new Intl.NumberFormat('zh-CN', { style: 'currency', currency: 'CNY', maximumFractionDigits: 0 }).format(value);
}

function formatNumber(value: number) {
  return new Intl.NumberFormat('zh-CN', { maximumFractionDigits: 0 }).format(value);
}

async function initialize() {
  try {
    await Promise.all([filterStore.loadFilterOptions(), dataStore.fetchDashboardData()]);
  } catch (error) {
    const message = error instanceof Error ? error.message : '初始化失败';
    toast.showError('加载数据失败', message);
  }
}

function handleMetricSwitch(metric: MetricKey) {
  if (metric === appStore.currentMetric) return;
  appStore.switchMetric(metric);
  dataStore.fetchChartData(metric).catch((error) => {
    const message = error instanceof Error ? error.message : '无法切换指标';
    toast.showError('切换失败', message);
  });
}

async function handleApplyFilters(nextFilters: Record<string, string>) {
  filterStore.setFilters(nextFilters);
  filterStore.togglePanel(false);
  try {
    await dataStore.fetchDashboardData();
    toast.showSuccess('筛选已更新');
  } catch (error) {
    const message = error instanceof Error ? error.message : '筛选应用失败';
    toast.showError('更新失败', message);
  }
}

async function handleResetFilters() {
  filterStore.resetFilters();
  try {
    await dataStore.fetchDashboardData();
    toast.showInfo('已重置筛选条件');
  } catch (error) {
    const message = error instanceof Error ? error.message : '筛选重置失败';
    toast.showError('重置失败', message);
  }
}

async function handleRefresh() {
  try {
    const message = await dataStore.refreshData();
    if (message) {
      toast.showSuccess('刷新成功', message);
    } else {
      toast.showSuccess('刷新成功');
    }
  } catch (error) {
    const message = error instanceof Error ? error.message : '刷新失败';
    toast.showError('刷新失败', message);
  }
}

onMounted(() => {
  initialize();
});
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
  padding: var(--space-6);
  background: linear-gradient(180deg, var(--primary-50), var(--gray-50));
  min-height: 100vh;
}

.dashboard__header {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.dashboard__titles {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.dashboard__title {
  font-size: var(--text-3xl);
  font-weight: 700;
}

.dashboard__subtitle {
  font-size: var(--text-base);
  color: var(--text-secondary);
}

.dashboard__actions {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--space-4);
}

.dashboard__date {
  font-size: var(--text-sm);
  color: var(--text-secondary);
}

.dashboard__metric-switcher {
  display: inline-flex;
  gap: 8px;
  padding: 4px;
  background: var(--surface-elevated);
  border-radius: 999px;
  box-shadow: var(--shadow-soft);
}

.dashboard__metric-button {
  border: none;
  background: transparent;
  padding: 8px 16px;
  border-radius: 999px;
  font-size: var(--text-sm);
  font-weight: 600;
  color: var(--text-secondary);
  cursor: pointer;
}

.dashboard__metric-button--active {
  background: var(--primary-600);
  color: var(--surface-elevated);
}

.dashboard__buttons {
  display: flex;
  gap: var(--space-3);
}

.dashboard__button {
  padding: 10px 18px;
  border-radius: 12px;
  border: none;
  background: var(--primary-600);
  color: var(--surface-elevated);
  font-weight: 600;
  cursor: pointer;
}

.dashboard__button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.dashboard__button--secondary {
  background: var(--gray-100);
  color: var(--text-secondary);
}

.dashboard__filters {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.dashboard__section-title {
  font-size: var(--text-xl);
  font-weight: 600;
}

.dashboard__chips {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
  list-style: none;
  padding: 0;
  margin: 0;
}

.dashboard__chip {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 6px 12px;
  border-radius: 999px;
  background: var(--surface-elevated);
  box-shadow: var(--shadow-soft);
}

.dashboard__chip-label {
  color: var(--text-secondary);
}

.dashboard__kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: var(--space-4);
}

.dashboard__chart {
  display: flex;
}

.dashboard__chart-meta {
  font-size: var(--text-sm);
  color: var(--text-secondary);
}

@media (max-width: 768px) {
  .dashboard {
    padding: var(--space-4);
  }

  .dashboard__actions {
    flex-direction: column;
    align-items: flex-start;
  }

  .dashboard__metric-switcher {
    width: 100%;
    justify-content: space-between;
  }

  .dashboard__buttons {
    width: 100%;
    flex-direction: column;
  }

  .dashboard__button {
    width: 100%;
  }
}
</style>
