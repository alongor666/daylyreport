# 运维作业手册

## 任务交代
本手册总结了当前项目经验中的“隐形流程”：如何准备每日清单、如何执行摄取脚本、如何回滚、如何排查映射冲突等。目的是让未来的 AI 或运维同学无需访问旧仓库，也能完整复制日常操作。

## 日常流程
1. **数据到货**
   - 业务侧在 08:30 前将 `车险清单_YYYY年MM-XX月_合并.xlsx` 放入 `data/inputs/`。
   - 若同日多份文件，需命名为 `..._part1.xlsx`、`..._part2.xlsx`，摄取脚本会自动合并。
2. **摄取脚本**
   - 执行 `python scripts/ingest_daily.py --input data/inputs --batch-date YYYY-MM-DD --mapping data/mappings/staff_mapping.json`。
   - 脚本完成后会将原文件移动到 `data/inputs/processed/` 并在 `data/logs/` 生成 JSON 日志，包含：批次、文件列表、行数、错误信息、mismatch_count。
3. **回滚策略**
   - DuckDB 仓库位于 `data/warehouse/daylyreport.duckdb`，每次摄取前自动创建时间戳备份（`daylyreport_<batch>.bak`）。
   - 若摄取失败，可用 `scripts/restore_duckdb.py --backup <path>` 恢复。
4. **映射更新**
   - HR 导出的 `业务员机构团队归属.json` 需由数据团队手动放入 `data/mappings/` 并命名为 `staff_mapping.json`。
   - 更新后必须重新运行摄取脚本以刷新 `policy_to_staff` 与 `staff_to_info`。

## 监控与告警
- `scripts/smoke_check.sh` 每小时执行一次，若任何 API 返回非 2xx 或响应时间 > 1s，则推送到钉钉告警。
- `data/logs/` 中的最新日志若 `status=failed`，需在 30 分钟内处理并记录在 `docs/QA_CHECKLIST.md`。

## 常见问题
1. **映射缺失**：若日志中 `missing_staff` 非空，需通知 HR 补充映射，同时在前端展示“不完整映射”的黄色提示。
2. **日期越界**：若 `投保确认时间` 超出 ±30 天，脚本会直接失败；处理方式是让数据提供方修正后重跑。
3. **占比为零**：如果新的批次只有少量数据，占比可能为 0；验证时需确认不是输错字段。

## 交接要求
- 每次修改摄取脚本、映射规则或恢复流程，都要同步更新本手册。
- 运维交接时至少携带最近一次 `data/logs/*.json` 和 `docs/QA_CHECKLIST.md` 的记录，以便快速回溯。
