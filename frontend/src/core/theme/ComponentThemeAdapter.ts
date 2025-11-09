/**
 * 组件主题适配器
 * 为每个组件提供主题化的抽象层
 */

import { ThemeTokens, ComponentTokens } from './types'
import { computed, ref, Ref, ComputedRef } from 'vue'

/**
 * 组件主题适配器接口
 */
export interface ComponentThemeAdapter<T extends keyof ComponentTokens> {
  readonly componentType: T
  readonly tokens: ComputedRef<ComponentTokens[T]>
  readonly className: ComputedRef<string>
  readonly styles: ComputedRef<Record<string, string>>
  
  getToken<K extends keyof ComponentTokens[T]>(key: K): ComputedRef<ComponentTokens[T][K]>
  getClassName(variant?: string): ComputedRef<string>
  getStyle(property: string): ComputedRef<string>
  mergeTokens(overrides: Partial<ComponentTokens[T]>): void
}

/**
 * 基础组件主题适配器
 */
export abstract class BaseComponentThemeAdapter<T extends keyof ComponentTokens> 
  implements ComponentThemeAdapter<T> {
  
  protected themeTokens: Ref<ThemeTokens>
  protected componentType: T
  protected overrideTokens: Ref<Partial<ComponentTokens[T]>>
  
  constructor(themeTokens: Ref<ThemeTokens>, componentType: T) {
    this.themeTokens = themeTokens
    this.componentType = componentType
    this.overrideTokens = ref({})
  }

  get tokens(): ComputedRef<ComponentTokens[T]> {
    return computed(() => {
      const baseTokens = this.themeTokens.value.components[this.componentType]
      return { ...baseTokens, ...this.overrideTokens.value }
    })
  }

  get className(): ComputedRef<string> {
    return computed(() => `theme-${this.componentType}`)
  }

  get styles(): ComputedRef<Record<string, string>> {
    return computed(() => this.generateStyles(this.tokens.value))
  }

  getToken<K extends keyof ComponentTokens[T]>(key: K): ComputedRef<ComponentTokens[T][K]> {
    return computed(() => this.tokens.value[key])
  }

  getClassName(variant?: string): ComputedRef<string> {
    return computed(() => {
      const baseClass = this.className.value
      return variant ? `${baseClass}--${variant}` : baseClass
    })
  }

  getStyle(property: string): ComputedRef<string> {
    return computed(() => this.styles.value[property] || '')
  }

  mergeTokens(overrides: Partial<ComponentTokens[T]>): void {
    this.overrideTokens.value = { ...this.overrideTokens.value, ...overrides }
  }

  /**
   * 生成组件样式
   */
  protected abstract generateStyles(tokens: ComponentTokens[T]): Record<string, string>
}

/**
 * 按钮组件主题适配器
 */
export class ButtonThemeAdapter extends BaseComponentThemeAdapter<'button'> {
  constructor(themeTokens: Ref<ThemeTokens>) {
    super(themeTokens, 'button')
  }

  protected generateStyles(tokens: ComponentTokens['button']): Record<string, string> {
    return {
      padding: `${tokens.padding.y} ${tokens.padding.x}`,
      borderRadius: tokens.borderRadius,
      fontWeight: String(tokens.fontWeight),
      boxShadow: tokens.shadow,
      transition: tokens.transition
    }
  }

  /**
   * 获取按钮变体样式
   */
  getVariantStyles(variant: 'primary' | 'secondary' | 'ghost'): ComputedRef<Record<string, string>> {
    return computed(() => {
      const baseStyles = this.styles.value
      
      switch (variant) {
        case 'primary':
          return {
            ...baseStyles,
            backgroundColor: 'var(--colors-primary-500)',
            color: 'white',
            border: 'none'
          }
        case 'secondary':
          return {
            ...baseStyles,
            backgroundColor: 'transparent',
            color: 'var(--colors-primary-500)',
            border: '1px solid var(--colors-primary-500)'
          }
        case 'ghost':
          return {
            ...baseStyles,
            backgroundColor: 'transparent',
            color: 'var(--colors-text-primary)',
            border: 'none',
            boxShadow: 'none'
          }
        default:
          return baseStyles
      }
    })
  }

