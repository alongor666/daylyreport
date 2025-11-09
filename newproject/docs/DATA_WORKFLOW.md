# 数据作业流程

## 任务交代
该文档用于详细描述每日数据如何从 Excel/CSV 流入新系统，包括命名约定、摄取脚本参数、验证步骤与派生逻辑，确保 AI 或工程师可以完全复制你的工作方式。

## 文件命名约定
- 主清单：`车险清单_<年份>年<月份>-<月份>月_合并.xlsx`，例如 `车险清单_2025年10-11月_合并.xlsx`。
- 多批次：追加 `_partN`，确保按时间顺序摄取。
- 映射文件：`业务员机构团队归属.json`，放在 `data/mappings/`，摄取脚本读取后会生成 `staff_mapping.cache.json`。

## 摄取步骤
1. 将所有输入文件放入 `data/inputs/`。
2. 执行 `python scripts/ingest_daily.py --input data/inputs --batch-date YYYY-MM-DD --mapping data/mappings/staff_mapping.json --output data/warehouse/daylyreport.duckdb`。
3. 脚本流程：
   - 解析 76 个字段，检查缺失与枚举。
   - 统一日期格式，去除空行，补齐数值列的缺失值。
   - 合并多文件后按保单号+投保确认时间去重（保留最新记录）。
   - 生成派生字段（电销、新能源、过户、异地、商险占比等）。
   - 写入 DuckDB（raw_records、daily_aggregate、policy_staff_map）。
   - 输出日志与 `validation.json`，供前端展示。
4. 完成后将原文件移动至 `data/inputs/processed/`。

## 特殊注意事项
- 日目标默认 200000 元，如需调整可在 `.env` 设置 `DAILY_TARGET`。
- 若保单号缺失业务员，需在日志中记录，同时前端会显示提示。
- 映射冲突会出现在 `validation.mismatch_count`，不得忽略。

## 派生逻辑（摘要）
- 万元整数：`round(amount / 10000)`。
- 占比：`metric / total`，并使用 `max(0, min(1, value))` 约束。
- 业务员筛选：务必要用映射中的中文姓名，而不是工号。

## 输出
- DuckDB 文件：`data/warehouse/daylyreport.duckdb`。
- 日志：`data/logs/<batch>.json`。
- 验证信息：供 `/api/kpi-windows` 与 `/api/policy-mapping` 使用。
