<template>
  <Teleport to="body">
    <Transition name="toast">
      <div v-if="visible" :class="['toast', `toast--${type}`]" role="alert">
        <div class="toast__icon">
          {{ iconMap[type] }}
        </div>
        <div class="toast__content">
          <div v-if="title" class="toast__title">{{ title }}</div>
          <div class="toast__message">{{ message }}</div>
        </div>
        <button
          v-if="closable"
          class="toast__close"
          @click="close"
          aria-label="关闭"
        >
          ×
        </button>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'

const props = defineProps({
  message: {
    type: String,
    required: true
  },
  title: {
    type: String,
    default: ''
  },
  type: {
    type: String,
    default: 'info',
    validator: (value) => ['success', 'error', 'warning', 'info'].includes(value)
  },
  duration: {
    type: Number,
    default: 3000 // 3秒后自动关闭
  },
  closable: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['close'])

const visible = ref(false)
let timer = null

const iconMap = {
  success: '✓',
  error: '✕',
  warning: '⚠',
  info: 'ℹ'
}

const close = () => {
  visible.value = false
  if (timer) {
    clearTimeout(timer)
    timer = null
  }
  emit('close')
}

const startTimer = () => {
  if (props.duration > 0) {
    timer = setTimeout(() => {
      close()
    }, props.duration)
  }
}

onMounted(() => {
  visible.value = true
  startTimer()
})

// 如果duration变化,重新启动定时器
watch(() => props.duration, () => {
  if (timer) {
    clearTimeout(timer)
  }
  startTimer()
})
</script>

<style scoped>
.toast {
  position: fixed;
  top: var(--space-6);
  right: var(--space-6);
  min-width: 300px;
  max-width: 500px;
  padding: var(--space-4);
  border-radius: var(--radius-lg);
  background: white;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  display: flex;
  align-items: flex-start;
  gap: var(--space-3);
  z-index: 9999;
  pointer-events: auto;
}

.toast__icon {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--text-sm);
  font-weight: 700;
  flex-shrink: 0;
}

.toast__content {
  flex: 1;
  min-width: 0;
}

.toast__title {
  font-size: var(--text-base);
  font-weight: 600;
  margin-bottom: var(--space-1);
  color: var(--text-primary);
}

.toast__message {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  line-height: 1.5;
  word-wrap: break-word;
}

.toast__close {
  width: 20px;
  height: 20px;
  border: none;
  background: none;
  font-size: 20px;
  line-height: 1;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 0;
  flex-shrink: 0;
  transition: color 0.2s;
}

.toast__close:hover {
  color: var(--text-primary);
}

/* 类型变体 - Success */
.toast--success {
  border-left: 4px solid var(--success-500);
}

.toast--success .toast__icon {
  background: rgba(16, 185, 129, 0.1);
  color: var(--success-500);
}

/* 类型变体 - Error */
.toast--error {
  border-left: 4px solid var(--error-500);
}

.toast--error .toast__icon {
  background: rgba(239, 68, 68, 0.1);
  color: var(--error-500);
}

/* 类型变体 - Warning */
.toast--warning {
  border-left: 4px solid var(--warning-500);
}

.toast--warning .toast__icon {
  background: rgba(245, 158, 11, 0.1);
  color: var(--warning-500);
}

/* 类型变体 - Info */
.toast--info {
  border-left: 4px solid var(--primary-500);
}

.toast--info .toast__icon {
  background: var(--surface-primary-tint);
  color: var(--primary-500);
}

/* 过渡动画 */
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.toast-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
</style>
