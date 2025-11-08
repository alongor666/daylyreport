import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'
import { useAppStore } from './app'
import { useFilterStore } from './filter'

/**
 * 数据状态管理
 * 管理KPI数据和图表数据的获取、缓存和刷新
 */
export const useDataStore = defineStore('data', () => {
  // ========== State ==========

  // KPI数据 (三口径: 当日/近7天/近30天)
  const kpiData = ref(null)

  // 图表数据 (周对比图表)
  const chartData = ref(null)

  // 数据加载状态
  const loading = ref(false)

  // 图表加载状态
  const chartLoading = ref(false)

  // 最后更新时间
  const lastUpdated = ref(null)

  // ========== Getters ==========

  /**
   * 是否有KPI数据
   */
  const hasKpiData = computed(() => {
    return kpiData.value !== null
  })

  /**
   * 是否有图表数据
   */
  const hasChartData = computed(() => {
    return chartData.value !== null
  })

  /**
   * 获取当日KPI数据
   */
  const todayKpi = computed(() => {
    if (!kpiData.value) return null

    return {
      premium: kpiData.value.premium?.day || 0,
      policyCount: kpiData.value.policy_count?.day || 0,
      commission: kpiData.value.commission?.day || 0,
      targetGap: kpiData.value.target_gap_day || 0
    }
  })

  /**
   * 获取近7天KPI数据
   */
  const last7dKpi = computed(() => {
    if (!kpiData.value) return null

    return {
      premium: kpiData.value.premium?.last7d || 0,
      policyCount: kpiData.value.policy_count?.last7d || 0,
      commission: kpiData.value.commission?.last7d || 0
    }
  })

  /**
   * 获取近30天KPI数据
   */
  const last30dKpi = computed(() => {
    if (!kpiData.value) return null

    return {
      premium: kpiData.value.premium?.last30d || 0,
      policyCount: kpiData.value.policy_count?.last30d || 0,
      commission: kpiData.value.commission?.last30d || 0
    }
  })

  /**
   * 锚定日期 (KPI数据对应的日期)
   */
  const anchorDate = computed(() => {
    return kpiData.value?.anchor_date || null
  })

  // ========== Actions ==========

  /**
   * 获取KPI数据
   * @param {string} date - 查询日期 (YYYY-MM-DD), 可选
   */
  async function fetchKpiData(date = null) {
    const appStore = useAppStore()

    loading.value = true
    try {
      const params = date ? { date } : {}
      const response = await axios.get('/api/kpi-windows', { params })

      if (response.data.success) {
        kpiData.value = response.data.data
        lastUpdated.value = new Date().toISOString()

        // 更新appStore中的最新日期
        if (response.data.data.anchor_date) {
          appStore.setLatestDate(response.data.data.anchor_date)
        }

        return kpiData.value
      } else {
        throw new Error(response.data.message || 'Failed to fetch KPI data')
      }
    } catch (error) {
      console.error('Failed to fetch KPI data:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  /**
   * 获取图表数据
   * @param {string} metric - 指标类型 (premium | count)
   * @param {object} filters - 筛选条件
   * @param {string} date - 查询日期, 可选
   */
  async function fetchChartData(metric = 'premium', filters = {}, date = null) {
    chartLoading.value = true
    try {
      const payload = {
        metric,
        filters,
        ...(date && { date })
      }

      const response = await axios.post('/api/week-comparison', payload)

      if (response.data.success) {
        chartData.value = response.data.data
        return chartData.value
      } else {
        throw new Error(response.data.message || 'Failed to fetch chart data')
      }
    } catch (error) {
      console.error('Failed to fetch chart data:', error)
      throw error
    } finally {
      chartLoading.value = false
    }
  }

  /**
   * 刷新所有数据
   * @param {string} date - 查询日期, 可选
   */
  async function refreshAllData(date = null) {
    const appStore = useAppStore()
    const filterStore = useFilterStore()

    appStore.setLoading(true)

    try {
      // 并行获取KPI数据和图表数据
      await Promise.all([
        fetchKpiData(date),
        fetchChartData(
          appStore.currentMetric,
          filterStore.getActiveFilters(),
          date
        )
      ])
    } catch (error) {
      console.error('Failed to refresh data:', error)
      throw error
    } finally {
      appStore.setLoading(false)
    }
  }

  /**
   * 刷新图表数据 (根据当前筛选条件和指标)
   */
  async function refreshChartData() {
    const appStore = useAppStore()
    const filterStore = useFilterStore()

    await fetchChartData(
      appStore.currentMetric,
      filterStore.getActiveFilters(),
      appStore.selectedDate
    )
  }

  /**
   * 处理后端数据刷新
   */
  async function triggerDataRefresh() {
    try {
      const response = await axios.post('/api/refresh')

      if (response.data.success) {
        // 刷新成功后,重新获取所有数据
        await refreshAllData()
        return response.data
      } else {
        throw new Error(response.data.message || 'Failed to refresh data')
      }
    } catch (error) {
      console.error('Failed to trigger data refresh:', error)
      throw error
    }
  }

  /**
   * 清空所有数据
   */
  function clearData() {
    kpiData.value = null
    chartData.value = null
    lastUpdated.value = null
  }

  /**
   * 重置所有状态
   */
  function reset() {
    clearData()
    loading.value = false
    chartLoading.value = false
  }

  // ========== Return ==========

  return {
    // State
    kpiData,
    chartData,
    loading,
    chartLoading,
    lastUpdated,

    // Getters
    hasKpiData,
    hasChartData,
    todayKpi,
    last7dKpi,
    last30dKpi,
    anchorDate,

    // Actions
    fetchKpiData,
    fetchChartData,
    refreshAllData,
    refreshChartData,
    triggerDataRefresh,
    clearData,
    reset
  }
})
