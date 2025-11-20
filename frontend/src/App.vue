<template>
  <div class="app-shell">
    <DashboardView />
    <Toast />
  </div>
</template>

<script setup lang="ts">
import DashboardView from '@/views/DashboardView.vue';
import Toast from '@/components/common/Toast.vue';
</script>

<style scoped>
.app-shell {
  min-height: 100vh;
  background: var(--gray-50);
}
</style>
