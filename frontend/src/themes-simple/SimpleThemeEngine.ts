/**
 * 简化主题引擎
 * 专注护眼和暗黑两种模式，轻量级实现
 */

import { EventEmitter } from 'events'
import { 
  SimpleThemeConfig, 
  ThemeMode, 
  RuntimeTheme, 
  ThemeOptions,
  OperatingSystem,
  BrowserInfo
} from './types'
import { CrossOSAdapter } from './CrossOSAdapter'

/**
 * 简化主题引擎
 */
export class SimpleThemeEngine extends EventEmitter {
  private currentTheme: RuntimeTheme | null = null
  private currentMode: ThemeMode
  private options: ThemeOptions
  private osAdapter: CrossOSAdapter
  private styleElement: HTMLStyleElement | null = null
  private isInitialized = false
  private isLoading = false

  constructor(options: Partial<ThemeOptions> = {}) {
    super()
    
    this.options = {
      defaultMode: 'eye-care',
      respectSystemPreference: true,
      enableTransitions: true,
      enableCache: true,
      performanceThreshold: 50,
      ...options
    }
    
    this.currentMode = this.options.defaultMode
    this.osAdapter = new CrossOSAdapter()
  }

  /**
   * 初始化主题引擎
   */
  async initialize(): Promise<void> {
    if (this.isInitialized) return

    try {
      // 创建样式元素
      this.createStyleElement()
      
      // 应用OS优化
      this.osAdapter.applyOSStyles()
      
      // 监听系统主题变化
      this.setupSystemPreferenceListener()
      
      // 加载默认主题
      await this.loadTheme(this.currentMode)
      
      this.isInitialized = true
      this.emit('engine:ready')
      
    } catch (error) {
      this.emit('engine:error', error)
      throw new Error(`Failed to initialize theme engine: ${error}`)
    }
  }

  /**
   * 创建样式元素
   */
  private createStyleElement(): void {
    this.styleElement = document.createElement('style')
    this.styleElement.id = 'simple-theme-styles'
    this.styleElement.setAttribute('data-theme-engine', 'simple')
    document.head.appendChild(this.styleElement)
  }

  /**
   * 加载主题模式
   */
  async loadTheme(mode: ThemeMode): Promise<void> {
    if (!this.isInitialized) {
      throw new Error('Theme engine not initialized')
    }

    if (this.isLoading) return
    this.isLoading = true

    try {
      const startTime = performance.now()
      
      // 性能检查
      if (!this.checkPerformance()) {
        throw new Error('Performance threshold exceeded')
      }

      // 获取主题配置
      const config = this.getThemeConfig(mode)
      
      // 生成运行时主题
      const runtimeTheme = await this.generateRuntimeTheme(config, mode)
      
      // 应用主题
      this.applyTheme(runtimeTheme)
      
      const loadTime = performance.now() - startTime
      
      // 触发事件
      this.emit('theme:loaded', {
        config,
        duration: loadTime
      })
      
    } catch (error) {
      this.emit('theme:error', {
        error: error instanceof Error ? error.message : String(error),
        type: 'load'
      })
      throw error
      
    } finally {
      this.isLoading = false
    }
  }

  /**
   * 获取主题配置 - 内建两种模式
   */
  private getThemeConfig(mode: ThemeMode): SimpleThemeConfig {
    return {
      id: 'simple-theme',
      name: 'Simple Theme',
      description: '护眼与暗黑双模式主题',
      modes: {
        'eye-care': this.getEyeCareModeConfig(),
        'dark': this.getDarkModeConfig()
      }
    }
  }

  /**
   * 护眼模式配置
   */
  private getEyeCareModeConfig(): any {
    return {
      colors: {
        background: {
          primary: '#fefcf3',      // 温暖的米白色
          secondary: '#f8f4e9',    // 浅米色
          elevated: '#ffffff',     // 纯白
          overlay: 'rgba(0, 0, 0, 0.4)'
        },
        text: {
          primary: '#3a3a3a',      // 深灰色，减少对比度
          secondary: '#5a5a5a',    // 中等灰色
          muted: '#8a8a8a',        // 浅灰色
          inverse: '#ffffff'
        },
        semantic: {
          success: '#4a7c59',      // 柔和的绿色
          warning: '#d4a574',      // 柔和的橙色
          error: '#c97064',        // 柔和的红色
          info: '#6a8caf'          // 柔和的蓝色
        },
        border: {
          light: 'rgba(0, 0, 0, 0.08)',
          medium: 'rgba(0, 0, 0, 0.15)',
          strong: 'rgba(0, 0, 0, 0.25)'
        },
        accent: {
          primary: '#8b7355',      // 温和的棕色
          secondary: '#a3907c'     // 浅棕色
        }
      },
      typography: this.getTypographyTokens(),
      spacing: this.getSpacingTokens(),
      shadows: this.getShadowTokens(),
      components: this.getComponentTokens('eye-care')
    }
  }

