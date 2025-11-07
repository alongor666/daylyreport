# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

车险签单数据分析Web应用，自动处理每日Excel报表，清洗数据并通过交互式仪表板可视化趋势。系统采用Python Flask后端 + 原生JavaScript前端架构。

## 开发命令

### 启动服务器

```bash
# 从项目根目录
start_server.bat

# 或手动启动
cd backend
python api_server.py
```

服务运行在 `http://localhost:5000`，前端访问 `http://localhost:5000/static/index.html`。

### 测试数据处理

```bash
# 从项目根目录
cd backend
python data_processor.py
```

这将扫描 `data/` 目录，处理新Excel文件，与现有数据合并，并输出测试报告。

### 安装依赖

```bash
pip install -r requirements.txt
```

## 架构概览

### 数据流管道

1. **Excel导入** (`data/` 目录)
   - 新Excel文件放入 `data/` 文件夹
   - 系统扫描 `*.xlsx` 和 `*.xls` 文件

2. **数据处理** (`backend/data_processor.py`)
   - `DataProcessor` 类处理所有数据操作
   - 数据清洗：日期标准化、数值转换、缺失值处理
   - 基于保单号+投保确认时间去重
   - 与现有CSV合并 (`车险清单_2025年10-11月_合并.csv`)
   - 处理后的文件移至 `data/processed/` 并加时间戳

3. **API层** (`backend/api_server.py`)
   - Flask REST API提供处理后的数据
   - 返回格式为 `{success: bool, data: ...}` 的JSON响应

4. **前端可视化** (`static/`)
   - 原生JS，无框架依赖
   - ECharts交互式图表
   - 从API获取数据并动态渲染

### 核心组件

**后端 (`backend/`):**
- `data_processor.py`: 核心数据处理逻辑
  - `DataProcessor` 类，包含Excel处理、查询、筛选方法
  - `get_daily_report()`: 返回指定日期的KPI指标
  - `get_week_trend()`: 返回7天或21天趋势数据
  - `get_week_comparison()`: 返回3个周期对比（最近、上个、前个7天周期）
  - `get_filter_options()`: 提取筛选器下拉框的唯一值
  - `_apply_filters()`: 对数据集应用多维度筛选

- `api_server.py`: Flask API端点
  - `POST /api/refresh`: 触发数据处理管道
  - `GET /api/daily-report`: 日报KPI数据
  - `GET /api/week-trend`: 周趋势数据
  - `POST /api/week-comparison`: 带筛选的3周期对比
  - `GET /api/filter-options`: 可用筛选值
  - `GET /api/latest-date`: 最新数据日期
  - `GET /api/health`: 健康检查

**前端 (`static/`):**
- `index.html`: 单页应用结构，筛选控件，图表容器
- `css/style.css`: 紫色渐变主题，响应式布局，卡片UI
- `js/app.js`: 应用逻辑
  - ECharts图表渲染
  - 筛选器管理和应用
  - 指标切换（保费 vs 保单件数）
  - 数据刷新工作流

**配置文件:**
- `业务员机构团队归属.json`: 业务员到机构团队的映射，用于按组织/团队筛选
  - 结构: `{"工号姓名": {"三级机构": "...", "四级机构": "...", "团队简称": "..."}}`
  - 被 `_apply_filters()` 用于将业务员姓名映射到组织单位

### 数据结构

**主数据集 (`车险清单_2025年10-11月_合并.csv`):**
- 主数据存储，持续追加
- 关键字段:
  - `投保确认时间`: 保单确认时间戳（用于日期筛选）
  - `签单/批改保费`: 保费金额
  - `签单数量`: 保单数量
  - `手续费含税`: 含税手续费
  - `保单号`: 保单号（用于去重）
  - `业务员`: 业务员姓名
  - `车险新业务分类`: 新转续分类
  - `是否新能源`: 能源类型
  - `是否过户车`: 过户车标记
  - `险种大类`: 险种类别
  - `吨位分段`: 吨位分段
  - `终端来源`: 来源渠道（用于识别电销"0110融合销售"）

### 关键实现细节

**日期处理:**
- 所有日期操作使用 pandas `pd.to_datetime()` 配合 `errors='coerce'`
- 日期比较使用 `.date()` 对象，而非datetime以避免时区问题
- 周对比使用基于最新日期的7天滚动窗口

**去重逻辑:**
- 组合键: `(保单号, 投保确认时间)`
- 使用 `drop_duplicates(keep='last')` 保留最新记录

**筛选应用:**
- 机构/团队筛选通过业务员映射JSON查找
- 使用正则 `[\u4e00-\u9fa5]+` 从映射键提取业务员姓名
- 筛选条件采用AND组合（所有激活的筛选器必须匹配）
- "全部"值表示该维度不应用筛选

**周对比X轴:**
- X轴显示从最近7天周期第一天开始的星期名称（周一-周日）
- 非固定的周一到周日，而是动态对齐数据（例如，如果最新数据是周四，显示周五→周四）
- 使用 `weekday_index = (date - period_start).days` 计算

**保单件数 vs 保费:**
- 保费: `签单/批改保费` 列求和
- 保单件数: `签单/批改保费 >= 50` 的记录数（过滤低值批改）

## 修改系统

### 修改日目标

编辑 `backend/data_processor.py` 第206行附近:

```python
daily_target = 200000  # 修改此值
```

### 添加新筛选维度

1. 更新 `data_processor.py` 中的 `get_filter_options()` 提取新维度值
2. 在 `static/index.html` 添加筛选控件
3. 更新 `static/js/app.js` 中的 `currentFilters` 对象
4. 在 `_apply_filters()` 方法添加筛选逻辑

### 修改服务器端口

编辑 `backend/api_server.py` 第211行:

```python
app.run(host='0.0.0.0', port=5000, debug=True)  # 修改端口
```

### 添加新API端点

1. 在 `backend/api_server.py` 添加路由处理器
2. 如需要，在 `DataProcessor` 类实现数据查询方法
3. 遵循现有模式: 返回 `{'success': bool, 'data': ..., 'message': ...}`

## 重要约束

- Excel文件必须符合预期模式（标准签单清单格式）
- CSV编码为 `utf-8-sig`（带BOM）以兼容Excel
- Windows特定: 通过 `pathlib.Path` 使用 `\` 路径分隔符
- 数据文件被Git忽略（除映射JSON外）
- 系统期望Excel文件中的字段名为中文
- Pandas可能对69-73列显示DtypeWarning（混合类型）- 这是正常的，读取CSV时使用 `low_memory=False`

## 文件路径

- 项目根目录: `backend/` 的父目录
- 主数据CSV: `{project_root}/车险清单_2025年10-11月_合并.csv`
- 业务员映射: `{project_root}/业务员机构团队归属.json`
- Excel输入: `{project_root}/data/*.xlsx`
- 已处理归档: `{project_root}/data/processed/`
- 前端资源: `{project_root}/static/`

`DataProcessor` 中的所有路径都使用 `Path(__file__).parent.parent` 相对于项目根目录构建。
