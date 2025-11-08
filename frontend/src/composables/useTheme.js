import { computed } from 'vue'

/**
 * 主题适配层 (临时实现)
 *
 * Phase 1: 使用CSS Variables (当前)
 * Phase 2: 接入ThemeEngine (未来)
 *
 * 优势: 组件只依赖此接口,未来切换主题系统时无需修改组件代码
 */

/**
 * 获取组件主题配置
 * @param {string} componentName - 组件名称 (header/kpiCard/chart等)
 * @returns {object} 主题配置对象
 */
export function useTheme(componentName) {
  // TODO: Phase 2 - 接入ThemeEngine
  // const themeSystem = inject('themeSystem')
  // return useComponentTheme(componentName, themeSystem.tokens)

  // Phase 1: 临时使用CSS Variables
  return {
    // 组件类名
    className: computed(() => `theme-${componentName}`),

    // 颜色系统
    colors: computed(() => ({
      primary: 'var(--primary-500)',
      primaryHover: 'var(--primary-600)',
      success: 'var(--success-500)',
      warning: 'var(--warning-500)',
      error: 'var(--error-500)',

      textPrimary: 'var(--text-primary)',
      textSecondary: 'var(--text-secondary)',
      textMuted: 'var(--text-muted)',

      bgDefault: 'var(--surface-default)',
      bgElevated: 'var(--surface-elevated)',
      bgTint: 'var(--surface-primary-tint)',

      border: 'var(--gray-300)',
      shadow: 'var(--shadow-md)'
    })),

    // 间距系统
    spacing: computed(() => ({
      xs: 'var(--space-1)',
      sm: 'var(--space-2)',
      md: 'var(--space-3)',
      lg: 'var(--space-4)',
      xl: 'var(--space-6)',
      xxl: 'var(--space-8)'
    })),

    // 字体系统
    typography: computed(() => ({
      xs: 'var(--text-xs)',
      sm: 'var(--text-sm)',
      base: 'var(--text-base)',
      lg: 'var(--text-lg)',
      xl: 'var(--text-xl)',
      '2xl': 'var(--text-2xl)',
      '3xl': 'var(--text-3xl)',
      fontFamily: 'var(--font-family-base)'
    })),

    // 圆角系统
    radius: computed(() => ({
      sm: 'var(--radius-sm)',
      md: 'var(--radius-md)',
      lg: 'var(--radius-lg)'
    })),

    // 阴影系统
    shadows: computed(() => ({
      soft: 'var(--shadow-soft)',
      md: 'var(--shadow-md)'
    })),

    // 专业商务风格特定配置
    business: computed(() => ({
      // macOS风格的卡片效果
      cardBg: 'rgba(255, 255, 255, 0.95)',
      cardBorder: '1px solid rgba(0, 0, 0, 0.08)',
      cardShadow: '0 2px 12px rgba(0, 0, 0, 0.06)',

      // 专业的渐变
      gradientPrimary: 'linear-gradient(135deg, var(--primary-500), var(--primary-600))',
      gradientSuccess: 'linear-gradient(135deg, #10b981, #059669)',
      gradientError: 'linear-gradient(135deg, #ef4444, #dc2626)',

      // 细腻的分隔线
      divider: '1px solid rgba(0, 0, 0, 0.06)',

      // 悬停效果
      hoverBg: 'rgba(168, 85, 247, 0.04)',
      activeBg: 'rgba(168, 85, 247, 0.08)'
    }))
  }
}

/**
 * 获取ECharts主题配置
 * 用于统一图表样式
 */
export function useEChartsTheme() {
  return {
    // 调色板
    color: [
      '#a855f7', // primary-500
      '#9333ea', // primary-600
      '#10b981', // success-500
      '#f59e0b', // warning-500
      '#ef4444', // error-500
      '#6366f1', // indigo-500
      '#ec4899'  // pink-500
    ],

    // 背景色
    backgroundColor: 'transparent',

    // 文本样式
    textStyle: {
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", sans-serif',
      fontSize: 12,
      color: '#111827' // text-primary
    },

    // 标题
    title: {
      textStyle: {
        color: '#111827',
        fontWeight: 600
      },
      subtextStyle: {
        color: '#6b7280' // text-secondary
      }
    },

    // 图例
    legend: {
      textStyle: {
        color: '#6b7280'
      }
    },

    // 提示框
    tooltip: {
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: 'rgba(0, 0, 0, 0.1)',
      borderWidth: 1,
      textStyle: {
        color: '#111827'
      },
      extraCssText: 'box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); border-radius: 8px;'
    },

    // 坐标轴
    categoryAxis: {
      axisLine: {
        lineStyle: {
          color: 'rgba(0, 0, 0, 0.1)'
        }
      },
      axisTick: {
        lineStyle: {
          color: 'rgba(0, 0, 0, 0.1)'
        }
      },
      axisLabel: {
        color: '#6b7280'
      },
      splitLine: {
        lineStyle: {
          color: 'rgba(0, 0, 0, 0.06)'
        }
      }
    },

    valueAxis: {
      axisLine: {
        lineStyle: {
          color: 'rgba(0, 0, 0, 0.1)'
        }
      },
      axisTick: {
        lineStyle: {
          color: 'rgba(0, 0, 0, 0.1)'
        }
      },
      axisLabel: {
        color: '#6b7280'
      },
      splitLine: {
        lineStyle: {
          color: 'rgba(0, 0, 0, 0.06)'
        }
      }
    },

    // 线条样式
    line: {
      smooth: true,
      symbolSize: 6,
      lineStyle: {
        width: 2
      }
    },

    // 柱状图
    bar: {
      barMaxWidth: 40
    }
  }
}
