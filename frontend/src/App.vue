<template>
  <div class="app">
    <Dashboard />
  </div>
</template>

<script setup>
import Dashboard from '@/views/Dashboard.vue'

// NOTE: 主题系统测试代码已备份到 App.vue.theme-system-backup
// 您的ThemeEngine完成后,可以在此处集成
</script>

<style>
/* 全局样式导入 */
@import './assets/styles/variables.css';
@import './assets/styles/base.css';

.app {
  min-height: 100vh;
}
</style>
