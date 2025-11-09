<template>
  <div class="app">
    <Dashboard />
  </div>
</template>

<script setup>
import Dashboard from '@/views/Dashboard.vue'
</script>

<style>
/* 全局样式导入 */
@import './assets/styles/variables.css';
@import './assets/styles/base.css';

.app {
  min-height: 100vh;
}
</style>
