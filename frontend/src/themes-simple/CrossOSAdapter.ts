/**
 * 轻量级跨操作系统适配器
 * 专注检测OS差异并提供最小化优化
 */

import { OperatingSystem, BrowserInfo, CrossOSConfig, BrowserCapabilities, OSOptimizations } from './types'

/**
 * 跨OS适配器 - 轻量级实现
 */
export class CrossOSAdapter {
  private os: OperatingSystem = 'unknown'
  private browser: BrowserInfo = { name: 'unknown', version: '0', engine: 'unknown' }
  private config: CrossOSConfig | null = null

  constructor() {
    this.detectEnvironment()
  }

  /**
   * 检测运行环境
   */
  private detectEnvironment(): void {
    if (typeof window === 'undefined') {
      this.os = 'unknown'
      this.browser = { name: 'unknown', version: '0', engine: 'unknown' }
      return
    }

    // 检测操作系统
    this.os = this.detectOS()
    
    // 检测浏览器
    this.browser = this.detectBrowser()
    
    // 生成配置
    this.config = this.generateConfig()
  }

  /**
   * 检测操作系统 - 简化版
   */
  private detectOS(): OperatingSystem {
    const userAgent = navigator.userAgent.toLowerCase()
    const platform = navigator.platform.toLowerCase()

    // macOS 检测
    if (platform.includes('mac') || userAgent.includes('mac')) {
      return 'macos'
    }
    
    // Windows 检测
    if (platform.includes('win') || userAgent.includes('win')) {
      return 'windows'
    }
    
    // Linux 检测（包含信创系统）
    if (platform.includes('linux') || userAgent.includes('linux')) {
      return 'linux'
    }
    
    return 'unknown'
  }

  /**
   * 检测浏览器 - 简化版
   */
  private detectBrowser(): BrowserInfo {
    const ua = navigator.userAgent
    
    // Chrome/Edge
    if (ua.includes('Chrome') || ua.includes('Edg')) {
      const match = ua.match(/(Chrome|Edg)\/(\d+)/)
      return {
        name: match?.[1] || 'Chrome',
        version: match?.[2] || '0',
        engine: 'Blink'
      }
    }
    
    // Firefox
    if (ua.includes('Firefox')) {
      const match = ua.match(/Firefox\/(\d+)/)
      return {
        name: 'Firefox',
        version: match?.[1] || '0',
        engine: 'Gecko'
      }
    }
    
    // Safari
    if (ua.includes('Safari') && !ua.includes('Chrome')) {
      const match = ua.match(/Version\/(\d+)/)
      return {
        name: 'Safari',
        version: match?.[1] || '0',
        engine: 'WebKit'
      }
    }
    
    return {
      name: 'Unknown',
      version: '0',
      engine: 'Unknown'
    }
  }

  /**
   * 生成跨OS配置
   */
  private generateConfig(): CrossOSConfig {
    const capabilities = this.detectCapabilities()
    const optimizations = this.getOSOptimizations()
    
    return {
      os: this.os,
      browser: this.browser,
      capabilities,
      optimizations
    }
  }

  /**
   * 检测浏览器能力 - 最小化检测
   */
  private detectCapabilities(): BrowserCapabilities {
    return {
      cssVariables: CSS.supports('color', 'var(--test)'),
      backdropFilter: CSS.supports('backdrop-filter', 'blur(1px)') || CSS.supports('-webkit-backdrop-filter', 'blur(1px)'),
      webGL: this.checkWebGL(),
      webFonts: 'FontFace' in window,
      prefersReducedMotion: window.matchMedia('(prefers-reduced-motion: reduce)').matches,
      colorGamut: this.detectColorGamut()
    }
  }

  /**
   * 获取OS特定优化
   */
  private getOSOptimizations(): OSOptimizations {
    const baseOptimizations: OSOptimizations = {
      fontSmoothing: true,
      textRendering: true,
      colorProfile: 'sRGB',
      scrollbar: 'auto'
    }

    switch (this.os) {
      case 'macos':
        return {
          ...baseOptimizations,
          fontSmoothing: true,
          textRendering: true,
          colorProfile: 'Display P3',
          scrollbar: 'thin'
        }
        
      case 'windows':
        return {
          ...baseOptimizations,
          fontSmoothing: true,
          textRendering: true,
          colorProfile: 'sRGB',
          scrollbar: 'auto'
        }
        
      case 'linux':
        return {
          ...baseOptimizations,
          fontSmoothing: false, // Linux 字体渲染差异较大
          textRendering: true,
          colorProfile: 'sRGB',
          scrollbar: 'auto'
        }
        
      default:
        return baseOptimizations
    }
  }

