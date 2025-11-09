# 进度记录

## 2025-11-08

- 前端：
  - 新增筛选维度“保单号”，选择后自动联动业务员/机构/团队
  - `FilterPanel.vue` 禁用在选择保单号后手动变更机构/团队
  - `Dashboard.vue` 增加不一致保单提示
  - 补充函数级中文注释到 `FilterPanel.vue` 与 `Dashboard.vue`
  - 调整 `ChartView.vue` 动态标签：仅显示日期、对应值、较7天前变化幅度与状态
  - 图例（仅UI显示）：中文标签“当周 / 上周 / 上上周”，内部仍使用 `D`/`D-7`/`D-14`
  - 动态标签实现三行显示：悬停某星期几展示 D-14、D-7、D 三条对应日期的数据与较7天前变化状态（D-14 无对比）
  - 优化 tooltip 样式：改为“箭头 + 变化值 + 变化率”的紧凑展示；颜色按阈值（>+5% 上升色、<-5% 下降色、其余中性）
  - 固定列布局：tooltip 每行采用 5 列网格（色点/日期/当期值/变化/变化幅度），三数值列固定宽度并居中对齐，提升可读性与一致性

- 后端：
  - `data_processor.py`：支持保单号唯一过滤与一致性校验
  - 新增 `GET /api/policy-mapping` 提供保单映射
  - `get_filter_options` 返回“保单号”选项

- 文档：
  - 创建“开发文档”目录并补充索引、问题记录、PRD-best与进度记录
  - 更新架构与开发者指南中关于保单号约束说明
  - 新增设计指南“筛选面板规范（保单号唯一约束）”并完善开发者指南端点与校验
  - 生成并归档《车险清单_2025年10-11月_合并-字段说明.md》，已包含字段类型/格式/值域；文本列取值全集穷举完备。
  - 执行隐私脱敏：对被保险人、投保人、车牌号码/车牌号/号牌号码、车架号码/车架号/VIN、发动机号码/发动机号、批单号、续保单号的“文本明细”进行屏蔽，文档仅保留统计信息。
  - 隐私合规更新：永久删除上述敏感字段的整段章节（数据字典不再生成对应条目），已完成备份与验证。
  - 新增：行驶证车主（含同义词：行驶证持有人/行驶证所有人）已纳入敏感字段范围并删除章节。
  - 细粒度隐私策略：对“客户名称”保留章节但屏蔽文本明细，已重生成并验证。

> 下一步：启动后端与前端并预览筛选面板UI，核验禁用态与提示展示。

## 2025-11-08（启动与测试）

- 后端：API 服务已启动在 `http://localhost:5001`，健康检查通过（`GET /api/health` 返回 `{"status":"healthy"}`）。
- 前端：开发服务器已启动在 `http://localhost:3000`，页面正常加载并可预览。
- 联调：Vite 代理 `/api` → `http://localhost:5001` 生效，前端可正常访问后端接口。
- 注意：若端口被占用（示例：5001 被残留 Python 进程占用），需结束占用进程后再启动。
- 结论：系统可启动，具备联调与预览能力；进入功能验收与UI细节核验阶段。

### Bug修复
- 修复后端根路径（`/`）访问 `http://127.0.0.1:5001/` 返回 404 的问题：
  - 新增根路径返回静态首页（`static/index.html`）或接口说明 JSON；配置 `static_folder` 指向项目根的 `static/`。

### 诊断修复记录（接口参数校验） — 2025-11-08

- 路由 `POST /api/staff-performance-distribution` 增强入参校验：
  - `period` 必须为字符串，归一化为小写后需属于白名单 `{day, last7d, last30d}`；
  - `filters` 必须为对象（JSON 字典）。
- 错误返回规范：
  - 非法 `period` 返回 HTTP 400，并附带 `allowed` 列表（`["day","last7d","last30d"]`）；
  - 非法 `filters` 返回 HTTP 400，并返回中文错误提示。
