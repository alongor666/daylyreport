/**
 * macOS 主题配置
 * 基于 Apple Human Interface Guidelines
 */

import { ThemeConfig } from '../types'

export const macosThemeConfig: ThemeConfig = {
  id: 'macos',
  name: 'macOS',
  description: 'Apple macOS 风格主题，遵循 Human Interface Guidelines',
  platform: ['web', 'electron', 'desktop'],
  metadata: {
    version: '1.0.0',
    author: 'Theme System',
    createdAt: '2025-01-01',
    updatedAt: '2025-01-01',
    tags: ['apple', 'macos', 'hig', 'elegant'],
    preview: '/themes/macos/preview.png'
  },
  tokens: {
    colors: {
      primary: {
        50: '#E8F4FD',
        100: '#D1E9FB',
        200: '#A3D3F7',
        300: '#75BDF3',
        400: '#47A7EF',
        500: '#007AFF', // macOS Blue
        600: '#0066D4',
        700: '#0052AA',
        800: '#003E7F',
        900: '#002A55',
        950: '#00162A'
      },
      secondary: {
        50: '#F2F2F7',
        100: '#E5E5EA',
        200: '#CBCBD4',
        300: '#B1B1BE',
        400: '#9797A8',
        500: '#8E8E93', // macOS Gray
        600: '#757580',
        700: '#5C5C66',
        800: '#43434C',
        900: '#2A2A32',
        950: '#111118'
      },
      semantic: {
        success: {
          50: '#E8F8EF',
          100: '#D1F1DF',
          200: '#A3E3BF',
          300: '#75D59F',
          400: '#47C77F',
          500: '#34C759', // macOS Green
          600: '#2AA147',
          700: '#208135',
          800: '#166123',
          900: '#0C4011',
          950: '#022000'
        },
        warning: {
          50: '#FFF4E6',
          100: '#FFE9CC',
          200: '#FFD399',
          300: '#FFBD66',
          400: '#FFA733',
          500: '#FF9500', // macOS Orange
          600: '#CC7700',
          700: '#995900',
          800: '#664000',
          900: '#332000',
          950: '#190D00'
        },
        error: {
          50: '#FFEBEA',
          100: '#FFD7D5',
          200: '#FFAFAB',
          300: '#FF8781',
          400: '#FF5F57',
          500: '#FF3B30', // macOS Red
          600: '#CC2F26',
          700: '#99231C',
          800: '#661712',
          900: '#330B08',
          950: '#190300'
        },
        info: {
          50: '#E6F7FF',
          100: '#CCEEFF',
          200: '#99DDFF',
          300: '#66CCFF',
          400: '#33BBFF',
          500: '#00A2FF', // macOS Light Blue
          600: '#0082CC',
          700: '#006199',
          800: '#004166',
          900: '#002033',
          950: '#000D19'
        }
      },
      neutral: {
        white: '#FFFFFF',
        black: '#000000',
        transparent: 'transparent',
        scale: {
          50: '#F2F2F7',
          100: '#E5E5EA',
          200: '#D1D1D6',
          300: '#C7C7CC',
          400: '#AEAEB2',
          500: '#8E8E93',
          600: '#757580',
          700: '#5C5C66',
          800: '#43434C',
          900: '#2A2A32',
          950: '#111118'
        }
      },
      background: {
        primary: '#FFFFFF',
        secondary: '#F2F2F7',
        tertiary: '#E5E5EA',
        elevated: '#FFFFFF',
        overlay: 'rgba(0, 0, 0, 0.4)'
      },
      text: {
        primary: '#000000',
        secondary: '#3C3C43',
        tertiary: '#8E8E93',
        inverse: '#FFFFFF',
        disabled: 'rgba(60, 60, 67, 0.3)'
      },
      border: {
        light: 'rgba(0, 0, 0, 0.1)',
        medium: 'rgba(0, 0, 0, 0.2)',
        strong: 'rgba(0, 0, 0, 0.3)',
        focus: '#007AFF'
      }
    },
    typography: {
      fontFamily: {
        sans: ['-apple-system', 'BlinkMacSystemFont', 'SF Pro Display', 'SF Pro Text', 'Helvetica Neue', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'sans-serif'],
        mono: ['SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', 'Consolas', 'monospace'],
        display: ['SF Pro Display', '-apple-system', 'BlinkMacSystemFont', 'sans-serif']
      },
      fontSize: {
        xs: '10px',
        sm: '12px',
        base: '13px',
        lg: '14px',
        xl: '16px',
        '2xl': '18px',
        '3xl': '20px',
        '4xl': '24px',
        '5xl': '28px',
        '6xl': '32px'
      },
      fontWeight: {
        light: 300,
        normal: 400,
        medium: 500,
        semibold: 600,
        bold: 700,
        extrabold: 800
      },
      lineHeight: {
        none: 1,
        tight: 1.2,
        snug: 1.3,
        normal: 1.4,
        relaxed: 1.6,
        loose: 1.8
      },
      letterSpacing: {
        tighter: '-0.05em',
        tight: '-0.025em',
        normal: '0',
        wide: '0.025em',
        wider: '0.05em',
        widest: '0.1em'
      }
    },
    spacing: {
      0: '0',
      1: '1px',
      2: '2px',
      3: '4px',
      4: '6px',
      5: '8px',
      6: '10px',
      8: '12px',
      10: '14px',
      12: '16px',
      16: '20px',
      20: '24px',
      24: '28px',
      32: '32px',
      40: '36px',
      48: '40px',
      56: '44px',
      64: '48px'
    },
    borderRadius: {
      none: '0',
      sm: '4px',
      base: '6px',
      md: '8px',
      lg: '10px',
      xl: '12px',
      '2xl': '14px',
      '3xl': '16px',
      full: '9999px'
    },
    shadows: {
      sm: '0 1px 2px rgba(0, 0, 0, 0.05)',
      base: '0 1px 3px rgba(0, 0, 0, 0.1)',
      md: '0 4px 6px rgba(0, 0, 0, 0.1)',
      lg: '0 10px 15px rgba(0, 0, 0, 0.1)',
      xl: '0 20px 25px rgba(0, 0, 0, 0.1)',
      '2xl': '0 25px 50px rgba(0, 0, 0, 0.15)',
      inner: 'inset 0 2px 4px rgba(0, 0, 0, 0.05)',
      none: 'none'
    },
    animations: {
      duration: {
        fast: '150ms',
        normal: '200ms',
        slow: '300ms',
        slower: '500ms'
      },
      easing: {
        linear: 'linear',
        in: 'ease-in',
        out: 'ease-out',
        inOut: 'ease-in-out',
        bounce: 'cubic-bezier(0.68, -0.55, 0.265, 1.55)'
      },
      keyframes: {
        'fade-in': {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' }
        },
        'slide-up': {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' }
        },
        'scale-in': {
          '0%': { transform: 'scale(0.9)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' }
        }
      }
    },
    components: {
      button: {
        padding: { x: '12px', y: '6px' },
        borderRadius: '6px',
        fontWeight: 400,
        shadow: 'var(--shadows-sm)',
        transition: 'all 0.2s ease-out'
      },
      card: {
        padding: { x: '16px', y: '16px' },
        borderRadius: '10px',
        shadow: 'var(--shadows-base)',
        background: 'var(--colors-background-elevated)',
        border: '1px solid var(--colors-border-light)'
      },
      input: {
        padding: { x: '12px', y: '6px' },
        borderRadius: '6px',
        borderWidth: '1px',
        focusRing: '0 0 0 3px rgba(0, 122, 255, 0.1)',
        background: 'var(--colors-background-primary)'
      },
      modal: {
        overlay: 'var(--colors-background-overlay)',
        background: 'var(--colors-background-elevated)',
        borderRadius: '12px',
        shadow: 'var(--shadows-xl)',
        maxWidth: '600px'
      },
      tooltip: {
        background: 'rgba(60, 60, 67, 0.9)',
        textColor: 'var(--colors-text-inverse)',
        borderRadius: '6px',
        padding: { x: '8px', y: '4px' },
        shadow: 'var(--shadows-md)',
        fontSize: '12px'
      },
      dropdown: {
        background: 'var(--colors-background-elevated)',
        borderRadius: '8px',
        shadow: 'var(--shadows-lg)',
        itemPadding: { x: '12px', y: '8px' },
        maxHeight: '300px'
      }
    }
  }
}