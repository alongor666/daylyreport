# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

**车险签单数据分析平台 v2.0** - 现代化Web应用，提供实时数据分析和可视化。

**技术栈**:
- **前端**: Vue 3 + Vite + Pinia + ECharts
- **后端**: Flask 3.0 + Pandas
- **支持平台**: macOS, Windows, Linux, 信创系统

---

## 开发命令

### 前端开发

```bash
# 安装前端依赖
npm install

# 启动Vite开发服务器 (http://localhost:5173)
npm run dev

# 构建生产版本
npm run build

# 预览生产构建
npm run preview

# 代码检查和格式化
npm run lint
```

### 后端开发

**安装Python依赖**:
```bash
# macOS/Linux
pip3 install -r requirements.txt

# Windows
pip install -r requirements.txt

# 信创系统/国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

**启动后端API服务器**:
```bash
# Windows
cd backend
python api_server.py

# macOS/Linux
cd backend
python3 api_server.py

# 使用虚拟环境
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
cd backend
python api_server.py
```

后端API默认运行在 `http://localhost:5001`

### 全栈开发

**开发模式** (前后端同时运行):
```bash
# 终端1: 启动后端
cd backend && python3 api_server.py

# 终端2: 启动前端
npm run dev
```

访问 `http://localhost:5173` 使用Vite开发服务器，API请求自动代理到后端。

---

## 架构概览

### 整体架构

```
┌──────────────────────────────────────────────┐
│           Vue 3 SPA (Vite)                   │
│  ┌────────────┬────────────┬──────────────┐  │
│  │ Components │  Stores    │  Services    │  │
│  │            │  (Pinia)   │  (Axios)     │  │
│  └────────────┴────────────┴──────────────┘  │
├──────────────────────────────────────────────┤
│           Flask REST API                     │
│  ┌────────────────────────────────────────┐  │
│  │  api_server.py (路由层)                │  │
│  │  data_processor.py (业务逻辑)          │  │
│  └────────────────────────────────────────┘  │
├──────────────────────────────────────────────┤
│           Data Layer                         │
│  ┌────────────────────────────────────────┐  │
│  │  Pandas (数据处理)                     │  │
│  │  CSV/Excel (数据存储)                  │  │
│  └────────────────────────────────────────┘  │
└──────────────────────────────────────────────┘
```

### 前端目录结构

```
src/
├── components/          # Vue组件
│   ├── common/         # 通用组件
│   │   ├── Toast.vue
│   │   ├── Loading.vue
│   │   └── DatePicker.vue
│   ├── dashboard/      # 仪表板组件
│   │   ├── KpiCard.vue
│   │   ├── ChartView.vue
│   │   └── FilterPanel.vue
│   └── layout/         # 布局组件
│       ├── Header.vue
│       └── Container.vue
├── stores/             # Pinia状态管理
│   ├── app.js          # 应用全局状态
│   ├── filter.js       # 筛选器状态
│   └── data.js         # 数据状态
├── services/           # API服务层
│   ├── api.js          # Axios配置
│   └── dataService.js  # 数据API
├── utils/              # 工具函数
│   ├── format.js       # 格式化函数
│   └── chart.js        # 图表配置
├── assets/             # 静态资源
│   └── styles/         # 样式文件
│       ├── variables.css  # CSS变量
│       ├── reset.css      # 样式重置
│       └── main.css       # 主样式
├── App.vue             # 根组件
└── main.js             # 应用入口
```

### 后端结构

```
backend/
├── api_server.py       # Flask应用入口和路由
├── data_processor.py   # 数据处理核心逻辑
└── config.py           # 配置文件 (新增)
```

### 数据流

```
用户操作 → Vue组件 → Pinia Store → API Service
                                        ↓
                                   Axios请求
                                        ↓
                                  Flask路由
                                        ↓
                                 DataProcessor
                                        ↓
                                  Pandas处理
                                        ↓
                                  JSON响应
                                        ↓
Store更新 ← API Service ← Flask响应
    ↓
组件响应式更新 → 用户看到变化
```

