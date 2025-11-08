<template>
  <div v-if="visible" :class="['loading', { 'loading--fullscreen': fullscreen }]">
    <div class="loading__backdrop" @click="handleBackdropClick"></div>
    <div class="loading__content">
      <div class="loading__spinner">
        <div class="loading__spinner-ring"></div>
        <div class="loading__spinner-ring"></div>
        <div class="loading__spinner-ring"></div>
      </div>
      <div v-if="text" class="loading__text">{{ text }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  // 是否显示
  visible: {
    type: Boolean,
    default: false
  },
  // 加载文本
  text: {
    type: String,
    default: '加载中...'
  },
  // 全屏模式
  fullscreen: {
    type: Boolean,
    default: false
  },
  // 点击背景是否关闭
  closeOnClickBackdrop: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close'])

const handleBackdropClick = () => {
  if (props.closeOnClickBackdrop) {
    emit('close')
  }
}
</script>

<style scoped>
.loading {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.loading--fullscreen {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 9998;
  display: flex;
}

.loading__backdrop {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(4px);
}

.loading--fullscreen .loading__backdrop {
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(8px);
}

.loading__content {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-6);
  background: white;
  border-radius: var(--radius-lg);
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
}

.loading--fullscreen .loading__content {
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
}

.loading__spinner {
  width: 60px;
  height: 60px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.loading__spinner-ring {
  position: absolute;
  width: 100%;
  height: 100%;
  border: 3px solid transparent;
  border-top-color: var(--primary-500);
  border-radius: 50%;
  animation: loading-spin 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite;
}

.loading__spinner-ring:nth-child(1) {
  animation-delay: -0.45s;
  border-top-color: var(--primary-500);
}

.loading__spinner-ring:nth-child(2) {
  animation-delay: -0.3s;
  border-top-color: var(--primary-600);
  width: 80%;
  height: 80%;
}

.loading__spinner-ring:nth-child(3) {
  animation-delay: -0.15s;
  border-top-color: var(--primary-700);
  width: 60%;
  height: 60%;
}

@keyframes loading-spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.loading__text {
  font-size: var(--text-base);
  color: var(--text-primary);
  font-weight: 500;
  text-align: center;
}

/* 内联模式(非全屏) */
.loading:not(.loading--fullscreen) .loading__backdrop {
  border-radius: var(--radius-md);
}

.loading:not(.loading--fullscreen) .loading__content {
  padding: var(--space-4);
}

.loading:not(.loading--fullscreen) .loading__spinner {
  width: 40px;
  height: 40px;
}

.loading:not(.loading--fullscreen) .loading__text {
  font-size: var(--text-sm);
}
</style>
