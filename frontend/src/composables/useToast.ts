import { computed, readonly, ref } from 'vue';

type ToastType = 'success' | 'error' | 'info';

export interface ToastMessage {
  id: number;
  type: ToastType;
  title: string;
  message?: string;
  duration: number;
}

const messages = ref<ToastMessage[]>([]);

function createToast(type: ToastType, title: string, message?: string, duration = 3200) {
  const id = Date.now() + Math.floor(Math.random() * 1000);
  const toast: ToastMessage = {
    id,
    type,
    title,
    message,
    duration
  };
  messages.value.push(toast);

  if (duration > 0 && typeof window !== 'undefined') {
    window.setTimeout(() => dismiss(id), duration);
  }

  return id;
}

export function dismiss(id: number) {
  messages.value = messages.value.filter((toast) => toast.id !== id);
}

export function useToast() {
  const hasMessages = computed(() => messages.value.length > 0);

  const showSuccess = (title: string, message?: string, duration?: number) =>
    createToast('success', title, message, duration);
  const showError = (title: string, message?: string, duration?: number) =>
    createToast('error', title, message, duration ?? 4200);
  const showInfo = (title: string, message?: string, duration?: number) =>
    createToast('info', title, message, duration ?? 2600);

  return {
    toasts: readonly(messages),
    hasMessages,
    showSuccess,
    showError,
    showInfo,
    dismiss
  };
}