---

## 核心功能实现

### 前端核心组件

#### 1. Dashboard (主仪表板)
**文件**: `src/views/Dashboard.vue`

**职责**:
- 布局KPI卡片和图表
- 协调各组件通信
- 处理数据刷新

**状态依赖**:
- `dataStore` - 获取KPI和图表数据
- `filterStore` - 获取筛选条件

#### 2. KpiCard (KPI卡片)
**文件**: `src/components/dashboard/KpiCard.vue`

**Props**:
```javascript
{
  title: String,       // 标题
  value: Number,       // 当前值
  trend: Number,       // 趋势百分比
  sparklineData: Array // 7天趋势数据
}
```

**功能**:
- 显示KPI指标
- 渲染迷你趋势图(sparkline)
- 显示同比增长率
- 点击展开详情(未来)

#### 3. ChartView (图表组件)
**文件**: `src/components/dashboard/ChartView.vue`

**Props**:
```javascript
{
  chartData: Object,   // ECharts配置
  loading: Boolean,    // 加载状态
  height: String       // 图表高度
}
```

**功能**:
- ECharts图表渲染
- 响应式尺寸调整 (debounced)
- 平滑过渡动画
- 悬停交互

#### 4. FilterPanel (筛选面板)
**文件**: `src/components/dashboard/FilterPanel.vue`

**功能**:
- 多维度筛选UI
- 折叠/展开动画
- 标签显示已选条件
- 应用筛选/重置

---

### 后端API端点

#### GET /api/kpi-windows
获取KPI三口径数据(当日/近7天/近30天)

**Query参数**:
- `date` (optional): 指定日期 (YYYY-MM-DD)

**响应**:
```json
{
  "success": true,
  "data": {
    "anchor_date": "2025-11-05",
    "premium": {
      "day": 205000,
      "last7d": 1452000,
      "last30d": 5800000
    },
    "policy_count": { "day": 120, "last7d": 850, "last30d": 3400 },
    "commission": { "day": 15000, "last7d": 105000, "last30d": 420000 },
    "target_gap_day": 5000
  }
}
```

#### POST /api/week-comparison
获取周对比图表数据

**Request Body**:
```json
{
  "metric": "premium",  // 或 "count"
  "filters": {
    "三级机构": "成都",
    "是否新能源": "是"
  },
  "date": "2025-11-05"  // optional
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "x_axis": ["周五", "周六", "周日", "周一", "周二", "周三", "周四"],
    "series": [
      {
        "name": "最近7天 (10/29-11/04)",
        "data": [180000, 150000, 120000, 200000, 220000, 190000, 205000],
        "dates": ["2025-10-31", "2025-11-01", ..., "2025-11-05"]
      },
      {
        "name": "上个7天 (10/22-10/28)",
        "data": [175000, 145000, 115000, 195000, 210000, 185000, 200000],
        "dates": [...]
      },
      {
        "name": "前个7天 (10/15-10/21)",
        "data": [170000, 140000, 110000, 190000, 205000, 180000, 195000],
        "dates": [...]
      }
    ],
    "latest_date": "2025-11-05"
  }
}
```

#### GET /api/filter-options
获取所有筛选维度的可选值

**响应**:
```json
{
  "success": true,
  "data": {
    "三级机构": ["成都", "德阳", "达州", ...],
    "团队": ["成都业务一部", "成都业务二部", ...],
    "机构团队映射": {
      "成都": ["成都业务一部", "成都业务二部"],
      "德阳": ["德阳业务一部"]
    },
    "是否续保": ["新保", "续保", "转保"],
    "是否新能源": ["是", "否"],
    "是否过户车": ["是", "否"],
    "险种大类": ["交强", "商业", "交商"],
    "吨位": ["2吨以下", "2-5吨", "5吨以上"]
  }
}
```

