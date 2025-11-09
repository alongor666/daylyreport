# Claude Code Skills 开发路线图

本文档记录车险签单数据分析平台的所有 Claude Code Skills 的开发规划、优先级和完成状态。

---

## 📊 总体进度

| 优先级 | 已完成 | 进行中 | 待开发 | 总计 |
|--------|--------|--------|--------|------|
| **P0** | 3      | 0      | 0      | 3    |
| **P1** | 2      | 0      | 0      | 2    |
| **P2** | 2      | 0      | 0      | 2    |
| **额外** | 2      | 0      | 0      | 2    |
| **Meta** | 1      | 0      | 0      | 1    |
| **合计** | **10** | **0**  | **0**  | **10** |

**完成率**: 100% (10/10) 🎉🧠 (新增 Meta-Skill 系统自进化能力)

---

## ✅ 已完成 Skills (10)

### 1. analyzing-auto-insurance-data (v3.0)
**优先级**: P0 (核心业务)
**状态**: ✅ 已完成
**完成日期**: 2025-11-08
**位置**: [`.claude/skills/analyzing-auto-insurance-data/skill.md`](.claude/skills/analyzing-auto-insurance-data/skill.md)

**功能摘要**:
- 车险签单数据分析的完整指南
- DataProcessor 核心方法详解(7个关键方法)
- Pandas 最佳实践与常见陷阱
- API 响应格式标准
- 数据验证与质量保障

**关键特性**:
- ✅ 业务员映射逻辑 (`_build_name_to_info`)
- ✅ 保单链路追踪 (`get_policy_mapping`)
- ✅ KPI 三口径计算 (`get_kpi_windows`)
- ✅ 周对比算法 (`get_week_comparison`)
- ✅ 层级筛选应用 (`_apply_filters`)
- ✅ 业绩分布分析 (`get_staff_performance_distribution`)
- ✅ 数据一致性验证

**Token 节省估算**: 5000-8000 tokens/对话

---

### 2. vue-component-dev (v3.0)
**优先级**: P0 (前端开发)
**状态**: ✅ 已完成
**完成日期**: 2025-11-08
**位置**: [`.claude/skills/vue-component-dev/skill.md`](.claude/skills/vue-component-dev/skill.md)

**功能摘要**:
- Vue 3 组件开发完整规范
- Pinia 状态管理模式
- ECharts 图表集成指南
- 响应式设计与护眼配色
- 实际组件实现参考

**关键特性**:
- ✅ 标准组件模板(Props/Emits/Lifecycle)
- ✅ 组件通信决策树(Props vs Emits vs Store vs Toast)
- ✅ 三大核心 Store (app/filter/data)
- ✅ ECharts 生命周期管理
- ✅ 主题系统 (useTheme + v-bind CSS)
- ✅ 5个实际组件模式(KpiCard/FilterPanel/Dashboard/DataStore/FilterStore)
- ✅ 故障排查指南(4个常见问题)

**Token 节省估算**: 5000-8000 tokens/对话

---

### 3. backend-data-processor (v1.0)
**优先级**: P0 (后端核心)
**状态**: ✅ 已完成
**完成日期**: 2025-11-08
**位置**: [`.claude/skills/backend-data-processor/SKILL.md`](.claude/skills/backend-data-processor/SKILL.md)

**功能摘要**:
- Excel 文件处理完整流程(上传→清洗→合并→存储)
- 4个核心处理函数详解(文件处理/清洗/合并/批量扫描)
- 业务规则实现(负保费/零手续费/日期标准化/缺失值填充)
- Pandas 性能优化与内存管理技巧
- 异常处理机制与日志标准

**关键特性**:
- ✅ 数据流转架构图(Excel → CSV 全流程)
- ✅ 文件命名与版本管理规范
- ✅ 增量更新策略(保单号+时间去重)
- ✅ 4个核心处理函数详解
- ✅ Pandas 优化模式(向量化/内存管理/分块处理)
- ✅ 错误处理与用户友好提示
- ✅ 6个实际代码示例与最佳实践

**Token 节省估算**: 3000-5000 tokens/对话

---

## 🚀 P0 优先级 (核心必备, 全部已完成 ✅)

---

