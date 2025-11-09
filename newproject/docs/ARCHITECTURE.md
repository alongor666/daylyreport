# 架构总览

## 任务交代
本文面向智能助手与工程团队，描述未来项目的整体架构、模块职责、数据流与部署拓扑，确保在无法访问旧仓库时仍可按此文档实施设计与开发。

## 系统视图
```
┌───────────────────────────────┐
│           浏览器 (Vue SPA)      │
│  - 全局筛选工具栏               │
│  - KPI 卡 / 周对比 / 占比卡      │
│  - Pinia 状态 / Axios 客户端     │
└──────────────┬────────────────┘
               │ HTTPS / REST
┌──────────────▼────────────────┐
│        FastAPI 后端服务         │
│  - API 路由 (/api/*)            │
│  - 服务层 (KPI/趋势/筛选)       │
│  - 缓存层 (可选 Redis)          │
│  - 验证与日志                   │
└──────────────┬────────────────┘
               │ DuckDB + 映射文件
┌──────────────▼────────────────┐
│      数据管道 / DuckDB 仓库      │
│  - scripts/ingest_daily.py      │
│  - raw_records / daily_aggregate│
│  - policy_staff_map             │
│  - data/logs + mappings         │
└───────────────────────────────┘
```

## 模块职责
### 前端 (frontend/)
- 技术：Vue 3 + Vite + TypeScript + Pinia + ECharts。
- 模块：
  - `stores/filter.ts`：筛选项、保单号锁定逻辑、policy mapping 缓存。
  - `stores/data.ts`：KPI / 周对比 / 饼图数据、缓存、错误与验证提示。
  - 组件：`GlobalFilterToolbar`、`KpiCard`、`WeekComparisonChart`、`RatioCard` 等。
  - 主题：根据 `DESIGN_SYSTEM.md` 实现配色与响应式布局。

### 后端 (backend/)
- 技术：FastAPI + Pydantic + SQLModel (或 duckdb python connector) + Uvicorn。
- 层次：
  - `app/api/routes`：定义 `/api/refresh`、`/api/kpi-windows` 等路由，并做参数校验。
  - `app/services`：封装 KPI、周对比、分布分析的查询逻辑。
  - `app/db`：负责连接 DuckDB、执行 SQL、返回 DataFrame/模型对象。
  - `app/schemas`：Pydantic 模型用于请求/响应契约；同时生成 OpenAPI 文档。
  - 可选 `app/cache`：封装 Redis，用于热数据缓存。

### 数据层 (scripts/ + data/)
- `scripts/ingest_daily.py`：处理 Excel/CSV → 验证 → 派生 → 写入 DuckDB。
- `scripts/restore_duckdb.py`：用于备份/回滚。
- 数据目录：
  - `data/inputs/`：待处理文件。
  - `data/mappings/staff_mapping.json`：业务员映射。
  - `data/warehouse/daylyreport.duckdb`：主仓库。
  - `data/logs/*.json`：批次日志。

## 数据流
1. 业务侧上传 Excel/CSV 到 `data/inputs/`。
2. 运行摄取脚本，写入 DuckDB 并生成验证信息。
3. FastAPI 通过 DuckDB 查询生成 KPI、趋势、分布等数据，附带 `validation` 元信息。
4. Vue SPA 调用 API，更新 Pinia 状态，渲染 UI。
5. Smoke 脚本定期检测 API 与关键 UI 流程。

## 部署建议
- 开发环境：
  - 本地运行 `scripts/run_dev.sh` 同时启动 DuckDB watcher、FastAPI、Vite。
- 测试/生产：
  - 使用 Docker Compose：`duckdb`（作为文件挂载）、`backend`、`frontend`（静态构建后由 Nginx 托管）、`redis`（可选缓存）。
  - 通过 CI/CD 完成 lint → test → build → docker image → 部署。

## 性能与扩展
- DuckDB 适合中等规模数据（≤百万行）；如需扩展，可切换至 PostgreSQL 或 ClickHouse，同时保留同样的数据模式。
- 后端可使用 redis 缓存热点 KPI；周对比等查询可提前在摄取阶段生成并写入汇总表。
- 前端需使用懒加载、虚拟化（如 filter 列表较大时）。

## 日志与可观测
- 摄取：`data/logs` 保存所有批次；失败时触发告警（参见 `OPERATIONS_PLAYBOOK.md`）。
- 后端：使用标准 JSON 日志输出请求耗时、状态码、mismatch_count。
- 前端：埋点记录主要交互（筛选变更、图表加载），便于转化为可观测指标。

## 变更控制
- 任何架构、数据库或 API 变化需同步更新本文件、`context.md` 与 `API_CONTRACTS.md`。
- 在提交 PR 前执行完整 QA checklist 与 smoke 流程。
