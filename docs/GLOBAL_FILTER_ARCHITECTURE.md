# 全局筛选架构设计文档

**文档版本**: 1.0
**创建日期**: 2025-11-09
**更新日期**: 2025-11-09
**状态**: 已实施

---

## 📋 目录

1. [设计目标](#1-设计目标)
2. [架构概览](#2-架构概览)
3. [核心组件](#3-核心组件)
4. [状态管理](#4-状态管理)
5. [数据流设计](#5-数据流设计)
6. [API接口](#6-api接口)
7. [交互设计](#7-交互设计)
8. [技术实现](#8-技术实现)

---

## 1. 设计目标

### 1.1 业务需求

- **全局筛选置顶**：筛选面板放置在页面顶部，任何板块都能方便筛选
- **新增业务类型**：增加"客户类别3"作为筛选维度（10个分类）
- **整合时间与口径**：将"时间段"和"数据口径"整合进全局筛选
- **指标切换独立**：保费/件数切换与筛选器解耦，单独放置
- **强壮性保证**：弱耦合、防止系统性问题、不影响其他功能

### 1.2 技术目标

- **单一真相源**：所有筛选状态集中在 filterStore 管理
- **响应式设计**：筛选变更自动触发相关图表刷新
- **向后兼容**：新增字段为可选，不影响现有接口
- **错误隔离**：筛选失败可回滚，不阻塞页面
- **性能优化**：使用 debounce 防止频繁请求

---

## 2. 架构概览

### 2.1 组件层级

```
Dashboard.vue
  ├── Header.vue (保持不变)
  ├── GlobalFilterPanel.vue (新建 - 全局筛选)
  │     ├── 时间段选择器 (从 Dashboard 移入)
  │     ├── 数据口径选择器 (从 Dashboard 移入)
  │     ├── 业务类型选择器 (新增)
  │     ├── 其他筛选维度 (从 FilterPanel 迁移)
  │     └── 指标切换器 (独立区域，右侧)
  ├── KpiCards.vue
  ├── ChartView.vue
  └── PieChartCards.vue
```

### 2.2 UI布局

```
┌─────────────────────────────────────────────────────────┐
│                      Header                             │
└─────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│ GlobalFilterPanel (可折叠，默认展开)                   │
│ ┌──────────────────────────┬─────────────────────────┐ │
│ │ 🔍 数据筛选 (3)          │ 📊 指标切换             │ │
│ │ [时间:近7天×]            │ [¥保费] [#件数]        │ │
│ │ [业务类型:摩托车×]       │                         │ │
│ │              [展开▼]     │                         │ │
│ └──────────────────────────┴─────────────────────────┘ │
│ [筛选表单 - 折叠时隐藏]                                │
└─────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│ KPI Cards (响应: 筛选+时间+口径+指标)                  │
└─────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│ ChartView (响应: 筛选+口径+指标，不受时间影响)         │
└─────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│ PieCharts (响应: 筛选+时间+口径)                       │
└─────────────────────────────────────────────────────────┘
```

---

## 3. 核心组件

### 3.1 GlobalFilterPanel.vue

**职责：**
- 管理所有筛选维度（含时间段、数据口径、业务类型）
- 提供指标切换功能（独立区域）
- 展示已选筛选标签
- 支持折叠/展开、应用/重置操作

**关键特性：**
- 默认展开，应用后自动折叠
- 折叠时显示已选标签（可点击×移除）
- 移除标签立即生效并刷新数据
- 指标切换独立，不属于筛选条件

**Props：**
无（直接使用 store）

**Events：**
无（通过 store 通信）

---

## 4. 状态管理

### 4.1 filter.js 扩展

**新增状态字段：**

```javascript
// ========== 全局筛选状态 ==========
const timePeriod = ref('day')              // 时间段: day | last7d | last30d
const dataScope = ref('exclude_correction') // 数据口径: exclude_correction | include_correction
const businessType = ref('')               // 业务类型: 客户类别3

// ========== 现有筛选条件 (保持不变) ==========
const activeFilters = ref({
  '业务员': '',
  '三级机构': '',
  '团队': '',
  '是否续保': '',
  '是否新能源': '',
  '是否过户车': '',
  '是否异地车': '',
  '险种大类': '',
  '吨位': ''
})
```

**新增 Getters：**

```javascript
// 获取完整的全局筛选参数（含时间、口径、业务类型、其他筛选）
const getAllGlobalFilters = computed(() => ({
  // 时间与数据范围
  time_period: timePeriod.value,
  data_scope: dataScope.value,

  // 业务类型
  business_type: businessType.value || undefined,

  // 其他筛选条件（过滤空值）
  ...Object.fromEntries(
    Object.entries(activeFilters.value).filter(([_, v]) => v)
  )
}))

// 激活筛选数量（含时间、口径、业务类型）
const activeFiltersCount = computed(() => {
  let count = 0
  if (timePeriod.value !== 'day') count++
  if (dataScope.value !== 'exclude_correction') count++
  if (businessType.value) count++
  Object.values(activeFilters.value).forEach(v => { if (v) count++ })
  return count
})

// 格式化的筛选标签
const filterTags = computed(() => {
  const tags = []

  // 时间段标签
  if (timePeriod.value !== 'day') {
    const labels = { last7d: '近7天', last30d: '近30天' }
    tags.push({ key: 'timePeriod', label: `时间: ${labels[timePeriod.value]}` })
  }

  // 数据口径标签
  if (dataScope.value === 'include_correction') {
    tags.push({ key: 'dataScope', label: '数据: 含批改' })
  }

  // 业务类型标签
  if (businessType.value) {
    tags.push({ key: 'businessType', label: `业务类型: ${businessType.value}` })
  }

  // 其他筛选标签
  Object.entries(activeFilters.value).forEach(([key, value]) => {
    if (value) {
      tags.push({ key, label: `${key}: ${value}` })
    }
  })

  return tags
})
```

**新增 Actions：**

```javascript
// 设置时间段
function setTimePeriod(period) {
  if (!['day', 'last7d', 'last30d'].includes(period)) {
    console.error('Invalid time period:', period)
    return
  }
  timePeriod.value = period
}

// 设置数据口径
function setDataScope(scope) {
  if (!['exclude_correction', 'include_correction'].includes(scope)) {
    console.error('Invalid data scope:', scope)
    return
  }
  dataScope.value = scope
}

// 设置业务类型
function setBusinessType(type) {
  businessType.value = type
}

// 移除单个筛选（支持时间、口径、业务类型）
function removeFilter(key) {
  if (key === 'timePeriod') {
    timePeriod.value = 'day'
  } else if (key === 'dataScope') {
    dataScope.value = 'exclude_correction'
  } else if (key === 'businessType') {
    businessType.value = ''
  } else {
    delete activeFilters.value[key]
  }
}

// 重置所有筛选（包括新增字段）
function resetFilters() {
  timePeriod.value = 'day'
  dataScope.value = 'exclude_correction'
  businessType.value = ''
  activeFilters.value = {}
}

// 保存当前状态（用于回滚）
function saveSnapshot() {
  return {
    timePeriod: timePeriod.value,
    dataScope: dataScope.value,
    businessType: businessType.value,
    activeFilters: { ...activeFilters.value }
  }
}

// 恢复快照（用于错误回滚）
function restoreSnapshot(snapshot) {
  timePeriod.value = snapshot.timePeriod
  dataScope.value = snapshot.dataScope
  businessType.value = snapshot.businessType
  activeFilters.value = { ...snapshot.activeFilters }
}
```

---

## 5. 数据流设计

### 5.1 筛选应用流程

```
用户操作 GlobalFilterPanel
  ↓
修改筛选条件（时间段/口径/业务类型/其他维度）
  ↓
点击"应用筛选"
  ↓
filterStore.setTimePeriod(period)
filterStore.setDataScope(scope)
filterStore.setBusinessType(type)
filterStore.applyFilters(otherFilters)
  ↓
收集 filterStore.getAllGlobalFilters()
  ↓
{
  time_period: 'last7d',
  data_scope: 'include_correction',
  business_type: '摩托车',
  三级机构: '成都',
  是否新能源: '是'
}
  ↓
并行请求后端 API:
  - POST /api/kpi-windows (使用 time_period)
  - POST /api/week-comparison (不使用 time_period)
  - POST /api/insurance-type-distribution (使用 time_period)
  - POST /api/premium-range-distribution (使用 time_period)
  - POST /api/renewal-type-distribution (使用 time_period)
  ↓
更新所有图表
  ↓
面板自动折叠，显示已选标签
```

### 5.2 标签移除流程

```
用户点击标签×按钮
  ↓
filterStore.removeFilter(key)
  ↓
立即更新对应状态
  ↓
自动刷新数据（调用 dataStore.refreshAllData()）
  ↓
标签消失，筛选数量更新
```

### 5.3 指标切换流程

```
用户点击"保费"或"件数"
  ↓
appStore.switchMetric(metric)
  ↓
dataStore.refreshAllData() (使用新指标)
  ↓
KPI、图表、饼图全部刷新
  ↓
注意: 指标切换不影响筛选状态
```

---

## 6. API接口

### 6.1 后端接口扩展

**所有POST接口统一支持新参数：**

```python
# Request Body 示例
{
  "time_period": "last7d",              # 新增: 时间段
  "data_scope": "exclude_correction",   # 已有: 数据口径
  "filters": {
    "business_type": "摩托车",          # 新增: 业务类型
    "三级机构": "成都",                 # 已有: 其他筛选
    "是否新能源": "是"
  }
}
```

**受影响的接口：**

1. `POST /api/kpi-windows` - 新增 `time_period`、`business_type` 支持
2. `POST /api/week-comparison` - 新增 `business_type` 支持（不使用 time_period）
3. `POST /api/insurance-type-distribution` - 新增 `time_period`、`business_type` 支持
4. `POST /api/premium-range-distribution` - 新增 `time_period`、`business_type` 支持
5. `POST /api/renewal-type-distribution` - 新增 `time_period`、`business_type` 支持
6. `GET /api/filter-options` - 新增返回"客户类别3"选项

### 6.2 筛选逻辑扩展

**data_processor.py `_apply_filters()` 方法：**

```python
def _apply_filters(self, df, filters):
    """
    应用筛选条件

    新增支持:
    - business_type: 客户类别3 筛选
    """
    if df.empty:
        return df

    result = df.copy()

    # ========== 新增：业务类型筛选 ==========
    if 'business_type' in filters and filters['business_type']:
        if '客户类别3' in result.columns:
            result = result[result['客户类别3'] == filters['business_type']]
        else:
            print(f"警告: 数据中不存在'客户类别3'字段，忽略业务类型筛选")

    # ========== 现有筛选逻辑 (保持不变) ==========
    # 业务员筛选
    if '业务员' in filters and filters['业务员']:
        result = result[result['业务员'] == filters['业务员']]

    # ... 其他筛选逻辑

    return result
```

---

## 7. 交互设计

### 7.1 面板状态

**状态1：首次加载（默认展开）**
- 筛选表单完整显示
- 默认值：时间段=当日，数据口径=不含批改，业务类型=全部
- 指标切换显示在右侧

**状态2：应用筛选后（自动折叠）**
- 筛选表单隐藏
- 显示已选筛选标签（可点击×移除）
- 指标切换保持可见

**状态3：点击展开（重新显示表单）**
- 筛选表单展开
- 保持当前筛选状态
- 可修改后重新应用

### 7.2 标签交互

- **显示条件**：面板折叠 且 有激活筛选
- **格式**：`[标签名: 值 ×]`
- **点击×**：立即移除该筛选并刷新数据
- **样式**：灰色背景、圆角、hover高亮

### 7.3 指标切换

- **位置**：筛选面板右侧，独立区域
- **样式**：按钮组，激活项高亮
- **行为**：点击切换指标，刷新所有图表
- **独立性**：不属于筛选条件，不影响筛选标签

---

## 8. 技术实现

### 8.1 防御性设计

**1. 向后兼容**

```javascript
// 新方法：获取完整全局筛选
const filters = filterStore.getAllGlobalFilters()
// 返回: { time_period: 'day', data_scope: 'exclude_correction', business_type: '', ... }

// 旧方法：仍然可用，不含时间、口径、业务类型
const oldFilters = filterStore.getActiveFilters()
// 返回: { 三级机构: '成都', ... }
```

**2. 错误隔离**

```javascript
async function handleApplyFilters() {
  const snapshot = filterStore.saveSnapshot()

  try {
    // 更新筛选
    await filterStore.applyFilters(newFilters)
    // 刷新数据
    await dataStore.refreshAllData()
    // 成功：折叠面板
    isOpen.value = false
    toast.success('筛选已应用')
  } catch (error) {
    // 失败：回滚状态
    filterStore.restoreSnapshot(snapshot)
    console.error('筛选失败:', error)
    toast.error('筛选失败，已回滚')
  }
}
```

**3. 性能优化**

```javascript
import { debounce } from 'lodash-es'

// 防抖刷新，避免频繁请求
const debouncedRefresh = debounce(async () => {
  await dataStore.refreshAllData()
}, 300)

// 监听筛选变更（标签移除等场景）
watch(
  () => filterStore.getAllGlobalFilters(),
  () => {
    debouncedRefresh()
  },
  { deep: true }
)
```

### 8.2 响应式设计

**桌面端（>768px）：**
- 筛选面板左侧，指标切换右侧（同一行）
- 筛选表单使用 Grid 3列布局
- 标签横向排列

**移动端（≤768px）：**
- 筛选面板与指标切换纵向堆叠
- 筛选表单改为 1列布局
- 标签自动换行

---

## 9. 文件清单

### 9.1 新建文件

- `frontend/src/components/dashboard/GlobalFilterPanel.vue` - 全局筛选组件

### 9.2 修改文件

**后端：**
- `backend/data_processor.py` - 扩展 `_apply_filters()`、`get_filter_options()`
- `backend/api_server.py` - 所有接口支持新参数

**前端：**
- `frontend/src/stores/filter.js` - 扩展状态、getters、actions
- `frontend/src/views/Dashboard.vue` - 使用新组件，调整布局

**文档：**
- `docs/GLOBAL_FILTER_ARCHITECTURE.md` - 本文档（新建）
- `docs/ARCHITECTURE.md` - 更新架构说明
- `docs/API.md` - 更新接口文档（如存在）

---

## 10. 测试清单

### 10.1 功能测试

- [ ] 时间段切换（当日/近7天/近30天）
- [ ] 数据口径切换（不含批改/含批改）
- [ ] 业务类型筛选（10个分类 + 全部）
- [ ] 其他筛选维度（业务员、机构、团队等）
- [ ] 指标切换（保费/件数）
- [ ] 面板折叠/展开
- [ ] 标签移除（点击×）
- [ ] 应用筛选
- [ ] 重置全部
- [ ] 筛选条件联动（业务员→机构/团队）

### 10.2 数据验证

- [ ] KPI 卡片响应筛选
- [ ] 周对比图表响应筛选（不受时间段影响）
- [ ] 饼图响应筛选
- [ ] 数据口径切换正确性
- [ ] 业务类型筛选结果准确性

### 10.3 异常处理

- [ ] 后端接口失败回滚
- [ ] 无效筛选条件拦截
- [ ] 网络错误提示
- [ ] 空数据友好提示

### 10.4 性能测试

- [ ] 筛选应用响应时间 <500ms
- [ ] 标签移除响应时间 <300ms
- [ ] 指标切换响应时间 <500ms
- [ ] 并发请求正常处理

---

## 11. 迁移计划

### 11.1 阶段1：后端准备（无破坏性）
1. 扩展 `_apply_filters()` 支持 `business_type`
2. 扩展 `get_filter_options()` 返回"客户类别3"
3. 所有接口支持可选参数（向后兼容）

### 11.2 阶段2：状态管理扩展（无破坏性）
1. 扩展 `filter.js` 新增状态
2. 保留旧方法 `getActiveFilters()`
3. 新增方法 `getAllGlobalFilters()`

### 11.3 阶段3：组件开发（渐进式）
1. 新建 `GlobalFilterPanel.vue`
2. Dashboard.vue 使用新组件
3. 保留旧代码注释（待验证后删除）

### 11.4 阶段4：测试与切换
1. 测试全局筛选功能
2. 测试指标切换独立性
3. 确认无副作用后删除旧代码

---

## 12. 附录

### 12.1 业务类型分类（客户类别3）

1. 挂车
2. 摩托车
3. 特种车
4. 营业公路客运
5. 营业出租租赁
6. 营业货车
7. 非营业个人客车
8. 非营业企业客车
9. 非营业机关客车
10. 非营业货车

### 12.2 默认值配置

```javascript
const DEFAULT_CONFIG = {
  timePeriod: 'day',
  dataScope: 'exclude_correction',
  businessType: '',
  panelOpen: true  // 首次加载默认展开
}
```

---

**文档结束**
