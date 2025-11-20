<template>
  <TransitionGroup name="toast-fade" tag="div" class="toast-stack" v-if="hasMessages">
    <article
      v-for="toast in toasts"
      :key="toast.id"
      class="toast-card"
      :class="`toast-card--${toast.type}`"
      role="status"
      aria-live="assertive"
    >
      <div class="toast-card__icon" aria-hidden="true">{{ icons[toast.type] }}</div>
      <div class="toast-card__content">
        <h3 class="toast-card__title">{{ toast.title }}</h3>
        <p v-if="toast.message" class="toast-card__message">{{ toast.message }}</p>
      </div>
      <button type="button" class="toast-card__close" @click="dismiss(toast.id)">×</button>
    </article>
  </TransitionGroup>
</template>

<script setup lang="ts">
import { useToast, dismiss } from '@/composables/useToast';

type ToastType = 'success' | 'error' | 'info';

const icons: Record<ToastType, string> = {
  success: '✅',
  error: '⚠️',
  info: 'ℹ️'
};
const { toasts, hasMessages } = useToast();
</script>

<style scoped>
.toast-stack {
  position: fixed;
  top: var(--space-4);
  right: var(--space-4);
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  z-index: 9999;
}

.toast-card {
  min-width: 320px;
  max-width: 420px;
  display: flex;
  align-items: flex-start;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  border-radius: 16px;
  box-shadow: var(--shadow-soft);
  background: var(--surface-elevated);
  color: var(--text-primary);
  border: 1px solid transparent;
}

.toast-card__icon {
  font-size: var(--text-xl);
  line-height: 1;
}

.toast-card__content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.toast-card__title {
  font-size: var(--text-base);
  font-weight: 600;
}

.toast-card__message {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  line-height: 1.5;
}

.toast-card__close {
  background: transparent;
  border: none;
  font-size: var(--text-lg);
  color: var(--text-secondary);
  cursor: pointer;
  padding: 0;
  line-height: 1;
}

.toast-card--success {
  border-color: var(--success-500);
}

.toast-card--error {
  border-color: var(--error-500);
}

.toast-card--info {
  border-color: var(--primary-500);
}

.toast-fade-enter-active,
.toast-fade-leave-active {
  transition: all 0.24s ease;
}

.toast-fade-enter-from,
.toast-fade-leave-to {
  opacity: 0;
  transform: translateY(-12px);
}
</style>
