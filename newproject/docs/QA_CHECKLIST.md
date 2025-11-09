# QA 检查清单

## 任务交代
本清单用于指导智能助手或工程同学在每日数据更新、后端部署或前端发版前执行一致的手动与自动验证，确保业务口径、筛选逻辑、UI 规范与性能指标保持稳定。

## 数据相关
1. 运行 `scripts/ingest_daily.py --input <文件>`，确认日志记录批次日期、文件名、行数、校验结果。
2. 校验 76 个字段：
   - 日期列（刷新时间/投保确认时间/保险起期）必须能解析且处于批次日期 ±30 天。
   - 枚举列（三级机构、是否新能源、是否续保等）值域与 `SCHEMA_CONTRACT.md` 一致。
   - 数值列（签单/批改保费、签单数量、手续费含税）无空值，无法解析立即报警。
3. 映射文件：
   - 运行映射解析脚本，输出 `policy_to_staff` 与 `staff_to_info`。
   - 若存在同名不同机构，`mismatch_count` 必须 >0 且在 API `/api/kpi-windows` 的 validation 字段中可见。

## 后端 API
1. `/health` — 返回 `status=healthy` 且响应时间 < 100ms。
2. `/api/filter-options` — 包含完整维度列表与机构-团队映射；随机抽样几个保单号验证联动。
3. `/api/policy-mapping` — `policy_to_staff` 与 `staff_to_info` 数量与数据源一致；冲突列表与日志匹配。
4. `/api/kpi-windows` — 在 `day`、`last7d`、`last30d` 下：
   - 保费/手续费单位为“万元整数”；件数千分位；占比字段范围 0~1。
   - `data_scope` 切换（含/不含批改）时，口径差异符合预期。
5. `/api/week-comparison` — 返回 D/D-7/D-14 三段，标签格式“D (MM-DD): 数值 趋势符号 变化率”；tooltip 数据包含箭头、变化值、变化率。
6. `/api/insurance-type-distribution`、`/api/premium-range-distribution`、`/api/renewal-type-distribution` — 对空数据、异常筛选需返回可读错误。

## 前端 UI / 交互
1. Global Filter Toolbar：
   - 默认展示“无筛选条件”；添加筛选后形成标签，可逐个移除。
   - 保单号 → 自动锁定业务员/机构/团队；业务员需要先选机构，团队为空时显示提示。
   - 数据口径、指标类型、时间段按钮均可键盘操作（aria 标签完整）。
2. KPI 卡：
   - 价值类型 `wanInt`、`percent`、`number`、`currency` 格式正确；Sparkline 与数据匹配。
   - `policy_consistency.mismatch_count > 0` 时显示提示徽标。
3. 周对比图：
   - 颜色遵循：D=#5B8DEF，D-7=#8B95A5，D-14=#C5CAD3。
   - Tooltip 为 6 列：色点、日期/标签、当期值、箭头、变化值、变化率；增长率 >5% 用绿色箭头，< -5% 用红色。
   - 悬停某日显示三行（D/D-7/D-14），若缺数据，显示“无对比”。
4. 占比 / 饼图 / 区间卡片：
   - 占比直接使用后端 ratios.*，不得自己计算。
   - 颜色与 Design System 配置一致，图例显示中文。
5. 响应式：
   - 320px 设备：筛选面板折叠为抽屉，KPI 卡单列。
   - ≥1024px：筛选置顶粘性、KPI 2x2 布局。

## 性能与稳定性
1. 首屏加载 < 2s（Chrome DevTools 模拟 4G）。
2. 图表渲染 < 500ms；筛选变更后的数据切换 < 300ms。
3. 若后端不可用，前端展示上次成功时间与缓存数据，确保可读提示。
4. Smoke 脚本：执行 `scripts/smoke_check.sh`，依次命中 /health、/api/filter-options、/api/kpi-windows 并跑一次 Playwright 流程。

## 交付文档
1. 在部署或交付前更新 `docs/QA_CHECKLIST.md` 的执行记录（日期、责任人、结论）。
2. 若新增口径、颜色、枚举，务必同步 `context.md`、`SCHEMA_CONTRACT.md` 与相关设计文档。
