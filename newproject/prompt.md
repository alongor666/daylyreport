<prompt>
  <objective>
    构建一个与现有仓库完全隔离的全新车险签单洞察 Web 应用，覆盖每日数据摄取、后端聚合 API、前端可视化、自动化测试与开发体验工具，满足伴随的 <context> 规范所列全部业务、数据与体验要求。
  </objective>

  <contextReference>
    在任何设计或实现之前，通读随附的上下文 XML，所有术语、度量、筛选规则、色彩与性能指标均以该规范为准；不得引用原仓库路径或文件。
  </contextReference>

  <scope>
    <track name="DataIngestion">
      <item>实现可配置的 Excel/CSV 批处理流水线：解析、字段校验、值域验证、生成列式存储（DuckDB/Parquet）与版本化批次日志。</item>
      <item>内置字段映射与业务员机构 JSON 的冲突检测，暴露 mismatch_count。</item>
    </track>
    <track name="BackendAPI">
      <item>以 Flask 或 FastAPI 提供 REST/GraphQL 接口：refresh、kpi-windows、week-comparison、filter-options、policy-mapping、insurance-type-distribution、premium-range-distribution、renewal-type-distribution、health。</item>
      <item>实现 filters、data_scope、anchor_date、period 的严格校验；所有金额按万元整数或百分比格式返回；返回 validation 元信息。</item>
      <item>加入缓存与配置驱动的指标目录，保证 500ms 内响应。</item>
    </track>
    <track name="FrontendSPA">
      <item>基于 Vue 3 + Vite + Pinia + ECharts 打造响应式单页：粘性全局筛选工具栏、KPI 卡、D/D-7/D-14 对比图、占比饼图、业务员保费区间、同比环比模块。</item>
      <item>实现 valueType currency/number/wanInt/percent 的格式化、Sparkline、tooltip 六列布局、颜色阈值与标签格式。</item>
      <item>提供离线回退：在 API 不可达时展示最后一次成功查询的数据及时间戳。</item>
    </track>
    <track name="QualityAndDX">
      <item>后端 PyTest（含缺失列、空数据、错误筛选）与前端 Vitest/Playwright（含筛选级联、tooltip、颜色规则）。</item>
      <item>Lint（ESLint、Prettier、ruff 或 flake8）、format、type-check（tsc --noEmit 可选）。</item>
      <item>脚本：ingest_daily.py、run_dev.sh、smoke_check.sh，配合 .env.example、docker-compose 与 CI 工作流。</item>
    </track>
  </scope>

  <deliverables>
    <item>模块化源码（data、backend、frontend、scripts、infra），所有依赖固定版本。</item>
    <item>自动化测试及其报告，确保在 CI 中可重复。</item>
    <item>文档：高阶 README、架构说明、API 合约、数据字典、运行/部署指南、验证 checklist。</item>
    <item>演示用截图或录屏脚本，证明 KPI、筛选、趋势图、占比卡片在三种时间段下的表现。</item>
  </deliverables>

  <nonGoals>
    <item>不实现权限管理、客户信息脱敏策略或外部分发机制；若有需要，仅占位注释。</item>
    <item>不依赖历史仓库中的任何脚本或资源，所有需要的内容必须在本新项目中重新定义。</item>
  </nonGoals>

  <qualityGates>
    <gate>所有 API 合约必须通过 JSON Schema 或 Pydantic 校验，并在契约测试中锁定。</gate>
    <gate>前端与后端的占比数值不得在 UI 端重新计算，需引用后端 ratios.* 字段。</gate>
    <gate>CI 需在 &lt;10 分钟内完成 lint+test+build；失败时输出可读日志。</gate>
  </qualityGates>

  <workflow>
    <step>读取上下文 XML，形成产品、数据、体验的共享词典。</step>
    <step>定义技术蓝图：管道、服务、前端、CI。</step>
    <step>实现数据流水线 → API → 前端 → 测试 → 文档 → 演示。</step>
    <step>在交付前执行 smoke_check.sh，确保关键 API 与 UI 流程可用。</step>
  </workflow>

  <acceptance>
    <item>新项目能在一台干净环境上通过 run_dev.sh 启动，展示实时 KPI、筛选和图表。</item>
    <item>ingest_daily.py 可导入示例数据并生成 mismatch_count 提示。</item>
    <item>Smoke 测试脚本验证 /health、/api/filter-options、筛选联动、颜色阈值与单位规范全部通过。</item>
  </acceptance>
</prompt>
