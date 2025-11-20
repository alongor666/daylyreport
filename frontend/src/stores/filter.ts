import { computed, reactive, toRefs } from 'vue';
import { defineStore } from 'pinia';
import { fetchFilterOptions } from '@/services/api';
import type { FilterOptionsPayload, StructuredFilterOptions } from '@/types/api';

interface FilterState {
  filterOptions: Record<string, string[]>;
  teamMapping: Record<string, string[]>;
  activeFilters: Record<string, string>;
  panelOpen: boolean;
  loading: boolean;
}

function normalizeFilterOptions(payload: FilterOptionsPayload): StructuredFilterOptions {
  const normalized: Record<string, string[]> = {};
  const teamMapping: Record<string, string[]> = {};

  Object.entries(payload).forEach(([key, value]) => {
    if (key === '机构团队映射' && value && typeof value === 'object' && !Array.isArray(value)) {
      Object.entries(value as Record<string, string[]>).forEach(([org, teams]) => {
        teamMapping[org] = [...teams];
      });
      return;
    }

    if (Array.isArray(value)) {
      normalized[key] = [...value];
    }
  });

  return { options: normalized, teamMapping };
}

export const useFilterStore = defineStore('filter', () => {
  const state = reactive<FilterState>({
    filterOptions: {},
    teamMapping: {},
    activeFilters: {},
    panelOpen: false,
    loading: false
  });

  const hasActiveFilters = computed(() => Object.keys(state.activeFilters).length > 0);

  const orderedDimensions = computed(() => {
    const preferredOrder = ['三级机构', '团队', '是否新能源', '是否续保', '是否过户车', '险种大类', '吨位'];
    const dimensions = Object.keys(state.filterOptions);
    return preferredOrder.filter((key) => dimensions.includes(key)).concat(
      dimensions.filter((key) => !preferredOrder.includes(key))
    );
  });

  async function loadFilterOptions(force = false) {
    if (state.loading) return;
    if (!force && Object.keys(state.filterOptions).length) return;

    state.loading = true;
    try {
      const response = await fetchFilterOptions();
      if (!response.success) {
        throw new Error(response.message || '无法加载筛选选项');
      }
      const { options, teamMapping } = normalizeFilterOptions(response.data);
      state.filterOptions = options;
      state.teamMapping = teamMapping;
    } finally {
      state.loading = false;
    }
  }

  function setFilters(filters: Record<string, string>) {
    state.activeFilters = { ...filters };
  }

  function applyFilter(key: string, value: string | null) {
    const nextFilters = { ...state.activeFilters };
    if (!value) {
      delete nextFilters[key];
    } else {
      nextFilters[key] = value;
    }
    state.activeFilters = nextFilters;
  }

  function resetFilters() {
    state.activeFilters = {};
  }

  function togglePanel(force?: boolean) {
    if (typeof force === 'boolean') {
      state.panelOpen = force;
      return;
    }
    state.panelOpen = !state.panelOpen;
  }

  return {
    ...toRefs(state),
    hasActiveFilters,
    orderedDimensions,
    loadFilterOptions,
    setFilters,
    applyFilter,
    resetFilters,
    togglePanel
  };
});
