# 筛选器架构完整探索报告

## 1. 当前筛选维度总览

### 前端筛选面板的筛选维度 (FilterPanel.vue)

当前实现的 **8 个筛选维度**：

1. **业务员** (主维度)
   - 说明：主要筛选维度，选择后自动联动"三级机构"和"团队"
   - 数据源：来自 filterOptions['业务员']
   - 联动逻辑：通过 resolveByStaff() 自动获取关联的机构和团队
   
2. **三级机构**
   - 说明：选择后会禁用"团队"字段（除非同时选了业务员），需要选择该机构对应的团队
   - 取值：12个机构（天府、乐山、宜宾、德阳、新都等）
   - 依赖关系：与团队有联动映射关系

3. **团队** (联动)
   - 说明：需依赖"三级机构"的选择，或通过"业务员"自动填充
   - 禁用条件：未选三级机构或已选业务员时
   - 数据源：filterOptions['团队']，通过 teamOptions computed 动态过滤

4. **是否续保**
   - 取值：新保、续保、转保
   - 说明：标识保单的续保状态

5. **是否新能源**
   - 取值：是、否
   - 说明：标识车辆是否为新能源

6. **是否过户车**
   - 取值：是、否
   - 说明：标识保单是否为过户车

7. **是否异地车** (新增, 2025-11-09)
   - 取值：是、否
   - 说明：标识车辆是否为异地车（省内/省外）
   - 后端支持：已在 _apply_filters() 中实现 (line 1016)

8. **险种大类**
   - 取值：车险（主要）
   - 说明：选择险种分类

9. **吨位** (实际为吨位分段)
   - 取值：1吨以下、1-2吨、2-5吨、5-9吨、9-10吨、10吨以上
   - 说明：针对货车的吨位分类

### 后端返回的可选值结构 (get_filter_options)

```javascript
{
  '三级机构': [...],           // 12个机构
  '团队': [...],               // 所有团队列表
  '是否续保': ['新保', '续保', '转保'],
  '是否新能源': ['是', '否'],
  '是否过户车': ['是', '否'],
  '是否异地车': ['是', '否'],  // 新增
  '险种大类': ['车险'],
  '吨位': ['1吨以下', '1-2吨', ...],
  '是否电销': ['全部', '是', '否'],
  '机构团队映射': {...},       // 机构→团队的映射关系
  '保单号': [...]              // 所有保单号列表
}
```

## 2. 指标切换与筛选的耦合关系

### 指标切换的独立性

**指标切换 (Premium vs Count) 与筛选器 NOT 耦合**

- 位置：Dashboard.vue 的 KPI 区域顶部有"全局指标切换"按钮
- 控制状态：appStore.currentMetric ('premium' | 'count')
- 工作原理：
  1. 指标切换只改变 appStore.currentMetric
  2. 数据刷新时，将当前指标传给 fetchChartData()
  3. 筛选器保持不变，只是数据以不同指标聚合
  4. 后端同时支持两种指标的计算

### 筛选与指标的关系

- **数据口径** (Data Scope) 与筛选分离：
  - 数据口径：exclude_correction (不含批改) vs include_correction (含批改)
  - 在 filterStore 中维护：dataScope state (line 26 in filter.js)
  - 每次请求时通过 getAllFilters() 合并到载荷

```javascript
{
  filters: { '业务员': 'xxx', ... },
  data_scope: 'exclude_correction'  // 单独传递
}
```

## 3. 筛选器使用的页面与组件

### 直接使用

1. **Dashboard.vue**
   - 位置：/views/Dashboard.vue
   - 使用方式：
     - FilterPanel 组件 (line 107)
     - 监听 filterStore.activeFilters 变化 (line 518-524)
     - 在数据刷新时传递筛选条件

2. **FilterPanel.vue** (核心筛选界面)
   - 组件化筛选UI
   - 支持展开/收起
   - 显示活跃筛选标签
   - 支持快速清空或单个移除

### 数据流向

```
FilterPanel
    ↓ (applyFilters)
filterStore.activeFilters (Pinia)
    ↓ (watch)
Dashboard (refreshPieChartsData)
    ↓ (getActiveFilters)
dataStore.fetchChartData() / fetchKpiData() / refreshPieCharts()
    ↓ (API请求)
后端处理 (_apply_filters)
    ↓
返回筛选后的聚合数据
```

## 4. 后端API与筛选参数支持

### 关键API端点

