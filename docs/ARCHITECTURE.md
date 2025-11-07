# 架构设计文档 - 车险签单数据分析平台 v2.0

**文档版本**: 1.0
**更新日期**: 2025-11-07
**作者**: AI Assistant
**状态**: 设计完成，待实施

---

## 目录

1. [概述](#1-概述)
2. [架构原则](#2-架构原则)
3. [系统架构](#3-系统架构)
4. [前端架构](#4-前端架构)
5. [后端架构](#5-后端架构)
6. [数据流设计](#6-数据流设计)
7. [状态管理](#7-状态管理)
8. [API设计](#8-api设计)
9. [部署架构](#9-部署架构)
10. [安全架构](#10-安全架构)
11. [性能优化](#11-性能优化)
12. [可扩展性设计](#12-可扩展性设计)

---

## 1. 概述

### 1.1 系统定位

车险签单数据分析平台v2.0是一个**前后端分离的单页Web应用**，采用**Vue 3 + Flask**架构，为车险业务团队提供实时数据分析和可视化服务。

### 1.2 架构升级动机

**v1.0问题**:
- 原生JS无组件化，代码难维护
- 全局变量污染，状态管理混乱
- 缺少构建工具，无法优化bundle
- alert()等原始交互，用户体验差

**v2.0目标**:
- 组件化架构，复用率提升100%
- 状态管理清晰，避免prop drilling
- Vite构建优化，首屏加载<2s
- 现代化交互，用户体验提升80%

### 1.3 技术选型理由

| 技术 | 理由 | 替代方案对比 |
|------|------|-------------|
| **Vue 3** | 渐进式框架，学习曲线平缓，适合团队快速上手 | React: 学习成本高，需额外状态管理库 |
| **Vite** | 极速启动，HMR快，开发体验好 | Webpack: 配置复杂，构建慢 |
| **Pinia** | Vue 3官方推荐，类型安全，API简洁 | Vuex: 过于臃肿，已被Pinia取代 |
| **ECharts** | 国内主流，中文文档全，图表类型丰富 | Chart.js: 功能较弱，定制性差 |
| **Flask** | 轻量级，Python生态丰富，与Pandas无缝集成 | FastAPI: 异步特性对本项目过度设计 |

---

## 2. 架构原则

### 2.1 设计原则

1. **关注点分离 (Separation of Concerns)**
   - 前端专注UI和交互
   - 后端专注数据处理和业务逻辑
   - 通过RESTful API通信

2. **单一职责 (Single Responsibility)**
   - 每个组件只负责一个UI功能
   - 每个Store只管理一类状态
   - 每个API端点只处理一种资源

3. **开闭原则 (Open-Closed)**
   - 对扩展开放：新增筛选维度无需改核心代码
   - 对修改关闭：修改一个组件不影响其他组件

4. **依赖倒置 (Dependency Inversion)**
   - 组件依赖抽象的API服务，而非具体实现
   - 使用Pinia抽象状态，避免组件直接访问localStorage

5. **性能优先 (Performance First)**
   - 懒加载非首屏组件
   - 虚拟滚动处理大数据列表（未来）
   - 防抖节流优化高频操作

### 2.2 约束条件

- **浏览器兼容**: Chrome 90+, Edge 90+, Firefox 88+, Safari 14+
- **响应式**: 320px - 2560px屏幕宽度
- **性能指标**: 首屏<2s, TTI<3s, FCP<1s
- **可访问性**: 符合WCAG 2.1 AA标准
- **国际化**: 预留i18n接口（暂未实现）

---

## 3. 系统架构

### 3.1 整体架构图

```
┌─────────────────────────────────────────────────────────────┐
│                      User Browser                            │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │            Vue 3 SPA (Port 3000)                     │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌───────────┐  │  │
│  │  │  Components  │  │   Stores     │  │ Services  │  │  │
│  │  │              │  │              │  │           │  │  │
│  │  │ - Dashboard  │  │ - appStore   │  │ - api.ts  │  │  │
│  │  │ - KpiCard    │  │ - filterStore│  │ - utils   │  │  │
│  │  │ - ChartView  │  │ - dataStore  │  │           │  │  │
│  │  │ - FilterPanel│  │              │  │           │  │  │
│  │  │ - Toast      │  │              │  │           │  │  │
│  │  └──────────────┘  └──────────────┘  └───────────┘  │  │
│  │          ↓                ↓                 ↓         │  │
│  │  ┌───────────────────────────────────────────────┐  │  │
│  │  │         Vite Dev Server / Build Bundle        │  │  │
│  │  └───────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
│                           │                                  │
│                           │ HTTP (Axios)                     │
│                           ↓                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │          Flask REST API (Port 5001)                  │  │
│  │  ┌───────────────────────────────────────────────┐  │  │
│  │  │  API Endpoints (api_server.py)                │  │  │
│  │  │  - POST /api/refresh                          │  │  │
│  │  │  - GET  /api/daily-report                     │  │  │
│  │  │  - POST /api/week-comparison                  │  │  │
│  │  │  - GET  /api/filter-options                   │  │  │
│  │  │  - GET  /api/latest-date                      │  │  │
│  │  └───────────────────────────────────────────────┘  │  │
│  │                           ↓                           │  │
│  │  ┌───────────────────────────────────────────────┐  │  │
│  │  │  Data Processor (data_processor.py)           │  │  │
│  │  │  - Excel → CSV 转换                           │  │  │
│  │  │  - 数据清洗（去重、格式化）                    │  │  │
│  │  │  - 数据查询（筛选、聚合）                      │  │  │
│  │  │  - 趋势计算（周对比、同环比）                  │  │  │
│  │  └───────────────────────────────────────────────┘  │  │
│  │                           ↓                           │  │
│  │  ┌───────────────────────────────────────────────┐  │  │
│  │  │         Pandas DataFrame Processing            │  │  │
│  │  │  - 车险清单_2025年10-11月_合并.csv            │  │  │
│  │  │  - 业务员机构团队归属.json                    │  │  │
│  │  └───────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
│                           │                                  │
│                           │ File I/O                         │
│                           ↓                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │               Data Storage Layer                     │  │
│  │  - data/*.xlsx (输入)                                │  │
│  │  - 车险清单_2025年10-11月_合并.csv (主数据)         │  │
│  │  - 业务员机构团队归属.json (映射配置)               │  │
│  │  - data/processed/*.xlsx (已处理归档)               │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 模块职责划分

| 模块 | 职责 | 输入 | 输出 |
|------|------|------|------|
| **Vue组件层** | UI渲染、用户交互、事件处理 | 用户操作、Store状态 | DOM更新、事件触发 |
| **Pinia状态层** | 全局状态管理、异步数据获取 | API响应、用户操作 | 响应式状态 |
| **API服务层** | HTTP请求封装、错误处理 | API参数 | Promise<Data> |
| **Flask端点层** | 路由处理、请求验证、响应封装 | HTTP请求 | JSON响应 |
| **数据处理层** | Excel处理、数据清洗、查询聚合 | CSV/Excel文件 | DataFrame |
| **存储层** | 文件读写、数据持久化 | 数据变更 | 文件系统 |

---

## 4. 前端架构

### 4.1 目录结构

```
frontend/
├── public/                    # 静态资源（不经过Vite处理）
│   └── favicon.ico
├── src/
│   ├── assets/               # 资源文件（经过Vite处理）
│   │   ├── images/
│   │   └── styles/
│   │       ├── variables.css # CSS变量（设计系统）
│   │       ├── reset.css     # CSS重置
│   │       └── global.css    # 全局样式
│   │
│   ├── components/           # Vue组件
│   │   ├── common/          # 通用组件
│   │   │   ├── Toast.vue    # 通知组件
│   │   │   ├── Loading.vue  # 加载组件
│   │   │   └── Button.vue   # 按钮组件
│   │   ├── Dashboard.vue    # 主仪表板（容器组件）
│   │   ├── KpiCard.vue      # KPI卡片
│   │   ├── ChartView.vue    # 图表容器
│   │   ├── FilterPanel.vue  # 筛选面板
│   │   └── Header.vue       # 页面头部
│   │
│   ├── stores/              # Pinia状态管理
│   │   ├── app.ts           # 应用全局状态
│   │   ├── filter.ts        # 筛选器状态
│   │   └── data.ts          # 数据状态
│   │
│   ├── services/            # 服务层
│   │   ├── api.ts           # API调用封装
│   │   └── utils.ts         # 工具函数
│   │
│   ├── types/               # TypeScript类型定义
│   │   ├── api.ts           # API响应类型
│   │   └── components.ts    # 组件Props类型
│   │
│   ├── App.vue              # 根组件
│   └── main.ts              # 入口文件
│
├── index.html               # HTML模板
├── vite.config.ts           # Vite配置
├── tsconfig.json            # TypeScript配置
└── package.json             # 依赖管理
```

### 4.2 组件设计

#### 4.2.1 组件分类

**容器组件 (Smart Components)**:
- `Dashboard.vue`: 主仪表板，协调所有子组件
- 职责: 数据获取、状态管理、子组件协调
- 特点: 有业务逻辑，连接Store

**展示组件 (Dumb Components)**:
- `KpiCard.vue`, `ChartView.vue`, `FilterPanel.vue`
- 职责: 接收props渲染UI，emit事件通知父组件
- 特点: 纯UI，无业务逻辑，可复用

**通用组件 (Common Components)**:
- `Toast.vue`, `Loading.vue`, `Button.vue`
- 职责: 提供跨页面通用UI元素
- 特点: 高度抽象，零业务耦合

#### 4.2.2 组件通信

```typescript
// 父 → 子: Props
<KpiCard :value="premiumValue" :trend="trendData" />

// 子 → 父: Events
const emit = defineEmits<{
  'refresh': []
  'filter-change': [filters: FilterOptions]
}>()
emit('refresh')

// 跨组件: Pinia Store
import { useDataStore } from '@/stores/data'
const dataStore = useDataStore()
const kpiData = computed(() => dataStore.kpiData)

// 全局通知: Event Bus (Toast)
import { useToast } from '@/composables/useToast'
const { showSuccess, showError } = useToast()
showSuccess('数据刷新成功')
```

#### 4.2.3 组件生命周期

```typescript
// Dashboard.vue 生命周期示例
import { onMounted, onUnmounted } from 'vue'
import { useDataStore } from '@/stores/data'

const dataStore = useDataStore()

onMounted(async () => {
  // 1. 获取最新日期
  await dataStore.fetchLatestDate()

  // 2. 加载筛选选项
  await dataStore.fetchFilterOptions()

  // 3. 加载初始数据
  await dataStore.fetchDashboardData()

  // 4. 设置自动刷新（未来功能）
  // startAutoRefresh()
})

onUnmounted(() => {
  // 清理定时器
  // stopAutoRefresh()
})
```

### 4.3 路由设计（未来扩展）

当前v2.0为单页应用，未使用Vue Router。未来v3.0计划:

```typescript
// router/index.ts (未来)
const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue')
  },
  {
    path: '/reports',
    name: 'Reports',
    component: () => import('@/views/Reports.vue')
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('@/views/Settings.vue'),
    meta: { requiresAuth: true }
  }
]
```

---

## 5. 后端架构

### 5.1 目录结构

```
backend/
├── api_server.py              # Flask应用主入口
├── data_processor.py          # 数据处理核心类
├── config.py                  # 配置管理（未来）
├── models/                    # 数据模型（未来）
│   └── data_schema.py
├── services/                  # 业务服务（未来重构）
│   ├── excel_service.py
│   ├── query_service.py
│   └── filter_service.py
└── utils/                     # 工具函数（未来）
    ├── date_utils.py
    └── validation.py
```

### 5.2 API端点设计

详见第8节"API设计"。

### 5.3 数据处理流程

```
┌────────────────────┐
│  用户上传Excel文件  │
│  放入data/目录      │
└──────────┬─────────┘
           │
           ↓
┌────────────────────────────────┐
│  POST /api/refresh             │
│  触发数据处理管道              │
└──────────┬─────────────────────┘
           │
           ↓
┌────────────────────────────────┐
│  DataProcessor.process_files() │
│  1. 扫描data/*.xlsx            │
│  2. 逐个读取Excel              │
│  3. 转换为DataFrame            │
└──────────┬─────────────────────┘
           │
           ↓
┌────────────────────────────────┐
│  DataProcessor._clean_data()   │
│  1. 删除空行                   │
│  2. 日期格式标准化             │
│  3. 数值类型转换               │
│  4. 缺失值填充                 │
└──────────┬─────────────────────┘
           │
           ↓
┌────────────────────────────────┐
│  去重 + 合并历史数据            │
│  1. 读取主CSV文件              │
│  2. concat新旧数据             │
│  3. drop_duplicates()          │
│  4. 保存回主CSV                │
└──────────┬─────────────────────┘
           │
           ↓
┌────────────────────────────────┐
│  归档处理完文件                 │
│  移动到data/processed/目录      │
│  文件名添加时间戳               │
└──────────┬─────────────────────┘
           │
           ↓
┌────────────────────────────────┐
│  返回成功响应                   │
│  {success: true, ...}          │
└────────────────────────────────┘
```

---

## 6. 数据流设计

### 6.1 数据获取流程

```
用户操作
   │
   ↓
Vue组件触发action
   │
   ↓
Pinia Store调用API service
   │
   ↓
Axios发送HTTP请求
   │
   ↓
Flask接收请求
   │
   ↓
DataProcessor查询数据
   │
   ↓
Pandas处理DataFrame
   │
   ↓
Flask返回JSON响应
   │
   ↓
Axios接收响应
   │
   ↓
Pinia Store更新状态
   │
   ↓
Vue组件响应式更新UI
```

### 6.2 筛选数据流

```typescript
// 1. 用户在FilterPanel选择筛选项
const handleFilterChange = () => {
  emit('filter-change', activeFilters.value)
}

// 2. Dashboard接收事件，调用Store
const onFilterChange = async (filters: FilterOptions) => {
  await dataStore.applyFilters(filters)
}

// 3. Store调用API
const applyFilters = async (filters: FilterOptions) => {
  loading.value = true
  try {
    const data = await api.fetchWeekComparison({ filters })
    chartData.value = data
  } catch (error) {
    showError('筛选失败')
  } finally {
    loading.value = false
  }
}

// 4. 后端处理筛选
def get_week_comparison(filters):
    df = self.data.copy()
    df = self._apply_filters(df, filters)
    # 按周聚合
    result = df.groupby('weekday').agg(...)
    return result
```

### 6.3 缓存策略

#### 前端缓存

```typescript
// stores/filter.ts
export const useFilterStore = defineStore('filter', () => {
  const filterOptions = ref<FilterOptions | null>(null)
  const cacheTime = ref<number>(0)
  const CACHE_DURATION = 5 * 60 * 1000 // 5分钟

  const fetchFilterOptions = async () => {
    const now = Date.now()
    if (filterOptions.value && now - cacheTime.value < CACHE_DURATION) {
      return filterOptions.value // 使用缓存
    }

    const data = await api.getFilterOptions()
    filterOptions.value = data
    cacheTime.value = now
    return data
  }
})
```

#### 后端缓存（未来）

```python
# 使用Flask-Caching（未来功能）
from flask_caching import Cache
cache = Cache(config={'CACHE_TYPE': 'simple'})

@app.route('/api/filter-options')
@cache.cached(timeout=300)  # 5分钟缓存
def get_filter_options():
    return processor.get_filter_options()
```

---

## 7. 状态管理

### 7.1 Pinia Store设计

#### appStore (全局应用状态)

```typescript
// stores/app.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAppStore = defineStore('app', () => {
  // State
  const loading = ref(false)
  const latestDate = ref<string | null>(null)
  const selectedDate = ref<string | null>(null)
  const currentMetric = ref<'premium' | 'count'>('premium')

  // Getters
  const displayDate = computed(() =>
    selectedDate.value || latestDate.value || '加载中...'
  )

  // Actions
  const setLoading = (value: boolean) => {
    loading.value = value
  }

  const setLatestDate = (date: string) => {
    latestDate.value = date
    if (!selectedDate.value) {
      selectedDate.value = date
    }
  }

  const switchMetric = (metric: 'premium' | 'count') => {
    currentMetric.value = metric
  }

  return {
    loading,
    latestDate,
    selectedDate,
    currentMetric,
    displayDate,
    setLoading,
    setLatestDate,
    switchMetric
  }
})
```

#### filterStore (筛选器状态)

```typescript
// stores/filter.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { FilterOptions, ActiveFilters } from '@/types/api'

export const useFilterStore = defineStore('filter', () => {
  const filterOptions = ref<FilterOptions>({})
  const activeFilters = ref<ActiveFilters>({})
  const filterPanelOpen = ref(false)

  const fetchFilterOptions = async () => {
    const data = await api.getFilterOptions()
    filterOptions.value = data
  }

  const setFilter = (key: string, value: string) => {
    activeFilters.value[key] = value
  }

  const clearFilters = () => {
    activeFilters.value = {}
  }

  const togglePanel = () => {
    filterPanelOpen.value = !filterPanelOpen.value
  }

  return {
    filterOptions,
    activeFilters,
    filterPanelOpen,
    fetchFilterOptions,
    setFilter,
    clearFilters,
    togglePanel
  }
})
```

#### dataStore (数据状态)

```typescript
// stores/data.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { KpiData, ChartData } from '@/types/api'
import { useAppStore } from './app'
import { useFilterStore } from './filter'

export const useDataStore = defineStore('data', () => {
  const kpiData = ref<KpiData | null>(null)
  const chartData = ref<ChartData | null>(null)

  const appStore = useAppStore()
  const filterStore = useFilterStore()

  const fetchDashboardData = async () => {
    appStore.setLoading(true)
    try {
      const [kpi, chart] = await Promise.all([
        api.getDailyReport(appStore.selectedDate),
        api.getWeekComparison(filterStore.activeFilters)
      ])
      kpiData.value = kpi
      chartData.value = chart
    } catch (error) {
      console.error('Failed to fetch data:', error)
    } finally {
      appStore.setLoading(false)
    }
  }

  const refreshData = async () => {
    await api.refresh()
    await fetchDashboardData()
  }

  return {
    kpiData,
    chartData,
    fetchDashboardData,
    refreshData
  }
})
```

### 7.2 状态持久化（未来）

```typescript
// plugins/persist.ts (未来功能)
import { createPersistedState } from 'pinia-plugin-persistedstate'

const pinia = createPinia()
pinia.use(createPersistedState({
  storage: localStorage,
  paths: ['filter.activeFilters', 'app.selectedDate']
}))
```

---

## 8. API设计

### 8.1 RESTful规范

#### 命名约定

- 使用名词复数表示资源集合: `/api/reports`
- 使用动词表示操作: `/api/refresh`
- 使用kebab-case: `/api/daily-report`

#### HTTP方法语义

| 方法 | 语义 | 幂等性 | 示例 |
|------|------|-------|------|
| GET | 查询资源 | 是 | `GET /api/daily-report` |
| POST | 创建资源或触发操作 | 否 | `POST /api/refresh` |
| PUT | 完整更新资源 | 是 | `PUT /api/settings` (未来) |
| PATCH | 部分更新资源 | 否 | `PATCH /api/settings` (未来) |
| DELETE | 删除资源 | 是 | `DELETE /api/data/:id` (未来) |

#### 响应格式统一

```typescript
// 成功响应
{
  "success": true,
  "data": {...},
  "message": "操作成功"  // 可选
}

// 失败响应
{
  "success": false,
  "error": "错误描述",
  "code": "ERROR_CODE",  // 错误代码
  "details": {...}        // 详细信息（可选）
}
```

### 8.2 端点详细设计

#### POST /api/refresh

**描述**: 处理新Excel文件并刷新数据

**请求**:
```http
POST /api/refresh HTTP/1.1
Content-Type: application/json

{}
```

**响应**:
```json
{
  "success": true,
  "message": "数据刷新成功",
  "processed_files": [
    "2025-11-07_签单清单.xlsx"
  ],
  "records_added": 125,
  "duplicates_removed": 3
}
```

**错误场景**:
- 400: 无新文件
- 500: 数据处理失败

---

#### GET /api/daily-report

**描述**: 获取指定日期的日报KPI数据

**请求**:
```http
GET /api/daily-report?date=2025-11-07 HTTP/1.1
```

**响应**:
```json
{
  "success": true,
  "data": {
    "date": "2025-11-07",
    "premium": 205000,          // 签单保费
    "count": 45,                // 保单件数
    "commission": 15000,        // 手续费
    "target_gap": 5000,         // 目标差距
    "target_completion": 102.5, // 目标完成度(%)
    "premium_7day": 1420000,    // 近7天保费
    "premium_30day": 5800000    // 近30天保费
  }
}
```

**查询参数**:
- `date` (可选): YYYY-MM-DD格式，默认最新日期

---

#### POST /api/week-comparison

**描述**: 获取3周期对比数据（支持筛选）

**请求**:
```http
POST /api/week-comparison HTTP/1.1
Content-Type: application/json

{
  "filters": {
    "三级机构": "成都",
    "是否新能源": "是"
  },
  "metric": "premium"  // 或 "count"
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "categories": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"],
    "recent_week": [45000, 52000, 48000, 55000, 60000, 35000, 40000],
    "last_week": [42000, 50000, 46000, 53000, 58000, 33000, 38000],
    "before_last_week": [40000, 48000, 44000, 51000, 56000, 31000, 36000],
    "period_start": "2025-10-28",
    "period_end": "2025-11-07"
  }
}
```

---

#### GET /api/filter-options

**描述**: 获取所有筛选维度的可选值

**请求**:
```http
GET /api/filter-options HTTP/1.1
```

**响应**:
```json
{
  "success": true,
  "data": {
    "三级机构": ["成都", "绵阳", "德阳", "乐山"],
    "团队": {
      "成都": ["团队A", "团队B"],
      "绵阳": ["团队C"]
    },
    "车险新业务分类": ["新", "转", "续"],
    "是否新能源": ["是", "否"],
    "是否过户车": ["是", "否"],
    "险种大类": ["交强险", "商业险", "特种车险"],
    "吨位分段": ["2吨以下", "2-5吨", "5-10吨", "10吨以上"],
    "电销": ["是", "否"]
  }
}
```

---

#### GET /api/latest-date

**描述**: 获取数据中的最新日期

**请求**:
```http
GET /api/latest-date HTTP/1.1
```

**响应**:
```json
{
  "success": true,
  "latest_date": "2025-11-07"
}
```

---

#### GET /api/health

**描述**: 健康检查端点

**请求**:
```http
GET /api/health HTTP/1.1
```

**响应**:
```json
{
  "status": "healthy",
  "message": "API服务运行正常",
  "timestamp": "2025-11-07T10:30:00Z",
  "version": "2.0.0"
}
```

---

### 8.3 错误处理

#### 错误码设计

| 错误码 | HTTP状态 | 说明 | 处理方式 |
|--------|---------|------|---------|
| `DATA_NOT_FOUND` | 404 | 指定日期无数据 | 提示用户选择其他日期 |
| `INVALID_DATE_FORMAT` | 400 | 日期格式错误 | 前端验证 |
| `PROCESSING_FAILED` | 500 | 数据处理失败 | 显示错误详情，提供重试按钮 |
| `FILE_NOT_FOUND` | 404 | Excel文件不存在 | 提示用户添加文件 |
| `FILTER_INVALID` | 400 | 筛选参数无效 | 重置筛选器 |

#### 前端错误处理

```typescript
// services/api.ts
import axios, { AxiosError } from 'axios'

const handleError = (error: AxiosError) => {
  if (error.response) {
    const { status, data } = error.response
    switch (status) {
      case 400:
        showError(data.error || '请求参数错误')
        break
      case 404:
        showError(data.error || '数据不存在')
        break
      case 500:
        showError('服务器错误，请稍后重试')
        break
      default:
        showError('未知错误')
    }
  } else if (error.request) {
    showError('网络连接失败，请检查网络')
  } else {
    showError('请求配置错误')
  }
}

api.interceptors.response.use(
  response => response,
  error => {
    handleError(error)
    return Promise.reject(error)
  }
)
```

---

## 9. 部署架构

### 9.1 开发环境

```
┌─────────────────────────────────┐
│  Developer Machine              │
│  ┌─────────────────────────┐   │
│  │  Vite Dev Server        │   │
│  │  http://localhost:3000  │   │
│  │  - HMR启用              │   │
│  │  - Source Map           │   │
│  └─────────────────────────┘   │
│  ┌─────────────────────────┐   │
│  │  Flask Dev Server       │   │
│  │  http://localhost:5001  │   │
│  │  - Debug模式            │   │
│  │  - 自动重载             │   │
│  └─────────────────────────┘   │
└─────────────────────────────────┘
```

**启动命令**:
```bash
# 终端1: 前端
cd frontend && npm run dev

# 终端2: 后端
cd backend && python api_server.py
```

---

### 9.2 生产环境

```
┌────────────────────────────────────────────────────────────┐
│                    Production Server                        │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐ │
│  │                  Nginx (Port 80/443)                 │ │
│  │  ┌────────────────────┐  ┌─────────────────────────┐│ │
│  │  │  Static Files      │  │  Reverse Proxy          ││ │
│  │  │  /dist/*           │  │  /api/* → :8000         ││ │
│  │  │  (Vue 3 Build)     │  │                         ││ │
│  │  └────────────────────┘  └─────────────────────────┘│ │
│  └─────────┬────────────────────────────┬───────────────┘ │
│            │                            │                  │
│            │                            ↓                  │
│  ┌─────────↓────────────┐  ┌──────────────────────────┐  │
│  │  CDN (未来)          │  │  Gunicorn (Port 8000)    │  │
│  │  - 静态资源加速      │  │  - 4 workers             │  │
│  │  - 图片压缩          │  │  - Sync/Async模式        │  │
│  └──────────────────────┘  └──────────┬───────────────┘  │
│                                       │                   │
│                                       ↓                   │
│                            ┌────────────────────────────┐ │
│                            │  Flask App                 │ │
│                            │  - data_processor.py       │ │
│                            │  - api_server.py           │ │
│                            └────────────┬───────────────┘ │
│                                         │                 │
│                                         ↓                 │
│                            ┌────────────────────────────┐ │
│                            │  Data Files                │ │
│                            │  - CSV主数据               │ │
│                            │  - JSON配置                │ │
│                            │  - Excel输入文件           │ │
│                            └────────────────────────────┘ │
└────────────────────────────────────────────────────────────┘
```

### 9.3 部署步骤

#### 前端构建

```bash
cd frontend
npm run build
# 输出到 frontend/dist/
```

#### 后端部署

```bash
# 安装Gunicorn
pip install gunicorn

# 启动Gunicorn
cd backend
gunicorn -w 4 -b 0.0.0.0:8000 api_server:app
```

#### Nginx配置

```nginx
# /etc/nginx/sites-available/daylyreport
server {
    listen 80;
    server_name your-domain.com;

    # 前端静态文件
    location / {
        root /var/www/daylyreport/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # 后端API代理
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Gzip压缩
    gzip on;
    gzip_types text/plain text/css application/json application/javascript;
    gzip_min_length 1000;
}
```

---

## 10. 安全架构

### 10.1 安全威胁模型

| 威胁 | 风险等级 | 防护措施 |
|------|---------|---------|
| XSS攻击 | 高 | Vue自动转义、CSP策略 |
| CSRF攻击 | 中 | Token验证（未来） |
| SQL注入 | 低 | 使用Pandas，无直接SQL |
| 文件上传漏洞 | 中 | 文件类型验证、大小限制 |
| API滥用 | 中 | 限流、认证（未来） |
| 数据泄露 | 高 | HTTPS、敏感字段脱敏 |

### 10.2 防护措施

#### 前端安全

```typescript
// CSP策略配置（index.html）
<meta http-equiv="Content-Security-Policy"
      content="default-src 'self';
               script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net;
               style-src 'self' 'unsafe-inline';">

// API请求添加CSRF Token（未来）
api.interceptors.request.use(config => {
  const token = localStorage.getItem('csrf_token')
  if (token) {
    config.headers['X-CSRF-Token'] = token
  }
  return config
})
```

#### 后端安全

```python
# Flask安全配置
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

# CORS配置（生产环境应限制源）
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://your-domain.com"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})

# 文件上传验证
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def validate_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 限流（未来 - 使用Flask-Limiter）
from flask_limiter import Limiter
limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/api/refresh', methods=['POST'])
@limiter.limit("10 per minute")
def refresh_data():
    ...
```

---

## 11. 性能优化

### 11.1 前端性能优化

#### 代码分割

```typescript
// router/index.ts (未来)
const routes = [
  {
    path: '/',
    component: () => import(/* webpackChunkName: "dashboard" */ '@/views/Dashboard.vue')
  },
  {
    path: '/reports',
    component: () => import(/* webpackChunkName: "reports" */ '@/views/Reports.vue')
  }
]
```

#### 组件懒加载

```typescript
// 大组件懒加载
const ChartView = defineAsyncComponent(() => import('@/components/ChartView.vue'))

// 带loading和error的懒加载
const AsyncComponent = defineAsyncComponent({
  loader: () => import('@/components/HeavyComponent.vue'),
  loadingComponent: LoadingSpinner,
  errorComponent: ErrorMessage,
  delay: 200,
  timeout: 3000
})
```

#### 虚拟滚动（未来 - 数据列表）

```typescript
import { useVirtualList } from '@vueuse/core'

const { list, containerProps, wrapperProps } = useVirtualList(
  largeDataArray,
  { itemHeight: 50 }
)
```

#### 防抖节流

```typescript
import { debounce, throttle } from 'lodash-es'

// 搜索防抖
const handleSearch = debounce((keyword: string) => {
  // 执行搜索
}, 300)

// 窗口resize节流
const handleResize = throttle(() => {
  chart.value?.resize()
}, 100)
```

#### 图片优化

```typescript
// vite.config.ts
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        assetFileNames: (assetInfo) => {
          let extType = assetInfo.name.split('.').at(1)
          if (/png|jpe?g|svg|gif|tiff|bmp|ico/i.test(extType)) {
            extType = 'images'
          }
          return `assets/${extType}/[name]-[hash][extname]`
        }
      }
    }
  },
  plugins: [
    viteImagemin({
      gifsicle: { optimizationLevel: 7 },
      optipng: { optimizationLevel: 7 },
      mozjpeg: { quality: 80 }
    })
  ]
})
```

### 11.2 后端性能优化

#### Pandas优化

```python
# 使用categoricals减少内存
df['三级机构'] = df['三级机构'].astype('category')
df['是否新能源'] = df['是否新能源'].astype('category')

# 只读取需要的列
usecols = ['投保确认时间', '签单/批改保费', '签单数量']
df = pd.read_csv('data.csv', usecols=usecols)

# 使用eval加速计算
df.eval('total = premium * count', inplace=True)
```

#### 缓存热点数据

```python
from functools import lru_cache

class DataProcessor:
    @lru_cache(maxsize=128)
    def get_filter_options(self):
        # 缓存筛选选项（5分钟内不变）
        return self._compute_filter_options()
```

#### 异步处理（未来 - FastAPI）

```python
# 使用FastAPI实现异步端点（未来重构）
@app.get('/api/daily-report')
async def get_daily_report(date: str = None):
    data = await asyncio.to_thread(processor.get_daily_report, date)
    return {"success": True, "data": data}
```

### 11.3 性能监控

#### 前端监控

```typescript
// main.ts
import { createApp } from 'vue'

const app = createApp(App)

// 性能监控
if (import.meta.env.PROD) {
  window.addEventListener('load', () => {
    const perfData = performance.getEntriesByType('navigation')[0]
    console.log('FCP:', perfData.domContentLoadedEventEnd)
    console.log('TTI:', perfData.loadEventEnd)
  })
}
```

#### 后端监控

```python
# 使用Flask-Monitoring（未来）
from flask_monitoring import Monitoring

monitoring = Monitoring(app)

# 记录API响应时间
import time
from functools import wraps

def timeit(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()
        print(f"{f.__name__} took {end - start:.2f}s")
        return result
    return wrapper

@app.route('/api/daily-report')
@timeit
def daily_report():
    ...
```

---

## 12. 可扩展性设计

### 12.1 水平扩展

#### 后端多实例部署

```bash
# 启动多个Gunicorn实例
gunicorn -w 4 --bind 127.0.0.1:8001 api_server:app
gunicorn -w 4 --bind 127.0.0.1:8002 api_server:app

# Nginx负载均衡
upstream flask_backend {
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}

location /api/ {
    proxy_pass http://flask_backend;
}
```

#### 数据库迁移（未来）

当数据量超过10万条时，考虑迁移到PostgreSQL:

```python
from sqlalchemy import create_engine

engine = create_engine('postgresql://user:pass@localhost/dbname')
df.to_sql('insurance_data', engine, if_exists='append', index=False)
```

### 12.2 功能扩展点

#### 插件化筛选器

```typescript
// 未来支持自定义筛选器插件
interface FilterPlugin {
  name: string
  type: 'select' | 'multiselect' | 'daterange'
  options: () => Promise<string[]>
  apply: (data: any[], value: any) => any[]
}

const registerFilterPlugin = (plugin: FilterPlugin) => {
  filterPlugins.set(plugin.name, plugin)
}
```

#### 图表类型扩展

```typescript
// 支持动态注册图表类型
interface ChartPlugin {
  type: string
  render: (container: HTMLElement, data: any) => void
}

const chartRegistry = new Map<string, ChartPlugin>()
chartRegistry.set('bar', BarChartPlugin)
chartRegistry.set('pie', PieChartPlugin)
chartRegistry.set('heatmap', HeatmapChartPlugin)  // 未来新增
```

---

## 附录

### A. 依赖版本

#### 前端依赖

```json
{
  "dependencies": {
    "vue": "^3.4.0",
    "pinia": "^2.1.7",
    "axios": "^1.6.0",
    "echarts": "^5.4.3"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.0.0",
    "vite": "^5.0.0",
    "typescript": "^5.3.0",
    "@types/node": "^20.10.0"
  }
}
```

#### 后端依赖

```txt
Flask==3.0.0
pandas==2.1.3
openpyxl==3.1.2
flask-cors==4.0.0
gunicorn==21.2.0
```

### B. 开发规范

#### 代码风格

- 前端: 遵循[Vue 3官方风格指南](https://vuejs.org/style-guide/)
- 后端: 遵循[PEP 8](https://peps.python.org/pep-0008/)
- 提交信息: 遵循[Conventional Commits](https://www.conventionalcommits.org/)

#### 命名约定

- Vue组件: PascalCase (`KpiCard.vue`)
- TypeScript文件: camelCase (`apiService.ts`)
- CSS类名: BEM (`kpi-card__value--up`)
- Python文件: snake_case (`data_processor.py`)

### C. 参考资料

- [Vue 3文档](https://vuejs.org/)
- [Pinia文档](https://pinia.vuejs.org/)
- [Vite文档](https://vitejs.dev/)
- [ECharts文档](https://echarts.apache.org/)
- [Flask文档](https://flask.palletsprojects.com/)
- [Pandas文档](https://pandas.pydata.org/)

---

**文档维护**: 随架构演进持续更新
**审核周期**: 每季度review一次
**反馈渠道**: GitHub Issues或内部项目群