  /**
   * 获取按钮尺寸样式
   */
  getSizeStyles(size: 'sm' | 'md' | 'lg'): ComputedRef<Record<string, string>> {
    return computed(() => {
      const baseTokens = this.tokens.value
      
      switch (size) {
        case 'sm':
          return {
            padding: '4px 8px',
            fontSize: '12px',
            borderRadius: '4px'
          }
        case 'md':
          return {
            padding: baseTokens.padding.y + ' ' + baseTokens.padding.x,
            fontSize: '14px',
            borderRadius: baseTokens.borderRadius
          }
        case 'lg':
          return {
            padding: '12px 24px',
            fontSize: '16px',
            borderRadius: '8px'
          }
        default:
          return {}
      }
    })
  }
}

/**
 * 卡片组件主题适配器
 */
export class CardThemeAdapter extends BaseComponentThemeAdapter<'card'> {
  constructor(themeTokens: Ref<ThemeTokens>) {
    super(themeTokens, 'card')
  }

  protected generateStyles(tokens: ComponentTokens['card']): Record<string, string> {
    return {
      padding: `${tokens.padding.y} ${tokens.padding.x}`,
      borderRadius: tokens.borderRadius,
      boxShadow: tokens.shadow,
      backgroundColor: tokens.background,
      border: tokens.border
    }
  }

  /**
   * 获取卡片变体样式
   */
  getVariantStyles(variant: 'elevated' | 'outlined' | 'filled'): ComputedRef<Record<string, string>> {
    return computed(() => {
      const baseStyles = this.styles.value
      
      switch (variant) {
        case 'elevated':
          return {
            ...baseStyles,
            boxShadow: 'var(--shadows-lg)',
            border: 'none'
          }
        case 'outlined':
          return {
            ...baseStyles,
            boxShadow: 'none',
            border: '1px solid var(--colors-border-medium)'
          }
        case 'filled':
          return {
            ...baseStyles,
            boxShadow: 'none',
            border: 'none',
            backgroundColor: 'var(--colors-background-secondary)'
          }
        default:
          return baseStyles
      }
    })
  }

  /**
   * 获取交互状态样式
   */
  getInteractiveStyles(state: 'hover' | 'focus' | 'active'): ComputedRef<Record<string, string>> {
    return computed(() => {
      switch (state) {
        case 'hover':
          return {
            transform: 'translateY(-2px)',
            boxShadow: 'var(--shadows-xl)',
            transition: 'all 0.2s ease'
          }
        case 'focus':
          return {
            outline: '2px solid var(--colors-primary-500)',
            outlineOffset: '2px'
          }
        case 'active':
          return {
            transform: 'translateY(0)',
            boxShadow: 'var(--shadows-base)'
          }
        default:
          return {}
      }
    })
  }
}

/**
 * 输入框组件主题适配器
 */
export class InputThemeAdapter extends BaseComponentThemeAdapter<'input'> {
  constructor(themeTokens: Ref<ThemeTokens>) {
    super(themeTokens, 'input')
  }

  protected generateStyles(tokens: ComponentTokens['input']): Record<string, string> {
    return {
      padding: `${tokens.padding.y} ${tokens.padding.x}`,
      borderRadius: tokens.borderRadius,
      borderWidth: tokens.borderWidth,
      backgroundColor: tokens.background,
      transition: 'all 0.2s ease'
    }
  }

