# Vue 组件开发 - 完整 API 参考文档

本文档提供项目中所有核心 API、高级用法和完整配置选项。仅在需要详细信息时参考。

---

## 📦 完整 CSS 变量清单

### 图表专用颜色
```css
/* 图表主色 - Chart Primary Colors (护眼蓝灰系) */
--chart-primary-blue: #5B8DEF;    /* D (最新周期) - 主蓝色 */
--chart-secondary-gray: #8B95A5;  /* D-7 (上周) - 次灰色 */
--chart-light-gray: #C5CAD3;      /* D-14 (前周) - 浅灰色 */
```

### 状态色
```css
/* 状态色 - Status Colors (克制的功能色) */
--status-success: #52C41A;        /* 上升 ↑ - 成功绿 */
--status-warning: #F5222D;        /* 下降 ↓ - 警示红 */
--status-neutral: #8B95A5;        /* 持平 — - 中性灰 */
```

### 主色板
```css
/* 主色 - Primary Palette */
--primary-50: #f3e8ff;
--primary-100: #e9d5ff;
--primary-500: #a855f7;
--primary-600: #9333ea;
--primary-700: #7e22ce;
```

### 功能色
```css
/* 功能色 - Semantic Colors */
--success-500: var(--status-success);
--warning-500: #f59e0b;
--error-500: var(--status-warning);
```

### 中性色
```css
/* 中性色 - Neutral Colors */
--gray-50: #f9fafb;
--gray-100: #f3f4f6;
--gray-300: #d1d5db;
--gray-500: #6b7280;
--gray-700: #374151;
--gray-900: #111827;
--text-primary: var(--gray-900);
--text-secondary: var(--gray-500);
--text-muted: rgba(17, 24, 39, 0.7);
```

### 表面与阴影
```css
/* 表面与阴影 - Surface & Shadows */
--surface-default: #ffffff;
--surface-elevated: #ffffff;
--surface-primary-tint: rgba(168, 85, 247, 0.08);
--shadow-soft: 0 10px 30px rgba(15, 23, 42, 0.08);
--shadow-md: 0 10px 30px rgba(15, 23, 42, 0.08);
```

### 间距系统
```css
/* 间距 - Spacing */
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px */
--space-5: 1.25rem;   /* 20px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
```

### 圆角
```css
/* 圆角 - Border Radius */
--radius-sm: 0.5rem;
--radius-md: 0.75rem;
--radius-lg: 1rem;
```

### 边框
```css
/* 边框 - Borders */
--border-accent-width: 0.25rem;
```

### 字体
```css
/* 字体 - Typography */
--text-xs: 0.75rem;   /* 12px */
--text-sm: 0.875rem;  /* 14px */
--text-base: 1rem;    /* 16px */
--text-lg: 1.125rem;  /* 18px */
--text-xl: 1.25rem;   /* 20px */
--text-2xl: 1.5rem;   /* 24px */
--text-3xl: 1.875rem; /* 30px */
--font-family-base: 'Inter', 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
```

---

## 🧩 Pinia Store 完整 API

### appStore 完整 API

```typescript
interface AppStore {
  // ===== State =====
  loading: Ref<boolean>                 // 全局 loading 状态
  latestDate: Ref<string | null>        // 数据中的最新日期
  selectedDate: Ref<string | null>      // 用户选择的日期
  currentMetric: Ref<'premium' | 'count'> // 当前指标（保费/件数）

  // ===== Getters =====
  isLoading: ComputedRef<boolean>       // loading 状态的计算属性
  displayDate: ComputedRef<string>      // 显示日期（优先 selectedDate，否则 latestDate）

  // ===== Actions =====
  setLoading(value: boolean): void      // 设置 loading 状态
  setLatestDate(date: string): void     // 设置最新日期（同时设置 selectedDate）
  setSelectedDate(date: string): void   // 设置用户选择的日期
  switchMetric(metric: 'premium' | 'count'): void  // 切换指标
}
```

**使用示例**：
```javascript
import { useAppStore } from '@/stores/app'

const appStore = useAppStore()

// 设置 loading
appStore.setLoading(true)

// 切换指标
appStore.switchMetric('count')

// 获取当前指标
const metric = appStore.currentMetric // 'premium' | 'count'
```

---

### filterStore 完整 API

