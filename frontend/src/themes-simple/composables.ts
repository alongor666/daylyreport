/**
 * 主题系统组合式 API
 * 提供简洁的主题使用接口
 */

import { ref, computed, inject, provide, onMounted, onUnmounted } from 'vue'
import { SimpleThemeEngine } from './SimpleThemeEngine'
import { ThemeMode, RuntimeTheme } from './types'

// 主题引擎注入键
const THEME_ENGINE_KEY = 'simpleThemeEngine'

/**
 * 提供主题引擎
 */
export function provideThemeEngine(engine: SimpleThemeEngine): void {
  provide(THEME_ENGINE_KEY, engine)
}

/**
 * 使用主题引擎
 */
export function useThemeEngine(): SimpleThemeEngine {
  const engine = inject<SimpleThemeEngine>(THEME_ENGINE_KEY)
  if (!engine) {
    throw new Error('Theme engine not provided. Call provideThemeEngine() first.')
  }
  return engine
}

/**
 * 主题切换组合式函数
 */
export function useThemeSwitch() {
  const engine = useThemeEngine()
  const currentMode = ref<ThemeMode>(engine.getCurrentMode())
  const isLoading = ref(false)

  // 监听主题变化
  const updateCurrentMode = () => {
    currentMode.value = engine.getCurrentMode()
  }

  onMounted(() => {
    engine.on('theme:changed', updateCurrentMode)
    updateCurrentMode()
  })

  onUnmounted(() => {
    engine.off('theme:changed', updateCurrentMode)
  })

  /**
   * 切换主题模式
   */
  const switchMode = async (mode: ThemeMode) => {
    if (mode === currentMode.value) return
    
    isLoading.value = true
    try {
      await engine.switchMode(mode)
    } finally {
      isLoading.value = false
    }
  }

  /**
   * 切换到下一种模式
   */
  const toggleMode = () => {
    const modes: ThemeMode[] = ['eye-care', 'dark']
    const currentIndex = modes.indexOf(currentMode.value)
    const nextIndex = (currentIndex + 1) % modes.length
    return switchMode(modes[nextIndex])
  }

  return {
    currentMode,
    isLoading,
    switchMode,
    toggleMode
  }
}

/**
 * 主题样式组合式函数
 */
export function useThemeStyles() {
  const engine = useThemeEngine()
  const currentTheme = ref<RuntimeTheme | null>(engine.getCurrentTheme())

  // 监听主题变化
  const updateCurrentTheme = () => {
    currentTheme.value = engine.getCurrentTheme()
  }

  onMounted(() => {
    engine.on('theme:changed', updateCurrentTheme)
    updateCurrentTheme()
  })

  onUnmounted(() => {
    engine.off('theme:changed', updateCurrentTheme)
  })

  /**
   * 获取CSS变量值
   */
  const getCssVar = (variable: string): string => {
    return currentTheme.value?.cssVariables[variable] || ''
  }

  /**
   * 获取主题类名
   */
  const getThemeClass = (baseClass: string, variant?: string) => {
    return variant ? `${baseClass} ${baseClass}--${variant}` : baseClass
  }

  /**
   * 获取基础主题样式
   */
  const baseThemeStyles = computed(() => ({
    backgroundColor: getCssVar('--colors-background-primary'),
    color: getCssVar('--colors-text-primary'),
    fontFamily: getCssVar('--typography-fontFamily-sans')
  }))

  /**
   * 获取卡片样式
   */
  const cardStyles = computed(() => ({
    backgroundColor: getCssVar('--colors-background-elevated'),
    borderRadius: getCssVar('--components-card-borderRadius'),
    padding: getCssVar('--components-card-padding-x'),
    boxShadow: getCssVar('--components-card-shadow'),
    border: getCssVar('--components-card-border')
  }))

  /**
   * 获取按钮样式
   */
  const buttonStyles = computed(() => ({
    padding: getCssVar('--components-button-padding-x'),
    borderRadius: getCssVar('--components-button-borderRadius'),
    fontWeight: getCssVar('--components-button-fontWeight'),
    transition: getCssVar('--components-button-transition')
  }))

  /**
   * 获取输入框样式
   */
  const inputStyles = computed(() => ({
    padding: getCssVar('--components-input-padding-x'),
    borderRadius: getCssVar('--components-input-borderRadius'),
    borderWidth: getCssVar('--components-input-borderWidth'),
    backgroundColor: getCssVar('--components-input-background')
  }))

  return {
    currentTheme,
    getCssVar,
    getThemeClass,
    baseThemeStyles,
    cardStyles,
    buttonStyles,
    inputStyles
  }
}

/**
 * 组件主题组合式函数
 */
