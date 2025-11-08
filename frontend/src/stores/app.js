import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

/**
 * 应用全局状态管理
 * 管理全局的加载状态、日期选择、当前指标等
 */
export const useAppStore = defineStore('app', () => {
  // ========== State ==========

  // 全局加载状态
  const loading = ref(false)

  // 最新数据日期 (从后端获取)
  const latestDate = ref(null)

  // 用户选择的日期 (用于查询特定日期数据)
  const selectedDate = ref(null)

  // 当前查看的指标 (premium: 保费, count: 单量)
  const currentMetric = ref('premium')

  // 应用初始化状态
  const initialized = ref(false)

  // ========== Getters ==========

  /**
   * 用于显示的日期 (优先使用选择的日期,否则使用最新日期)
   */
  const displayDate = computed(() => {
    return selectedDate.value || latestDate.value || '未知'
  })

  /**
   * 格式化的显示日期 (YYYY-MM-DD → YYYY年MM月DD日)
   */
  const formattedDisplayDate = computed(() => {
    const date = displayDate.value
    if (!date || date === '未知') return date

    try {
      const [year, month, day] = date.split('-')
      return `${year}年${month}月${day}日`
    } catch (e) {
      return date
    }
  })

  /**
   * 当前指标的中文名称
   */
  const currentMetricLabel = computed(() => {
    return currentMetric.value === 'premium' ? '签单保费' : '签单单量'
  })

  /**
   * 是否正在加载
   */
  const isLoading = computed(() => loading.value)

  // ========== Actions ==========

  /**
   * 设置加载状态
   * @param {boolean} value - 加载状态
   */
  function setLoading(value) {
    loading.value = value
  }

  /**
   * 设置最新数据日期
   * @param {string} date - 日期字符串 (YYYY-MM-DD)
   */
  function setLatestDate(date) {
    latestDate.value = date
    // 如果没有选择日期,默认使用最新日期
    if (!selectedDate.value) {
      selectedDate.value = date
    }
  }

  /**
   * 设置用户选择的日期
   * @param {string} date - 日期字符串 (YYYY-MM-DD)
   */
  function setSelectedDate(date) {
    selectedDate.value = date
  }

  /**
   * 重置选择的日期(恢复到最新日期)
   */
  function resetSelectedDate() {
    selectedDate.value = latestDate.value
  }

  /**
   * 切换当前指标
   * @param {string} metric - 指标类型 (premium | count)
   */
  function switchMetric(metric) {
    if (['premium', 'count'].includes(metric)) {
      currentMetric.value = metric
    } else {
      console.warn(`Invalid metric: ${metric}. Use 'premium' or 'count'.`)
    }
  }

  /**
   * 标记应用已初始化
   */
  function markInitialized() {
    initialized.value = true
  }

  /**
   * 重置所有状态
   */
  function reset() {
    loading.value = false
    latestDate.value = null
    selectedDate.value = null
    currentMetric.value = 'premium'
    initialized.value = false
  }

  // ========== Return ==========

  return {
    // State
    loading,
    latestDate,
    selectedDate,
    currentMetric,
    initialized,

    // Getters
    displayDate,
    formattedDisplayDate,
    currentMetricLabel,
    isLoading,

    // Actions
    setLoading,
    setLatestDate,
    setSelectedDate,
    resetSelectedDate,
    switchMetric,
    markInitialized,
    reset
  }
})
