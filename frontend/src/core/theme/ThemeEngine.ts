/**
 * 主题引擎核心实现
 * 负责主题加载、应用、切换和生命周期管理
 */

import { EventEmitter } from 'events'
import { 
  ThemeConfig, 
  ThemeTokens, 
  RuntimeTheme, 
  ThemeMode, 
  Platform,
  ThemeChangeEvent,
  ThemeLoadEvent,
  ThemeErrorEvent
} from './types'
import { ThemeValidator } from './ThemeValidator'
import { CSSGenerator } from './CSSGenerator'
import { AssetLoader } from './AssetLoader'
import { PerformanceMonitor } from './PerformanceMonitor'

export interface ThemeEngineOptions {
  defaultTheme: string
  availableThemes: ThemeConfig[]
  platform: Platform
  enableCache: boolean
  enablePrefetch: boolean
  performanceThreshold: number
  fallbackTheme: string
}

export class ThemeEngine extends EventEmitter {
  private currentTheme: RuntimeTheme | null = null
  private currentMode: ThemeMode = 'light'
  private themes: Map<string, ThemeConfig> = new Map()
  private isInitialized = false
  private isLoading = false
  
  private validator: ThemeValidator
  private cssGenerator: CSSGenerator
  private assetLoader: AssetLoader
  private performanceMonitor: PerformanceMonitor
  
  private options: ThemeEngineOptions
  private styleElement: HTMLStyleElement | null = null
  private cache: Map<string, RuntimeTheme> = new Map()

  constructor(options: ThemeEngineOptions) {
    super()
    this.options = options
    
    this.validator = new ThemeValidator()
    this.cssGenerator = new CSSGenerator()
    this.assetLoader = new AssetLoader()
    this.performanceMonitor = new PerformanceMonitor()
    
    this.initialize()
  }

  /**
   * 初始化主题引擎
   */
  private async initialize(): Promise<void> {
    try {
      // 注册可用主题
      this.registerThemes(this.options.availableThemes)
      
      // 创建样式元素
      this.createStyleElement()
      
      // 加载默认主题
      await this.loadTheme(this.options.defaultTheme, this.currentMode)
      
      // 监听系统主题变化
      this.setupSystemThemeListener()
      
      this.isInitialized = true
      this.emit('engine:initialized')
    } catch (error) {
      this.emit('engine:error', error)
      throw new Error(`Failed to initialize ThemeEngine: ${error}`)
    }
  }

  /**
   * 注册主题配置
   */
  private registerThemes(themes: ThemeConfig[]): void {
    themes.forEach(theme => {
      try {
        this.validator.validateThemeConfig(theme)
        this.themes.set(theme.id, theme)
      } catch (error) {
        console.warn(`Invalid theme configuration: ${theme.id}`, error)
      }
    })
  }

  /**
   * 创建样式元素
   */
  private createStyleElement(): void {
    this.styleElement = document.createElement('style')
    this.styleElement.id = 'theme-engine-styles'
    this.styleElement.setAttribute('data-theme-engine', 'true')
    document.head.appendChild(this.styleElement)
  }

  /**
   * 加载主题
   */
  public async loadTheme(themeId: string, mode: ThemeMode = this.currentMode): Promise<void> {
    if (this.isLoading) {
      throw new Error('Theme loading already in progress')
    }

    if (!this.themes.has(themeId)) {
      throw new Error(`Theme not found: ${themeId}`)
    }

    const startTime = performance.now()
    this.isLoading = true

    try {
      // 性能检查
      if (!this.performanceMonitor.canLoadTheme()) {
        throw new Error('Performance threshold exceeded')
      }

      // 检查缓存
      const cacheKey = `${themeId}-${mode}`
      if (this.options.enableCache && this.cache.has(cacheKey)) {
        await this.applyCachedTheme(this.cache.get(cacheKey)!)
        return
      }

      const themeConfig = this.themes.get(themeId)!
      
      // 生成运行时主题
      const runtimeTheme = await this.generateRuntimeTheme(themeConfig, mode)
      
      // 应用主题
      await this.applyTheme(runtimeTheme)
      
      // 缓存主题
      if (this.options.enableCache) {
        this.cache.set(cacheKey, runtimeTheme)
      }

      const loadTime = performance.now() - startTime
      
      // 触发事件
      const loadEvent: ThemeLoadEvent = {
        theme: themeId,
        duration: loadTime,
        assets: runtimeTheme.assets ? Object.keys(runtimeTheme.assets).length : 0
      }
      
      this.emit('theme:loaded', loadEvent)
      
    } catch (error) {
      const errorEvent: ThemeErrorEvent = {
        theme: themeId,
        error: error instanceof Error ? error.message : String(error),
        type: 'load'
      }
      
      this.emit('theme:error', errorEvent)
      
      // 回退到默认主题
      if (themeId !== this.options.fallbackTheme) {
        await this.loadTheme(this.options.fallbackTheme, mode)
      }
      
    } finally {
      this.isLoading = false
    }
  }

  /**
   * 生成运行时主题
   */
  private async generateRuntimeTheme(config: ThemeConfig, mode: ThemeMode): Promise<RuntimeTheme> {
    // 合并主题模式变体
    const tokens = this.mergeThemeVariants(config.tokens, mode)
    
    // 生成 CSS 变量
    const cssVariables = this.cssGenerator.generateCSSVariables(tokens)
    
    // 生成类名映射
    const classNames = this.cssGenerator.generateClassNames(tokens)
    
    // 加载资源
    const assets = await this.assetLoader.loadAssets(config, this.options.platform)
    
    return {
      config,
      cssVariables,
      classNames,
      assets
    }
  }