```typescript
interface FilterOptions {
  '三级机构': string[]
  '团队': string[]
  '是否续保': string[]
  '是否新能源': string[]
  '是否过户车': string[]
  '险种大类': string[]
  '吨位': string[]
  'is_dianxiao': string[]
  '机构团队映射': Record<string, string[]>
  '保单号': string[]
}

interface ActiveFilters {
  [key: string]: string
}

interface FilterStore {
  // ===== State =====
  filterOptions: Ref<FilterOptions>     // 所有筛选器的可选值
  activeFilters: Ref<ActiveFilters>     // 当前已选的筛选条件
  filterPanelOpen: Ref<boolean>         // 筛选面板是否展开

  // ===== Actions =====
  fetchFilterOptions(): Promise<void>   // 从 API 获取筛选器选项
  applyFilter(key: string, value: string): void  // 应用单个筛选条件
  clearFilters(): void                  // 清除所有筛选条件
  togglePanel(): void                   // 切换筛选面板展开/收起
  removeFilter(key: string): void       // 移除单个筛选条件
}
```

**使用示例**：
```javascript
import { useFilterStore } from '@/stores/filter'

const filterStore = useFilterStore()

// 加载筛选器选项
await filterStore.fetchFilterOptions()

// 应用筛选条件
filterStore.applyFilter('三级机构', '成都')
filterStore.applyFilter('是否新能源', '是')

// 清除所有筛选
filterStore.clearFilters()

// 获取当前筛选条件
const filters = filterStore.activeFilters
// { '三级机构': '成都', '是否新能源': '是' }
```

---

### dataStore 完整 API

```typescript
interface KpiData {
  anchor_date: string
  premium: {
    day: number
    last7d: number
    last30d: number
  }
  policy_count: {
    day: number
    last7d: number
    last30d: number
  }
  commission: {
    day: number
    last7d: number
    last30d: number
  }
  target_gap_day: number
  validation: {
    unmatched_staff: string[]
    unmatched_count: number
    policy_consistency: {
      mismatch_policies: string[]
      mismatch_count: number
    }
  }
}

interface ChartSeries {
  name: string          // 'D-14 (10-22): 781万'
  data: number[]        // [120, 200, 150, ...]
  dates: string[]       // ['2025-10-22', '2025-10-23', ...]
  code: string          // 'D-14'
  total_value: number   // 7814320.5
  period_index: number  // 0 | 1 | 2
}

interface ChartData {
  latest_date: string
  x_axis: string[]      // ['周一', '周二', ...]
  series: ChartSeries[]
  validation: {
    unmatched_staff: string[]
    unmatched_count: number
  }
}

interface DataStore {
  // ===== State =====
  kpiData: Ref<KpiData | null>
  chartData: Ref<ChartData | null>

  // ===== Actions =====
  fetchKpiData(): Promise<void>         // 获取 KPI 数据
  fetchChartData(): Promise<void>       // 获取图表数据
  fetchDashboardData(): Promise<void>   // 同时获取 KPI 和图表数据
  refreshData(): Promise<void>          // 刷新数据（调用 /api/refresh）
}
```

**使用示例**：
```javascript
import { useDataStore } from '@/stores/data'
import { computed } from 'vue'

const dataStore = useDataStore()

// 获取数据
await dataStore.fetchDashboardData()

// 在组件中使用（必须用 computed 包装）
const kpiData = computed(() => dataStore.kpiData)
const chartData = computed(() => dataStore.chartData)

// 访问具体数据
const dayPremium = computed(() => dataStore.kpiData?.premium.day || 0)
```

---

## 📊 ECharts 完整配置选项

### 标准柱状图配置