#### POST /api/refresh
刷新数据 (处理新Excel文件)

**响应**:
```json
{
  "success": true,
  "message": "数据刷新成功",
  "latest_date": "2025-11-05"
}
```

---

## 状态管理 (Pinia)

### appStore (应用状态)
**文件**: `src/stores/app.js`

```javascript
{
  loading: false,        // 全局加载状态
  latestDate: null,      // 最新数据日期
  selectedDate: null,    // 用户选择的日期
  currentMetric: 'premium'  // 当前指标 (premium/count)
}
```

**Actions**:
- `setLoading(bool)` - 设置加载状态
- `setSelectedDate(date)` - 设置选择日期
- `switchMetric(metric)` - 切换指标

### filterStore (筛选状态)
**文件**: `src/stores/filter.js`

```javascript
{
  filterOptions: {},     // 所有筛选选项
  activeFilters: {},     // 当前激活的筛选条件
  filterPanelOpen: false // 筛选面板展开状态
}
```

**Actions**:
- `loadFilterOptions()` - 加载筛选选项
- `applyFilter(key, value)` - 应用单个筛选
- `resetFilters()` - 重置所有筛选
- `togglePanel()` - 切换面板状态

### dataStore (数据状态)
**文件**: `src/stores/data.js`

```javascript
{
  kpiData: null,         // KPI数据
  chartData: null,       // 图表数据
  loading: false         // 数据加载状态
}
```

**Actions**:
- `fetchKpiData(date)` - 获取KPI数据
- `fetchChartData(filters)` - 获取图表数据
- `refreshData()` - 刷新所有数据

---

## 设计系统

### CSS变量定义
**文件**: `src/assets/styles/variables.css`

```css
:root {
  /* 主色 */
  --primary-50: #EFF6FF;
  --primary-500: #3B82F6;
  --primary-700: #1D4ED8;

  /* 功能色 */
  --success-500: #10B981;
  --warning-500: #F59E0B;
  --error-500: #EF4444;

  /* 中性色 */
  --gray-50: #F9FAFB;
  --gray-100: #F3F4F6;
  --gray-500: #6B7280;
  --gray-900: #111827;

  /* 字体 */
  --font-family: -apple-system, BlinkMacSystemFont, "Segoe UI",
                 "Microsoft YaHei", sans-serif;
  --font-size-xs: 12px;
  --font-size-sm: 14px;
  --font-size-base: 16px;
  --font-size-lg: 20px;
  --font-size-xl: 24px;

  /* 间距 */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-6: 24px;
  --space-8: 32px;

  /* 圆角 */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-full: 9999px;

  /* 阴影 */
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
}
```

### 组件命名规范
使用BEM (Block Element Modifier) 命名法:

```css
/* Block */
.kpi-card {}

/* Element */
.kpi-card__title {}
.kpi-card__value {}
.kpi-card__trend {}

/* Modifier */
.kpi-card--loading {}
.kpi-card__trend--up {}
.kpi-card__trend--down {}
```

---

## 开发规范

### Vue组件规范

1. **组件命名**: PascalCase (如 `KpiCard.vue`)
2. **Props定义**: 必须定义类型和默认值
3. **Emit事件**: 使用kebab-case (如 `update:value`)
4. **样式**: 使用scoped样式 + CSS变量

**示例**:
```vue
<script setup>
const props = defineProps({
  title: {
    type: String,
    required: true
  },
  value: {
    type: Number,
    default: 0
  }
})

const emit = defineEmits(['refresh', 'click'])
</script>

<template>
  <div class="kpi-card">
    <h3 class="kpi-card__title">{{ title }}</h3>
    <div class="kpi-card__value">{{ value }}</div>
  </div>
</template>

<style scoped>
.kpi-card {
  padding: var(--space-4);
  border-radius: var(--radius-lg);
  background: white;
}
</style>
```

