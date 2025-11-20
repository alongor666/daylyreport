<template>
  <article class="kpi-card" :class="kpiCardModifier">
    <header class="kpi-card__header">
      <div class="kpi-card__icon" aria-hidden="true">{{ icon }}</div>
      <div class="kpi-card__meta">
        <span class="kpi-card__label">{{ title }}</span>
        <span v-if="subtitle" class="kpi-card__subtitle">{{ subtitle }}</span>
      </div>
    </header>
    <div class="kpi-card__value-row">
      <span class="kpi-card__value">{{ formattedValue }}</span>
      <span v-if="trendLabel" class="kpi-card__trend" :class="trendModifier">{{ trendLabel }}</span>
    </div>
    <footer class="kpi-card__footer">
      <span v-if="description" class="kpi-card__description">{{ description }}</span>
      <span v-if="targetGap !== null" class="kpi-card__description">
        距目标 {{ formatNumber(Math.abs(targetGap)) }}
        <span v-if="targetGap > 0">↓</span>
        <span v-else-if="targetGap < 0">↑</span>
      </span>
    </footer>
    <svg
      v-if="sparklinePoints"
      class="kpi-card__sparkline"
      viewBox="0 0 120 40"
      preserveAspectRatio="none"
      role="presentation"
      aria-hidden="true"
    >
      <defs>
        <linearGradient :id="gradientId" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" :stop-color="sparklineColor" stop-opacity="0.28" />
          <stop offset="100%" :stop-color="sparklineColor" stop-opacity="0" />
        </linearGradient>
      </defs>
      <polyline :points="sparklinePoints" :stroke="sparklineColor" fill="none" stroke-width="2" />
      <polygon :points="sparklineAreaPoints" :fill="`url(#${gradientId})`" />
    </svg>
  </article>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface Props {
  title: string;
  value: number;
  unit?: 'currency' | 'number';
  trend?: number | null;
  icon?: string;
  subtitle?: string;
  description?: string;
  sparklineData?: number[] | null;
  targetGap?: number | null;
}

const props = withDefaults(defineProps<Props>(), {
  unit: 'currency',
  trend: null,
  icon: '📊',
  subtitle: '',
  description: '',
  sparklineData: null,
  targetGap: null
});

const gradientId = `sparkline-gradient-${Math.random().toString(36).slice(2, 8)}`;

const formattedValue = computed(() => {
  if (props.unit === 'currency') {
    const currency = new Intl.NumberFormat('zh-CN', {
      style: 'currency',
      currency: 'CNY',
      maximumFractionDigits: 0
    });
    return currency.format(props.value);
  }
  return new Intl.NumberFormat('zh-CN', { maximumFractionDigits: 0 }).format(props.value);
});

const trendModifier = computed(() => {
  if (props.trend === null || props.trend === undefined) return 'kpi-card__trend--neutral';
  if (props.trend > 0) return 'kpi-card__trend--up';
  if (props.trend < 0) return 'kpi-card__trend--down';
  return 'kpi-card__trend--neutral';
});

const trendLabel = computed(() => {
  if (props.trend === null || props.trend === undefined) return '';
  const arrow = props.trend > 0 ? '↑' : props.trend < 0 ? '↓' : '→';
  return `${arrow} ${Math.abs(props.trend).toFixed(1)}%`;
});

const kpiCardModifier = computed(() => {
  if (props.trend === null || props.trend === undefined) return '';
  if (props.trend > 0) return 'kpi-card--positive';
  if (props.trend < 0) return 'kpi-card--negative';
  return 'kpi-card--neutral';
});

const sparklineColor = computed(() => {
  if (props.trend === null || props.trend === undefined) {
    return 'var(--primary-500)';
  }
  return props.trend >= 0 ? 'var(--success-500)' : 'var(--error-500)';
});

const sparklinePoints = computed(() => {
  if (!props.sparklineData || props.sparklineData.length === 0) return '';
  const max = Math.max(...props.sparklineData);
  const min = Math.min(...props.sparklineData);
  const range = max - min || 1;
  const step = props.sparklineData.length === 1 ? 120 : 120 / (props.sparklineData.length - 1);
  return props.sparklineData
    .map((value, index) => {
      const x = index * step;
      const normalized = (value - min) / range;
      const y = 36 - normalized * 32;
      return `${x},${y}`;
    })
    .join(' ');
});

const sparklineAreaPoints = computed(() => {
  if (!props.sparklineData || props.sparklineData.length === 0) return '';
  const points = sparklinePoints.value;
  return `0,40 ${points} 120,40`;
});

function formatNumber(value: number) {
  return new Intl.NumberFormat('zh-CN', { maximumFractionDigits: 0 }).format(value);
}
</script>

<style scoped>
.kpi-card {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  padding: var(--space-4);
  border-radius: 20px;
  background: var(--surface-elevated);
  box-shadow: var(--shadow-soft);
  border: 1px solid transparent;
  overflow: hidden;
}

.kpi-card--positive {
  border-color: var(--success-500);
}

.kpi-card--negative {
  border-color: var(--error-500);
}

.kpi-card--neutral {
  border-color: var(--primary-500);
}

.kpi-card__header {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.kpi-card__icon {
  font-size: var(--text-2xl);
  line-height: 1;
}

.kpi-card__meta {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.kpi-card__label {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  letter-spacing: 0.02em;
}

.kpi-card__subtitle {
  font-size: var(--text-sm);
  color: var(--text-primary);
  font-weight: 600;
}

.kpi-card__value-row {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: var(--space-3);
}

.kpi-card__value {
  font-size: var(--text-3xl);
  font-weight: 700;
  letter-spacing: 0.01em;
}

.kpi-card__trend {
  font-size: var(--text-sm);
  font-weight: 600;
  padding: 4px 12px;
  border-radius: 999px;
  background: var(--gray-100);
}

.kpi-card__trend--up {
  color: var(--success-500);
}

.kpi-card__trend--down {
  color: var(--error-500);
}

.kpi-card__trend--neutral {
  color: var(--text-secondary);
}

.kpi-card__footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: var(--text-sm);
  color: var(--text-secondary);
}

.kpi-card__description {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.kpi-card__sparkline {
  position: absolute;
  inset: auto 0 0 0;
  width: 100%;
  height: 60px;
  opacity: 0.4;
}
</style>