```javascript
const barChartOption = {
  // 颜色（必须使用护眼配色）
  color: ['#5B8DEF', '#8B95A5', '#C5CAD3'],

  // 提示框
  tooltip: {
    trigger: 'axis',                    // 'item' | 'axis' | 'none'
    axisPointer: {
      type: 'shadow'                    // 'line' | 'shadow' | 'cross'
    },
    backgroundColor: 'rgba(255, 255, 255, 0.95)',
    borderColor: '#E5E7EB',
    borderWidth: 1,
    padding: [8, 12],
    textStyle: {
      color: '#374151',
      fontSize: 14,
      fontFamily: 'Inter, sans-serif'
    },
    formatter: (params) => {
      // 自定义提示框内容
      let result = `<div style="font-weight: 600; margin-bottom: 4px;">${params[0].axisValue}</div>`
      params.forEach(item => {
        const value = metric === 'count'
          ? `${item.value}件`
          : `${(item.value / 10000).toFixed(1)}万`
        result += `
          <div style="display: flex; align-items: center; margin-top: 4px;">
            <span style="display: inline-block; width: 10px; height: 10px; border-radius: 50%; background: ${item.color}; margin-right: 8px;"></span>
            <span style="flex: 1;">${item.seriesName}:</span>
            <span style="font-weight: 600; margin-left: 12px;">${value}</span>
          </div>
        `
      })
      return result
    }
  },

  // 图例
  legend: {
    show: true,
    bottom: 0,                          // 位置：top | bottom | left | right | 数值
    left: 'center',
    itemWidth: 16,
    itemHeight: 10,
    itemGap: 16,
    textStyle: {
      fontSize: 14,
      color: '#374151',
      fontFamily: 'Inter, sans-serif'
    },
    icon: 'rect'                        // 'circle' | 'rect' | 'roundRect' | 'triangle'
  },

  // 网格
  grid: {
    left: '3%',                         // 距容器左侧距离
    right: '4%',                        // 距容器右侧距离
    bottom: '12%',                      // 距容器底部距离
    top: '10%',                         // 距容器顶部距离
    containLabel: true                  // grid 区域是否包含坐标轴的刻度标签
  },

  // X 轴
  xAxis: {
    type: 'category',                   // 'value' | 'category' | 'time' | 'log'
    data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
    boundaryGap: true,                  // true=柱状图 | false=折线图
    axisLine: {
      show: true,
      lineStyle: {
        color: '#E5E7EB',
        width: 1
      }
    },
    axisTick: {
      show: true,
      lineStyle: {
        color: '#E5E7EB'
      }
    },
    axisLabel: {
      color: '#6B7280',
      fontSize: 12,
      fontFamily: 'Inter, sans-serif',
      margin: 8,
      rotate: 0                         // 标签旋转角度
    }
  },

  // Y 轴
  yAxis: {
    type: 'value',
    axisLine: {
      show: false
    },
    axisTick: {
      show: false
    },
    axisLabel: {
      color: '#6B7280',
      fontSize: 12,
      fontFamily: 'Inter, sans-serif',
      formatter: (value) => {
        if (metric === 'count') {
          return value
        }
        return (value / 10000).toFixed(0) + '万'
      }
    },
    splitLine: {
      lineStyle: {
        color: '#F3F4F6',
        type: 'dashed'                  // 'solid' | 'dashed' | 'dotted'
      }
    }
  },

  // 数据系列
  series: [
    {
      name: 'D-14 (10-22): 781万',
      type: 'bar',                      // 'bar' | 'line' | 'pie' | 'scatter'
      data: [120, 200, 150, 80, 70, 110, 130],
      barWidth: '40%',                  // 柱宽度（百分比或数值）
      barGap: '30%',                    // 柱间距
      barCategoryGap: '20%',            // 类目间距
      itemStyle: {
        borderRadius: [4, 4, 0, 0],     // 圆角 [左上, 右上, 右下, 左下]
        color: '#5B8DEF'                // 可以是颜色值或渐变对象
      },
      emphasis: {                       // 高亮状态
        itemStyle: {
          color: '#4A7DD8'
        }
      },
      label: {                          // 数据标签
        show: false,                    // 是否显示
        position: 'top',                // 'top' | 'inside' | 'bottom'
        formatter: '{c}'
      }
    }
  ],

  // 动画
  animation: true,
  animationDuration: 800,
  animationEasing: 'cubicOut',          // 'linear' | 'cubicIn' | 'cubicOut' | 'cubicInOut'
  animationDelay: 0
}
```

---

### 标准折线图配置