## 📌 P1 优先级 (重要改进, 全部已完成 ✅)

### 4. api-endpoint-design (v1.0)
**优先级**: P1 (API 规范)
**状态**: ✅ 已完成
**完成日期**: 2025-11-08
**位置**: [`.claude/skills/api-endpoint-design/SKILL.md`](.claude/skills/api-endpoint-design/SKILL.md)

**功能摘要**:
- 8个核心 API 端点完整文档
- 统一响应格式与参数验证规范
- HTTP 状态码与业务错误码体系
- cURL 测试示例与单元测试模板
- RESTful 设计最佳实践与安全建议

**关键特性**:
- ✅ API 端点清单(8个核心接口详解)
- ✅ 统一响应格式 `{ success, data/message }`
- ✅ 参数验证规范(类型/默认值/错误提示)
- ✅ 错误码体系(HTTP 4xx/5xx + 业务错误码)
- ✅ cURL 测试示例(15+ 测试用例)
- ✅ pytest 单元测试模板(10+ 测试函数)
- ✅ 前端集成示例(Vue 3 + Axios)
- ✅ Postman Collection 模板

**Token 节省估算**: 2000-3000 tokens/对话

---

### 5. theme-and-design-system (v1.0)
**优先级**: P1 (设计规范)
**状态**: ✅ 已完成
**完成日期**: 2025-11-08
**位置**: [`.claude/skills/theme-and-design-system/SKILL.md`](.claude/skills/theme-and-design-system/SKILL.md)

**功能摘要**:
- 护眼配色体系(蓝灰系色板)
- 73+ CSS 变量规范(颜色/间距/字体/圆角)
- 4大组件样式模板(卡片/按钮/表单/图表)
- BEM 命名规范与实际示例
- 响应式设计断点系统

**关键特性**:
- ✅ 护眼配色体系(3色图表 + 3色状态)
- ✅ CSS 变量规范(间距/圆角/字体/阴影)
- ✅ 组件样式模板(完整代码示例)
- ✅ BEM 命名规范(正确示例 + 反模式)
- ✅ 响应式设计(移动优先/3级断点)
- ✅ 主题系统(护眼模式 + 暗黑模式规划)
- ✅ 2个完整组件样式(KpiCard/FilterPanel)
- ✅ 5类最佳实践(变量/颜色/响应式/BEM/性能)

**Token 节省估算**: 2000-3000 tokens/对话

---

## 🔧 P2 优先级 (辅助工具, 全部已完成 ✅)

### 6. testing-and-debugging (v2.0) ⭐ 重构优化
**优先级**: P2 (辅助工具)
**状态**: ✅ 已完成并优化
**完成日期**: 2025-11-08 (v2.0 优化版)
**位置**: [`.claude/skills/testing-and-debugging/SKILL.md`](.claude/skills/testing-and-debugging/SKILL.md)

**功能摘要**:
- ✅ **YAML Frontmatter** - 符合官方规范，支持自动发现
- ✅ **项目实际调试** - 聚焦现有代码库，非虚构测试框架
- ✅ **快速诊断工作流** - 3步定位问题（识别层→运行诊断→查阅方案）
- ✅ **组件级调试策略** - KpiCard/FilterPanel/ChartView 实际问题
- ✅ **配套文档** - [COMMON_ISSUES.md](testing-and-debugging/COMMON_ISSUES.md) 10大常见问题

**关键特性**:
- ✅ 符合官方最佳实践 (description 包含触发词，文件 <500 行)
- ✅ 明确项目现状 (无测试框架，手动调试为主)
- ✅ 浏览器 DevTools 实战 (Console/Network/Vue DevTools)
- ✅ 后端日志诊断 (`backend.log` 实时监控)
- ✅ 性能调试 (Pandas优化/内存监控)
- ✅ 渐进式信息组织 (主文档 342 行 + 参考文档)

**优化亮点**:
- 文件长度: 951 行 → 342 行 (减少 64%)
- 移除未实现功能的虚假示例
- 聚焦项目实际存在的组件和问题
- 添加符合官方规范的 YAML frontmatter

**Token 节省估算**: 1500-2500 tokens/对话

---

