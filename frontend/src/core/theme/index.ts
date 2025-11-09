/**
 * 主题系统主入口
 * 提供统一的 API 和工具函数
 */

import { App } from 'vue'
import { ThemeEngine, ThemeEngineOptions } from './ThemeEngine'
import { PlatformAdapterFactory } from './PlatformAdapter'
import { ComponentThemeAdapterManager } from './ComponentThemeAdapter'
import { ThemeConfig, Platform, ThemeMode } from './types'

// 主题配置
import { defaultThemeConfig } from './themes/default'
import { macosThemeConfig } from './themes/macos'
import { materialThemeConfig } from './themes/material'

/**
 * 主题系统配置
 */
export interface ThemeSystemConfig {
  defaultTheme?: string
  availableThemes?: ThemeConfig[]
  platform?: Platform
  enableCache?: boolean
  enablePrefetch?: boolean
  performanceThreshold?: number
  autoDetectPlatform?: boolean
}

/**
 * 主题系统主类
 */
export class ThemeSystem {
  private engine: ThemeEngine | null = null
  private componentManager: ComponentThemeAdapterManager | null = null
  private config: ThemeSystemConfig

  constructor(config: ThemeSystemConfig = {}) {
    this.config = {
      defaultTheme: 'default',
      availableThemes: [
        defaultThemeConfig,
        macosThemeConfig,
        materialThemeConfig
      ],
      platform: 'web',
      enableCache: true,
      enablePrefetch: true,
      performanceThreshold: 100, // ms
      autoDetectPlatform: true,
      ...config
    }
  }

  /**
   * 初始化主题系统
   */
  async initialize(): Promise<void> {
    // 自动检测平台
    const platform = this.config.autoDetectPlatform 
      ? this.detectPlatform() 
      : this.config.platform!

    // 创建主题引擎
    const engineOptions: ThemeEngineOptions = {
      defaultTheme: this.config.defaultTheme!,
      availableThemes: this.config.availableThemes!,
      platform,
      enableCache: this.config.enableCache!,
      enablePrefetch: this.config.enablePrefetch!,
      performanceThreshold: this.config.performanceThreshold!,
      fallbackTheme: 'default'
    }

    this.engine = new ThemeEngine(engineOptions)
    
    // 等待引擎初始化
    await new Promise<void>((resolve) => {
      this.engine!.once('engine:initialized', () => resolve())
    })

    // 创建组件管理器
    this.componentManager = new ComponentThemeAdapterManager(
      computed(() => this.engine!.getCurrentTheme()?.config.tokens || defaultThemeConfig.tokens)
    )
  }

  /**
   * 检测当前平台
   */
  private detectPlatform(): Platform {
    if (typeof window === 'undefined') return 'web'
    
    // Electron 检测
    if (process.env.IS_ELECTRON || (window as any).process) {
      return 'electron'
    }
    
    // PWA 检测
    if ('serviceWorker' in navigator && 'BeforeInstallPromptEvent' in window) {
      return 'pwa'
    }
    
    // 移动端检测
    const userAgent = navigator.userAgent.toLowerCase()
    const isMobile = /android|webos|iphone|ipad|ipod|blackberry|iemobile|opera mini/i.test(userAgent)
    
    if (isMobile) {
      return 'mobile'
    }
    
    return 'web'
  }

  /**
   * 获取主题引擎
   */
  getEngine(): ThemeEngine {
    if (!this.engine) {
      throw new Error('ThemeSystem not initialized')
    }
    return this.engine
  }

  /**
   * 获取组件管理器
   */
  getComponentManager(): ComponentThemeAdapterManager {
    if (!this.componentManager) {
      throw new Error('ThemeSystem not initialized')
    }
    return this.componentManager
  }

  /**
   * 切换主题
   */
  async switchTheme(themeId: string): Promise<void> {
    await this.engine?.loadTheme(themeId)
  }

  /**
   * 切换主题模式
   */
  async switchMode(mode: ThemeMode): Promise<void> {
    await this.engine?.switchMode(mode)
  }

  /**
   * 获取当前主题
   */
  getCurrentTheme() {
    return this.engine?.getCurrentTheme()
  }

  /**
   * 获取当前模式
   */
  getCurrentMode() {
    return this.engine?.getCurrentMode()
  }

  /**
   * 销毁主题系统
   */
  destroy(): void {
    this.engine?.destroy()
    this.engine = null
    this.componentManager = null
  }
}

/**
 * Vue 插件安装函数
 */
export const ThemePlugin = {
  install(app: App, config: ThemeSystemConfig = {}) {
    const themeSystem = new ThemeSystem(config)
    
    // 将主题系统注入到全局属性
    app.config.globalProperties.$theme = themeSystem
    
    // 提供主题系统
    app.provide('themeSystem', themeSystem)
    
    // 初始化主题系统
    themeSystem.initialize().then(() => {
      // 提供组合式 API
      app.provide('useTheme', () => themeSystem)
      app.provide('useComponentTheme', (componentType: any) => {
        return themeSystem.getComponentManager().getAdapter(componentType)
      })
    })
  }
}

/**
 * 组合式 API 工具函数
 */
export function useTheme() {
  const themeSystem = inject<ThemeSystem>('themeSystem')
  if (!themeSystem) {
    throw new Error('useTheme must be used within a ThemeProvider')
  }
  return themeSystem
}

export function useComponentTheme<T extends keyof ComponentTokens>(
  componentType: T
) {
  const themeSystem = useTheme()
  return themeSystem.getComponentManager().getAdapter(componentType)
}

export function useThemeSwitch() {
  const themeSystem = useTheme()
  const currentTheme = ref(themeSystem.getCurrentTheme())
  const currentMode = ref(themeSystem.getCurrentMode())
  const isLoading = ref(false)

  const switchTheme = async (themeId: string) => {
    isLoading.value = true
    try {
      await themeSystem.switchTheme(themeId)
      currentTheme.value = themeSystem.getCurrentTheme()
    } finally {
      isLoading.value = false
    }
  }

  const switchMode = async (mode: ThemeMode) => {
    isLoading.value = true
    try {
      await themeSystem.switchMode(mode)
      currentMode.value = themeSystem.getCurrentMode()
    } finally {
      isLoading.value = false
    }
  }

  return {
    currentTheme,
    currentMode,
    isLoading,
    switchTheme,
    switchMode
  }
}

// 工具函数
export { PlatformAdapterFactory } from './PlatformAdapter'
export { ComponentThemeAdapterManager } from './ComponentThemeAdapter'
export * from './types'

// 主题配置
export { defaultThemeConfig } from './themes/default'
export { macosThemeConfig } from './themes/macos'
export { materialThemeConfig } from './themes/material'

// 默认导出
export default ThemeSystem