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

  // 验证信息（未匹配业务员等）
  const validationInfo = ref(null)

  // 最后更新时间
  const lastUpdated = ref(null)

  // 饼图数据 (险别组合占比)
  const insuranceTypeData = ref(null)

  // 饼图数据 (业务员保费区间占比)
  const premiumRangeData = ref(null)

  // 饼图数据 (新转续占比)
  const renewalTypeData = ref(null)

  // 饼图加载状态
  const pieChartsLoading = ref(false)

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
   * @param {object} filters - 筛选条件, 可选
   */
  async function fetchKpiData(date = null, filters = {}) {
    const appStore = useAppStore()
    const filterStore = useFilterStore()

    loading.value = true
    try {
      // 将 payload 提升到函数作用域，确保 catch 可访问，避免 ReferenceError
      let payload = {
        ...(date && { date }),
        ...(filters && { filters }),
        data_scope: filterStore.getDataScope()
      }
      const response = await axios.post('/api/kpi-windows', payload)

      if (response.data.success) {
        kpiData.value = response.data.data
        lastUpdated.value = new Date().toISOString()

        // 更新appStore中的最新日期
        if (response.data.data.anchor_date) {
          appStore.setLatestDate(response.data.data.anchor_date)
        }

        // 保存验证信息
        if (response.data.data.validation) {
          validationInfo.value = response.data.data.validation
        }

        return kpiData.value
      } else {
        throw new Error(response.data.message || 'Failed to fetch KPI data')
      }
    } catch (error) {
      // 函数级中文注释：
      // KPI数据请求失败时输出详细错误信息，包含状态码与响应体，便于快速定位问题。
      // 同时打印请求载荷(payload)以确认筛选条件类型是否正确。
      const status = error?.response?.status
      const data = error?.response?.data
      console.error('Failed to fetch KPI data:', error)
      console.error('KPI request status:', status, 'response:', data)
      // 注意：payload 在 try 中定义会造成作用域问题，此处已提升作用域
      console.debug('KPI payload:', { ...(date && { date }), ...(filters && { filters }), data_scope: filterStore.getDataScope() })
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
    const filterStore = useFilterStore()
    try {
      // 将 payload 提升到函数作用域，确保 catch 可访问，避免 ReferenceError
      let payload = {
        metric,
        filters,
        ...(date && { date }),
        data_scope: filterStore.getDataScope()
      }

      const response = await axios.post('/api/week-comparison', payload)

      if (response.data.success) {
        chartData.value = response.data.data
        
        // 保存验证信息
        if (response.data.data.validation) {
          validationInfo.value = response.data.data.validation
        }
        
        return chartData.value
      } else {
        throw new Error(response.data.message || 'Failed to fetch chart data')
      }
    } catch (error) {
      // 函数级中文注释：
      // 图表数据请求失败时输出详细错误信息，包含状态码与响应体。
      // 若 filters 非字典或 metric 非法，后端会返回 400；日志将协助定位。
      const status = error?.response?.status
      const data = error?.response?.data
      console.error('Failed to fetch chart data:', error)
      console.error('Chart request status:', status, 'response:', data)
      // 注意：payload 在 try 中定义会造成作用域问题，此处已提升作用域
      console.debug('Chart payload:', { metric, filters, ...(date && { date }), data_scope: filterStore.getDataScope() })
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
      const filters = filterStore.getActiveFilters()
      // 并行获取KPI数据和图表数据，都应用筛选条件
      await Promise.all([
        fetchKpiData(date, filters),
        fetchChartData(
          appStore.currentMetric,
          filters,
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

    const filters = filterStore.getActiveFilters()
    
    // 同时刷新图表和KPI数据
    await Promise.all([
      fetchKpiData(appStore.selectedDate, filters),
      fetchChartData(
        appStore.currentMetric,
        filters,
        appStore.selectedDate
      )
    ])
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
    validationInfo.value = null
  }

  /**
   * 重置所有状态
   */
  function reset() {
    clearData()
    loading.value = false
    chartLoading.value = false
    pieChartsLoading.value = false
  }

  /**
   * 获取险别组合占比数据
   * @param {string} period - 时间段 (day | last7d | last30d)
   * @param {object} filters - 筛选条件
   * @param {string} date - 查询日期, 可选
   */
  async function fetchInsuranceTypeData(period = 'day', filters = {}, date = null) {
    const filterStore = useFilterStore()
    try {
      const payload = {
        period,
        filters,
        ...(date && { date }),
        data_scope: filterStore.getDataScope()
      }

      const response = await axios.post('/api/insurance-type-distribution', payload)

      if (response.data.success) {
        insuranceTypeData.value = response.data.data
        return insuranceTypeData.value
      } else {
        throw new Error(response.data.message || 'Failed to fetch insurance type distribution')
      }
    } catch (error) {
      console.error('Failed to fetch insurance type distribution:', error)
      const status = error?.response?.status
      const data = error?.response?.data
      console.error('Insurance type request status:', status, 'response:', data)
      throw error
    }
  }

  /**
   * 获取业务员保费区间占比数据
   * @param {string} period - 时间段 (day | last7d | last30d)
   * @param {object} filters - 筛选条件
   * @param {string} date - 查询日期, 可选
   */
  async function fetchPremiumRangeData(period = 'day', filters = {}, date = null) {
    const filterStore = useFilterStore()
    try {
      const payload = {
        period,
        filters,
        ...(date && { date }),
        data_scope: filterStore.getDataScope()
      }

      const response = await axios.post('/api/premium-range-distribution', payload)

      if (response.data.success) {
        premiumRangeData.value = response.data.data
        return premiumRangeData.value
      } else {
        throw new Error(response.data.message || 'Failed to fetch premium range distribution')
      }
    } catch (error) {
      console.error('Failed to fetch premium range distribution:', error)
      const status = error?.response?.status
      const data = error?.response?.data
      console.error('Premium range request status:', status, 'response:', data)
      throw error
    }
  }

  /**
   * 获取新转续占比数据
   * @param {string} period - 时间段 (day | last7d | last30d)
   * @param {object} filters - 筛选条件
   * @param {string} date - 查询日期, 可选
   */
  async function fetchRenewalTypeData(period = 'day', filters = {}, date = null) {
    const filterStore = useFilterStore()
    try {
      const payload = {
        period,
        filters,
        ...(date && { date }),
        data_scope: filterStore.getDataScope()
      }

      const response = await axios.post('/api/renewal-type-distribution', payload)

      if (response.data.success) {
        renewalTypeData.value = response.data.data
        return renewalTypeData.value
      } else {
        throw new Error(response.data.message || 'Failed to fetch renewal type distribution')
      }
    } catch (error) {
      console.error('Failed to fetch renewal type distribution:', error)
      const status = error?.response?.status
      const data = error?.response?.data
      console.error('Renewal type request status:', status, 'response:', data)
      throw error
    }
  }

  /**
   * 刷新所有饼图数据
   * @param {string} period - 时间段 (day | last7d | last30d)
   * @param {object} filters - 筛选条件
   * @param {string} date - 查询日期, 可选
   */
  async function refreshPieCharts(period = 'day', filters = {}, date = null) {
    pieChartsLoading.value = true
    try {
      // 并行获取3个饼图数据
      await Promise.all([
        fetchInsuranceTypeData(period, filters, date),
        fetchPremiumRangeData(period, filters, date),
        fetchRenewalTypeData(period, filters, date)
      ])
    } catch (error) {
      console.error('Failed to refresh pie charts:', error)
      throw error
    } finally {
      pieChartsLoading.value = false
    }
  }

  // ========== Return ==========

  return {
    // State
    kpiData,
    chartData,
    loading,
    chartLoading,
    lastUpdated,
    validationInfo,
    insuranceTypeData,
    premiumRangeData,
    renewalTypeData,
    pieChartsLoading,

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
    reset,
    fetchInsuranceTypeData,
    fetchPremiumRangeData,
    fetchRenewalTypeData,
    refreshPieCharts
  }
})
