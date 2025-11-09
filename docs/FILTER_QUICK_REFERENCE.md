# 筛选器架构 - 快速参考指南

## 关键要点速览

### 1. 8个筛选维度
| 维度 | 可选值 | 联动依赖 | 备注 |
|------|------|--------|------|
| 业务员 | 动态 | 自动→机构/团队 | 主筛选维度，选择后禁用机构/团队 |
| 三级机构 | 12个机构 | ←业务员或→团队 | 机构选择后动态过滤团队列表 |
| 团队 | 动态 | ←业务员或←机构 | 依赖机构或业务员选择 |
| 是否续保 | 新保/续保/转保 | 无 | 区分业务类型 |
| 是否新能源 | 是/否 | 无 | 新能源车辆识别 |
| 是否过户车 | 是/否 | 无 | 过户车辆识别 |
| 是否异地车 | 是/否 | 无 | 省外车辆识别 |
| 险种大类 | 车险 | 无 | 当前仅支持车险 |
| 吨位 | 1-10+吨 | 无 | 针对货车分类 |

### 2. 指标与筛选的关系
```
指标切换 (Premium ↔ Count)
    ↓ 独立
筛选条件 (业务员、机构等)
    ↓ 组合
数据口径 (不含批改 ↔ 含批改)
    ↓ 一起
API 请求
```

### 3. 文件路径速查
```
前端:
  - FilterPanel.vue      /frontend/src/components/dashboard/FilterPanel.vue
  - filter.js (Store)    /frontend/src/stores/filter.js
  - Dashboard.vue        /frontend/src/views/Dashboard.vue

后端:
  - api_server.py        /backend/api_server.py
  - data_processor.py    /backend/data_processor.py
  - _apply_filters()     line 907 in data_processor.py
  - get_filter_options() line 354 in data_processor.py

配置:
  - 业务员映射          /业务员机构团队归属.json
  - CSV 数据            /车险清单_2025年10-11月_合并.csv
```

### 4. 工作流程图
```
FilterPanel (UI)
    ↓ localFilters
    ↓ [业务员变化→自动联动]
    ↓ handleApplyFilters()
    ↓
filterStore (Pinia)
    ↓ activeFilters
    ↓ [watch triggered]
    ↓
Dashboard/dataStore
    ↓ refreshChartData()
    ↓ POST /api/kpi-windows + filters
    ↓
后端 _apply_filters()
    ↓
返回聚合数据
    ↓
前端展示 (KPI/图表)
```

### 5. API 端点筛选参数
```javascript
// 所有数据端点支持
{
  "filters": {
    "业务员": "姓名",
    "三级机构": "机构名",
    "团队": "团队名",
    "是否续保": "新保|续保|转保",
    "是否新能源": "是|否",
    "是否过户车": "是|否",
    "是否异地车": "是|否",
    "险种大类": "车险",
    "吨位": "1吨以下|1-2吨|..."
  },
  "data_scope": "exclude_correction|include_correction"
}
```

### 6. 数据口径定义
- **exclude_correction** (默认)：仅正常承保（批单类型为空）
- **include_correction**：全部业务（包括批改、退保等）

### 7. 业务员→机构/团队的解析
```javascript
// 前端调用
const linked = filterStore.resolveByStaff('业务员姓名')
// 返回值
{
  org: '三级机构',
  org4: '四级机构',
  team: '团队简称'
}
```

### 8. 常见问题排查
| 问题 | 可能原因 | 检查方向 |
|------|---------|--------|
| 筛选后无数据 | 筛选条件过严 | 检查映射文件/CSV 字段值 |
| 团队列表为空 | 机构未正确映射 | 检查 inst_team_map 结构 |
| 业务员无法选择 | 未加载筛选选项 | 检查 loadFilterOptions() 调用 |
| 指标切换无效 | 缺少 watch 监听 | 检查 currentMetric 的响应式 |
| 数据口径未生效 | 未传递 data_scope | 检查 getAllFilters() 调用 |

### 9. 关键方法签名
```javascript
// filter.js
filterStore.applyFilters(filters: object)
filterStore.resolveByStaff(name: string) → {org, team}
filterStore.getAllFilters() → {filters, data_scope}

// data.js
dataStore.fetchKpiData(date?: string, filters?: object)
dataStore.fetchChartData(metric: 'premium'|'count', filters: object)
dataStore.refreshPieCharts(period: string, filters: object)
```

### 10. 新增筛选维度的步骤
```
1. CSV 确认新字段存在
2. data_processor.py::get_filter_options() 中追加
3. FilterPanel.vue 中添加 <select> 框
4. data_processor.py::_apply_filters() 中追加过滤逻辑
5. 测试端到端的筛选流程
```

---

## 业务类型字段说明

### 现有相关字段
- **是否续保**：新保、续保、转保（3种，最常用）
- **车险新业务分类**：其他、清亏业务、目标业务、管控业务（4种）
- **终端来源**：柜面、App、B2B、融合销售(电销)、AI出单等（7种）

### 为什么没有"业务类型"字段
当前 CSV 中不存在直接命名为"业务类型"的列，但功能上由以下字段组合实现：
- 业务新旧性：由"是否续保"表示
- 销售渠道类型：由"终端来源"表示
- 业务质量类型：由"车险新业务分类"表示

### 未来规划
若需增加"业务类型"，建议：
1. 在 premium_plan.json 中定义
2. 建立保费计划与业务类型的对应关系
3. 在 FilterPanel 中添加该维度的下拉框
4. 在后端 _apply_filters() 中实现关联查询

---

## 重要提示

1. **业务员是唯一主筛选维度**，其他维度为可选补充
2. **机构和团队联动紧密**，通过映射文件维护，避免不一致
3. **数据口径独立于筛选条件**，两者需同时传递给后端
4. **指标切换与筛选完全解耦**，用户可独立操作
5. **映射冲突会自动校正**，后端以映射文件为准覆盖 CSV 数据