- 函数级中文注释：在路由函数注释中明确校验目的与错误处理策略（尽早拦截无效入参、减少未定义变量与类型不匹配问题）。
- 冒烟测试：
  - 非法 `period=week`：`curl -s -X POST http://127.0.0.1:5001/api/staff-performance-distribution -H 'Content-Type: application/json' -d '{"period":"week","filters":{}}'` → HTTP 400，JSON 包含 `message` 与 `allowed`；
  - 合法 `period=day`：`curl -s -X POST http://127.0.0.1:5001/api/staff-performance-distribution -H 'Content-Type: application/json' -d '{"period":"day","filters":{}}'` → HTTP 200，返回分布数据；
  - 非法 `filters` 类型：`curl -s -X POST http://127.0.0.1:5001/api/staff-performance-distribution -H 'Content-Type: application/json' -d '{"period":"day","filters":"not-an-object"}'` → HTTP 400，返回中文提示。
- 目标：提升接口健壮性与可诊断性，减少 IDE 诊断中的未定义变量与类型不匹配告警来源。
---
诊断修复记录（2025-11-08 21:05）

本次进展
- 修复 Dashboard 趋势类型：`calculateTrend` 改为返回数字并注释。
- 前端环境化：`vite.config.ts/js` 支持从 `.env` 读取端口与代理；新增 `frontend/.env.example`、`frontend/.env.development`。
- 后端提示动态化：`api_server.py` 读取 `FRONTEND_URL/VITE_PORT` 输出前端地址，读取 `API_PORT/PORT` 作为后端端口。
- 数据层错误日志增强：`stores/data.js` 输出状态码、响应体与载荷。

验证
- `curl` 周对比接口成功；Vue 控制台不再出现 trend 类型警告。

后续任务
- 如需更换端口或代理，更新 `.env` 并重启对应服务。

---
诊断修复记录（2025-11-08 21:30）

问题与处理
- 前端控制台报错：`ReferenceError: payload is not defined`（源自 `stores/data.js` 在 `catch` 中访问了 `try` 内的变量）。
- 接口状态 500：确认后端未启动导致代理请求失败。

修复
- 数据层：将 `payload` 提升为函数级作用域，确保错误日志能输出请求载荷；保留 `status` 与 `response` 的打印。
- 后端：启动 Flask（`python3 backend/api_server.py`），端口读取 `API_PORT`/`PORT` 环境变量。

验证
- `GET /api/filter-options` 返回筛选选项；`POST /api/kpi-windows` 返回三口径数据。
- 前端不再出现 `payload 未定义` 与 500 错误。

建议
- 开发时确保前后端均启动；端口或代理目标变更需同步 `.env` 并重启。
## 2025-11-09（单位与布局优化）

- 前端：
  - `ChartView.vue`：当 `currentMetric==='premium'` 时，轴与 tooltip 采用“万元整数”显示；Tooltip 行布局改为 6 列（色点/日期/当期值/箭头/变化值/变化幅度），增大列间距与行距。
  - `KpiCard.vue`：新增 `valueType: 'wanInt'` 并以“万元整数”显示；`Dashboard.vue` 将保费/佣金/目标差距卡片统一改为 `wanInt`。
- 验证：
  - 预览 `http://localhost:3001/` 加载正常；KPI 主值与周对比图单位一致，tooltip 箭头独立列对齐明显。
- 影响：
  - 单量（policy_count）保持数字千分位显示；不受单位改动影响。

## 2025-11-09（渠道判定规则：电销）

- 规则新增：以 `终端来源` 为唯一口径，取值为 `0110融合销售` 认定为“电销”，其余均为“非电销”。
- 后端实施建议：
  - 在聚合层新增布尔字段 `is_telesales` 与占比统计（支持保费与单量两个维度）。
  - 电销保费采用 `签单/批改保费`（支持负值与批改），展示按“万元整数”。
  - 电销单量采用 `签单数量`，与批改类型一致性由口径规则另行约定。
- 前端实施建议：
  - KPI 卡片新增“电销占比/电销保费/电销单量”展示，保费沿用 `wanInt` 口径；
  - 过滤与联动不改动，规则仅用于统计展示；`业务来源/客户源` 的“电销”字样仅用于核对，不参与认定。
- 验证计划：
  - 随机抽取 `终端来源=0110融合销售` 的样本检查布尔映射与占比计算；
  - 与包含“(电销)”字样的 `业务来源/客户源` 进行比对，确认差异解释与一致性。

## 2025-11-09（KPI卡扩展计划）