  /**
   * 暗黑模式配置
   */
  private getDarkModeConfig(): any {
    return {
      colors: {
        background: {
          primary: '#1a1a1a',      // 深灰黑
          secondary: '#242424',    // 深灰色
          elevated: '#2d2d2d',     // 稍浅灰色
          overlay: 'rgba(0, 0, 0, 0.7)'
        },
        text: {
          primary: '#e8e8e8',      // 亮灰色
          secondary: '#b8b8b8',    // 中等灰色
          muted: '#888888',        // 暗灰色
          inverse: '#000000'
        },
        semantic: {
          success: '#6b9f7f',      // 柔和的绿色
          warning: '#e0b974',      // 柔和的黄色
          error: '#d47c70',        // 柔和的红色
          info: '#7ba7d1'          // 柔和的蓝色
        },
        border: {
          light: 'rgba(255, 255, 255, 0.08)',
          medium: 'rgba(255, 255, 255, 0.15)',
          strong: 'rgba(255, 255, 255, 0.25)'
        },
        accent: {
          primary: '#a3907c',      // 柔和的棕色
          secondary: '#8b7355'     // 深棕色
        }
      },
      typography: this.getTypographyTokens(),
      spacing: this.getSpacingTokens(),
      shadows: this.getDarkShadowTokens(),
      components: this.getComponentTokens('dark')
    }
  }