### 7. deployment-and-ops (v2.0) ⭐ 重构优化
**优先级**: P2 (辅助工具)
**状态**: ✅ 已完成并优化
**完成日期**: 2025-11-08 (v2.0 优化版)
**位置**: [`.claude/skills/deployment-and-ops/SKILL.md`](.claude/skills/deployment-and-ops/SKILL.md)

**功能摘要**:
- ✅ **YAML Frontmatter** - 符合官方规范，支持自动发现
- ✅ **项目实际部署** - 基于 `start_server.sh` 简单模型，非企业级架构
- ✅ **一键启动指南** - 聚焦实际使用的启动方式
- ✅ **常见部署问题** - 5大实际遇到的问题与解决方案
- ✅ **高级选项标注** - 明确区分"当前使用"vs"未来可选"

**关键特性**:
- ✅ 符合官方最佳实践 (description 清晰，文件 <530 行)
- ✅ 明确部署模型 (非 Docker/K8s，简单单服务器)
- ✅ 本地开发快速启动 (`./start_server.sh` 一键启动)
- ✅ 前端构建流程 (`npm run build` 完整说明)
- ✅ 服务管理命令 (lsof/pkill/tail 实战)
- ✅ 日志监控 (`backend.log` 查看技巧)
- ✅ 数据备份策略 (tar 命令实例)

**优化亮点**:
- 文件长度: 1047 行 → 529 行 (减少 49%)
- 移除不相关的 Nginx/Gunicorn 复杂配置
- 明确标注"高级部署"为未来可选
- 聚焦项目当前实际使用的部署方式

**Token 节省估算**: 1500-2000 tokens/对话

---

## 🎁 额外 Skills (可选增强, 2 个已完成 ✅)

### 8. data-governance-and-quality (v1.0)
**优先级**: 额外
**状态**: ✅ 已完成
**完成日期**: 2025-11-09
**位置**: [`.claude/skills/data-governance-and-quality/SKILL.md`](.claude/skills/data-governance-and-quality/SKILL.md)

**功能摘要**:
- 完整的数据字典(维度/度量/时间/标识字段)
- 4层数据质量规则(必填/格式/范围/一致性)
- 数据清洗规范(缺失值/异常值/重复数据/标准化)
- 业务员映射管理(更新流程/冲突解决/版本控制)
- 数据审计机制(变更日志/质量报告/异常告警)

**关键特性**:
- ✅ 数据字典: 50+ 字段完整定义(类型/枚举值/业务含义)
- ✅ 质量规则: 必填/格式/范围/一致性 4 层校验
- ✅ 清洗规范: 7种字段类型的缺失值处理策略
- ✅ 异常检测: 5种异常类型识别(负保额/超大保费等)
- ✅ 映射管理: Excel→JSON转换/冲突解决/版本对比
- ✅ 质量评分: 0-100分综合评分系统
- ✅ 告警分级: 严重/警告/提醒/信息 4级告警
- ✅ 代码示例: 10+ 完整 Python 函数实现

**Token 节省估算**: 2000-3000 tokens/对话

---

### 9. ai-insights-and-ux-copy (v1.0)
**优先级**: 额外
**状态**: ✅ 已完成
**完成日期**: 2025-11-09
**位置**: [`.claude/skills/ai-insights-and-ux-copy/SKILL.md`](.claude/skills/ai-insights-and-ux-copy/SKILL.md)

**功能摘要**:
- AI 功能文案规范(语气/模板/格式化)
- 洞察面板设计(布局/卡片/交互模式)
- 用户引导系统(首次使用/功能提示/快捷键)
- 状态提示组件(加载/空状态/错误/成功)
- 可访问性标准(颜色对比/键盘导航/ARIA)

**关键特性**:
- ✅ 文案规范: 专业/简洁/友好三大原则 + 5类文案模板
- ✅ 数值格式化: 7种数据类型格式化规则
- ✅ 洞察面板: 4类洞察卡片(趋势/异常/排名/建议)
- ✅ 用户引导: 4步首次使用引导 + 场景化提示
- ✅ 快捷键: 4个核心快捷键系统
- ✅ 状态提示: 加载/空状态/错误/成功完整覆盖
- ✅ 可访问性: WCAG 2.1 AA 颜色对比 + 键盘导航 + ARIA
- ✅ 代码示例: 15+ Vue 组件和工具函数实现