- 目标：新增四个占比类KPI卡（电销占比/新能源占比/过户车占比/交强险占比），与筛选器和“数据口径”切换弱耦合集成。
- 原始字段（数据字典）：
  - `终端来源`（含 `0110融合销售` 认定电销）、`是否新能源`（是/否）、`是否过户车`（是/否）、`险种名称`（0301交强险/0312商险2020版/0313特种商险2020版/0317新能源商险）、`签单/批改保费`（含负值）、`签单数量`（0/1）。
- 口径定义：
  - 电销占比：保费占比为 `电销保费 ÷ 全保费`；单量占比为 `电销件数 ÷ 全件数`（备选）。
  - 新能源占比：单量占比为 `是否新能源=是 的件数 ÷ 全件数`；保费占比为 `是否新能源=是 的保费 ÷ 全保费`（备选）。
  - 过户车占比：单量占比为 `是否过户车=是 的件数 ÷ 全件数`；保费占比（备选）。
  - 交强险占比：保费占比为 `险种名称=0301 的保费 ÷ 全保费`。
- 后端建议：
  - `DataProcessor.get_kpi_windows` 应用 `_apply_data_scope_filter(df, data_scope)` 与现有 `get_week_comparison` 保持一致；
  - 扩展返回字典 `ratios`（不改动既有键名）：
    - `ratios.telesales.premium = { day, last7d, last30d }`
    - `ratios.telesales.count = { day, last7d, last30d }`
    - `ratios.new_energy.count = { day, last7d, last30d }`
    - `ratios.transfer.count = { day, last7d, last30d }`
    - `ratios.mandatory.premium = { day, last7d, last30d }`
  - 分母为0返回0，结果裁剪至 `[0,1]`，确保稳健。
- 前端建议：
  - `KpiCard.vue` 新增 `valueType: 'percent'` 显示 `XX.X%`；不影响既有 `wanInt/number/currency`。
  - `Dashboard.vue` 在 `kpiCards` 中追加四张卡，数据源取 `dataStore.kpiData.ratios.*`；既有卡片不改动。
  - `stores/data.js` 在 `fetchKpiData`/`fetchChartData` 载荷中携带 `data_scope`（`filterStore.getDataScope()`）。
- 验收：抽样核对电销分子（`终端来源=0110融合销售`）、交强险分子（`险种名称=0301`）；新能源/过户车按标志字段校验计件准确。

## 2025-11-09（实施更新：占比类KPI上线）

- 后端：
  - `get_kpi_windows` 已应用 `data_scope` 过滤，与 `get_week_comparison` 保持一致；新增占比计算辅助函数（函数级中文注释），返回 `ratios` 字段，包含：
    - `ratios.telesales.premium/count`（电销保费/件数占比）
    - `ratios.new_energy.count`（新能源件数占比）
    - `ratios.transfer.count`（过户车件数占比）
    - `ratios.mandatory.premium`（交强险保费占比）
  - 分母为 0 返回 0.0，比例裁剪至 `[0,1]`，异常值防护完备。
- 前端：
  - `KpiCard.vue` 增加 `valueType: 'percent'` 并对异常值进行裁剪；添加函数级中文注释。
  - `Dashboard.vue` 在 `kpiCards` 中新增四张占比卡，绑定 `dataStore.kpiData.ratios.*`；趋势与微型折线采用与既有卡一致的生成逻辑。
  - `stores/data.js` 在所有请求载荷中注入 `data_scope`，确保口径切换一致。
- 验证：
  - 切换“数据口径”后，四张占比卡数据随之变化；抽样核对电销/新能源/过户车/交强险占比与原始样本一致。
  - UI 预览通过：百分比显示为 `XX.X%`，与单位/格式规范一致。

## 2025-11-09（设计确认与文档更新）

- 架构文档：`docs/ARCHITECTURE.md` 新增第14章《置顶工具栏与全局指标切换》，明确：
  - 工具栏置顶与控件顺序（数据口径｜保费/客户数｜时间周期）；
  - 筛选维度从“保单号”改为“业务员”，联动归一化机构/团队；
  - 占比类KPI随全局切换联动的返回结构（`ratios.*.premium/count`）。