  /**
   * 获取输入框状态样式
   */
  getStateStyles(state: 'focus' | 'error' | 'disabled'): ComputedRef<Record<string, string>> {
    return computed(() => {
      const baseStyles = this.styles.value
      
      switch (state) {
        case 'focus':
          return {
            ...baseStyles,
            borderColor: 'var(--colors-primary-500)',
            boxShadow: this.tokens.value.focusRing,
            outline: 'none'
          }
        case 'error':
          return {
            ...baseStyles,
            borderColor: 'var(--colors-semantic-error-500)',
            backgroundColor: 'rgba(239, 68, 68, 0.05)'
          }
        case 'disabled':
          return {
            ...baseStyles,
            opacity: '0.6',
            cursor: 'not-allowed',
            backgroundColor: 'var(--colors-background-tertiary)'
          }
        default:
          return baseStyles
      }
    })
  }

  /**
   * 获取输入框尺寸样式
   */
  getSizeStyles(size: 'sm' | 'md' | 'lg'): ComputedRef<Record<string, string>> {
    return computed(() => {
      const baseTokens = this.tokens.value
      
      switch (size) {
        case 'sm':
          return {
            padding: '6px 10px',
            fontSize: '12px',
            borderRadius: '4px'
          }
        case 'md':
          return {
            padding: baseTokens.padding.y + ' ' + baseTokens.padding.x,
            fontSize: '14px',
            borderRadius: baseTokens.borderRadius
          }
        case 'lg':
          return {
            padding: '12px 16px',
            fontSize: '16px',
            borderRadius: '8px'
          }
        default:
          return {}
      }
    })
  }
}

/**
 * 组件主题适配器管理器
 */
export class ComponentThemeAdapterManager {
  private adapters: Map<string, BaseComponentThemeAdapter<any>> = new Map()
  private themeTokens: Ref<ThemeTokens>

  constructor(themeTokens: Ref<ThemeTokens>) {
    this.themeTokens = themeTokens
    this.initializeAdapters()
  }

  private initializeAdapters(): void {
    // 注册所有组件适配器
    this.adapters.set('button', new ButtonThemeAdapter(this.themeTokens))
    this.adapters.set('card', new CardThemeAdapter(this.themeTokens))
    this.adapters.set('input', new InputThemeAdapter(this.themeTokens))
  }

  /**
   * 获取组件适配器
   */
  getAdapter<T extends keyof ComponentTokens>(
    componentType: T
  ): BaseComponentThemeAdapter<T> {
    const adapter = this.adapters.get(componentType)
    if (!adapter) {
      throw new Error(`Component adapter not found: ${componentType}`)
    }
    return adapter as BaseComponentThemeAdapter<T>
  }

  /**
   * 获取所有适配器
   */
  getAllAdapters(): Map<string, BaseComponentThemeAdapter<any>> {
    return this.adapters
  }

  /**
   * 更新主题令牌
   */
  updateThemeTokens(themeTokens: Ref<ThemeTokens>): void {
    this.themeTokens = themeTokens
    // 重新初始化所有适配器
    this.initializeAdapters()
  }

  /**
   * 注册自定义组件适配器
   */
  registerAdapter<T extends keyof ComponentTokens>(
    componentType: T,
    adapter: BaseComponentThemeAdapter<T>
  ): void {
    this.adapters.set(componentType, adapter)
  }

  /**
   * 获取组件样式工具函数
   */
  createStyleHelpers<T extends keyof ComponentTokens>(componentType: T) {
    const adapter = this.getAdapter(componentType)
    
    return {
      base: adapter.styles,
      className: adapter.className,
      getVariant: (variant: string) => adapter.getClassName(variant),
      getToken: (key: keyof ComponentTokens[T]) => adapter.getToken(key)
    }
  }
}

/**
 * 组合式 API 工具函数
 */
export function useComponentTheme<T extends keyof ComponentTokens>(
  componentType: T,
  themeTokens: Ref<ThemeTokens>
) {
  const manager = new ComponentThemeAdapterManager(themeTokens)
  const adapter = manager.getAdapter(componentType)
  
  return {
    tokens: adapter.tokens,
    styles: adapter.styles,
    className: adapter.className,
    getVariantStyles: (variant: string) => adapter.getClassName(variant),
    getToken: (key: keyof ComponentTokens[T]) => adapter.getToken(key)
  }
}