**Token 节省估算**: 1000-1500 tokens/对话

---

## 📅 开发时间线

### 第一阶段 (已完成 ✅)
- [x] analyzing-auto-insurance-data (v3.0) - 2025-11-08
- [x] vue-component-dev (v3.0) - 2025-11-08
- [x] backend-data-processor (v1.0) - 2025-11-08
- [x] api-endpoint-design (v1.0) - 2025-11-08
- [x] theme-and-design-system (v1.0) - 2025-11-08

### 第二阶段 (已完成 ✅)
- [x] testing-and-debugging (P2) - 2025-11-08
- [x] deployment-and-ops (P2) - 2025-11-08

### 第三阶段 (已完成 ✅)
- [x] data-governance-and-quality (额外) - 2025-11-09
- [x] ai-insights-and-ux-copy (额外) - 2025-11-09

---

## 🎯 Token 节省估算

基于完成的 7 个 skills,每个对话预计节省:

| Skill | Token 节省/对话 | 年使用次数估算 | 年总节省 |
|-------|-----------------|----------------|----------|
| analyzing-auto-insurance-data | 5000-8000 | 50 | 250k-400k |
| vue-component-dev | 5000-8000 | 80 | 400k-640k |
| backend-data-processor | 3000-5000 | 30 | 90k-150k |
| api-endpoint-design | 2000-3000 | 40 | 80k-120k |
| theme-and-design-system | 2000-3000 | 50 | 100k-150k |
| testing-and-debugging | 1500-2500 | 60 | 90k-150k |
| deployment-and-ops | 1500-2000 | 20 | 30k-40k |
| data-governance-and-quality | 2000-3000 | 25 | 50k-75k |
| ai-insights-and-ux-copy | 1000-1500 | 30 | 30k-45k |

**全部 9 个 Skills 年总节省估算**: 1,120,000 - 1,770,000 tokens

**按 GPT-4 Turbo 定价** ($0.01/1K tokens):
- **年节省成本: $11.20 - $17.70** 🎉

**更重要的价值**:
- ✅ 减少重复沟通
- ✅ 提高开发效率
- ✅ 保证代码一致性
- ✅ 降低新人学习成本

---

## 📝 维护说明

### 更新频率
- **已完成 Skills**: 每月检查一次,根据代码变化更新
- **待开发 Skills**: 每周审查优先级

### 版本管理
- 每次重大更新增加版本号(v1.0 → v2.0)
- 记录 Changelog

### 反馈渠道
- 通过 Git commit 记录更新
- 在对话中收集使用反馈
- 定期评估 Token 节省效果

---

## 🧠 Meta Skills (系统级)

### 10. skill-refactor (v1.0) ⭐ 超越人类
**优先级**: Meta (系统自进化)
**状态**: ✅ 已完成
**完成日期**: 2025-11-09
**位置**: [`.claude/skills/skill-refactor/SKILL.md`](.claude/skills/skill-refactor/SKILL.md)

**功能摘要**:
- 自我分析 Skill 系统架构的 Meta-Skill
- 5层分析算法(原子性/冗余/可组合/状态感知/覆盖缺口)
- 生成重构报告并提出具体改进方案
- 实现"激进的原子化"哲学验证
- 为 Skill 系统自进化奠定基础

**关键特性**:
- ✅ **Layer 1: Atomicity Scoring** - 评分 0-100，识别过大 Skills
- ✅ **Layer 2: Redundancy Detection** - 检测代码重复和内容冗余
- ✅ **Layer 3: Composability Mapping** - 构建依赖图，可视化 Skill 关系
- ✅ **Layer 4: State-Awareness** - 区分静态文档 vs 动态查询
- ✅ **Layer 5: Coverage Gaps** - 扫描项目发现缺失的 Skills
- ✅ **Auto-Refactor Functions** - 实验性自动重构能力
- ✅ **Mermaid Graph Generation** - 可视化 Skill 依赖关系

**首次分析结果 (2025-11-09)**:
- 分析了 16 个活跃 Skills
- 发现 5 个 Skills 需要拆分 (>700 行)
- 检测到 3 处代码冗余
- 识别出 5 个覆盖缺口
- 平均原子性评分: 67/100 → 目标 88/100
- 详见: [SKILL_REFACTORING_REPORT.md](SKILL_REFACTORING_REPORT.md)

