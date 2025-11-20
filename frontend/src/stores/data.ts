import { defineStore } from 'pinia';
import { fetchKpiWindows, fetchWeekComparison, triggerRefresh } from '@/services/api';
import { useAppStore } from '@/stores/app';
import { useFilterStore } from '@/stores/filter';
import type {
  ComparisonMetric,
  KpiWindowsPayload,
  MetricKey,
  WeekComparisonPayload
} from '@/types/api';

interface DataState {
  kpiSummary: KpiWindowsPayload | null;
  chartData: WeekComparisonPayload | null;
  kpiLoading: boolean;
  chartLoading: boolean;
  refreshing: boolean;
}

function resolveComparisonMetric(metric: MetricKey): ComparisonMetric {
  return metric === 'policy_count' ? 'count' : 'premium';
}

export const useDataStore = defineStore('data', {
  state: (): DataState => ({
    kpiSummary: null,
    chartData: null,
    kpiLoading: false,
    chartLoading: false,
    refreshing: false
  }),
  actions: {
    async fetchKpiData() {
      this.kpiLoading = true;
      const appStore = useAppStore();
      try {
        const response = await fetchKpiWindows({
          date: appStore.selectedDate ?? undefined
        });
        if (!response.success) {
          throw new Error(response.message || '获取KPI数据失败');
        }
        this.kpiSummary = response.data;
        appStore.setLatestDate(response.data.anchor_date);
        if (!appStore.selectedDate) {
          appStore.setSelectedDate(response.data.anchor_date);
        }
        return response.data;
      } finally {
        this.kpiLoading = false;
      }
    },
    async fetchChartData(metric?: MetricKey) {
      this.chartLoading = true;
      const appStore = useAppStore();
      const filterStore = useFilterStore();
      try {
        const requestMetric = resolveComparisonMetric(metric ?? appStore.currentMetric);
        const response = await fetchWeekComparison({
          metric: requestMetric,
          filters: { ...filterStore.activeFilters },
          date: appStore.selectedDate ?? undefined
        });
        if (!response.success) {
          throw new Error(response.message || '获取图表数据失败');
        }
        this.chartData = response.data;
        if (!appStore.latestDate) {
          appStore.setLatestDate(response.data.latest_date);
        }
        return response.data;
      } finally {
        this.chartLoading = false;
      }
    },
    async fetchDashboardData() {
      const appStore = useAppStore();
      appStore.setLoading(true);
      try {
        await Promise.all([this.fetchKpiData(), this.fetchChartData()]);
      } finally {
        appStore.setLoading(false);
      }
    },
    async refreshData() {
      if (this.refreshing) return;
      this.refreshing = true;
      const appStore = useAppStore();
      try {
        const response = await triggerRefresh();
        if (!response.success) {
          throw new Error(response.message || '数据刷新失败');
        }
        if (response.data.latest_date) {
          appStore.setLatestDate(response.data.latest_date);
          appStore.setSelectedDate(response.data.latest_date);
        }
        await this.fetchDashboardData();
        return response.data.message;
      } finally {
        this.refreshing = false;
      }
    }
  }
});