  /**
   * 获取排版令牌
   */
  private getTypographyTokens() {
    return {
      fontFamily: {
        sans: ['-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        mono: ['SF Mono', 'Monaco', 'Consolas', 'monospace']
      },
      fontSize: {
        xs: '12px',
        sm: '14px',
        base: '16px',
        lg: '18px',
        xl: '20px',
        '2xl': '24px'
      },
      fontWeight: {
        normal: 400,
        medium: 500,
        semibold: 600,
        bold: 700
      },
      lineHeight: {
        tight: 1.25,
        normal: 1.5,
        relaxed: 1.75
      }
    }
  }

  /**
   * 获取间距令牌
   */
  private getSpacingTokens() {
    const unit = 4 // 基础单位 4px
    return {
      unit,
      scale: {
        1: `${unit}px`,      // 4px
        2: `${unit * 2}px`,  // 8px
        3: `${unit * 3}px`,  // 12px
        4: `${unit * 4}px`,  // 16px
        6: `${unit * 6}px`,  // 24px
        8: `${unit * 8}px`,  // 32px
        12: `${unit * 12}px`, // 48px
        16: `${unit * 16}px`, // 64px
        20: `${unit * 20}px`, // 80px
        24: `${unit * 24}px`  // 96px
      }
    }
  }

  /**
   * 获取阴影令牌
   */
  private getShadowTokens() {
    return {
      sm: '0 1px 2px rgba(0, 0, 0, 0.05)',
      base: '0 2px 4px rgba(0, 0, 0, 0.1)',
      md: '0 4px 8px rgba(0, 0, 0, 0.12)',
      lg: '0 8px 16px rgba(0, 0, 0, 0.15)'
    }
  }

  /**
   * 获取暗黑模式阴影
   */
  private getDarkShadowTokens() {
    return {
      sm: '0 1px 2px rgba(0, 0, 0, 0.3)',
      base: '0 2px 4px rgba(0, 0, 0, 0.4)',
      md: '0 4px 8px rgba(0, 0, 0, 0.5)',
      lg: '0 8px 16px rgba(0, 0, 0, 0.6)'
    }
  }

  /**
   * 获取组件令牌
   */
  private getComponentTokens(mode: ThemeMode) {
    const isDark = mode === 'dark'
    
    return {
      button: {
        padding: { x: '16px', y: '8px' },
        borderRadius: '6px',
        fontWeight: 500,
        transition: 'all 0.2s ease-out'
      },
      card: {
        padding: { x: '20px', y: '20px' },
        borderRadius: '8px',
        shadow: isDark ? 'var(--shadows-base)' : 'var(--shadows-sm)',
        background: isDark ? 'var(--colors-background-elevated)' : '#ffffff',
        border: `1px solid var(--colors-border-light)`
      },
      input: {
        padding: { x: '12px', y: '8px' },
        borderRadius: '6px',
        borderWidth: '1px',
        background: isDark ? 'var(--colors-background-secondary)' : '#ffffff'
      }
    }
  }

  /**
   * 生成运行时主题
   */
  private async generateRuntimeTheme(config: SimpleThemeConfig, mode: ThemeMode): Promise<RuntimeTheme> {
    const modeConfig = config.modes[mode]
    
    // 生成CSS变量
    const cssVariables = this.generateCSSVariables(modeConfig)
    
    return {
      config,
      currentMode: mode,
      cssVariables,
      os: this.osAdapter.getOS(),
      browser: this.osAdapter.getBrowser()
    }
  }

  /**
   * 生成CSS变量
   */
  private generateCSSVariables(modeConfig: any): Record<string, string> {
    const variables: Record<string, string> = {}
    
    // 颜色变量
    Object.entries(modeConfig.colors).forEach(([category, colors]: [string, any]) => {
      Object.entries(colors).forEach(([key, value]: [string, any]) => {
        if (typeof value === 'string') {
          variables[`--colors-${category}-${key}`] = value
        } else if (typeof value === 'object') {
          Object.entries(value).forEach(([subKey, subValue]: [string, any]) => {
            variables[`--colors-${category}-${key}-${subKey}`] = subValue
          })
        }
      })
    })
    
    // 排版变量
    Object.entries(modeConfig.typography).forEach(([category, values]: [string, any]) => {
      Object.entries(values).forEach(([key, value]: [string, any]) => {
        if (typeof value === 'string' || typeof value === 'number') {
          variables[`--typography-${category}-${key}`] = String(value)
        }
      })
    })
    
    // 间距变量
    Object.entries(modeConfig.spacing.scale).forEach(([key, value]: [string, any]) => {
      variables[`--spacing-${key}`] = value
    })
    
    // 阴影变量
    Object.entries(modeConfig.shadows).forEach(([key, value]: [string, any]) => {
      variables[`--shadows-${key}`] = value
    })
    
    // 组件变量
    Object.entries(modeConfig.components).forEach(([component, tokens]: [string, any]) => {
      Object.entries(tokens).forEach(([key, value]: [string, any]) => {
        if (typeof value === 'string' || typeof value === 'number') {
          variables[`--components-${component}-${key}`] = String(value)
        } else if (typeof value === 'object') {
          Object.entries(value).forEach(([subKey, subValue]: [string, any]) => {
            variables[`--components-${component}-${key}-${subKey}`] = String(subValue)
          })
        }
      })
    })
    
    return variables
  }

  /**
   * 应用主题
   */
  private applyTheme(runtimeTheme: RuntimeTheme): void {
    if (!this.styleElement) return

    const previousTheme = this.currentTheme
    
    try {
      // 构建CSS内容
      const cssContent = this.buildCSSContent(runtimeTheme)
      
      // 应用样式
      this.styleElement.textContent = cssContent
      
      // 更新HTML属性
      this.updateHTMLAttributes(runtimeTheme.currentMode)
      
      // 更新当前主题
      this.currentTheme = runtimeTheme
      this.currentMode = runtimeTheme.currentMode
      
      // 触发变更事件
      this.emit('theme:changed', {
        mode: runtimeTheme.currentMode,
        previous: previousTheme?.currentMode || runtimeTheme.currentMode
      })
      
    } catch (error) {
      // 回滚
      if (previousTheme) {
        this.applyTheme(previousTheme)
      }
      throw error
    }
  }

  /**
   * 构建CSS内容
   */
  private buildCSSContent(runtimeTheme: RuntimeTheme): string {
    const { cssVariables } = runtimeTheme
    
    // 添加过渡动画
    const transitionStyles = this.options.enableTransitions ? `
      * {
        transition: background-color 0.2s ease-out, 
                   color 0.2s ease-out,
                   border-color 0.2s ease-out;
      }
    ` : ''
    
    // 生成CSS变量
    const cssVars = Object.entries(cssVariables)
      .map(([key, value]) => `  ${key}: ${value};`)
      .join('\n')
    
    return `:root {\n${cssVars}\n}\n\n${transitionStyles}`
  }

  /**
   * 更新HTML属性
   */
  private updateHTMLAttributes(mode: ThemeMode): void {
    document.documentElement.setAttribute('data-theme-mode', mode)
    document.documentElement.setAttribute('data-os', this.osAdapter.getOS())
  }

  /**
   * 设置系统偏好监听
   */
  private setupSystemPreferenceListener(): void {
    if (!this.options.respectSystemPreference) return
    
    if (window.matchMedia) {
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
      
      const handleChange = (e: MediaQueryListEvent) => {
        const systemMode = e.matches ? 'dark' : 'eye-care'
        if (systemMode !== this.currentMode) {
          this.switchMode(systemMode)
        }
      }
      
      mediaQuery.addEventListener('change', handleChange)
    }
  }

  /**
   * 性能检查
   */
  private checkPerformance(): boolean {
    if (!window.performance) return true
    
    const memory = (performance as any).memory
    if (memory) {
      const usedMemory = memory.usedJSHeapSize
      const totalMemory = memory.totalJSHeapSize
      
      // 内存使用超过90%时限制主题加载
      if (usedMemory / totalMemory > 0.9) {
        return false
      }
    }
    
    return true
  }

  /**
   * 切换主题模式
   */
  async switchMode(mode: ThemeMode): Promise<void> {
    if (mode === this.currentMode) return
    
    this.currentMode = mode
    await this.loadTheme(mode)
  }

  /**
   * 获取当前主题
   */
  getCurrentTheme(): RuntimeTheme | null {
    return this.currentTheme
  }

  /**
   * 获取当前模式
   */
  getCurrentMode(): ThemeMode {
    return this.currentMode
  }

  /**
   * 销毁主题引擎
   */
  destroy(): void {
    if (this.styleElement) {
      document.head.removeChild(this.styleElement)
      this.styleElement = null
    }
    
    this.removeAllListeners()
    this.isInitialized = false
  }
}