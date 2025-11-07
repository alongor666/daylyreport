# Repository Guidelines

## 项目结构与模块组织
按照 docs/ARCHITECTURE.md 与 docs/PRD.md 的定义，前端源码位于 `frontend/`：`src/components` 存放 Vue 3 组件、`src/stores` 承载 Pinia 状态、`src/services/api.ts` 统一封装 Axios 调用。后端服务集中在 `backend/`，`api_server.py` 提供 REST 接口，`data_processor.py` 负责 Pandas 清洗、聚合与指标计算；任何共享逻辑都应首先写在这里再被 CLI 或脚本复用。静态可交付物打包到 `static/`，其中的 JS/CSS 必须来自最新的 Vite 构建。所有原始 Excel、合并 CSV 以及映射 JSON 仅可放在 `data/`，而调研、设计和迁移说明全部存放于 `docs/`（详见 docs/README_FOR_DEVELOPERS.md 的导航路径）。

## 构建、测试与开发命令
- `python3 -m venv .venv && source .venv/bin/activate`：初始化后端虚拟环境（CLAUDE.md 要求）。
- `pip install -r requirements.txt`：安装 Flask 3.0、Flask-CORS、Pandas 2.x、openpyxl 与限定 NumPy。
- `cd backend && python3 api_server.py` 或 `./start_server.sh`：在 5001 端口启动 API，便于前端代理。
- `cd frontend && npm install && npm run dev`：启用 Vite HMR（5173），调试时请确认代理目标指向后端。
- `npm run build && npm run lint && cp -R dist/* ../static/`：生成生产资源、执行 ESLint/Prettier，然后同步至 Flask 静态目录。
- `python scripts/check_env.py` 与 `python scripts/read_excel_sample.py data/<file>.xlsx`：文档推荐的环境自检与数据抽样。

## 编码风格与命名约定
后端遵循 PEP 8（4 空格缩进、snake_case 函数、ALL_CAPS 常量），关键聚合函数需编写 docstring 并保持纯函数特性，便于未来接入 PyTest。前端按 docs/DESIGN_SYSTEM.md：组件命名用 PascalCase（如 `KpiCard.vue`），props 需显式类型与默认值，事件采用 kebab-case；状态只能通过 Pinia store 更新，禁止全局变量与直接操作 localStorage。样式使用 CSS Variables + BEM，例如 `.kpi-card__value`，不得硬编码颜色或间距。

## 测试与验证准则
因自动化尚在建设阶段（参见 docs/README_FOR_DEVELOPERS.md），每次变更都要记录手动验证：完成数据脚本抽样、命中 `/health` 与 `/api/filter-options`、在 Vite 开发服或 `static/index.html` 下走通 KPI、筛选与趋势图。新增 PyTest 时以 `tests/backend/test_<module>.py` 命名，覆盖正常路径与缺失列、空数据等异常；UI 变更需附上根据 docs/DESIGN_SYSTEM.md 的截图或录屏验证响应式与配色。

## 提交与 Pull Request 流程
Git 历史遵循 Conventional Commits（示例：`docs: 更新架构图`、`feat(backend): 支持新能源筛选`）。在创建 PR 前请：1）`git pull --rebase` 同步主干；2）重跑上述后端脚本与 `npm run lint`；3）若改动前端，务必将最新 `dist/` 写回 `static/` 并说明来源。PR 描述需包含关联需求（PRD/Issue 链接）、影响的 API 或页面、验证步骤、截图/录屏，以及部署动作（如“重新导入 data/processed CSV”）。任何文档更新要同步对应的 docs/*.md，以免破坏 docs/README_FOR_DEVELOPERS.md 所述阅读路径。

## 数据与配置安全
docs/MIGRATION_GUIDE.md 强调所有含客户信息的 Excel/CSV 不得提交仓库；请将临时文件存放在 `data/`（已 .gitignore）或本地受控目录，并在日志、截图中脱敏。配置密钥使用 `.env` 或系统变量管理，切勿硬编码在源码或脚本里；若新增配置项，需在 docs/ARCHITECTURE.md 或 CLAUDE.md 中登记说明，确保多终端协作遵循同一约定。