  /**
   * 检测WebGL支持
   */
  private checkWebGL(): boolean {
    try {
      const canvas = document.createElement('canvas')
      const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl')
      return !!gl
    } catch {
      return false
    }
  }

  /**
   * 检测色域支持
   */
  private detectColorGamut(): 'srgb' | 'p3' | 'rec2020' {
    if (window.matchMedia('(color-gamut: rec2020)').matches) {
      return 'rec2020'
    }
    if (window.matchMedia('(color-gamut: p3)').matches) {
      return 'p3'
    }
    return 'srgb'
  }

  /**
   * 应用OS特定样式
   */
  applyOSStyles(): void {
    if (!this.config) return

    const { optimizations } = this.config
    
    // 字体优化
    if (optimizations.fontSmoothing) {
      document.documentElement.style.setProperty('-webkit-font-smoothing', 'antialiased')
      document.documentElement.style.setProperty('-moz-osx-font-smoothing', 'grayscale')
    }
    
    // 文字渲染优化
    if (optimizations.textRendering) {
      document.documentElement.style.setProperty('text-rendering', 'optimizeLegibility')
    }
    
    // 滚动条优化
    this.applyScrollbarStyles(optimizations.scrollbar)
  }

  /**
   * 应用滚动条样式
   */
  private applyScrollbarStyles(type: 'auto' | 'thin' | 'none'): void {
    let styles = ''
    
    switch (type) {
      case 'thin':
        styles = `
          ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
          }
          ::-webkit-scrollbar-track {
            background: transparent;
          }
          ::-webkit-scrollbar-thumb {
            background: rgba(0, 0, 0, 0.2);
            border-radius: 4px;
          }
          ::-webkit-scrollbar-thumb:hover {
            background: rgba(0, 0, 0, 0.3);
          }
        `
        break
        
      case 'none':
        styles = `
          ::-webkit-scrollbar {
            display: none;
          }
        `
        break
        
      default:
        // 保持默认滚动条
        break
    }
    
    if (styles) {
      const styleElement = document.createElement('style')
      styleElement.textContent = styles
      document.head.appendChild(styleElement)
    }
  }

  /**
   * 获取系统颜色模式偏好
   */
  getSystemColorPreference(): 'light' | 'dark' {
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      return 'dark'
    }
    return 'light'
  }

  /**
   * 获取减少动画偏好
   */
  getReducedMotionPreference(): boolean {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches
  }

  /**
   * 获取高对比度偏好
   */
  getHighContrastPreference(): boolean {
    return window.matchMedia('(prefers-contrast: high)').matches
  }

  /**
   * 获取当前配置
   */
  getConfig(): CrossOSConfig | null {
    return this.config
  }

  /**
   * 获取操作系统
   */
  getOS(): OperatingSystem {
    return this.os
  }

  /**
   * 获取浏览器信息
   */
  getBrowser(): BrowserInfo {
    return this.browser
  }

  /**
   * 是否为触摸设备
   */
  isTouchDevice(): boolean {
    return 'ontouchstart' in window || navigator.maxTouchPoints > 0
  }

  /**
   * 获取设备像素比
   */
  getDevicePixelRatio(): number {
    return window.devicePixelRatio || 1
  }

  /**
   * 获取视口信息
   */
  getViewportInfo() {
    return {
      width: window.innerWidth,
      height: window.innerHeight,
      devicePixelRatio: this.getDevicePixelRatio()
    }
  }
}

/**
 * 跨OS适配器工厂函数
 */
export function createCrossOSAdapter(): CrossOSAdapter {
  return new CrossOSAdapter()
}

/**
 * 快速检测函数
 */
export function quickOSDetection(): { os: OperatingSystem; browser: BrowserInfo } {
  const adapter = new CrossOSAdapter()
  return {
    os: adapter.getOS(),
    browser: adapter.getBrowser()
  }
}