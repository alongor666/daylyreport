/**
 * 内置主题配置
 * 护眼模式和暗黑模式
 */

import { SimpleThemeConfig } from './types'

/**
 * 护眼主题配置
 * 基于眼科医学研究，减少蓝光，提供舒适的阅读体验
 */
export const eyeCareTheme: SimpleThemeConfig = {
  id: 'eye-care',
  name: '护眼模式',
  description: '专为长时间阅读设计的护眼主题，减少蓝光刺激',
  modes: {
    'eye-care': {
      colors: {
        background: {
          primary: '#fefcf3',      // 温暖的米白色 - 减少蓝光
          secondary: '#f8f4e9',    // 浅米色
          elevated: '#ffffff',     // 纯白
          overlay: 'rgba(0, 0, 0, 0.4)'
        },
        text: {
          primary: '#3a3a3a',      // 深灰色，降低对比度
          secondary: '#5a5a5a',    // 中等灰色
          muted: '#8a8a8a',        // 浅灰色
          inverse: '#ffffff'
        },
        semantic: {
          success: '#5a8a69',      // 柔和的绿色
          warning: '#c89660',      // 柔和的橙色
          error: '#b86a5e',        // 柔和的红色
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
      typography: {
        fontFamily: {
          sans: ['-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'Helvetica Neue', 'Arial', 'sans-serif'],
          mono: ['SF Mono', 'Monaco', 'Consolas', 'Liberation Mono', 'Courier New', 'monospace']
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
          normal: 1.6,    // 增加行高，减少视觉疲劳
          relaxed: 1.75
        }
      },
      spacing: {
        unit: 4,
        scale: {
          1: '4px',
          2: '8px',
          3: '12px',
          4: '16px',
          6: '24px',
          8: '32px',
          12: '48px',
          16: '64px',
          20: '80px',
          24: '96px'
        }
      },
      shadows: {
        sm: '0 1px 2px rgba(0, 0, 0, 0.05)',
        base: '0 2px 4px rgba(0, 0, 0, 0.08)',
        md: '0 4px 8px rgba(0, 0, 0, 0.1)',
        lg: '0 8px 16px rgba(0, 0, 0, 0.12)'
      },
      components: {
        button: {
          padding: { x: '16px', y: '10px' },
          borderRadius: '8px',      // 更大的圆角，更柔和
          fontWeight: 500,
          transition: 'all 0.2s ease-out'
        },
        card: {
          padding: { x: '24px', y: '24px' },
          borderRadius: '12px',     // 更大的圆角
          shadow: 'var(--shadows-sm)',
          background: '#ffffff',
          border: '1px solid var(--colors-border-light)'
        },
        input: {
          padding: { x: '16px', y: '12px' },
          borderRadius: '8px',      // 更大的圆角
          borderWidth: '1px',
          background: '#ffffff'
        }
      }
    },
    'dark': {
      colors: {
        background: {
          primary: '#2a2a2a',      // 深灰黑
          secondary: '#333333',    // 深灰色
          elevated: '#3d3d3d',     // 稍浅灰色
          overlay: 'rgba(0, 0, 0, 0.7)'
        },
        text: {
          primary: '#e8e8e8',      // 亮灰色
          secondary: '#b8b8b8',    // 中等灰色
          muted: '#888888',        // 暗灰色
          inverse: '#000000'
        },
        semantic: {
          success: '#7ba789',      // 柔和的绿色
          warning: '#e0b974',      // 柔和的黄色
          error: '#d47c70',        // 柔和的红色
          info: '#8bb4d8'          // 柔和的蓝色
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
      typography: {
        fontFamily: {
          sans: ['-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'Helvetica Neue', 'Arial', 'sans-serif'],
          mono: ['SF Mono', 'Monaco', 'Consolas', 'Liberation Mono', 'Courier New', 'monospace']
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
          normal: 1.6,
          relaxed: 1.75
        }
      },
      spacing: {
        unit: 4,
        scale: {
          1: '4px',
          2: '8px',
          3: '12px',
          4: '16px',
          6: '24px',
          8: '32px',
          12: '48px',
          16: '64px',
          20: '80px',
          24: '96px'
        }
      },
      shadows: {
        sm: '0 1px 2px rgba(0, 0, 0, 0.3)',
        base: '0 2px 4px rgba(0, 0, 0, 0.4)',
        md: '0 4px 8px rgba(0, 0, 0, 0.5)',
        lg: '0 8px 16px rgba(0, 0, 0, 0.6)'
      },
      components: {
        button: {
          padding: { x: '16px', y: '10px' },
          borderRadius: '8px',
          fontWeight: 500,
          transition: 'all 0.2s ease-out'
        },
        card: {
          padding: { x: '24px', y: '24px' },
          borderRadius: '12px',
          shadow: 'var(--shadows-base)',
          background: 'var(--colors-background-elevated)',
          border: '1px solid var(--colors-border-light)'
        },
        input: {
          padding: { x: '16px', y: '12px' },
          borderRadius: '8px',
          borderWidth: '1px',
          background: 'var(--colors-background-secondary)'
        }
      }
    }
  }
}

/**
 * 暗黑主题配置
 * 适合夜间使用，减少眼部疲劳
 */
export const darkTheme: SimpleThemeConfig = {
  id: 'dark',
  name: '暗黑模式',
  description: '适合夜间使用的深色主题，减少屏幕亮度刺激',
  modes: {
    'eye-care': {
      // 护眼模式下的护眼配置（很少使用，但保持一致性）
      colors: {
        background: {
          primary: '#fefcf3',
          secondary: '#f8f4e9',
          elevated: '#ffffff',
          overlay: 'rgba(0, 0, 0, 0.4)'
        },
        text: {
          primary: '#3a3a3a',
          secondary: '#5a5a5a',
          muted: '#8a8a8a',
          inverse: '#ffffff'
        },
        semantic: {
          success: '#5a8a69',
          warning: '#c89660',
          error: '#b86a5e',
          info: '#6a8caf'
        },
        border: {
          light: 'rgba(0, 0, 0, 0.08)',
          medium: 'rgba(0, 0, 0, 0.15)',
          strong: 'rgba(0, 0, 0, 0.25)'
        },
        accent: {
          primary: '#8b7355',
          secondary: '#a3907c'
        }
      },
      typography: {
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
          normal: 1.6,
          relaxed: 1.75
        }
      },
      spacing: {
        unit: 4,
        scale: {
          1: '4px',
          2: '8px',
          3: '12px',
          4: '16px',
          6: '24px',
          8: '32px',
          12: '48px',
          16: '64px',
          20: '80px',
          24: '96px'
        }
      },
      shadows: {
        sm: '0 1px 2px rgba(0, 0, 0, 0.05)',
        base: '0 2px 4px rgba(0, 0, 0, 0.08)',
        md: '0 4px 8px rgba(0, 0, 0, 0.1)',
        lg: '0 8px 16px rgba(0, 0, 0, 0.12)'
      },
      components: {
        button: {
          padding: { x: '16px', y: '10px' },
          borderRadius: '8px',
          fontWeight: 500,
          transition: 'all 0.2s ease-out'
        },
        card: {
          padding: { x: '24px', y: '24px' },
          borderRadius: '12px',
          shadow: 'var(--shadows-sm)',
          background: '#ffffff',
          border: '1px solid var(--colors-border-light)'
        },
        input: {
          padding: { x: '16px', y: '12px' },
          borderRadius: '8px',
          borderWidth: '1px',
          background: '#ffffff'
        }
      }
    },
    'dark': {
      // 暗黑模式下的暗黑配置（主要使用）
      colors: {
        background: {
          primary: '#0d0d0d',      // 纯黑
          secondary: '#1a1a1a',    // 近黑
          elevated: '#262626',     // 深灰
          overlay: 'rgba(0, 0, 0, 0.8)'
        },
        text: {
          primary: '#f0f0f0',      // 亮白
          secondary: '#c0c0c0',    // 亮灰
          muted: '#909090',        // 中灰
          inverse: '#000000'
        },
        semantic: {
          success: '#7ddc8c',      // 亮绿色
          warning: '#ffd966',      // 亮黄色
          error: '#ff8a7a',        // 亮红色
          info: '#7ec8e8'          // 亮蓝色
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
      typography: {
        fontFamily: {
          sans: ['-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'Helvetica Neue', 'Arial', 'sans-serif'],
          mono: ['SF Mono', 'Monaco', 'Consolas', 'Liberation Mono', 'Courier New', 'monospace']
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
          normal: 1.6,
          relaxed: 1.75
        }
      },
      spacing: {
        unit: 4,
        scale: {
          1: '4px',
          2: '8px',
          3: '12px',
          4: '16px',
          6: '24px',
          8: '32px',
          12: '48px',
          16: '64px',
          20: '80px',
          24: '96px'
        }
      },
      shadows: {
        sm: '0 1px 2px rgba(0, 0, 0, 0.5)',
        base: '0 2px 4px rgba(0, 0, 0, 0.6)',
        md: '0 4px 8px rgba(0, 0, 0, 0.7)',
        lg: '0 8px 16px rgba(0, 0, 0, 0.8)'
      },
      components: {
        button: {
          padding: { x: '16px', y: '10px' },
          borderRadius: '8px',
          fontWeight: 500,
          transition: 'all 0.2s ease-out'
        },
        card: {
          padding: { x: '24px', y: '24px' },
          borderRadius: '12px',
          shadow: 'var(--shadows-base)',
          background: 'var(--colors-background-elevated)',
          border: '1px solid var(--colors-border-light)'
        },
        input: {
          padding: { x: '16px', y: '12px' },
          borderRadius: '8px',
          borderWidth: '1px',
          background: 'var(--colors-background-secondary)'
        }
      }
    }
  }
}

/**
 * 主题配置映射
 */
export const themeConfigs: Record<string, SimpleThemeConfig> = {
  'eye-care': eyeCareTheme,
  'dark': darkTheme
}

/**
 * 获取主题配置
 */
export function getThemeConfig(id: string): SimpleThemeConfig {
  return themeConfigs[id] || eyeCareTheme
}

/**
 * 获取所有可用主题
 */
export function getAvailableThemes(): SimpleThemeConfig[] {
  return Object.values(themeConfigs)
}