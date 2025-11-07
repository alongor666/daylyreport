# 本地车险日报可视化（Flask + ECharts）

## 概述
- 目的：从本地Excel（xlsx）车险保/批单清单读取数据，生成管理视角的现代化可视化看板。
- 技术栈：后端 Flask 提供API；前端 ECharts + 原生JS；UI为苹果发布会风格深色极简。

## 运行
- 准备虚拟环境并安装依赖：
  - `python3 -m venv .venv`
  - `./.venv/bin/pip install flask flask-cors pandas openpyxl xlrd python-dateutil`
- 启动：
  - `./.venv/bin/python web_dashboard/app.py`
  - 浏览器打开 `http://127.0.0.1:8000/`
- 切换输入目录（可选）：
  - `export REPORT_INPUT_DIR="/你的xlsx目录"`

## 数据来源
- 默认扫描工作目录中的 `保批单业务报表-YYYYMMDD.xlsx` 文件，忽略 `混乱/` 子目录。
- 日期范围自动从文件名解析，可在页面通过日期框选择区间。

## 指标口径与单位
- 所有保费在前端显示为“万元”（÷10000），保留两位小数。
- KPI定义：
  - `净保费`：按签单保费（原保为正，批单净额为正/负）合计。
  - `原保保费`：原保合计。
  - `批单保费净额`：批单净额合计（含正负）。
  - `商/交占比`：商业/交强保费占净保费比例。
  - 件数：原保件数、批单件数、总件数。

## 页面功能
- 日期选择与刷新。
- KPI卡片：净保费、原保保费、批单净额、总件数、商/交占比。
- 图表：
  - `净保费趋势（万元）`
  - `原保与批单保费（万元）`
  - `交强 vs 商业（万元）`
  - `月度净保费对比（万元）`
  - `机构Top10（万元）`、`渠道Top10（万元）`（含数值标签）
- 数据质量检查：负保费与重复保单号弹窗表格。

## API说明
- `GET /api/meta`：文件数与最小/最大日期。
- `GET /api/daily?start=YYYY-MM-DD&end=YYYY-MM-DD`：每日粒度指标列表。
- `GET /api/dim?type=org|channel|risk&start=...&end=...`：维度聚合。
- `GET /api/kpi?start=...&end=...`：区间KPI对象。
- `GET /api/quality?start=...&end=...`：质量检查结果对象（negative/duplicates/duplicate_count）。
- `GET /api/monthly?start=...&end=...`：月度净保费列表（字段：月份、签单保费）。

## 设计风格
- 深色极简，减少视觉噪音，突出数据本身；控件与图表统一中文、单位“万元”。

## 常见调整
- 列名不匹配：在 `local_xlsx_reporting/generate_daily_report.py` 的 `COLUMN_SYNONYMS` 中补充映射。
- 批单符号规则：如需更细粒度规则，可在该脚本中调整 `assign_signed_premium` 逻辑。
- 维度扩展：按机构层级或渠道层级进一步聚合，可扩展后端 `aggregate_dimensions` 并增加新图表。

## 更新说明
- 本README作为活文档，随功能更新同步维护。如新增图表、变更口径，将在此处与PRD中记录。