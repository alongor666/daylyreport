<template>
  <aside class="filter-panel" :class="{ 'filter-panel--open': isOpen }">
    <header class="filter-panel__header">
      <h3 class="filter-panel__title">筛选条件</h3>
      <button type="button" class="filter-panel__close" @click="$emit('toggle')">关闭</button>
    </header>
    <div class="filter-panel__body">
      <form class="filter-panel__form" @submit.prevent="handleApply">
        <div v-if="loading" class="filter-panel__loading">加载筛选项中…</div>
        <template v-else>
          <fieldset v-for="dimension in orderedDimensions" :key="dimension" class="filter-panel__fieldset">
            <label class="filter-panel__label" :for="`filter-${dimension}`">{{ dimension }}</label>
            <select
              :id="`filter-${dimension}`"
              class="filter-panel__select"
              v-model="localFilters[dimension]"
            >
              <option value="">全部</option>
              <option
                v-for="option in resolveOptions(dimension)"
                :key="option"
                :value="option"
              >
                {{ option }}
              </option>
            </select>
          </fieldset>
        </template>
      </form>
    </div>
    <footer class="filter-panel__footer">
      <button type="button" class="filter-panel__button filter-panel__button--reset" @click="handleReset">
        重置
      </button>
      <button type="button" class="filter-panel__button filter-panel__button--primary" @click="handleApply">
        应用筛选
      </button>
    </footer>
  </aside>
</template>

<script setup lang="ts">
import { computed, reactive, watch, withDefaults } from 'vue';

interface Props {
  options: Record<string, string[]>;
  teamMapping: Record<string, string[]>;
  activeFilters: Record<string, string>;
  loading: boolean;
  isOpen: boolean;
  dimensions?: string[];
}

const props = withDefaults(defineProps<Props>(), {
  dimensions: () => []
});

const emit = defineEmits<{
  (event: 'apply', value: Record<string, string>): void;
  (event: 'reset'): void;
  (event: 'toggle'): void;
}>();

const localFilters = reactive<Record<string, string>>({ ...props.activeFilters });

watch(
  () => props.activeFilters,
  (next) => {
    Object.keys(localFilters).forEach((key) => delete localFilters[key]);
    Object.entries(next).forEach(([key, value]) => {
      localFilters[key] = value;
    });
  },
  { deep: true }
);

const orderedDimensions = computed(() => {
  if (props.dimensions && props.dimensions.length) {
    return props.dimensions;
  }
  return Object.keys(props.options);
});

function resolveOptions(dimension: string) {
  if (dimension === '团队') {
    const org = localFilters['三级机构'];
    if (org && props.teamMapping[org]) {
      return props.teamMapping[org];
    }
  }
  return props.options[dimension] ?? [];
}

watch(
  () => localFilters['三级机构'],
  () => {
    const team = localFilters['团队'];
    if (!team) return;
    const availableTeams = resolveOptions('团队');
    if (!availableTeams.includes(team)) {
      localFilters['团队'] = '';
    }
  }
);

function handleApply() {
  emit('apply', Object.fromEntries(Object.entries(localFilters).filter(([, value]) => value)));
}

function handleReset() {
  Object.keys(localFilters).forEach((key) => {
    localFilters[key] = '';
  });
  emit('reset');
}
</script>

<style scoped>
.filter-panel {
  position: fixed;
  top: 0;
  right: -360px;
  width: 320px;
  height: 100vh;
  background: var(--surface-elevated);
  box-shadow: var(--shadow-soft);
  transition: right 0.24s ease;
  display: flex;
  flex-direction: column;
  z-index: 9980;
}

.filter-panel--open {
  right: 0;
}

.filter-panel__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-4);
  border-bottom: 1px solid var(--gray-100);
}

.filter-panel__title {
  font-size: var(--text-lg);
  font-weight: 600;
}

.filter-panel__close {
  background: transparent;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  font-size: var(--text-base);
}

.filter-panel__body {
  flex: 1;
  overflow-y: auto;
  padding: var(--space-4);
  display: flex;
  flex-direction: column;
}

.filter-panel__loading {
  color: var(--text-secondary);
  font-size: var(--text-sm);
}

.filter-panel__form {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.filter-panel__fieldset {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.filter-panel__label {
  font-size: var(--text-sm);
  color: var(--text-secondary);
}

.filter-panel__select {
  padding: 10px 12px;
  border: 1px solid var(--gray-300);
  border-radius: 12px;
  background: var(--surface-elevated);
  font-size: var(--text-base);
}

.filter-panel__select:focus {
  outline: 2px solid var(--primary-500);
  outline-offset: 1px;
}

.filter-panel__footer {
  padding: var(--space-4);
  display: flex;
  gap: var(--space-3);
  border-top: 1px solid var(--gray-100);
}

.filter-panel__button {
  flex: 1;
  padding: 10px 16px;
  border-radius: 999px;
  border: none;
  font-size: var(--text-base);
  font-weight: 600;
  cursor: pointer;
}

.filter-panel__button--reset {
  background: var(--gray-100);
  color: var(--text-secondary);
}

.filter-panel__button--primary {
  background: var(--primary-600);
  color: var(--surface-elevated);
}
</style>
