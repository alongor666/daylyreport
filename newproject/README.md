# New Project — 车险签单洞察平台

> 全新架构的车险签单多维分析 Web 应用，需求/数据/体验规范详见同目录的 `context.md` 与 `prompt.md`。

## 目录结构（初始）
- `backend/` — FastAPI + DuckDB 服务（待实现）。
- `frontend/` — Vue 3 + Vite 单页（待实现）。
- `data/` — 示例输入、DuckDB 文件、日志。
- `scripts/` — ingestion、dev orchestration、smoke 检查脚本。
- `docs/` — 架构、数据、API、QA 文档。
- `infra/` — Docker / CI / IaC 配置。
- `IMPLEMENTATION_PLAN.md` — 阶段性路线图。
- `context.md` — 产品与技术上下文（XML）。
- `prompt.md` — AI 实施指令（XML）。

## 即刻行动
1. **Scaffold**: 依据 `IMPLEMENTATION_PLAN.md` Phase 1 创建配置与依赖骨架。
2. **Ingestion**: 实现 `scripts/ingest_daily.py`，定义数据契约与 DuckDB 表。
3. **Backend**: FastAPI app with validated endpoints + caching。
4. **Frontend**: Sticky filter toolbar、KPI 卡、D/D-7/D-14 周对比图。
5. **Quality**: PyTest、Vitest、Playwright + lint/format + CI。

所有开发应保持与原仓库逻辑完全脱钩，仅以本目录中的文档为唯一信息源。
