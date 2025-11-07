<template>
  <div class="app-shell">
    <header class="app-shell__header">
      <h1 class="app-shell__title">车险签单数据分析平台 v2.0</h1>
      <p class="app-shell__subtitle">欢迎使用 Vue 3 + Vite + Pinia 全新前端</p>
    </header>
    <main class="app-shell__content">
      <p>
        接下来请按照 <code>docs/ARCHITECTURE.md</code> 与 <code>docs/DESIGN_SYSTEM.md</code> 完成仪表盘、筛选器等核心模块的开发。
      </p>
      <p class="app-shell__hint">
        ✅ 当前项目已经完成基础初始化，包含 Pinia、Axios、ECharts 依赖与 API 代理配置。
      </p>
    </main>
  </div>
</template>

<script setup>
// 预留 Composition API 区域，后续用于加载全局状态与业务逻辑
</script>

<style scoped>
.app-shell {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  padding: var(--space-6);
  background-color: var(--gray-50);
  color: var(--text-primary);
}

.app-shell__header {
  margin-bottom: var(--space-6);
}

.app-shell__title {
  font-size: var(--text-2xl);
  margin-bottom: var(--space-4);
}

.app-shell__subtitle {
  font-size: var(--text-base);
  color: var(--text-muted);
}

.app-shell__content {
  background-color: var(--surface-elevated);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  box-shadow: var(--shadow-md);
}

.app-shell__hint {
  margin-top: var(--space-4);
  padding: var(--space-3) var(--space-4);
  border-left: var(--border-accent-width) solid var(--primary-500);
  background: var(--surface-primary-tint);
}
</style>