```javascript
const lineChartOption = {
  color: ['#5B8DEF', '#8B95A5', '#C5CAD3'],

  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'line',                     // 折线图用 'line'
      lineStyle: {
        color: '#5B8DEF',
        type: 'dashed'
      }
    }
  },

  legend: {
    bottom: 0,
    left: 'center'
  },

  grid: {
    left: '3%',
    right: '4%',
    bottom: '12%',
    top: '10%',
    containLabel: true
  },

  xAxis: {
    type: 'category',
    data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
    boundaryGap: false,                 // 折线图设为 false
    axisLine: { lineStyle: { color: '#E5E7EB' } },
    axisTick: { show: false },
    axisLabel: { color: '#6B7280', fontSize: 12 }
  },

  yAxis: {
    type: 'value',
    axisLine: { show: false },
    axisTick: { show: false },
    axisLabel: { color: '#6B7280', fontSize: 12 },
    splitLine: { lineStyle: { color: '#F3F4F6', type: 'dashed' } }
  },

  series: [
    {
      name: 'D-14',
      type: 'line',
      data: [120, 200, 150, 80, 70, 110, 130],
      smooth: true,                     // 平滑曲线
      symbol: 'circle',                 // 'circle' | 'rect' | 'roundRect' | 'triangle' | 'diamond' | 'none'
      symbolSize: 6,                    // 标记点大小
      lineStyle: {
        width: 2,
        color: '#5B8DEF'
      },
      itemStyle: {
        color: '#5B8DEF',
        borderColor: '#fff',
        borderWidth: 2
      },
      areaStyle: {                      // 区域填充
        color: {
          type: 'linear',
          x: 0,
          y: 0,
          x2: 0,
          y2: 1,
          colorStops: [
            { offset: 0, color: 'rgba(91, 141, 239, 0.3)' },
            { offset: 1, color: 'rgba(91, 141, 239, 0)' }
          ]
        }
      }
    }
  ]
}
```

---

### Sparkline 迷你图配置

```javascript
const sparklineOption = {
  grid: {
    top: 5,
    right: 5,
    bottom: 5,
    left: 5
  },
  xAxis: {
    type: 'category',
    show: false,
    data: [0, 1, 2, 3, 4, 5, 6]
  },
  yAxis: {
    type: 'value',
    show: false
  },
  series: [
    {
      type: 'line',
      data: [120, 200, 150, 80, 70, 110, 130],
      smooth: true,
      symbol: 'none',                   // 不显示标记点
      lineStyle: {
        width: 2,
        color: {
          type: 'linear',
          x: 0,
          y: 0,
          x2: 1,
          y2: 0,
          colorStops: [
            { offset: 0, color: '#a855f7' },
            { offset: 1, color: '#9333ea' }
          ]
        }
      },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0,
          y: 0,
          x2: 0,
          y2: 1,
          colorStops: [
            { offset: 0, color: 'rgba(168, 85, 247, 0.2)' },
            { offset: 1, color: 'rgba(168, 85, 247, 0)' }
          ]
        }
      }
    }
  ],
  animation: true,
  animationDuration: 800,
  animationEasing: 'cubicOut'
}
```

---

## 🎯 高级用法

### 动态组件

**场景**：根据数据类型动态渲染不同组件

```vue
<script setup>
import { computed } from 'vue'
import BarChart from '@/components/charts/BarChart.vue'
import LineChart from '@/components/charts/LineChart.vue'
import PieChart from '@/components/charts/PieChart.vue'

const props = defineProps({
  chartType: { type: String, default: 'bar' } // 'bar' | 'line' | 'pie'
})

const currentComponent = computed(() => {
  const componentMap = {
    bar: BarChart,
    line: LineChart,
    pie: PieChart
  }
  return componentMap[props.chartType] || BarChart
})
</script>

<template>
  <component :is="currentComponent" :data="chartData" />
</template>
```

---

### Teleport（传送门）

**场景**：将组件渲染到 DOM 树的其他位置（如 Modal、Toast）

```vue
<!-- Toast.vue -->
<script setup>
import { ref } from 'vue'

const visible = ref(false)
const message = ref('')

const show = (msg) => {
  message.value = msg
  visible.value = true
  setTimeout(() => { visible.value = false }, 3000)
}

defineExpose({ show })
</script>

<template>
  <!-- 渲染到 body 下 -->
  <Teleport to="body">
    <div v-if="visible" class="toast">
      {{ message }}
    </div>
  </Teleport>
</template>

<style scoped>
.toast {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 16px 24px;
  background: #fff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  border-radius: 8px;
  z-index: 9999;
}
</style>
```

**使用**：
```vue
<script setup>
import { ref } from 'vue'
import Toast from '@/components/common/Toast.vue'

const toastRef = ref(null)

const handleClick = () => {
  toastRef.value.show('操作成功')
}
</script>

<template>
  <button @click="handleClick">显示提示</button>
  <Toast ref="toastRef" />
</template>
```

---

### Suspense（异步组件）

**场景**：等待异步组件加载完成

```vue
<!-- AsyncComponent.vue -->
<script setup>
// setup 顶层使用 await（自动返回 Promise）
const data = await fetch('/api/data').then(res => res.json())
</script>

<template>
  <div>{{ data }}</div>
</template>
```

