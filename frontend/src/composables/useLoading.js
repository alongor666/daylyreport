import { createApp, h, ref } from 'vue'
import Loading from '@/components/common/Loading.vue'

/**
 * Loading加载管理器
 * 使用方法:
 * import { useLoading } from '@/composables/useLoading'
 *
 * const loading = useLoading()
 * const instance = loading.show('正在加载数据...')
 * // ... 执行异步操作
 * instance.close()
 *
 * 或者使用Promise模式:
 * await loading.wrap(async () => {
 *   await fetchData()
 * }, '加载中...')
 */

let loadingInstance = null

export function useLoading() {
  return {
    /**
     * 显示全屏Loading
     * @param {string} text - 加载文本
     * @returns {object} 返回包含close方法的实例
     */
    show(text = '加载中...') {
      // 如果已有实例,先关闭
      if (loadingInstance) {
        this.close()
      }

      const container = document.createElement('div')
      document.body.appendChild(container)

      const visible = ref(true)

      const app = createApp({
        render() {
          return h(Loading, {
            visible: visible.value,
            text,
            fullscreen: true,
            onClose: () => {
              visible.value = false
            }
          })
        }
      })

      app.mount(container)

      loadingInstance = {
        app,
        container,
        visible,
        close: () => {
          visible.value = false
          setTimeout(() => {
            app.unmount()
            document.body.removeChild(container)
            loadingInstance = null
          }, 300) // 等待动画完成
        }
      }

      return loadingInstance
    },

    /**
     * 关闭Loading
     */
    close() {
      if (loadingInstance) {
        loadingInstance.close()
      }
    },

    /**
     * 包装异步函数,自动显示/隐藏Loading
     * @param {Function} fn - 异步函数
     * @param {string} text - 加载文本
     * @returns {Promise} 返回函数执行结果
     */
    async wrap(fn, text = '加载中...') {
      const instance = this.show(text)
      try {
        const result = await fn()
        return result
      } finally {
        instance.close()
      }
    }
  }
}
