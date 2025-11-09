/**
 * 简化主题系统类型定义
 * 专注网页端跨操作系统支持
 */

// 主题模式 - 仅支持护眼和暗黑模式
export type ThemeMode = 'eye-care' | 'dark'

// 操作系统类型
export type OperatingSystem = 'windows' | 'macos' | 'linux' | 'unknown'

// 浏览器信息
export interface BrowserInfo {
  name: string
  version: string
  engine: string
}

// 简化主题配置
export interface SimpleThemeConfig {
  id: string
  name: string
  description: string
  modes: Record<ThemeMode, ThemeModeConfig>
}

// 主题模式配置
export interface ThemeModeConfig {
  colors: ColorTokens
  typography: TypographyTokens
  spacing: SpacingTokens
  shadows: ShadowTokens
  components: ComponentTokens
}

// 颜色令牌 - 精简版
export interface ColorTokens {
  // 背景色
  background: {
    primary: string    // 主背景
    secondary: string  // 次背景
    elevated: string   //  elevated 背景
    overlay: string    // 遮罩层
  }
  
  // 文字色
  text: {
    primary: string    // 主要文字
    secondary: string  // 次要文字
    muted: string      // 弱化文字
    inverse: string    // 反色文字
  }
  
  // 功能色
  semantic: {
    success: string
    warning: string
    error: string
    info: string
  }
  
  // 边框色
  border: {
    light: string
    medium: string
    strong: string
  }
  
  // 强调色
  accent: {
    primary: string
    secondary: string
  }
}

// 排版令牌
export interface TypographyTokens {
  fontFamily: {
    sans: string[]
    mono: string[]
  }
  fontSize: {
    xs: string
    sm: string
    base: string
    lg: string
    xl: string
    '2xl': string
  }
  fontWeight: {
    normal: number
    medium: number
    semibold: number
    bold: number
  }
  lineHeight: {
    tight: number
    normal: number
    relaxed: number
  }
}

// 间距令牌
export interface SpacingTokens {
  unit: number  // 基础单位，通常为 4px
  scale: {
    1: string
    2: string
    3: string
    4: string
    6: string
    8: string
    12: string
    16: string
    20: string
    24: string
  }
}

// 阴影令牌
export interface ShadowTokens {
  sm: string
  base: string
  md: string
  lg: string
}

// 组件令牌
export interface ComponentTokens {
  button: ButtonTokens
  card: CardTokens
  input: InputTokens
}

export interface ButtonTokens {
  padding: { x: string; y: string }
  borderRadius: string
  fontWeight: number
  transition: string
}

export interface CardTokens {
  padding: { x: string; y: string }
  borderRadius: string
  shadow: string
  background: string
  border: string
}

export interface InputTokens {
  padding: { x: string; y: string }
  borderRadius: string
  borderWidth: string
  background: string
}

// 运行时主题数据
export interface RuntimeTheme {
  config: SimpleThemeConfig
  currentMode: ThemeMode
  cssVariables: Record<string, string>
  os: OperatingSystem
  browser: BrowserInfo
}

// 跨OS适配配置
export interface CrossOSConfig {
  os: OperatingSystem
  browser: BrowserInfo
  capabilities: BrowserCapabilities
  optimizations: OSOptimizations
}

// 浏览器能力
export interface BrowserCapabilities {
  cssVariables: boolean
  backdropFilter: boolean
  webGL: boolean
  webFonts: boolean
  prefersReducedMotion: boolean
  colorGamut: 'srgb' | 'p3' | 'rec2020'
}

// OS特定优化
export interface OSOptimizations {
  fontSmoothing: boolean
  textRendering: boolean
  colorProfile: string
  scrollbar: 'auto' | 'thin' | 'none'
}

// 主题事件
export interface ThemeEvents {
  'theme:changed': { mode: ThemeMode; previous: ThemeMode }
  'theme:loaded': { config: SimpleThemeConfig; duration: number }
  'theme:error': { error: string; type: string }
}

// 主题选项
export interface ThemeOptions {
  defaultMode: ThemeMode
  respectSystemPreference: boolean
  enableTransitions: boolean
  enableCache: boolean
  performanceThreshold: number
}