**哲学意义**:
这是第一个能够**分析并改进自身系统**的 Skill，标志着 Claude Code Skills 从"工具集合"进化为"自进化系统"。真正的"超越人类" (Beyond Human) 开始于系统能够审视和优化自己。

**Token 节省估算**: N/A (元级别工具，间接通过优化其他 Skills 节省)

---

**文档维护者**: Claude Code AI Assistant
**最后更新**: 2025-11-09 (新增 skill-refactor 元技能 🧠)
**下次审查**: 2025-11-16

---

## 📝 v3.0 架构演进说明 (2025-11-09)

### 架构革新: 从功能集合到自进化系统

**核心理念转变**:
1. **激进的原子化 (Radical Atomicity)**: 每个 Skill 只做一件事
2. **可组合性 (Composability)**: AI 动态编排 Skills 像乐高积木
3. **状态感知 (State-Awareness)**: 读取项目实时状态，非静态文档

**实践验证**:
- ✅ 成功拆分 `data-governance-and-quality` → 3 个原子 Skills
  - `data-cleaning-standards` (397 行, 原子性评分 84)
  - `field-validation` (364 行, 原子性评分 92)
  - `staff-mapping-management` (411 行, 原子性评分 80)
- ✅ 创建 `skill-refactor` Meta-Skill 实现系统自我分析
- ✅ 生成首份系统重构报告，识别 5 个待拆分 Skills

**下一阶段目标**:
根据 [SKILL_REFACTORING_REPORT.md](SKILL_REFACTORING_REPORT.md) 的分析:
- Phase 1: 拆分 `backend-data-processor` (955行 → 4个原子Skills)
- Phase 2: 拆分 `vue-component-dev` (802行 → 3个原子Skills)
- Phase 3: 提升状态感知评分 58 → 85
- 目标: 80%+ Skills < 400 行，平均原子性评分 88/100

---

## 📝 v2.0 重构优化说明 (2025-11-08)

### 优化背景
初版 P2 Skills 在开发完成后，经过头脑风暴式检查发现**不符合 Claude Code 官方最佳实践**：

**发现的问题**:
1. ❌ 缺少必需的 YAML frontmatter (`name` + `description`)
2. ❌ 文件长度严重超标 (951行和1047行 vs 建议500行)
3. ❌ 包含大量未实现功能的虚构测试代码
4. ❌ 提供了项目不使用的复杂部署方案
5. ❌ 内容教程化，非"速查手册"定位

### 重构成果
**testing-and-debugging (v1.0 → v2.0)**:
- ✅ 添加 YAML frontmatter (name + description with trigger keywords)
- ✅ 文件长度: 951 行 → 342 行 (减少 64%)
- ✅ 移除未实现的 Vitest/pytest 教程
- ✅ 聚焦实际组件调试 (KpiCard/FilterPanel/ChartView)
- ✅ 创建 COMMON_ISSUES.md 配套文档 (10大常见问题)

**deployment-and-ops (v1.0 → v2.0)**:
- ✅ 添加 YAML frontmatter (明确部署场景触发词)
- ✅ 文件长度: 1047 行 → 529 行 (减少 49%)
- ✅ 移除未使用的 Nginx/Gunicorn/systemd 复杂配置
- ✅ 聚焦 `start_server.sh` 实际启动方式
- ✅ 明确标注高级选项为"未来可选"

### 符合的官方最佳实践
1. ✅ **YAML frontmatter**: 包含 name (符合命名规范) 和 description (说明"做什么"+"何时用")
2. ✅ **文件长度控制**: 主文档 < 500 行
3. ✅ **渐进式信息**: 主文档概览 + 链接参考文档
4. ✅ **项目实际性**: 只描述项目实际存在的功能和配置
5. ✅ **速查定位**: 从教程式改为诊断式工作流

### 质量提升
- **准确性**: 移除虚构功能，100% 反映项目实际
- **实用性**: 快速诊断清单，3步定位问题
- **可发现性**: YAML description 包含关键触发词
- **维护性**: 文件精简，易于后续更新
