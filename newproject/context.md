<context>
  <productOverview>
    <name>车险签单洞察平台</name>
    <mission>为分公司与业务团队提供每日更新的车险签单绩效、趋势与多维筛选分析，支持分钟级响应和一键自助分析。</mission>
    <version>3.0-vision</version>
    <coreValues>
      <value>实时洞察：首屏加载&lt;2s，指标切换&lt;300ms。</value>
      <value>多维分析：任意组合机构、团队、业务员、车辆属性等条件。</value>
      <value>移动友好：响应式体验覆盖 320px–2560px。</value>
      <value>一致口径：后端统一计算万元整数、占比、保单号映射。</value>
    </coreValues>
  </productOverview>

  <personas>
    <persona name="业务经理" usageShare="40%">
      <habits>每日查看 3-5 次，关注当日目标、团队对比，移动端占 60%。</habits>
    </persona>
    <persona name="数据分析师" usageShare="30%">
      <habits>深度分析周/月趋势，导出数据做二次建模，PC 为主。</habits>
    </persona>
    <persona name="高层管理" usageShare="20%">
      <habits>关注整体 KPI、机构排名，碎片时间快速浏览。</habits>
    </persona>
    <persona name="一线业务员" usageShare="10%">
      <habits>查看个人业绩与团队均值，移动端优先。</habits>
    </persona>
  </personas>

  <scenarios>
    <scenario name="早会汇报" frequency="daily" pain="旧系统数据刷新慢、筛选繁琐" outcome="秒级获取昨日/本周 KPI、生成可视化截图" />
    <scenario name="碎片化查看" frequency="daily" pain="移动端体验差" outcome="随时查看关键指标与趋势" />
    <scenario name="深度分析" frequency="weekly" pain="缺少高级筛选与对比" outcome="多维组合筛选、导出或下钻" />
  </scenarios>

  <capabilities>
    <feature id="F1" priority="P0" name="数据仪表板">
      <details>4 张 KPI 卡 + D/D-7/D-14 周对比柱状图 + 日期选择器（今天/昨天/本周/上周/自定义）。</details>
      <performance>首屏&lt;2s、图表渲染&lt;500ms、数据切换&lt;300ms。</performance>
      <interactions>KPI 卡可展开详情，图表支持拖拽缩放与 tooltip。</interactions>
    </feature>
    <feature id="F2" priority="P0" name="高级筛选器">
      <details>8+ 维度复合筛选（三级机构、团队、业务员、保单号、新转续、能源类型、过户车、险种大类、吨位、电销标记、业务类型等）。</details>
      <interactions>折叠面板、标签展示、实时搜索、机构联动团队、保单号锁定业务员。</interactions>
      <performance>筛选响应&lt;500ms，需支持 10 万+ 记录。</performance>
    </feature>
    <feature id="F3" priority="P0" name="数据刷新">
      <details>一键刷新 + 进度反馈 + Toast；未来支持自动调度。</details>
      <performance>1000 条数据处理&lt;3s，前端刷新&lt;1s。</performance>
    </feature>
    <feature id="F4" priority="P1" name="数据导出">
      <details>根据当前筛选导出 Excel/CSV，附图表截图。</details>
    </feature>
    <feature id="F5" priority="P1" name="同比环比分析">
      <details>多指标同比/环比、可视化对比、告警阈值。</details>
    </feature>
  </capabilities>

  <dataModel>
    <dataset name="车险清单_每日合并" rows="55375" columns="76">
      <timeCoverage>2025-10-16 至 2025-11-07（示例），每日生成。</timeCoverage>
      <keyFields>
        <field name="刷新时间" type="datetime" note="判定数据新鲜度" />
        <field name="投保确认时间" type="datetime" note="所有时间筛选的锚点" />
        <field name="保险起期" type="datetime" />
        <field name="保单号" type="string" note="唯一主键，用于保单号筛选" />
        <field name="业务员" type="string" note="可能包含工号+姓名，需提取中文名" />
        <field name="三级机构" type="enum" values="乐山、天府、宜宾、德阳、新都、武侯、泸州、自贡、资阳、达州、青羊、高新" />
        <field name="团队简称" type="enum" note="来自外部映射，可为 null" />
        <field name="是否续保" values="新保、续保、转保" />
        <field name="终端来源" values="0110融合销售 等" note="判定电销" />
        <field name="是否新能源" values="是/否" />
        <field name="是否过户车" values="是/否" />
        <field name="是否异地车" values="是/否" />
        <field name="险种名称" values="0301交强、0312/0313/0317 商业险" />
        <field name="签单/批改保费" type="number" role="主度量（元）" />
        <field name="签单数量" type="number" role="件数" />
        <field name="手续费含税" type="number" role="佣金" />
        <field name="客户类别3" values="非营业个人客车、摩托车、营业货车等" />
      </keyFields>
      <derivedFields>
        <field name="premium" formula="sum(签单/批改保费)" />
        <field name="policy_count" formula="sum(签单数量)" />
        <field name="commission" formula="sum(手续费含税)" />
        <field name="telesales_flag" rule="终端来源 == 0110融合销售" />
        <field name="commercial_flag" rule="险种名称 ∈ {0312,0313,0317}" />
        <field name="new_energy_flag" rule="是否新能源 == 是" />
        <field name="transfer_flag" rule="是否过户车 == 是" />
        <field name="non_local_flag" rule="是否异地车 == 是" />
        <field name="ratios.*" note="占比类指标，范围 0~1，由后端计算，不在前端重算" />
      </derivedFields>
    </dataset>
    <mappingSource name="业务员机构团队归属" format="JSON">
      <rule>键：工号+姓名；需提取中文姓名作为唯一键，附带三级机构、四级机构、团队简称。</rule>
      <validation>检测同名冲突并暴露 mismatch_count。</validation>
    </mappingSource>
  </dataModel>

  <filters>
    <dimension name="保单号" behavior="唯一" note="选择后锁定业务员/机构/团队" />
    <dimension name="业务员" dependency="三级机构→团队" note="需先选机构" />
    <dimension name="三级机构" />
    <dimension name="团队" />
    <dimension name="是否续保" aliases="新保/续保/转保" />
    <dimension name="能源类型" source="是否新能源" />
    <dimension name="是否过户车" />
    <dimension name="是否异地车" />
    <dimension name="险种大类" />
    <dimension name="吨位分段" />
    <dimension name="电销标记" values="是/否/全部" />
    <dimension name="业务类型" source="客户类别3" />
    <dimension name="数据口径" values="exclude_correction/include_correction" />
    <dimension name="时间段" values="day/last7d/last30d" />
  </filters>

  <apiSurface>
    <endpoint method="POST" path="/api/refresh" purpose="触发 Excel→CSV 批处理" />
    <endpoint method="POST" path="/api/kpi-windows">
      <request>{ date?: YYYY-MM-DD, filters?: dict, data_scope?: enum }</request>
      <response>{ anchor_date, premium/policy_count/commission (day/last7d/last30d), target_gap_day, ratios.* , validation }</response>
    </endpoint>
    <endpoint method="POST" path="/api/week-comparison">
      <request>{ metric: premium|count, filters, date?, data_scope }</request>
      <response>{ latest_date, x_axis, series[{code:D|D-7|D-14, data[], dates[], total_value, label}] }</response>
    </endpoint>
    <endpoint method="GET" path="/api/filter-options" purpose="返回所有筛选维度选项与机构-团队映射" />
    <endpoint method="GET" path="/api/policy-mapping" purpose="返回 policy_to_staff、staff_to_info、conflicts" />
    <endpoint method="POST" path="/api/insurance-type-distribution" />
    <endpoint method="POST" path="/api/premium-range-distribution" />
    <endpoint method="POST" path="/api/renewal-type-distribution" />
    <endpoint method="GET" path="/api/health" />
  </apiSurface>

  <uiGuidelines>
    <colorSystem>
      <color name="D (最新周)" value="#5B8DEF" role="主数据" />
      <color name="D-7" value="#8B95A5" role="辅助" />
      <color name="D-14" value="#C5CAD3" role="背景" />
      <color name="上升" value="#52C41A" role="正向" />
      <color name="下降" value="#F5222D" role="警示" />
      <color name="持平" value="#8B95A5" role="中性" />
    </colorSystem>
    <components>
      <component name="GlobalFilterPanel" traits="置顶工具栏，标签 summary bar，支持键盘 aria" />
      <component name="KpiCard" traits="支持 valueType currency/number/wanInt/percent，value=万元整数，percent inputs clamp 0-1，含 sparkline" />
      <component name="ChartView" traits="tooltip 6 列网格（色点、事件名、当期值、箭头、变化值、变化率）" />
    </components>
    <labels>周对比标签格式：“D (MM-DD): 数值 趋势符号 变化率”。</labels>
  </uiGuidelines>

  <validation>
    <manualChecklist>
      <item>抽样运行数据脚本，核对字段枚举与空值。</item>
      <item>命中 /health 与 /api/filter-options。</item>
      <item>在 Dev 服务器或静态包中走通 KPI、筛选、趋势图。</item>
      <item>验证筛选联动（保单号锁定、机构→团队→业务员级联）。</item>
      <item>核对颜色阈值：增长率 &gt; 5% 用上升色，&lt; -5% 用下降色，其余中性。</item>
    </manualChecklist>
  </validation>

  <engineeringExpectations>
    <backend>Python 3.11+，Flask/FastAPI，Pandas 或 DuckDB；模块化拆分 ingestion、aggregation、query。</backend>
    <frontend>Vue 3 + Vite + Pinia + ECharts，Composition API，响应式和可访问性。</frontend>
    <ops>dev_full 脚本、CI 包括 lint/test/build、npm run lint、pip tests。</ops>
    <performance>API 并发友好，必要时缓存；图表数据序列化为精简 JSON。</performance>
    <quality>新增 PyTest 覆盖正常与异常（缺失列、空数据），前端需截图或录屏验证。</quality>
  </engineeringExpectations>

  <glossary>
    <term name="数据口径">exclude_correction=不含批改数据；include_correction=含批改。</term>
    <term name="ratios.*">后端输出的占比字段，如 telesales_ratio、new_energy_ratio、transfer_ratio、commercial_ratio。</term>
    <term name="policy_consistency.mismatch_count">映射冲突数，KPI 顶部展示提示。</term>
  </glossary>
</context>