- PRD 更新：`开发文档/PRD-best.md` 追加新需求章节，约定年度保费计划文件与 `plan_exists/progress/gap` 行为。
- 开发索引：`开发文档/README.md` 增补更新摘要与检查清单（置顶工具栏、全局切换、年度计划）。
- 问题记录：`开发文档/问题记录表.md` 追加“计划维度缺失、异地车值域、商险集合配置、业务员筛选冲突”等问题项。
- 规范要点：`开发文档/CLAUDE.md` 增加函数级中文注释与弱耦合规范（控件迁移不改状态结构、接口扩展不破坏）。
- 预览与验证计划：待前端迁移控件后进行 UI 预览与联动校验；后端扩展 `ratios` 与计划读取后抽样核对。

## 2025-11-09（筛选维度变更：业务员为主 + 联动禁用 + 全局指标联动）

- 前端改动：
  - `FilterPanel.vue` 将筛选入口从“保单号”切换为“业务员”，选择业务员后自动归一化其所属“三级机构/团队”，并在控件层面禁用手动修改机构/团队；避免口径冲突。
  - `Dashboard.vue` 全局指标切换（保费/客户数）已联动至四张占比类 KPI 卡（电销/新能源/过户车/交强险），展示依据 `appStore.currentMetric` 动态选择 `premium/count`。
  - `ChartView.vue` 仅消费全局 `currentMetric`，移除局部切换；单位显示与 tooltip 布局保持既有规范。
- 数据层与状态：
  - `frontend/src/stores/filter.js` 暴露 `resolveByStaff` 方法至返回对象，供筛选面板调用；`applyFilter` 扩展联动逻辑（按业务员归一化机构/团队）。
  - `frontend/src/stores/app.js` 的 `switchMetric(metric)` 保持签名不变，作为全局唯一指标切换入口；函数级中文注释已补充。
- 验收计划：
  - 启动前后端并预览，验证“业务员选择后控件禁用”“全局切换联动占比卡”“请求载荷携带 `data_scope/currentMetric/filters`”。
  - 数据抽样核验：占比卡在 `premium/count` 两口径下均能随切换正确刷新。

### 启动与预览（2025-11-09 进行中）
- 后端：`python3 backend/api_server.py`（端口 `5001`，支持 `API_PORT/PORT` 环境变量）。
- 前端：`npm run dev`（端口读取 `.env` 的 `VITE_PORT=3000`，如占用则自动递增）；当前预览地址：`http://localhost:3003/`。
- 预览检查点：
  - 业务员选择后，“团队/三级机构”变为禁用态且显示归一化值；
  - 切换“保费/客户数”后，四张占比类 KPI 的主值与迷你折线一起联动刷新；
  - `stores/data.js` 载荷包含 `filters/data_scope`，后端返回结构包含 `ratios.*.premium/count`。

> 验收结果将在预览完成后补充至本节（通过/问题与跟进）。

## 2025-11-09（晚）— KPI 优化需求解读与实施计划

- 背景：新增 KPI 指标需求，包含签单保费、保费达成率、保费缺口，以及占比类指标：商业险占比、新能源占比、过户车占比、异地车占比、电销占比。占比需可随全局“保费/客户数”切换联动。
- 原始字段确认：
  - 主度量：`签单/批改保费`、`签单数量`
  - 判定维度：`终端来源(0110融合销售=电销)`、`是否新能源`、`是否过户车`、`是否异地车`
  - 险种：`险种代码/险种名称`（商业险识别将新增配置映射，默认按代码前缀0312/0313/0317或名称含“商业”）
  - 组织：`业务员`、`团队简称`、`三级机构`
- 架构约束：遵循 docs/ARCHITECTURE.md 既定规则，弱耦合、向后兼容、前后端接口不破坏，UI 通过全局 currentMetric 联动。
- 差异与问题：
  - 后端 `get_kpi_windows` 仅返回四类占比（telesales/new_energy/transfer/mandatory），缺少 `commercial/non_local`，且新能源/过户仅支持 `count`，未提供 `premium` 口径；年度保费计划（progress/gap）尚未接入。
  - 前端 Dashboard 目前渲染四张占比卡，未包含商业险/异地占比，也未按“计划存在”显示达成率/缺口。