  /**
   * 合并主题模式变体
   */
  private mergeThemeVariants(tokens: ThemeTokens, mode: ThemeMode): ThemeTokens {
    if (mode === 'light') {
      return tokens
    }
    
    // 这里应该根据模式合并暗色变体
    // 简化实现，实际需要更复杂的合并逻辑
    const darkTokens = this.generateDarkTokens(tokens)
    return { ...tokens, ...darkTokens }
  }

  /**
   * 生成暗色主题令牌
   */
  private generateDarkTokens(tokens: ThemeTokens): Partial<ThemeTokens> {
    // 智能暗色主题生成算法
    return {
      colors: {
        ...tokens.colors,
        background: {
          primary: '#1C1C1E',
          secondary: '#2C2C2E',
          tertiary: '#3A3A3C',
          elevated: '#2C2C2E',
          overlay: 'rgba(0, 0, 0, 0.8)'
        },
        text: {
          primary: '#FFFFFF',
          secondary: '#EBEBF5',
          tertiary: '#8E8E93',
          inverse: '#000000',
          disabled: 'rgba(235, 235, 245, 0.3)'
        }
      }
    }
  }

  /**
   * 应用主题
   */
  private async applyTheme(runtimeTheme: RuntimeTheme): Promise<void> {
    if (!this.styleElement) {
      throw new Error('Style element not found')
    }

    const previousTheme = this.currentTheme
    
    try {
      // 构建 CSS 内容
      const cssContent = this.buildCSSContent(runtimeTheme)
      
      // 应用样式
      this.styleElement.textContent = cssContent
      
      // 更新 HTML 属性
      this.updateHTMLAttributes(runtimeTheme.config.id, this.currentMode)
      
      // 更新当前主题
      this.currentTheme = runtimeTheme
      
      // 触发变更事件
      const changeEvent: ThemeChangeEvent = {
        previous: previousTheme?.config.id || '',
        current: runtimeTheme.config.id,
        mode: this.currentMode,
        timestamp: Date.now()
      }
      
      this.emit('theme:changed', changeEvent)
      
    } catch (error) {
      // 回滚到之前的主题
      if (previousTheme) {
        await this.applyCachedTheme(previousTheme)
      }
      throw error
    }
  }

  /**
   * 应用缓存的主题
   */
  private async applyCachedTheme(runtimeTheme: RuntimeTheme): Promise<void> {
    const cssContent = this.buildCSSContent(runtimeTheme)
    
    if (this.styleElement) {
      this.styleElement.textContent = cssContent
      this.updateHTMLAttributes(runtimeTheme.config.id, this.currentMode)
      this.currentTheme = runtimeTheme
    }
  }

  /**
   * 构建 CSS 内容
   */
  private buildCSSContent(runtimeTheme: RuntimeTheme): string {
    const { cssVariables } = runtimeTheme
    
    // 生成 CSS 自定义属性
    const cssVars = Object.entries(cssVariables)
      .map(([key, value]) => `  ${key}: ${value};`)
      .join('\n')
    
    return `:root {\n${cssVars}\n}`
  }

  /**
   * 更新 HTML 属性
   */
  private updateHTMLAttributes(themeId: string, mode: ThemeMode): void {
    document.documentElement.setAttribute('data-theme', themeId)
    document.documentElement.setAttribute('data-theme-mode', mode)
    
    // 更新平台相关属性
    document.documentElement.setAttribute('data-platform', this.options.platform)
  }

  /**
   * 设置系统主题监听器
   */
  private setupSystemThemeListener(): void {
    if (window.matchMedia) {
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
      
      const handleChange = (e: MediaQueryListEvent) => {
        if (this.currentMode === 'auto') {
          const newMode = e.matches ? 'dark' : 'light'
          this.switchMode(newMode)
        }
      }
      
      mediaQuery.addEventListener('change', handleChange)
    }
  }

  /**
   * 切换主题模式
   */
  public async switchMode(mode: ThemeMode): Promise<void> {
    if (mode === this.currentMode) return
    
    this.currentMode = mode
    
    if (this.currentTheme) {
      await this.loadTheme(this.currentTheme.config.id, mode)
    }
  }

  /**
   * 获取当前主题
   */
  public getCurrentTheme(): RuntimeTheme | null {
    return this.currentTheme
  }

  /**
   * 获取当前模式
   */
  public getCurrentMode(): ThemeMode {
    return this.currentMode
  }

  /**
   * 获取可用主题
   */
  public getAvailableThemes(): ThemeConfig[] {
    return Array.from(this.themes.values())
  }

  /**
   * 销毁主题引擎
   */
  public destroy(): void {
    if (this.styleElement) {
      document.head.removeChild(this.styleElement)
      this.styleElement = null
    }
    
    this.cache.clear()
    this.themes.clear()
    this.removeAllListeners()
    
    this.isInitialized = false
  }

  /**
   * 性能优化
   */
  public async prefetchTheme(themeId: string): Promise<void> {
    if (!this.options.enablePrefetch) return
    
    try {
      const themeConfig = this.themes.get(themeId)
      if (themeConfig) {
        const runtimeTheme = await this.generateRuntimeTheme(themeConfig, this.currentMode)
        this.cache.set(`${themeId}-${this.currentMode}`, runtimeTheme)
      }
    } catch (error) {
      console.warn(`Failed to prefetch theme: ${themeId}`, error)
    }
  }

  /**
   * 清理缓存
   */
  public clearCache(): void {
    this.cache.clear()
  }

  /**
   * 获取性能统计
   */
  public getPerformanceStats() {
    return this.performanceMonitor.getStats()
  }
}