#### POST /api/kpi-windows (KPI数据)
```javascript
// 请求体
{
  filters: {
    '业务员': 'xxx',
    '三级机构': 'xxx',
    '团队': 'xxx',
    '是否续保': 'xxx',
    '是否新能源': 'xxx',
    '是否过户车': 'xxx',
    '是否异地车': 'xxx',  // 新增支持
    '险种大类': 'xxx',
    '吨位': 'xxx'
  },
  data_scope: 'exclude_correction'
}
```

#### POST /api/week-comparison (周对比数据)
- 同样支持上述所有筛选条件

#### GET /api/filter-options (筛选选项)
- 返回所有可用的筛选维度值和映射关系
- **核心数据**：机构团队映射 (inst_team_map_sorted)

### 后端筛选实现 (_apply_filters)

**执行顺序**（data_processor.py, line 907）：
1. 保单号筛选（唯一标识）→ 强制同步业务员/机构/团队
2. 业务员筛选（通过名字->工号查询）
3. 三级机构筛选（通过业务员映射反向查询）
4. 团队筛选（通过业务员映射反向查询）
5. 是否续保 → 是否新能源 → 是否过户车 → 险种大类 → 吨位
6. 电销筛选（终端来源 = '0110融合销售'）
7. 异地车筛选（直接对 '是否异地车' 字段过滤）

**关键映射逻辑**：
- 业务员 → 机构/团队：通过 staff_mapping (业务员机构团队归属.json)
- 机构 ← → 团队：通过业务员的反向查询

## 5. 业务类型相关字段分析

### CSV数据中的业务类型字段

根据字段分析文档，**没有找到直接命名为"业务类型"的字段**，但存在以下相关字段：

1. **是否续保** (车险新业务分类的扩展)
   - 新保、续保、转保 (3种)
   - 用于区分新老客户的业务类型

2. **车险新业务分类**
   - 其他、清亏业务、目标业务、管控业务 (4种)
   - 按业务质量/策略分类

3. **终端来源** (销售渠道)
   - 0101柜面、0106移动展业(App)、0107B2B、**0110融合销售(电销)**、0112AI出单、0201PC、0202APP
   - 用于识别销售渠道（电销 vs 非电销）

4. **新旧车标志**
   - N新车、O旧车
   - 标识车辆是否为新车

### 未来可能的"业务类型"扩展

根据开发文档 (PRD-best.md)，计划支持：
- 业务类型作为保费计划匹配的一个维度
- 字段来自：premium_plan.json 中的 `业务类型` 字段
- 但当前 CSV 数据中尚未包含此字段

## 6. 筛选器核心机制解析

### 筛选数据流（前端 → 后端）

#### 前端处理 (FilterPanel.vue + filter.js)

```javascript
// 1. 用户在 FilterPanel 中操作
localFilters['业务员'] = '某业务员'  // 本地状态

// 2. 点击"应用筛选"时
handleApplyFilters() {
  // 依据业务员联动同步机构/团队
  const linked = filterStore.resolveByStaff('某业务员')
  filtersToApply['三级机构'] = linked.org
  filtersToApply['团队'] = linked.team
  
  // 应用到全局状态
  filterStore.applyFilters(filtersToApply)
  
  // 刷新数据
  dataStore.refreshChartData()
}

// 3. 数据刷新时
refreshChartData() {
  const filters = filterStore.getActiveFilters()
  // 同时获取数据口径
  const allFilters = filterStore.getAllFilters()
  // 发送请求
  await fetchKpiData(filters)
}
```

#### 后端处理 (data_processor.py)

```python
# 1. 接收筛选条件
def get_kpi_windows(self, date=None, filters=None, data_scope='exclude_correction'):
    df = pd.read_csv(...)
    
    # 2. 应用数据口径过滤
    df = self._apply_data_scope_filter(df, data_scope)
    
    # 3. 应用业务筛选
    df = self._apply_filters(df, filters)
    
    # 4. 聚合计算
    # 计算 premium, policy_count, commission, ratios 等
    
    # 5. 验证映射一致性
    validation = self._validate_policy_consistency(df)
```

### 特殊联动机制

#### 业务员 → 机构/团队的强制联动

```javascript
// FilterPanel.vue, line 340-357
if (key === '业务员') {
  const staff = localFilters.value['业务员']
  if (staff) {
    const linked = filterStore.resolveByStaff(staff)
    localFilters.value['三级机构'] = linked.org
    localFilters.value['团队'] = linked.team
  } else {
    // 清除
    localFilters.value['三级机构'] = ''
    localFilters.value['团队'] = ''
  }
}
```