- 实施计划（当晚）：
  1) 文档更新：PRD、CLAUDE、README 同步新增 KPI 定义与年度计划接入要求；PROGRESS 记录实施步骤；问题表登记现状问题与回归项。
  2) 后端扩展：在 `get_kpi_windows` 新增 `ratios.commercial` 与 `ratios.non_local`；为 `new_energy/transfer` 同步补齐 `premium` 口径；统一比例返回 `[day/last7d/last30d]`。
  3) 计划接入：支持 `data/premium_plan.json`（可选）。命中维度组合时返回 `premium_progress/premium_gap/plan_exists`；未命中时 `plan_exists=false` 并前端隐藏相关 KPI。
  4) 前端渲染：新增“商业险占比、异地车占比”两张卡；若 `plan_exists=true`，显示“保费达成率（percent）”“保费缺口（wanInt）”。
  5) 预览与验收：在 `http://localhost:3003/` 进行 UI 联动和回归。

验收清单：
- 全局“保费/客户数”切换下，五类占比（电销/商业险/新能源/过户/异地）随口径联动刷新；分母为0时显示0.0%。
- 有计划的维度组合显示达成率与缺口；无计划则隐藏（不展示占位）。
- 接口结构与既有字段保持不破坏（保留 `telesales/mandatory` 等）。

## 2025-11-09（新增：商业险/异地车占比 + 异地车筛选）

- 后端：`data_processor.py` 新增 `_mask_commercial/_mask_non_local` 与 `ratios.commercial/non_local`；`get_filter_options` 返回“是否异地车”，`_apply_filters` 支持该项过滤。
- 前端：`Dashboard.vue` 新增两张 KPI 卡“商业险占比”“异地车占比”（百分比显示，随全局口径联动）；`FilterPanel.vue` 新增“是否异地车”筛选项。
- 文档：README/PRD-best/CLAUDE/问题记录表 已更新，补充口径、来源与联动说明。
- 预览：
  - 切换“保费/客户数”，两卡按口径正确刷新；分母为 0 显示 0.0%。
  - 切换“是否异地车”为“是/否”，KPI 与明细联动变化；选“全部”不影响结果。
- UI 与数据联动通过，进入回归阶段。

### 预览链接与联调（2025-11-09 继续）
 
## 2025-11-09（新增：清亏业务占比）

- 后端：
  - `data_processor.py` 新增 `_mask_loss_business`（函数级中文注释），基于 `车险新业务分类=清亏业务` 识别分子集合；在 `get_kpi_windows` 返回 `ratios.loss_business.premium/count = { day, last7d, last30d }`。
  - 分母为 0 返回 0.0；比例裁剪至 `[0,1]`；聚合函数与掩码均补充中文注释，说明入参/出参与边界策略。

- 前端：
  - `Dashboard.vue` 新增“KPI 卡：清亏业务占比”，绑定 `dataStore.kpiData.ratios.loss_business[appStore.currentMetric]`；百分比显示 `XX.X%`；支持与全局 `currentMetric` 联动。
  - 迷你折线与窗口切换逻辑沿用既有卡片生成方式，保持弱耦合。

- 文档：
  - 已更新 `开发文档/README.md` 与 `开发文档/PRD-best.md`，记录业务定义、双口径契约与前端展示；
  - 已更新 `开发文档/CLAUDE.md`，补充后端/前端约束与验收要点；
  - 已更新 `开发文档/问题记录表.md`，登记值域与回归项。

- 预览与验收：
  - 在 `http://localhost:3010/` 预览 Dashboard，确认新增卡片显示与联动；
  - 切换“保费/件数”两口径，值随之刷新；Day/7D/30D 三窗口折线显示一致；分母为 0 显示 `0.0%`。

> 结论：功能与契约已对齐，等待用户现场预览反馈。如数据存在“清亏业务”别名（如“清亏/亏损”），将在清洗映射阶段统一标准值域。
- 前端预览地址：`http://localhost:3010/`（通过 `VITE_PORT=3010 npm run dev` 启动）。
- 后端 API 地址：`http://localhost:5001`（已有进程占用，保留现有服务用于联调）。
- 代理联通：`vite.config.js` 代理 `/api` → `http://localhost:5001`，页面数据可正常拉取。

## 2025-11-09（文档维护：技能批判文档优化）

