/**
 * Material Design 3 主题配置
 * 基于 Google Material Design 3 规范
 */

import { ThemeConfig } from '../types'

export const materialThemeConfig: ThemeConfig = {
  id: 'material',
  name: 'Material Design 3',
  description: 'Google Material Design 3 风格主题',
  platform: ['web', 'pwa', 'mobile'],
  metadata: {
    version: '1.0.0',
    author: 'Theme System',
    createdAt: '2025-01-01',
    updatedAt: '2025-01-01',
    tags: ['google', 'material', 'md3', 'modern'],
    preview: '/themes/material/preview.png'
  },
  tokens: {
    colors: {
      primary: {
        50: '#E8F0FE',
        100: '#D2E1FC',
        200: '#A5C3F9',
        300: '#78A5F6',
        400: '#4B87F3',
        500: '#1F6EF0', // Material Blue
        600: '#1754D5',
        700: '#0F3ABA',
        800: '#07209F',
        900: '#000684',
        950: '#000052'
      },
      secondary: {
        50: '#F0F4F8',
        100: '#E1E7F0',
        200: '#C3CFE1',
        300: '#A5B7D2',
        400: '#879FC3',
        500: '#6A87B4',
        600: '#526A94',
        700: '#3A4D74',
        800: '#223054',
        900: '#0A1334',
        950: '#030814'
      },
      semantic: {
        success: {
          50: '#E8F5E8',
          100: '#D1E8D1',
          200: '#A3D1A3',
          300: '#75BA75',
          400: '#47A347',
          500: '#198C19',
          600: '#137013',
          700: '#0D540D',
          800: '#073807',
          900: '#011C01',
          950: '#000A00'
        },
        warning: {
          50: '#FFF8E1',
          100: '#FFF0C2',
          200: '#FFE185',
          300: '#FFD147',
          400: '#FFC20A',
          500: '#FFB300',
          600: '#CC8F00',
          700: '#996B00',
          800: '#664700',
          900: '#332300',
          950: '#190F00'
        },
        error: {
          50: '#FCE4EC',
          100: '#F8BBD9',
          200: '#F191B7',
          300: '#E96895',
          400: '#E43F73',
          500: '#D81B60',
          600: '#AD1750',
          700: '#821340',
          800: '#560E30',
          900: '#2B0A20',
          950: '#12040E'
        },
        info: {
          50: '#E3F2FD',
          100: '#BBDEFB',
          200: '#90CAF9',
          300: '#64B5F6',
          400: '#42A5F5',
          500: '#2196F3',
          600: '#1E88E5',
          700: '#1976D2',
          800: '#1565C0',
          900: '#0D47A1',
          950: '#072C64'
        }
      },
      neutral: {
        white: '#FFFFFF',
        black: '#000000',
        transparent: 'transparent',
        scale: {
          50: '#F8F9FA',
          100: '#F1F3F4',
          200: '#E8EAED',
          300: '#DADCE0',
          400: '#BDC1C6',
          500: '#9AA0A6',
          600: '#80868B',
          700: '#5F6368',
          800: '#3C4043',
          900: '#202124',
          950: '#131314'
        }
      },
      background: {
        primary: '#FFFFFF',
        secondary: '#F8F9FA',
        tertiary: '#F1F3F4',
        elevated: '#FFFFFF',
        overlay: 'rgba(0, 0, 0, 0.32)'
      },
      text: {
        primary: '#202124',
        secondary: '#5F6368',
        tertiary: '#9AA0A6',
        inverse: '#FFFFFF',
        disabled: 'rgba(32, 33, 36, 0.38)'
      },
      border: {
        light: '#DADCE0',
        medium: '#BDC1C6',
        strong: '#9AA0A6',
        focus: '#1F6EF0'
      }
    },
    typography: {
      fontFamily: {
        sans: ['Roboto', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Helvetica Neue', 'Arial', 'sans-serif'],
        mono: ['Roboto Mono', 'SFMono-Regular', 'Menlo', 'Monaco', 'Consolas', 'Liberation Mono', 'Courier New', 'monospace'],
        display: ['Google Sans', 'Roboto', 'system-ui', 'sans-serif']
      },
      fontSize: {
        xs: '0.75rem',
        sm: '0.875rem',
        base: '1rem',
        lg: '1.125rem',
        xl: '1.25rem',
        '2xl': '1.5rem',
        '3xl': '1.75rem',
        '4xl': '2rem',
        '5xl': '2.25rem',
        '6xl': '2.5rem'
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
        tight: 1.25,
        snug: 1.375,
        normal: 1.5,
        relaxed: 1.625,
        loose: 2
      },
      letterSpacing: {
        tighter: '-0.025em',
        tight: '-0.0125em',
        normal: '0em',
        wide: '0.0125em',
        wider: '0.025em',
        widest: '0.05em'
      }
    },
    spacing: {
      0: '0px',
      1: '0.25rem',
      2: '0.5rem',
      3: '0.75rem',
      4: '1rem',
      5: '1.25rem',
      6: '1.5rem',
      8: '2rem',
      10: '2.5rem',
      12: '3rem',
      16: '4rem',
      20: '5rem',
      24: '6rem',
      32: '8rem',
      40: '10rem',
      48: '12rem',
      56: '14rem',
      64: '16rem'
    },
    borderRadius: {
      none: '0px',
      sm: '0.125rem',
      base: '0.25rem',
      md: '0.375rem',
      lg: '0.5rem',
      xl: '0.75rem',
      '2xl': '1rem',
      '3xl': '1.5rem',
      full: '9999px'
    },
    shadows: {
      sm: '0 1px 2px 0 rgba(60, 64, 67, 0.3), 0 1px 3px 1px rgba(60, 64, 67, 0.15)',
      base: '0 1px 3px 0 rgba(60, 64, 67, 0.3), 0 4px 8px 3px rgba(60, 64, 67, 0.15)',
      md: '0 4px 4px 0 rgba(60, 64, 67, 0.3), 0 8px 12px 6px rgba(60, 64, 67, 0.15)',
      lg: '0 6px 10px 0 rgba(60, 64, 67, 0.3), 0 16px 24px 12px rgba(60, 64, 67, 0.15)',
      xl: '0 8px 12px 0 rgba(60, 64, 67, 0.3), 0 22px 32px 16px rgba(60, 64, 67, 0.15)',
      '2xl': '0 12px 17px 0 rgba(60, 64, 67, 0.3), 0 28px 40px 20px rgba(60, 64, 67, 0.15)',
      inner: 'inset 0 1px 2px 0 rgba(60, 64, 67, 0.3)',
      none: 'none'
    },
    animations: {
      duration: {
        fast: '150ms',
        normal: '200ms',
        slow: '250ms',
        slower: '300ms'
      },
      easing: {
        linear: 'linear',
        in: 'cubic-bezier(0.4, 0, 1, 1)',
        out: 'cubic-bezier(0, 0, 0.2, 1)',
        inOut: 'cubic-bezier(0.4, 0, 0.2, 1)',
        bounce: 'cubic-bezier(0.68, -0.55, 0.265, 1.55)'
      },
      keyframes: {
        'fade-in': {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' }
        },
        'slide-up': {
          '0%': { transform: 'translateY(24px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' }
        },
        'scale-in': {
          '0%': { transform: 'scale(0.8)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' }
        }
      }
    },
    components: {
      button: {
        padding: { x: '1rem', y: '0.625rem' },
        borderRadius: '0.25rem',
        fontWeight: 500,
        shadow: 'var(--shadows-sm)',
        transition: 'all 0.2s cubic-bezier(0.4, 0, 0.2, 1)'
      },
      card: {
        padding: { x: '1.5rem', y: '1.5rem' },
        borderRadius: '0.75rem',
        shadow: 'var(--shadows-base)',
        background: 'var(--colors-background-elevated)',
        border: 'none'
      },
      input: {
        padding: { x: '1rem', y: '0.75rem' },
        borderRadius: '0.25rem',
        borderWidth: '1px',
        focusRing: '0 0 0 2px rgba(31, 110, 240, 0.2)',
        background: 'var(--colors-background-primary)'
      },
      modal: {
        overlay: 'var(--colors-background-overlay)',
        background: 'var(--colors-background-elevated)',
        borderRadius: '1rem',
        shadow: 'var(--shadows-xl)',
        maxWidth: '560px'
      },
      tooltip: {
        background: 'rgba(32, 33, 36, 0.9)',
        textColor: 'var(--colors-text-inverse)',
        borderRadius: '0.25rem',
        padding: { x: '0.75rem', y: '0.5rem' },
        shadow: 'var(--shadows-md)',
        fontSize: '0.75rem'
      },
      dropdown: {
        background: 'var(--colors-background-elevated)',
        borderRadius: '0.5rem',
        shadow: 'var(--shadows-lg)',
        itemPadding: { x: '1rem', y: '0.75rem' },
        maxHeight: '320px'
      }
    }
  }
}