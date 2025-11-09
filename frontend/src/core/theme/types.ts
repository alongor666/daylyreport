/**
 * 主题系统核心类型定义
 * 遵循 SOLID 原则，确保类型安全和可扩展性
 */

// 基础主题令牌类型
export interface ThemeTokens {
  // 颜色系统
  colors: {
    primary: ColorScale
    secondary: ColorScale
    semantic: SemanticColors
    neutral: NeutralScale
    background: BackgroundColors
    text: TextColors
    border: BorderColors
  }
  
  // 排版系统
  typography: {
    fontFamily: FontFamilies
    fontSize: FontScale
    fontWeight: FontWeights
    lineHeight: LineHeights
    letterSpacing: LetterSpacings
  }
  
  // 间距系统
  spacing: SpacingScale
  
  // 圆角系统
  borderRadius: BorderRadiusScale
  
  // 阴影系统
  shadows: ShadowScale
  
  // 动画系统
  animations: AnimationConfig
  
  // 组件特定令牌
  components: ComponentTokens
}

// 颜色渐变类型
export interface ColorScale {
  50: string
  100: string
  200: string
  300: string
  400: string
  500: string
  600: string
  700: string
  800: string
  900: string
  950: string
}

export interface SemanticColors {
  success: ColorScale
  warning: ColorScale
  error: ColorScale
  info: ColorScale
}

export interface NeutralScale {
  white: string
  black: string
  transparent: string
  scale: ColorScale
}

export interface BackgroundColors {
  primary: string
  secondary: string
  tertiary: string
  elevated: string
  overlay: string
}

export interface TextColors {
  primary: string
  secondary: string
  tertiary: string
  inverse: string
  disabled: string
}

export interface BorderColors {
  light: string
  medium: string
  strong: string
  focus: string
}

// 排版相关类型
export interface FontFamilies {
  sans: string[]
  mono: string[]
  display: string[]
}

export interface FontScale {
  xs: string
  sm: string
  base: string
  lg: string
  xl: string
  '2xl': string
  '3xl': string
  '4xl': string
  '5xl': string
  '6xl': string
}

export interface FontWeights {
  light: number
  normal: number
  medium: number
  semibold: number
  bold: number
  extrabold: number
}

export interface LineHeights {
  none: number
  tight: number
  snug: number
  normal: number
  relaxed: number
  loose: number
}

export interface LetterSpacings {
  tighter: string
  tight: string
  normal: string
  wide: string
  wider: string
  widest: string
}

// 间距系统
export interface SpacingScale {
  0: string
  1: string
  2: string
  3: string
  4: string
  5: string
  6: string
  8: string
  10: string
  12: string
  16: string
  20: string
  24: string
  32: string
  40: string
  48: string
  56: string
  64: string
}

// 圆角系统
export interface BorderRadiusScale {
  none: string
  sm: string
  base: string
  md: string
  lg: string
  xl: string
  '2xl': string
  '3xl': string
  full: string
}

// 阴影系统
export interface ShadowScale {
  sm: string
  base: string
  md: string
  lg: string
  xl: string
  '2xl': string
  inner: string
  none: string
}

// 动画配置
export interface AnimationConfig {
  duration: AnimationDurations
  easing: AnimationEasings
  keyframes: KeyframeDefinitions
}

export interface AnimationDurations {
  fast: string
  normal: string
  slow: string
  slower: string
}

export interface AnimationEasings {
  linear: string
  in: string
  out: string
  inOut: string
  bounce: string
}

export interface KeyframeDefinitions {
  [key: string]: CSSKeyframes
}

// 组件特定令牌
export interface ComponentTokens {
  button: ButtonTokens
  card: CardTokens
  input: InputTokens
  modal: ModalTokens
  tooltip: TooltipTokens
  dropdown: DropdownTokens
}

export interface ButtonTokens {
  padding: SpacingTokens
  borderRadius: string
  fontWeight: number
  shadow: string
  transition: string
}

export interface CardTokens {
  padding: SpacingTokens
  borderRadius: string
  shadow: string
  background: string
  border: string
}

export interface InputTokens {
  padding: SpacingTokens
  borderRadius: string
  borderWidth: string
  focusRing: string
  background: string
}

export interface ModalTokens {
  overlay: string
  background: string
  borderRadius: string
  shadow: string
  maxWidth: string
}

export interface TooltipTokens {
  background: string
  textColor: string
  borderRadius: string
  padding: SpacingTokens
  shadow: string
  fontSize: string
}

export interface DropdownTokens {
  background: string
  borderRadius: string
  shadow: string
  itemPadding: SpacingTokens
  maxHeight: string
}

export interface SpacingTokens {
  x: string
  y: string
}

export interface CSSKeyframes {
  [key: string]: CSSProperties
}

export interface CSSProperties {
  [key: string]: string | number
}

// 主题配置接口
export interface ThemeConfig {
  id: string
  name: string
  description: string
  platform: Platform[]
  tokens: ThemeTokens
  metadata: ThemeMetadata
}

export interface ThemeMetadata {
  version: string
  author: string
  createdAt: string
  updatedAt: string
  tags: string[]
  preview: string
}

// 平台类型
export type Platform = 'web' | 'electron' | 'pwa' | 'mobile' | 'desktop'

// 主题模式
export type ThemeMode = 'light' | 'dark' | 'auto'

// 主题变体
export interface ThemeVariant {
  mode: ThemeMode
  tokens: Partial<ThemeTokens>
}

// 主题继承
export interface ThemeInheritance {
  extends?: string
  overrides: Partial<ThemeTokens>
}

// 主题验证
export interface ThemeValidation {
  required: string[]
  optional: string[]
  constraints: ValidationConstraints
}

export interface ValidationConstraints {
  [key: string]: ValidationRule
}

export interface ValidationRule {
  type: 'color' | 'length' | 'number' | 'string'
  min?: number
  max?: number
  pattern?: RegExp
  required?: boolean
}

// 运行时主题数据
export interface RuntimeTheme {
  config: ThemeConfig
  cssVariables: Record<string, string>
  classNames: Record<string, string>
  assets: ThemeAssets
}

export interface ThemeAssets {
  fonts: FontAsset[]
  icons: IconAsset[]
  images: ImageAsset[]
}

export interface FontAsset {
  family: string
  src: string
  weight: number
  style: 'normal' | 'italic'
}

export interface IconAsset {
  name: string
  src: string
  format: 'svg' | 'png' | 'woff'
}

export interface ImageAsset {
  name: string
  src: string
  type: 'background' | 'texture' | 'pattern'
}

// 主题事件
export interface ThemeEvents {
  'theme:changed': ThemeChangeEvent
  'theme:loaded': ThemeLoadEvent
  'theme:error': ThemeErrorEvent
}

export interface ThemeChangeEvent {
  previous: string
  current: string
  mode: ThemeMode
  timestamp: number
}

export interface ThemeLoadEvent {
  theme: string
  duration: number
  assets: number
}

export interface ThemeErrorEvent {
  theme: string
  error: string
  type: 'validation' | 'load' | 'apply'
}