export function useComponentTheme() {
  const { getCssVar, getThemeClass } = useThemeStyles()

  /**
   * 获取按钮变体样式
   */
  const getButtonVariantStyles = (variant: 'primary' | 'secondary' | 'ghost') => {
    const baseStyles = {
      backgroundColor: getCssVar('--components-button-background') || 'transparent',
      color: getCssVar('--colors-text-primary'),
      border: '1px solid transparent',
      cursor: 'pointer',
      outline: 'none'
    }

    switch (variant) {
      case 'primary':
        return {
          ...baseStyles,
          backgroundColor: getCssVar('--colors-accent-primary'),
          color: '#ffffff',
          '&:hover': {
            backgroundColor: getCssVar('--colors-accent-secondary')
          }
        }
      case 'secondary':
        return {
          ...baseStyles,
          backgroundColor: 'transparent',
          color: getCssVar('--colors-accent-primary'),
          border: `1px solid ${getCssVar('--colors-accent-primary')}`,
          '&:hover': {
            backgroundColor: getCssVar('--colors-accent-primary'),
            color: '#ffffff'
          }
        }
      case 'ghost':
        return {
          ...baseStyles,
          backgroundColor: 'transparent',
          color: getCssVar('--colors-text-primary'),
          '&:hover': {
            backgroundColor: getCssVar('--colors-background-secondary')
          }
        }
      default:
        return baseStyles
    }
  }

  /**
   * 获取卡片变体样式
   */
  const getCardVariantStyles = (variant: 'elevated' | 'outlined' | 'flat') => {
    const baseStyles = {
      backgroundColor: getCssVar('--colors-background-elevated'),
      borderRadius: getCssVar('--components-card-borderRadius'),
      overflow: 'hidden'
    }

    switch (variant) {
      case 'elevated':
        return {
          ...baseStyles,
          boxShadow: getCssVar('--shadows-md'),
          border: 'none'
        }
      case 'outlined':
        return {
          ...baseStyles,
          boxShadow: 'none',
          border: `1px solid ${getCssVar('--colors-border-medium')}`
        }
      case 'flat':
        return {
          ...baseStyles,
          boxShadow: 'none',
          border: 'none',
          backgroundColor: getCssVar('--colors-background-secondary')
        }
      default:
        return baseStyles
    }
  }

  /**
   * 获取输入框状态样式
   */
  const getInputStateStyles = (state: 'focus' | 'error' | 'disabled') => {
    switch (state) {
      case 'focus':
        return {
          outline: 'none',
          borderColor: getCssVar('--colors-accent-primary'),
          boxShadow: `0 0 0 2px ${getCssVar('--colors-accent-primary')}20`
        }
      case 'error':
        return {
          borderColor: getCssVar('--colors-semantic-error'),
          backgroundColor: `${getCssVar('--colors-semantic-error')}10`
        }
      case 'disabled':
        return {
          opacity: '0.6',
          cursor: 'not-allowed',
          backgroundColor: getCssVar('--colors-background-secondary')
        }
      default:
        return {}
    }
  }

  return {
    getButtonVariantStyles,
    getCardVariantStyles,
    getInputStateStyles,
    getThemeClass
  }
}

/**
 * 主题模式指示器组合式函数
 */
export function useThemeIndicator() {
  const engine = useThemeEngine()
  const { currentMode } = useThemeSwitch()

  const modeIcon = computed(() => {
    switch (currentMode.value) {
      case 'eye-care':
        return '😊' // 护眼图标
      case 'dark':
        return '🌙' // 月亮图标
      default:
        return '💡'
    }
  })

  const modeDescription = computed(() => {
    switch (currentMode.value) {
      case 'eye-care':
        return '护眼模式 - 减少蓝光，保护视力'
      case 'dark':
        return '暗黑模式 - 适合夜间使用'
      default:
        return '未知模式'
    }
  })

  return {
    currentMode,
    modeIcon,
    modeDescription
  }
}

/**
 * 系统偏好监听组合式函数
 */
export function useSystemPreference() {
  const engine = useThemeEngine()
  const systemPreference = ref<'light' | 'dark'>('light')
  const respectsSystem = ref(true)

  const updateSystemPreference = () => {
    if (window.matchMedia) {
      const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches
      systemPreference.value = isDark ? 'dark' : 'light'
    }
  }

  onMounted(() => {
    updateSystemPreference()
    
    if (window.matchMedia) {
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
      mediaQuery.addEventListener('change', updateSystemPreference)
      
      onUnmounted(() => {
        mediaQuery.removeEventListener('change', updateSystemPreference)
      })
    }
  })

  const toggleSystemPreference = () => {
    respectsSystem.value = !respectsSystem.value
    // 这里可以更新引擎的设置
  }

  return {
    systemPreference,
    respectsSystem,
    toggleSystemPreference
  }
}