/**
 * 平台适配器
 * 处理不同平台的主题适配和优化
 */

import { Platform, ThemeTokens, RuntimeTheme } from './types'

export interface PlatformAdapterConfig {
  platform: Platform
  userAgent?: string
  devicePixelRatio?: number
  viewport?: {
    width: number
    height: number
  }
  capabilities: PlatformCapabilities
}

export interface PlatformCapabilities {
  webGL: boolean
  backdropFilter: boolean
  cssVariables: boolean
  webFonts: boolean
  prefersReducedMotion: boolean
  touch: boolean
  pointer: boolean
}

export abstract class PlatformAdapter {
  protected config: PlatformAdapterConfig
  
  constructor(config: PlatformAdapterConfig) {
    this.config = config
  }

  /**
   * 适配主题令牌到特定平台
   */
  abstract adaptTokens(tokens: ThemeTokens): ThemeTokens
  
  /**
   * 优化运行时主题
   */
  abstract optimizeRuntimeTheme(theme: RuntimeTheme): RuntimeTheme
  
  /**
   * 获取平台特定的样式覆盖
   */
  abstract getPlatformOverrides(): Record<string, string>
  
  /**
   * 检测平台能力
   */
  abstract detectCapabilities(): PlatformCapabilities
  
  /**
   * 应用平台特定的优化
   */
  abstract applyPlatformOptimizations(): void
}

/**
 * Web 平台适配器
 */
export class WebPlatformAdapter extends PlatformAdapter {
  adaptTokens(tokens: ThemeTokens): ThemeTokens {
    const adapted = { ...tokens }
    
    // Web 平台特定的适配
    if (!this.config.capabilities.backdropFilter) {
      // 降级处理毛玻璃效果
      adapted.components = {
        ...adapted.components,
        card: {
          ...adapted.components.card,
          background: adapted.colors.background.primary
        }
      }
    }
    
    // 响应式字体大小调整
    if (this.config.viewport && this.config.viewport.width < 768) {
      adapted.typography = {
        ...adapted.typography,
        fontSize: {
          ...adapted.typography.fontSize,
          base: '14px',
          lg: '16px',
          xl: '18px'
        }
      }
    }
    
    return adapted
  }

  optimizeRuntimeTheme(theme: RuntimeTheme): RuntimeTheme {
    const optimized = { ...theme }
    
    // 根据设备像素比优化阴影
    const dpr = this.config.devicePixelRatio || 1
    if (dpr > 2) {
      optimized.cssVariables = {
        ...optimized.cssVariables,
        '--shadow-sm': '0 1px 2px rgba(0, 0, 0, 0.05)',
        '--shadow-md': '0 4px 6px rgba(0, 0, 0, 0.1)'
      }
    }
    
    return optimized
  }

  getPlatformOverrides(): Record<string, string> {
    return {
      '-webkit-font-smoothing': 'antialiased',
      '-moz-osx-font-smoothing': 'grayscale',
      'text-rendering': 'optimizeLegibility'
    }
  }

  detectCapabilities(): PlatformCapabilities {
    if (typeof window === 'undefined') {
      return {
        webGL: false,
        backdropFilter: false,
        cssVariables: false,
        webFonts: false,
        prefersReducedMotion: false,
        touch: false,
        pointer: true
      }
    }

    return {
      webGL: this.detectWebGL(),
      backdropFilter: this.detectBackdropFilter(),
      cssVariables: this.detectCSSVariables(),
      webFonts: this.detectWebFonts(),
      prefersReducedMotion: this.detectPrefersReducedMotion(),
      touch: this.detectTouch(),
      pointer: this.detectPointer()
    }
  }

  applyPlatformOptimizations(): void {
    // 应用 Web 平台优化
    if (this.config.capabilities.prefersReducedMotion) {
      document.documentElement.style.setProperty('--animation-duration-fast', '0ms')
      document.documentElement.style.setProperty('--animation-duration-normal', '0ms')
    }
  }

  private detectWebGL(): boolean {
    try {
      const canvas = document.createElement('canvas')
      const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl')
      return !!gl
    } catch {
      return false
    }
  }

  private detectBackdropFilter(): boolean {
    return CSS.supports('backdrop-filter', 'blur(1px)') || 
           CSS.supports('-webkit-backdrop-filter', 'blur(1px)')
  }

  private detectCSSVariables(): boolean {
    return CSS.supports('color', 'var(--test)')
  }

  private detectWebFonts(): boolean {
    return 'FontFace' in window
  }

  private detectPrefersReducedMotion(): boolean {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches
  }

  private detectTouch(): boolean {
    return 'ontouchstart' in window || navigator.maxTouchPoints > 0
  }

  private detectPointer(): boolean {
    return window.matchMedia('(pointer: fine)').matches
  }
}

/**
 * Electron 平台适配器
 */
export class ElectronPlatformAdapter extends PlatformAdapter {
  adaptTokens(tokens: ThemeTokens): ThemeTokens {
    const adapted = { ...tokens }
    
    // Electron 平台特定的适配
    adapted.components = {
      ...adapted.components,
      modal: {
        ...adapted.components.modal,
        // Electron 中模态框可以更大
        maxWidth: '90vw'
      }
    }
    
    return adapted
  }