- 重写归档文档：`归档文件/技能批判.md` 从冗长教程改为“针对技能开发的批判与行动指南”，统一为“一屏摘要 + 快速参考”风格，删除重复与非必要说明。
- 批判维度确立：常见性/独特性/可验证性/投入产出比；每项提供判断要点与改进建议，支持研发评审与取舍。
- 联动更新：`开发文档/CLAUDE.md` 增补“技能开发批判原则”；`开发文档/PRD-best.md` 增补“技能文档最佳实践（摘要）”；`开发文档/问题记录表.md` 登记本次变更；`开发文档/README.md` 将新增维护规范章节。
- 验收要点：文档结构更简洁、可执行；相关术语与口径在 PRD/README/CLAUDE 中保持一致；问题记录与进度均有可追踪条目。
- 下一步行动：
  - 新技能评审采用“四问法”，要求提交一屏摘要与验收清单；不满足者降级或合并。
  - 清理现有冗长技能说明，转入归档并在主文档保留摘要与链接。
  - 将“清亏/商业险/异地车”等占比口径在 README/PRD-best 一致维护，新增或变更时同时更新问题记录表。
  - 回归检查：核对问题记录表新增项是否覆盖；预览是否无 UI 漂移，单位与格式规范是否一致。
- 验收步骤（人工）：
  - Dashboard 顶部查看新增 KPI 卡“商业险占比”“异地车占比”，值随全局 `currentMetric` 切换联动。
  - 在筛选面板切换“是否异地车＝是/否/全部”，确认两卡与其他明细同步刷新。
  - 空值或分母为 0 时显示为 `0.0%`，无异常告警。
- 待确认：请在预览页面执行上述步骤并反馈，如有问题在“开发文档/问题记录表.md”登记并回归。
### 2025-11-09（文档修订：全局看板占比双口径与目标分解）
- 已更新 ARCHITECTURE.md：确立 43100 目标与 Day/7D/30D 分解，监控指标双口径契约与识别规则（单交/新保）。
- 已更新 PRD-best.md：明确核心KPI（签单保费/达成率/目标缺口）与监控指标清单，交互与验收清单。
- 已更新 CLAUDE.md：约束后端返回双口径，占比兜底为 0，弱耦合与颜色规则对齐。
- 已更新 README.md（开发文档）：补充升级摘要与验收提示。
- 已更新 问题记录表.md：登记值域与识别回归项（`是否续保` 值域、`险别组合=单交`）。
- 下一步：在后端 `get_kpi_windows` 扩展 `ratios.*` 返回结构，补齐所有监控指标的 `count/premium` 双口径；前端为监控区域添加口径切换控件。
### 2025-11-09（更正：值域与默认口径）
- 更正：`是否续保` 的值域为 `新保/转保/续保`；新保占比仅取 `新保`。
- 更正：单交占比仅用“险别组合=单交”，取消回退规则。
- 更正：监控指标默认展示保费口径，切换到件数无需确认但需视觉反馈；统一筛选视觉规范（字体、颜色、状态）。
- 下一步：后端补齐 `ratios.*` 的双口径返回，前端实现口径切换的视觉反馈与筛选视觉统一。

## 2025-11-09（晚）— 监控双口径补齐与 UI 标签统一（完成）

- 后端：`get_kpi_windows` 为 `new_energy/transfer/mandatory/commercial` 全量补齐 `premium/count` 双口径；新增两类占比：
  - `single_mandatory_ratio`（单交占比）：识别“险别组合=单交”，支持 `premium/count`；
  - `new_policy_ratio`（新保占比）：识别 `是否续保=新保`，支持 `premium/count`。
- 前端：
  - Dashboard 将“交强占比”替换为“单交占比”，并新增“新保占比”；两卡与既有监控卡统一消费 `kpiData.ratios.*[currentMetric]`；
  - 全局指标切换标签由“客户数”改为“件数”，样式与筛选控件统一（默认/悬停/选中态）。
- 预览与联调：
  - 前端预览 `http://localhost:3010/`；后端沿用 `http://localhost:5001`（端口占用，复用既有进程）。
  - 切换“保费/件数”时，占比卡与折线联动刷新；分母为 0 显示 `0.0%`。
- 结论：功能与视觉通过；进入回归与文档同步阶段。

## 2025-11-09（分区重构与标题补充 — 已完成）

