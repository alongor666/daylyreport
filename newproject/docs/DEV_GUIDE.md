# 开发指南

## 任务交代
本指南帮助新成员或 AI 在无外部参考的情况下完成环境搭建、脚本执行、开发调试与提交流程。所有步骤均基于 `newproject/` 内的文档与脚本。

## 环境准备
1. 安装依赖：Python 3.11、Node.js 20+、Poetry、pnpm 或 npm、DuckDB CLI（可选）、Redis（可选缓存）。
2. 复制 `.env.example` → `.env`，根据需要修改端口、目标值、映射路径。
3. 目录说明：
   - `backend/`：FastAPI 服务与测试。
   - `frontend/`：Vue 3 SPA。
   - `data/`：输入、仓库、日志、映射。
   - `scripts/`：跨组件脚本（ingest、run_dev、smoke）。
   - `docs/`：全部规范文档。

## 常用命令
- 摄取数据：`python scripts/ingest_daily.py --input data/inputs --batch-date <date> --mapping data/mappings/staff_mapping.json`。
- 启动后端：`cd backend && poetry install && poetry run uvicorn app.main:app --reload --port ${API_PORT}`。
- 启动前端：`cd frontend && npm install && npm run dev`。
- 一键开发：`bash scripts/run_dev.sh`（需后续实现）。
- 冒烟测试：`bash scripts/smoke_check.sh`。
- 单元测试：
  - 后端：`cd backend && poetry run pytest`。
  - 前端：`cd frontend && npm run test`（Vitest）。
  - 端到端：`cd frontend && npm run test:e2e`（Playwright）。

## 开发流程
1. **拉取最新文档**：阅读 `context.md`、`prompt.md`、`SCHEMA_CONTRACT.md`、`DESIGN_SYSTEM.md`、`QA_CHECKLIST.md`，确保语义一致。
2. **实现 / 修改功能**：
   - 数据/派生逻辑 → 参考 `docs/data/SCHEMA_CONTRACT.md`。
   - API → 参考 `docs/API_CONTRACTS.md`。
   - UI → 参考 `docs/DESIGN_SYSTEM.md`、`QA_CHECKLIST.md`。
3. **本地验证**：
   - 跑摄取脚本并检查 `data/logs`。
   - 执行后端/前端测试。
   - 执行 Smoke 脚本，记录结果。
4. **文档同步**：
   - 若新增字段、枚举、配色或流程，务必更新对应文档。
   - 在 `QA_CHECKLIST.md` 记录本次验证时间与结论。
5. **提交规范**：
   - 使用 Conventional Commits 格式（如 `feat(backend): add week comparison cache`）。
   - PR 描述需附：需求链接、影响范围、验证步骤、截图/录屏。

## 目录与脚本占位
- `scripts/` 需补充：
  - `ingest_daily.py`（数据流水线）。
  - `run_dev.sh`（后台/前台一键启动）。
  - `smoke_check.sh`（API + Playwright）。
- `infra/` 将存放 CI/CD、容器配置，后续需根据实际部署方案补全。

## 常见问题与排查
- **摄取脚本失败**：查看 `data/logs/<batch>.json`，若为枚举/日期错误，需联系数据提供方修正；若为映射缺失，补齐 mapping 并重新摄取。
- **KPI 占比全为 0**：检查 DuckDB 是否写入 `ratios.*`；确认摄取脚本内分母不为 0。
- **前端颜色/单位异常**：核对 `DESIGN_SYSTEM.md`，确保组件使用正确的 `valueType` 与 CSS 变量。
- **缓存不更新**：清理 Redis 或禁用缓存（`.env` 中配置）。

## 交接要求
- 新人入组需阅读本指南与 `OPERATIONS_PLAYBOOK.md`，并完成一次从摄取到前端展示的端到端演练。
- 若手册内容过期，发现者需在 1 个工作日内更新。