```vue
<!-- Parent.vue -->
<script setup>
import { defineAsyncComponent } from 'vue'

const AsyncComponent = defineAsyncComponent(() =>
  import('@/components/AsyncComponent.vue')
)
</script>

<template>
  <Suspense>
    <!-- 异步组件 -->
    <template #default>
      <AsyncComponent />
    </template>

    <!-- 加载中状态 -->
    <template #fallback>
      <div>加载中...</div>
    </template>
  </Suspense>
</template>
```

---

### 虚拟滚动（大列表优化）

**场景**：渲染数千条数据的列表

```vue
<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  items: { type: Array, required: true }
})

const itemHeight = 50 // 每项高度
const visibleCount = 20 // 可见项数量
const scrollTop = ref(0)

const containerHeight = computed(() => visibleCount * itemHeight)
const totalHeight = computed(() => props.items.length * itemHeight)

const startIndex = computed(() => Math.floor(scrollTop.value / itemHeight))
const endIndex = computed(() => startIndex.value + visibleCount)

const visibleItems = computed(() =>
  props.items.slice(startIndex.value, endIndex.value)
)

const offsetY = computed(() => startIndex.value * itemHeight)

const handleScroll = (e) => {
  scrollTop.value = e.target.scrollTop
}
</script>

<template>
  <div
    class="virtual-scroll"
    :style="{ height: containerHeight + 'px' }"
    @scroll="handleScroll"
  >
    <div :style="{ height: totalHeight + 'px', position: 'relative' }">
      <div :style="{ transform: `translateY(${offsetY}px)` }">
        <div
          v-for="(item, index) in visibleItems"
          :key="startIndex + index"
          :style="{ height: itemHeight + 'px' }"
          class="list-item"
        >
          {{ item }}
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.virtual-scroll {
  overflow-y: auto;
}

.list-item {
  display: flex;
  align-items: center;
  padding: 0 16px;
  border-bottom: 1px solid #E5E7EB;
}
</style>
```

---

## ⚡ 性能优化技巧

### computed vs watch 选择

**使用 computed**：
- ✅ 需要基于其他响应式数据**计算**出新值
- ✅ 需要**缓存**计算结果（依赖未变时不重新计算）
- ✅ 需要在模板中使用

```javascript
// ✅ 正确：使用 computed
const fullName = computed(() => {
  return `${firstName.value} ${lastName.value}`
})
```

**使用 watch**：
- ✅ 需要在数据变化时**执行副作用**（如 API 调用、日志记录）
- ✅ 需要访问变化前后的值
- ✅ 需要异步操作

```javascript
// ✅ 正确：使用 watch
watch(selectedDate, async (newDate, oldDate) => {
  console.log('日期从', oldDate, '变为', newDate)
  await fetchData(newDate)
})
```

**反例**：
```javascript
// ❌ 错误：在 computed 中执行副作用
const result = computed(() => {
  fetch('/api/data') // 错误！computed 不应有副作用
  return someValue.value
})

// ❌ 错误：在 watch 中返回计算值
watch(firstName, () => {
  return `${firstName.value} ${lastName.value}` // 错误！应该用 computed
})
```

---

### v-show vs v-if 选择

**使用 v-show**：
- ✅ 频繁切换显示/隐藏
- ✅ 初始渲染成本不重要
- ✅ 切换性能优先

```vue
<!-- ✅ 正确：Tab 切换用 v-show -->
<div v-show="activeTab === 'tab1'">Tab 1 内容</div>
<div v-show="activeTab === 'tab2'">Tab 2 内容</div>
```

**使用 v-if**：
- ✅ 条件很少变化
- ✅ 初始渲染性能优先
- ✅ 条件为 false 时组件不需要存在

```vue
<!-- ✅ 正确：权限控制用 v-if -->
<AdminPanel v-if="isAdmin" />

<!-- ✅ 正确：加载状态用 v-if -->
<Loading v-if="loading" />
<Content v-else />
```

---

### 避免在模板中使用复杂表达式

```vue
<!-- ❌ 错误：模板中复杂计算 -->
<template>
  <div>{{ items.filter(i => i.active).map(i => i.name).join(', ') }}</div>
</template>

<!-- ✅ 正确：使用 computed -->
<script setup>
const activeItemNames = computed(() =>
  items.value.filter(i => i.active).map(i => i.name).join(', ')
)
</script>

<template>
  <div>{{ activeItemNames }}</div>
</template>
```