  optimizeRuntimeTheme(theme: RuntimeTheme): RuntimeTheme {
    const optimized = { ...theme }
    
    // Electron 可以使用更丰富的效果
    if (process.env.IS_ELECTRON) {
      optimized.cssVariables = {
        ...optimized.cssVariables,
        '--shadow-xl': '0 20px 25px rgba(0, 0, 0, 0.2)'
      }
    }
    
    return optimized
  }

  getPlatformOverrides(): Record<string, string> {
    return {
      // Electron 特定的样式优化
      'cursor': 'default',
      'user-select': 'none'
    }
  }

  detectCapabilities(): PlatformCapabilities {
    return {
      webGL: true, // Electron 支持 WebGL
      backdropFilter: true, // Electron 支持 backdrop-filter
      cssVariables: true,
      webFonts: true,
      prefersReducedMotion: false,
      touch: false,
      pointer: true
    }
  }

  applyPlatformOptimizations(): void {
    // Electron 平台不需要特定的优化
  }
}

/**
 * PWA 平台适配器
 */
export class PWAPlatformAdapter extends WebPlatformAdapter {
  adaptTokens(tokens: ThemeTokens): ThemeTokens {
    let adapted = super.adaptTokens(tokens)
    
    // PWA 特定的适配
    if ('serviceWorker' in navigator) {
      // 离线模式下的优化
      adapted = {
        ...adapted,
        shadows: {
          ...adapted.shadows,
          // 使用更简单的阴影以减少资源消耗
          md: '0 2px 4px rgba(0, 0, 0, 0.1)'
        }
      }
    }
    
    return adapted
  }

  optimizeRuntimeTheme(theme: RuntimeTheme): RuntimeTheme {
    let optimized = super.optimizeRuntimeTheme(theme)
    
    // PWA 性能优化
    if (navigator.connection) {
      const connection = navigator.connection as any
      if (connection.effectiveType === '2g') {
        // 慢速网络下的优化
        optimized.cssVariables = {
          ...optimized.cssVariables,
          '--animation-duration-normal': '0ms',
          '--animation-duration-slow': '0ms'
        }
      }
    }
    
    return optimized
  }

  detectCapabilities(): PlatformCapabilities {
    const baseCapabilities = super.detectCapabilities()
    
    return {
      ...baseCapabilities,
      // PWA 支持离线
      offline: 'serviceWorker' in navigator && 'CacheStorage' in window
    } as any
  }
}

/**
 * 平台适配器工厂
 */
export class PlatformAdapterFactory {
  static createAdapter(platform: Platform, config: Partial<PlatformAdapterConfig> = {}): PlatformAdapter {
    const defaultConfig: PlatformAdapterConfig = {
      platform,
      userAgent: typeof navigator !== 'undefined' ? navigator.userAgent : undefined,
      devicePixelRatio: typeof window !== 'undefined' ? window.devicePixelRatio : 1,
      viewport: typeof window !== 'undefined' ? {
        width: window.innerWidth,
        height: window.innerHeight
      } : undefined,
      capabilities: this.detectCapabilities(platform)
    }

    const finalConfig = { ...defaultConfig, ...config }

    switch (platform) {
      case 'web':
        return new WebPlatformAdapter(finalConfig)
      case 'electron':
        return new ElectronPlatformAdapter(finalConfig)
      case 'pwa':
        return new PWAPlatformAdapter(finalConfig)
      default:
        return new WebPlatformAdapter(finalConfig)
    }
  }

  private static detectCapabilities(platform: Platform): PlatformCapabilities {
    // 基础能力检测
    const baseCapabilities = {
      webGL: false,
      backdropFilter: false,
      cssVariables: false,
      webFonts: false,
      prefersReducedMotion: false,
      touch: false,
      pointer: true
    }

    if (typeof window === 'undefined') {
      return baseCapabilities
    }

    // 根据平台返回不同的能力集
    switch (platform) {
      case 'electron':
        return {
          ...baseCapabilities,
          webGL: true,
          backdropFilter: true,
          cssVariables: true,
          webFonts: true
        }
      case 'pwa':
        return {
          ...baseCapabilities,
          webGL: 'WebGLRenderingContext' in window,
          backdropFilter: CSS.supports('backdrop-filter', 'blur(1px)'),
          cssVariables: CSS.supports('color', 'var(--test)'),
          webFonts: 'FontFace' in window
        }
      default:
        return {
          ...baseCapabilities,
          webGL: 'WebGLRenderingContext' in window,
          backdropFilter: CSS.supports('backdrop-filter', 'blur(1px)'),
          cssVariables: CSS.supports('color', 'var(--test)'),
          webFonts: 'FontFace' in window,
          prefersReducedMotion: window.matchMedia('(prefers-reduced-motion: reduce)').matches,
          touch: 'ontouchstart' in window
        }
    }
  }
}