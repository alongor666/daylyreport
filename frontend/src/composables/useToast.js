import { createApp, h } from 'vue'
import Toast from '@/components/common/Toast.vue'

/**
 * Toast通知管理器
 * 使用方法:
 * import { useToast } from '@/composables/useToast'
 *
 * const toast = useToast()
 * toast.success('操作成功!')
 * toast.error('操作失败!', '错误详情')
 * toast.warning('请注意')
 * toast.info('提示信息')
 */

let toastContainer = null
const activeToasts = []

// 创建Toast容器
function ensureContainer() {
  if (!toastContainer) {
    toastContainer = document.createElement('div')
    toastContainer.id = 'toast-container'
    toastContainer.style.cssText = `
      position: fixed;
      top: 0;
      right: 0;
      z-index: 9999;
      pointer-events: none;
    `
    document.body.appendChild(toastContainer)
  }
  return toastContainer
}

// 显示Toast
function showToast(options) {
  const container = ensureContainer()

  const toastWrapper = document.createElement('div')
  toastWrapper.style.cssText = 'pointer-events: auto;'
  container.appendChild(toastWrapper)

  const app = createApp({
    render() {
      return h(Toast, {
        ...options,
        onClose: () => {
          app.unmount()
          container.removeChild(toastWrapper)

          // 从活动列表中移除
          const index = activeToasts.indexOf(app)
          if (index > -1) {
            activeToasts.splice(index, 1)
          }

          // 如果没有活动Toast,移除容器
          if (activeToasts.length === 0 && toastContainer) {
            document.body.removeChild(toastContainer)
            toastContainer = null
          }
        }
      })
    }
  })

  app.mount(toastWrapper)
  activeToasts.push(app)

  return app
}

export function useToast() {
  return {
    /**
     * 成功通知
     * @param {string} message - 消息内容
     * @param {string} title - 标题(可选)
     * @param {number} duration - 持续时间(默认3000ms)
     */
    success(message, title = '', duration = 3000) {
      return showToast({
        type: 'success',
        message,
        title,
        duration
      })
    },

    /**
     * 错误通知
     * @param {string} message - 消息内容
     * @param {string} title - 标题(可选)
     * @param {number} duration - 持续时间(默认4000ms)
     */
    error(message, title = '错误', duration = 4000) {
      return showToast({
        type: 'error',
        message,
        title,
        duration
      })
    },

    /**
     * 警告通知
     * @param {string} message - 消息内容
     * @param {string} title - 标题(可选)
     * @param {number} duration - 持续时间(默认3500ms)
     */
    warning(message, title = '警告', duration = 3500) {
      return showToast({
        type: 'warning',
        message,
        title,
        duration
      })
    },

    /**
     * 信息通知
     * @param {string} message - 消息内容
     * @param {string} title - 标题(可选)
     * @param {number} duration - 持续时间(默认3000ms)
     */
    info(message, title = '', duration = 3000) {
      return showToast({
        type: 'info',
        message,
        title,
        duration
      })
    },

    /**
     * 自定义通知
     * @param {object} options - 完整选项
     */
    show(options) {
      return showToast(options)
    }
  }
}
