<template>
  <div class="app-shell">
    <header class="app-shell__header">
      <h1 class="app-shell__title">车险签单数据分析平台 v2.0</h1>
      <p class="app-shell__subtitle">Vue 3 + Vite 开发环境已就绪</p>
    </header>
    <main class="app-shell__content">
      <p class="app-shell__hint">
        请参考 docs/ARCHITECTURE.md 与 docs/DESIGN_SYSTEM.md，开始构建仪表板组件。
      </p>
      <p class="app-shell__meta">{{ welcomeMessage }}</p>
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useAppStore } from '@/stores/app';

const appStore = useAppStore();
const welcomeMessage = computed(() => appStore.welcomeMessage);
</script>

<style scoped>
.app-shell {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--space-6);
  background: linear-gradient(135deg, var(--primary-500), var(--primary-600));
  color: #fff;
  text-align: center;
  padding: var(--space-6);
}

.app-shell__title {
  font-size: var(--text-3xl);
  font-weight: 700;
}

.app-shell__subtitle {
  font-size: var(--text-lg);
  opacity: 0.85;
}

.app-shell__content {
  background: rgba(255, 255, 255, 0.12);
  padding: var(--space-6);
  border-radius: 24px;
  backdrop-filter: blur(12px);
  max-width: 640px;
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  box-shadow: var(--shadow-soft);
}

.app-shell__hint {
  font-size: var(--text-base);
  line-height: 1.6;
}

.app-shell__meta {
  font-size: var(--text-sm);
  opacity: 0.75;
}
</style>