### API服务规范

**文件**: `src/services/dataService.js`

```javascript
import api from './api'

export const dataService = {
  // 获取KPI数据
  async getKpiData(date = null) {
    const params = date ? { date } : {}
    const { data } = await api.get('/api/kpi-windows', { params })
    return data
  },

  // 获取图表数据
  async getChartData(payload) {
    const { data } = await api.post('/api/week-comparison', payload)
    return data
  }
}
```

### 错误处理规范

**Toast通知** - 替代alert():
```javascript
import { useToast } from '@/composables/useToast'

const toast = useToast()

try {
  await fetchData()
  toast.success('数据加载成功')
} catch (error) {
  toast.error(`加载失败: ${error.message}`)
}
```

---

## 性能优化

### 前端优化

1. **懒加载路由**:
```javascript
const Dashboard = () => import('./views/Dashboard.vue')
```

2. **图表resize防抖**:
```javascript
import { useDebounceFn } from '@vueuse/core'

const handleResize = useDebounceFn(() => {
  chart.resize()
}, 300)
```

3. **虚拟滚动** (大量数据时):
```vue
<virtual-list :data="items" :item-height="50" />
```

### 后端优化

1. **数据缓存** (Redis - 未来):
```python
@cache.memoize(timeout=300)
def get_filter_options():
    # 缓存5分钟
    pass
```

2. **分页查询**:
```python
def get_data(page=1, per_page=100):
    offset = (page - 1) * per_page
    return df.iloc[offset:offset+per_page]
```

---

## 测试

### 单元测试 (Vitest)

**安装**:
```bash
npm install -D vitest @vue/test-utils
```

**示例**:
```javascript
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import KpiCard from '@/components/KpiCard.vue'

describe('KpiCard', () => {
  it('renders title correctly', () => {
    const wrapper = mount(KpiCard, {
      props: { title: '签单保费', value: 200000 }
    })
    expect(wrapper.text()).toContain('签单保费')
  })
})
```

### E2E测试 (Cypress - 未来)

```javascript
describe('Dashboard', () => {
  it('loads KPI data', () => {
    cy.visit('/')
    cy.get('.kpi-card').should('have.length', 4)
  })
})
```

---

## 部署

### 开发环境
```bash
# 前端
npm run dev

# 后端
cd backend && python3 api_server.py
```

### 生产环境

**前端构建**:
```bash
npm run build
# 生成 dist/ 目录
```

**后端部署**:
```bash
# 使用Gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 backend.api_server:app
```

**Nginx配置**:
```nginx
server {
  listen 80;

  # 前端静态文件
  location / {
    root /path/to/dist;
    try_files $uri $uri/ /index.html;
  }

  # API代理
  location /api/ {
    proxy_pass http://localhost:5001;
  }
}
```

---

## 故障排查

### 常见问题

**问题1: Vite开发服务器无法连接后端API**

解决方案:
```javascript
// vite.config.js
export default {
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:5001',
        changeOrigin: true
      }
    }
  }
}
```

**问题2: macOS AirPlay占用5000端口**

解决方案: 后端已改用5001端口 (见 `backend/api_server.py:229`)

**问题3: npm install失败**

解决方案:
```bash
# 清除缓存
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

---

## 相关文档

- [PRD.md](docs/PRD.md) - 产品需求文档
- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - 详细架构设计
- [DESIGN_SYSTEM.md](docs/DESIGN_SYSTEM.md) - 设计系统规范
- [MIGRATION_GUIDE.md](docs/MIGRATION_GUIDE.md) - v1到v2迁移指南
- [CHANGELOG.md](CHANGELOG.md) - 版本更新日志

---

## 版本信息

- **当前版本**: 2.0.0-dev
- **发布日期**: 2025-11-07
- **兼容性**: Chrome 90+, Edge 90+, Firefox 88+, Safari 14+
