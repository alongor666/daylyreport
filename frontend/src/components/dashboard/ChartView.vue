<template>
  <section class="chart-view">
    <header class="chart-view__header">
      <slot name="title">
        <h2 class="chart-view__title">趋势对比</h2>
      </slot>
      <div class="chart-view__meta">
        <slot name="meta" />
      </div>
    </header>
    <div class="chart-view__body">
      <div v-if="loading" class="chart-view__overlay">
        <div class="chart-view__spinner" aria-hidden="true" />
        <span class="chart-view__hint">图表加载中…</span>
      </div>
      <div v-else-if="!option" class="chart-view__empty">暂无数据</div>
      <div v-else ref="chartRef" class="chart-view__canvas" :style="{ height }" />
    </div>
  </section>
</template>

<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref, watch } from 'vue';
import * as echarts from 'echarts/core';
import { LineChart } from 'echarts/charts';
import { GridComponent, LegendComponent, TooltipComponent } from 'echarts/components';
import { CanvasRenderer } from 'echarts/renderers';
import type { EChartsOption } from 'echarts';

echarts.use([LineChart, GridComponent, LegendComponent, TooltipComponent, CanvasRenderer]);

interface Props {
  option: EChartsOption | null;
  loading?: boolean;
  height?: string;
}

const props = withDefaults(defineProps<Props>(), {
  loading: false,
  height: '360px'
});

const chartRef = ref<HTMLDivElement | null>(null);
let chartInstance: echarts.ECharts | null = null;

function debounce<T extends (...args: never[]) => void>(fn: T, delay = 200) {
  let timer: number | undefined;
  return (...args: Parameters<T>) => {
    if (typeof window === 'undefined') {
      fn(...args);
      return;
    }
    window.clearTimeout(timer);
    timer = window.setTimeout(() => fn(...args), delay);
  };
}

const resizeChart = debounce(() => {
  chartInstance?.resize();
}, 160);

function renderChart(option: EChartsOption | null) {
  if (!chartInstance || !option) return;
  chartInstance.setOption(option, true);
}

onMounted(() => {
  if (!chartRef.value) return;
  chartInstance = echarts.init(chartRef.value);
  if (props.option) {
    renderChart(props.option);
  }
  if (typeof window !== 'undefined') {
    window.addEventListener('resize', resizeChart);
  }
});

onBeforeUnmount(() => {
  if (typeof window !== 'undefined') {
    window.removeEventListener('resize', resizeChart);
  }
  if (chartInstance) {
    chartInstance.dispose();
    chartInstance = null;
  }
});

watch(
  () => props.option,
  (option) => {
    if (!chartInstance && chartRef.value) {
      chartInstance = echarts.init(chartRef.value);
    }
    renderChart(option ?? null);
  },
  { deep: true }
);

watch(
  () => props.height,
  () => {
    if (chartRef.value) {
      chartRef.value.style.height = props.height;
      chartInstance?.resize();
    }
  }
);
</script>

<style scoped>
.chart-view {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  background: var(--surface-elevated);
  border-radius: 24px;
  padding: var(--space-4);
  box-shadow: var(--shadow-soft);
  border: 1px solid var(--gray-100);
}

.chart-view__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-3);
}

.chart-view__title {
  font-size: var(--text-xl);
  font-weight: 700;
}

.chart-view__body {
  position: relative;
  min-height: 320px;
}

.chart-view__canvas {
  width: 100%;
  height: 100%;
}

.chart-view__overlay {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--space-3);
  background: color-mix(in srgb, var(--surface-elevated) 75%, transparent);
  border-radius: 20px;
}

.chart-view__spinner {
  width: 48px;
  height: 48px;
  border: 4px solid var(--gray-100);
  border-top-color: var(--primary-600);
  border-radius: 50%;
  animation: chart-spin 1s linear infinite;
}

.chart-view__hint {
  font-size: var(--text-sm);
  color: var(--text-secondary);
}

.chart-view__empty {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  color: var(--text-secondary);
  background: var(--gray-100);
  border-radius: 16px;
}

@keyframes chart-spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
