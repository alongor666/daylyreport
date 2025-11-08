import axios from 'axios'
import { useToast } from '@/composables/useToast'

/**
 * Axios HTTP客户端配置
 * 提供统一的请求/响应拦截器和错误处理
 */

// 创建axios实例
const apiClient = axios.create({
  baseURL: '/api',
  timeout: 30000, // 30秒超时
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
apiClient.interceptors.request.use(
  (config) => {
    // 在请求发送前添加统一的请求头或处理
    // 例如: 添加token
    // const token = localStorage.getItem('token')
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`
    // }

    // 打印请求日志 (开发环境)
    if (import.meta.env.DEV) {
      console.log(`[API Request] ${config.method.toUpperCase()} ${config.url}`, config.data || config.params)
    }

    return config
  },
  (error) => {
    console.error('[API Request Error]', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
apiClient.interceptors.response.use(
  (response) => {
    // 打印响应日志 (开发环境)
    if (import.meta.env.DEV) {
      console.log(`[API Response] ${response.config.url}`, response.data)
    }

    // 统一处理后端返回格式
    const { success, data, message } = response.data

    if (success === false) {
      // 后端返回业务错误
      console.warn(`[API Business Error] ${message}`)
      throw new Error(message || '操作失败')
    }

    return response
  },
  (error) => {
    // 处理HTTP错误
    handleError(error)
    return Promise.reject(error)
  }
)

/**
 * 统一错误处理
 * @param {Error} error - 错误对象
 */
function handleError(error) {
  const toast = useToast()

  let errorMessage = '请求失败,请稍后重试'
  let errorTitle = '错误'

  if (error.response) {
    // 服务器返回错误响应
    const { status, data } = error.response

    switch (status) {
      case 400:
        errorMessage = data.message || '请求参数错误'
        errorTitle = '参数错误'
        break
      case 401:
        errorMessage = '未授权,请重新登录'
        errorTitle = '未授权'
        // 可以在这里触发登出逻辑
        // logout()
        break
      case 403:
        errorMessage = '拒绝访问,权限不足'
        errorTitle = '权限错误'
        break
      case 404:
        errorMessage = '请求的资源不存在'
        errorTitle = '资源不存在'
        break
      case 500:
        errorMessage = '服务器内部错误'
        errorTitle = '服务器错误'
        break
      case 502:
        errorMessage = '网关错误'
        errorTitle = '网关错误'
        break
      case 503:
        errorMessage = '服务暂时不可用'
        errorTitle = '服务不可用'
        break
      default:
        errorMessage = data.message || `请求失败 (${status})`
        errorTitle = `HTTP ${status} 错误`
    }

    console.error(`[API Error] ${status}:`, data)
  } else if (error.request) {
    // 请求已发送但没有收到响应
    errorMessage = '网络连接失败,请检查您的网络'
    errorTitle = '网络错误'
    console.error('[API Error] No response received:', error.request)
  } else {
    // 请求配置错误
    errorMessage = error.message || '请求配置错误'
    errorTitle = '请求错误'
    console.error('[API Error] Request setup error:', error.message)
  }

  // 显示Toast通知
  toast.error(errorMessage, errorTitle)
}

/**
 * 封装的API请求方法
 */
export const api = {
  /**
   * GET请求
   * @param {string} url - 请求URL
   * @param {object} params - 查询参数
   * @param {object} config - 额外配置
   */
  get(url, params = {}, config = {}) {
    return apiClient.get(url, {
      params,
      ...config
    })
  },

  /**
   * POST请求
   * @param {string} url - 请求URL
   * @param {object} data - 请求体数据
   * @param {object} config - 额外配置
   */
  post(url, data = {}, config = {}) {
    return apiClient.post(url, data, config)
  },

  /**
   * PUT请求
   * @param {string} url - 请求URL
   * @param {object} data - 请求体数据
   * @param {object} config - 额外配置
   */
  put(url, data = {}, config = {}) {
    return apiClient.put(url, data, config)
  },

  /**
   * DELETE请求
   * @param {string} url - 请求URL
   * @param {object} config - 额外配置
   */
  delete(url, config = {}) {
    return apiClient.delete(url, config)
  },

  /**
   * PATCH请求
   * @param {string} url - 请求URL
   * @param {object} data - 请求体数据
   * @param {object} config - 额外配置
   */
  patch(url, data = {}, config = {}) {
    return apiClient.patch(url, data, config)
  }
}

// 默认导出axios实例 (向后兼容)
export default apiClient
