/**
 * 简化版应用主入口
 * 专注网页端跨操作系统主题系统
 */

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App-simple.vue'

// 简化主题系统
import { SimpleThemePlugin } from '@/themes-simple'

// 基础样式
import '@/assets/styles/global.css'

// 创建应用实例
const app = createApp(App)

// 配置 Pinia
const pinia = createPinia()
app.use(pinia)

// 配置简化主题系统
const themeOptions = {
  defaultMode: 'eye-care',  // 默认护眼模式
  respectSystemPreference: true,  // 跟随系统偏好
  enableTransitions: true,  // 启用过渡动画
  enableCache: true,  // 启用缓存
  performanceThreshold: 50  // 性能阈值 50ms
}

// 使用简化主题插件
app.use(SimpleThemePlugin, themeOptions)

// 全局错误处理
app.config.errorHandler = (error, instance, info) => {
  console.error('应用错误:', error)
  console.error('错误信息:', info)
}

// 全局属性
app.config.globalProperties.$appVersion = '2.0.0-simple'
app.config.globalProperties.$buildTime = new Date().toISOString()

// 等待主题系统就绪
app.config.globalProperties.$onSimpleThemeReady = () => {
  console.log('🎨 简化主题系统已就绪')
  console.log('📱 跨操作系统主题系统已加载')
  console.log('😊 支持护眼模式和暗黑模式')
  console.log('🖥️ 适配 Windows、macOS、信创系统')
}

// 应用配置
const appConfig = {
  name: '跨操作系统主题系统',
  version: '2.0.0-simple',
  description: '网页端跨操作系统护眼主题系统',
  features: {
    crossOS: true,
    eyeCare: true,
    darkMode: true,
    simple: true,
    performance: true
  }
}

// 提供应用配置
app.provide('appConfig', appConfig)

// 挂载应用
app.mount('#app')

// 性能监控
if ('performance' in window) {
  window.addEventListener('load', () => {
    const perfData = window.performance.timing
    const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart
    console.log(`⏱️ 页面加载时间: ${pageLoadTime}ms`)
  })
}

// 跨OS检测
const detectOS = () => {
  const userAgent = navigator.userAgent.toLowerCase()
  if (userAgent.includes('mac')) return 'macOS'
  if (userAgent.includes('win')) return 'Windows'
  if (userAgent.includes('linux')) return 'Linux'
  return 'Unknown'
}

const osType = detectOS()
console.log(`🖥️ 检测到操作系统: ${osType}`)
console.log(`🌐 浏览器: ${navigator.userAgent}`)

// 错误监控
window.addEventListener('error', (event) => {
  console.error('🚨 全局错误:', event.error)
})

window.addEventListener('unhandledrejection', (event) => {
  console.error('🚨 未处理的 Promise 拒绝:', event.reason)
})

// 导出应用实例
export default app