/**
 * 简化主题系统主入口
 * 专注网页端跨操作系统支持
 */

import { App } from 'vue'
import { SimpleThemeEngine } from './SimpleThemeEngine'
import { ThemeOptions, ThemeMode } from './types'
import { provideThemeEngine } from './composables'
import { eyeCareTheme, darkTheme } from './themes'

// 默认配置
const defaultOptions: ThemeOptions = {
  defaultMode: 'eye-care',
  respectSystemPreference: true,
  enableTransitions: true,
  enableCache: true,
  performanceThreshold: 50
}

/**
 * 创建简化主题引擎
 */
export function createSimpleThemeEngine(options?: Partial<ThemeOptions>): SimpleThemeEngine {
  const finalOptions = { ...defaultOptions, ...options }
  return new SimpleThemeEngine(finalOptions)
}

/**
 * Vue 插件
 */
export const SimpleThemePlugin = {
  install(app: App, options?: Partial<ThemeOptions>) {
    const engine = createSimpleThemeEngine(options)
    
    // 提供主题引擎
    provideThemeEngine(engine)
    
    // 全局属性
    app.config.globalProperties.$simpleTheme = engine
    
    // 异步初始化
    engine.initialize().then(() => {
      app.config.globalProperties.$onSimpleThemeReady?.()
    })
  }
}

/**
 * 快速初始化函数
 */
export async function initSimpleTheme(options?: Partial<ThemeOptions>): Promise<SimpleThemeEngine> {
  const engine = createSimpleThemeEngine(options)
  await engine.initialize()
  return engine
}

// 组合式 API 导出
export {
  useThemeEngine,
  useThemeSwitch,
  useThemeStyles,
  useComponentTheme,
  useThemeIndicator,
  useSystemPreference
} from './composables'

// 类型导出
export type {
  ThemeMode,
  OperatingSystem,
  SimpleThemeConfig,
  RuntimeTheme,
  ThemeOptions
} from './types'

// 主题配置导出
export { eyeCareTheme, darkTheme, themeConfigs, getThemeConfig } from './themes'

// 工具函数导出
export { createCrossOSAdapter, quickOSDetection } from './CrossOSAdapter'

// 默认导出
export default {
  createSimpleThemeEngine,
  SimpleThemePlugin,
  initSimpleTheme,
  eyeCareTheme,
  darkTheme
}