- 目标：将 Dashboard KPI 区域重构为三分区并补充中文标题，符合“核心KPI是三个”的验收要求。
- 代码：
  - `Dashboard.vue` 模板拆分为“核心KPI/监控占比/计划达成”三分区，新增中文标题；核心分区仅渲染三张卡（保费/单量/佣金）。
  - 抽取模块级辅助函数 `generateSparklineData/calculateTrend/getCurrentValue`（函数级中文注释），三分区复用；新增 `coreKpiCards/ratioKpiCards/planKpiCards` 三个 computed。
  - 计划分区：`plan_exists=true` 时追加“保费达成率（percent）”“保费缺口（wanInt）”；默认包含“目标差距”。
- 文档：README/PRD-best/CLAUDE 更新分区与标题规范、数据绑定与验收要点；问题记录表补充布局与标题规范问题项。
- 预览与验收：
  - 预览地址 `http://localhost:3010/`；页面存在三个中文分区标题；核心KPI仅三张卡。
  - 切换“保费/件数”与时间窗口，监控占比卡联动刷新；命中计划时显示达成率/缺口，未命中仅显示目标差距。
### 2025-11-09 文档维护：隐藏精友车型明细

- 背景：`开发文档/车险清单_2025年10-11月_合并-字段说明.md` 的“厂牌车型名称”字段包含约 6495 条车型取值明细，导致文档体积过大、阅读与渲染性能下降。
- 处理：使用 HTML 注释在“取值全集”行后开启注释，并在下一个字段标题“车主证件号前六位”前关闭注释，隐藏中间大段明细列表；保留统计与字段说明。
- 影响：页面加载更快、可读性提升；如需查看完整明细，可查阅归档或通过脚本单独生成。
### 2025-11-09 字段核查与文档完善

- 已核对：`原始数据字段说明.md` 与 `车险清单_2025年10-11月_合并.csv` 表头。
  - 结果：MD字段数 63，CSV字段数 76；集合一致（MD未出现CSV没有的字段），但MD缺少 13 个CSV字段（如：续保单号、被保险人*、车牌号码、发动机号码、车架号、行驶证车主、批单号、投保人*、车牌号 等），顺序不一致。
- 架构文档：`docs/ARCHITECTURE.md` 仅有“原始字段与口径映射”文字性说明，无逐列映射表。
- 处理：新增 `docs/FIELD_MAPPING.md` 标准映射表，明确同名直传与派生口径，并给出维护建议。
### 2025-11-09 修复进展：业务员姓名筛选兼容性

- 完成后端修复：`_apply_filters` 支持中文姓名与工号+姓名两种传值，避免姓名筛选无数据。
- 补充测试：新增 `backend/test_staff_filter.py` 自动选取姓名进行验证，测试通过。
- 下一步：观察前端 GlobalFilterPanel 时间快捷切换的饼图刷新频率与口径一致性（如需优化）。
 
## 2025-11-09（后端统一：日期筛选与去重向量化）

- 代码修复：
  - 日期筛选统一为 `Series.dt.normalize()` 比较与区间掩码，替换 `.dt.date == date.date()` 等写法；覆盖 `get_daily_report/get_week_trend/get_week_comparison/get_kpi_windows` 及分布函数的所有按天筛选。
  - 星期索引统一为 `Series.dt.dayofweek`（周一=0），替换 `date_obj.weekday()` 与 `apply(lambda ...)`，提升周窗口与分组的向量化性能与一致性。
  - 去重逻辑改为 `duplicated(..., keep='first'|'last')` 掩码反选，替换 `drop_duplicates(...)`：映射保单保留首条，历史合并保留最新一条；避免混合类型列下的类型报错。
- 兼容性：
  - 周窗口（D/D-7/D-14）语义与返回结构保持不变；UI 图例中文不参与计算。
  - 占比与分布接口值域一致，分母为 0 仍返回 0.0 并裁剪至 `[0,1]`。
- 验证：
  - 构造含 `NaT/时区` 的样本验证日期筛选稳定；抽样重复保单验证保留/剔除口径正确；周对比与 KPI 返回与预期一致。
- 文档同步：
  - 更新 `开发文档/README.md`/`PRD-best.md`/`CLAUDE.md`/`问题记录表.md` 记录本次修复的技术约束与验证要点。