**效果**：
- 选择业务员时，自动确定其所属机构和团队，防止不一致
- UI上，机构和团队字段变为 disabled (line 74, 94)

#### 机构选择 → 团队动态过滤

```javascript
// filter.js, line 74-84
const teamOptions = computed(() => {
  const selectedOrg = activeFilters.value['三级机构']
  const orgTeamMap = filterOptions.value['机构团队映射'] || {}
  
  if (selectedOrg && orgTeamMap[selectedOrg]) {
    return orgTeamMap[selectedOrg]  // 仅返回该机构的团队
  }
  return filterOptions.value['团队'] || []  // 返回全部团队
})
```

## 7. 状态管理结构

### filter.js (Pinia Store)

```javascript
State:
  - filterOptions          // 所有筛选选项
  - activeFilters          // 当前激活的筛选（应用后）
  - panelOpen              // 筛选面板展开/收起
  - dataScope              // 数据口径 (exclude_correction | include_correction)
  - policyMapping          // 保单号→业务员→机构/团队 映射

Getters:
  - hasActiveFilters       // 是否有活跃筛选
  - activeFiltersCount     // 活跃筛选数量
  - filterTags             // 格式化的标签列表
  - teamOptions            // 动态过滤的团队选项
  - getOptions(dimension)  // 获取特定维度的选项

Actions:
  - loadFilterOptions()    // 从后端加载选项
  - applyFilter(key, value)
  - applyFilters(filters)  // 批量应用
  - removeFilter(key)
  - resetFilters()
  - resolveByPolicy(policyNo)    // 保单号→业务员/机构/团队
  - resolveByStaff(name)         // 业务员→机构/团队
  - setDataScope(scope)
  - getAllFilters()        // 返回 {filters, data_scope}
```

### app.js (全局应用状态)

```javascript
State:
  - currentMetric     // 'premium' | 'count'
  - latestDate        // 最新数据日期

Actions:
  - switchMetric(metric)  // 切换全局指标
  - setLatestDate(date)
```

## 8. 数据流完整图示

```
用户操作 (FilterPanel)
    ↓
localFilters (组件本地状态)
    ↓
[业务员自动联动] → 更新 三级机构/团队
    ↓
点击"应用筛选"
    ↓
handleApplyFilters()
    ↓
    ├─ 过滤空值
    ├─ 业务员联动补充机构/团队
    └─ 调用 filterStore.applyFilters(filtersToApply)
        ↓
        [全局状态更新]
        activeFilters = filtersToApply
        ↓
        [触发 watch]
        Dashboard 监听到 activeFilters 变化
        ↓
        refreshPieChartsData()
        ↓
        dataStore.refreshPieCharts()
        ↓
        [构建请求载荷]
        {
          filters: filterStore.getActiveFilters(),
          data_scope: filterStore.getDataScope()
        }
        ↓
        POST /api/pie-charts (或其他数据端点)
        ↓
        [后端处理]
        _apply_filters(df, filters)  // 应用8个维度的过滤
        _apply_data_scope_filter(df, data_scope)  // 应用数据口径
        ↓
        [聚合并返回]
        返回筛选后的统计结果
        ↓
        [前端展示]
        图表/KPI 卡更新
        活跃筛选标签更新
```

## 9. 关键设计特点

### 1. 弱耦合的指标切换
- 指标只影响数据聚合方式，不影响筛选条件
- 每个组件独立消费 appStore.currentMetric

### 2. 映射驱动的业务员筛选
- 业务员→机构/团队通过 staff_mapping 文件维护
- 防止不一致的组织结构选择

### 3. 三层筛选体系
- **UI层**：FilterPanel 组件，本地 localFilters 状态
- **业务层**：filterStore 管理全局筛选状态和映射关系
- **数据层**：后端 _apply_filters 执行实际数据过滤

### 4. 双向联动防护
- 选业务员 → 自动设机构/团队
- 选机构 → 动态过滤团队列表
- 选机构后 → 禁用团队变更

### 5. 数据口径隔离
- 数据口径 (批改与否) 与业务筛选分离
- 通过 data_scope 参数独立传递

## 10. 后续扩展建议

### 短期 (已规划)
- "是否异地车" 筛选 ✓ (已实现)
- 商业险/交强险占比 KPI (需后端支持)

### 中期 (计划中)
- "业务类型"维度 (需补充数据源)
- 保费计划管理 (premium_plan.json)
- 保单详情查询接口

### 长期
- 自定义筛选组合保存
- 动态筛选维度配置
- 多维度交叉分析

