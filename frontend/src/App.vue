<template>
  <div class="app-shell">
    <header class="app-shell__header">
      <h1 class="app-shell__title">车险签单数据分析平台 v2.0</h1>
      <p class="app-shell__subtitle">Vue 3 + Vite + Pinia + ECharts 现代化前端框架</p>
    </header>
    <main class="app-shell__content">
      <div class="app-shell__status">
        <h2 class="app-shell__status-title">✅ 项目初始化完成</h2>
        <ul class="app-shell__checklist">
          <li>Vue 3 Composition API</li>
          <li>Vite 开发服务器</li>
          <li>Pinia 状态管理</li>
          <li>Axios HTTP 客户端</li>
          <li>ECharts 图表库</li>
          <li>CSS Variables 设计系统</li>
          <li>API 代理到后端 (port 5001)</li>
        </ul>
      </div>
      <div class="app-shell__hint">
        <p>接下来请按照以下文档完成核心模块开发:</p>
        <ul>
          <li><code>docs/ARCHITECTURE.md</code> - 架构设计</li>
          <li><code>docs/DESIGN_SYSTEM.md</code> - UI/UX 规范</li>
          <li><code>CLAUDE.md</code> - 开发指南</li>
        </ul>
      </div>
    </main>
  </div>
</template>

<script setup>
// Vue 3 Composition API setup area
// 预留用于引入全局状态管理和业务逻辑
</script>

<style scoped>
.app-shell {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--space-8);
  background: linear-gradient(135deg, var(--primary-600), var(--primary-500));
  padding: var(--space-6);
}

.app-shell__header {
  text-align: center;
  color: white;
}

.app-shell__title {
  font-size: var(--text-3xl);
  font-weight: 700;
  margin: 0 0 var(--space-3) 0;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.app-shell__subtitle {
  font-size: var(--text-lg);
  margin: 0;
  opacity: 0.9;
}

.app-shell__content {
  background: white;
  border-radius: var(--radius-lg);
  padding: var(--space-8);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
  max-width: 640px;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

.app-shell__status {
  border-left: var(--border-accent-width) solid var(--success-500);
  padding-left: var(--space-4);
  background: rgba(16, 185, 129, 0.05);
  padding: var(--space-4);
  border-radius: var(--radius-md);
}

.app-shell__status-title {
  font-size: var(--text-xl);
  color: var(--success-500);
  margin: 0 0 var(--space-4) 0;
}

.app-shell__checklist {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.app-shell__checklist li {
  font-size: var(--text-base);
  color: var(--text-primary);
  padding-left: var(--space-6);
  position: relative;
}

.app-shell__checklist li::before {
  content: '✓';
  position: absolute;
  left: 0;
  color: var(--success-500);
  font-weight: 700;
}

.app-shell__hint {
  background: var(--surface-primary-tint);
  border-left: var(--border-accent-width) solid var(--primary-500);
  padding: var(--space-4);
  border-radius: var(--radius-md);
}

.app-shell__hint p {
  margin: 0 0 var(--space-3) 0;
  font-size: var(--text-base);
  color: var(--text-primary);
  font-weight: 600;
}

.app-shell__hint ul {
  margin: 0;
  padding-left: var(--space-5);
}

.app-shell__hint li {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  margin-bottom: var(--space-2);
}

.app-shell__hint code {
  background: rgba(168, 85, 247, 0.1);
  padding: 2px 6px;
  border-radius: 4px;
  font-size: var(--text-sm);
  color: var(--primary-600);
}
</style>