---

### 使用 v-memo 优化列表渲染

```vue
<!-- 仅当 item.id 或 selected 改变时才重新渲染 -->
<div
  v-for="item in list"
  :key="item.id"
  v-memo="[item.id, selected]"
>
  {{ item.name }}
</div>
```

---

## 🛠️ TypeScript 类型定义

### Props 类型定义

```typescript
// 方式 1: 使用 defineProps 泛型
<script setup lang="ts">
interface Props {
  title: string
  value: number
  trend?: 'up' | 'down' | 'flat'
  loading?: boolean
}

const props = defineProps<Props>()

// 默认值需要单独定义
const props = withDefaults(defineProps<Props>(), {
  trend: 'flat',
  loading: false
})
</script>

// 方式 2: 使用运行时声明
<script setup>
const props = defineProps({
  title: { type: String, required: true },
  value: { type: Number, required: true },
  trend: { type: String as PropType<'up' | 'down' | 'flat'>, default: 'flat' },
  loading: { type: Boolean, default: false }
})
</script>
```

---

### Emits 类型定义

```typescript
<script setup lang="ts">
// 方式 1: 使用 defineEmits 泛型
const emit = defineEmits<{
  'refresh': []                         // 无参数
  'filter-change': [filters: Record<string, string>] // 一个参数
  'update': [id: number, value: string] // 多个参数
}>()

emit('refresh')
emit('filter-change', { '三级机构': '成都' })
emit('update', 123, 'new value')

// 方式 2: 使用运行时声明
const emit = defineEmits(['refresh', 'filter-change', 'update'])
</script>
```

---

### Store 类型定义

```typescript
// stores/data.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'

interface KpiData {
  anchor_date: string
  premium: {
    day: number
    last7d: number
    last30d: number
  }
  policy_count: {
    day: number
    last7d: number
    last30d: number
  }
}

export const useDataStore = defineStore('data', () => {
  const kpiData = ref<KpiData | null>(null)

  const fetchKpiData = async (): Promise<void> => {
    const response = await apiClient.post<{ data: KpiData }>('/api/kpi-windows')
    kpiData.value = response.data
  }

  return {
    kpiData,
    fetchKpiData
  }
})
```

---

### API 响应类型定义

```typescript
// types/api.ts
export interface ApiResponse<T = any> {
  success: boolean
  data: T
  message?: string
}

export interface KpiResponse {
  anchor_date: string
  premium: {
    day: number
    last7d: number
    last30d: number
  }
  policy_count: {
    day: number
    last7d: number
    last30d: number
  }
  commission: {
    day: number
    last7d: number
    last30d: number
  }
  target_gap_day: number
}

export interface ChartResponse {
  latest_date: string
  x_axis: string[]
  series: Array<{
    name: string
    data: number[]
    dates: string[]
    code: string
    total_value: number
    period_index: number
  }>
}

// 使用
import type { ApiResponse, KpiResponse } from '@/types/api'

const response = await apiClient.post<ApiResponse<KpiResponse>>('/api/kpi-windows')
const kpiData: KpiResponse = response.data
```

---

## 📚 组件测试（未来）

### 单元测试模板

```typescript
// KpiCard.spec.ts
import { mount } from '@vue/test-utils'
import { describe, it, expect } from 'vitest'
import KpiCard from '@/components/dashboard/KpiCard.vue'

describe('KpiCard.vue', () => {
  it('renders title correctly', () => {
    const wrapper = mount(KpiCard, {
      props: {
        title: '签单保费',
        value: 125000,
        trend: 'up'
      }
    })

    expect(wrapper.find('.kpi-card__title').text()).toBe('签单保费')
  })

  it('emits refresh event when button clicked', async () => {
    const wrapper = mount(KpiCard, {
      props: {
        title: '签单保费',
        value: 125000
      }
    })

    await wrapper.find('.kpi-card__btn').trigger('click')

    expect(wrapper.emitted('refresh')).toBeTruthy()
    expect(wrapper.emitted('refresh')?.length).toBe(1)
  })

  it('formats currency value correctly', () => {
    const wrapper = mount(KpiCard, {
      props: {
        title: '签单保费',
        value: 125000,
        valueType: 'currency'
      }
    })

    expect(wrapper.find('.value').text()).toBe('12.5万')
  })
})
```

---

**文档版本**: 1.0
**最后更新**: 2025-11-08
**维护者**: Claude Code AI Assistant
