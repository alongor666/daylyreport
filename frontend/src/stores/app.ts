import { defineStore } from 'pinia';
import type { MetricKey } from '@/types/api';

interface AppState {
  loading: boolean;
  latestDate: string | null;
  selectedDate: string | null;
  currentMetric: MetricKey;
}

export const useAppStore = defineStore('app', {
  state: (): AppState => ({
    loading: false,
    latestDate: null,
    selectedDate: null,
    currentMetric: 'premium'
  }),
  getters: {
    isPremiumMetric: (state) => state.currentMetric === 'premium',
    hasSelectedDate: (state) => Boolean(state.selectedDate)
  },
  actions: {
    setLoading(value: boolean) {
      this.loading = value;
    },
    setLatestDate(date: string | null) {
      this.latestDate = date;
    },
    setSelectedDate(date: string | null) {
      this.selectedDate = date;
    },
    switchMetric(metric: MetricKey) {
      this.currentMetric = metric;
    }
  }
});
