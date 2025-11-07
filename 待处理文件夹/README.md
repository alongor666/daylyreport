# 待处理文件夹说明

此文件夹包含旧的分析脚本、测试文件和历史数据,已从项目主目录移出。

## 文件分类

### 旧的分析脚本
- `analyze_excel.py` - 旧的Excel分析脚本
- `analyze_excel_structure.py` - Excel结构分析
- `analyze_institution_structure.py` - 机构结构分析
- `quick_stats.py` - 快速统计脚本
- `数据分析预警规则.py` - 预警规则脚本

### 测试文件
- `test_excel.py` - Excel测试
- `test_mcp.js` - MCP测试
- `excel_mcp_server.py` - MCP服务器

### 配置文件
- `claude_desktop_config.json` - Claude配置
- `package.json` / `package-lock.json` - Node.js配置
- `MCP_EXCEL_SETUP.md` - MCP设置说明

### 历史分析报告
- `车险业务数据结构分析报告.md`
- `待确认事项.md`
- `签单日平台业绩分析_10-15至11-05.txt`
- `签单日平台业绩分析报告_10-15至11-05.md`
- `签单日平台业绩明细_10-15至11-05.xlsx`
- `签单日平台业绩详细分析_10-15至11-05.md`
- `业务规则与数据洞察.md`
- `excel_analysis_report.md`

### 历史数据文件
- `三周合并数据.csv` (23MB)
- `三周趋势分析数据.csv` (24MB)
- `业务员机构团队对照表20251104.xlsx`
- `daily_stats.json`

### 旧的项目目录
- `web_dashboard/` - 旧的网页dashboard项目
- `local_xlsx_reporting/` - 本地Excel报告项目
- `车险清单_2025年10-11月/` - 旧的数据文件夹

### 临时文件
- `nul` - 系统临时文件

## 处理建议

### 可以删除的文件
- 所有测试文件 (`test_*.py`, `test_*.js`)
- 临时文件 (`nul`)
- 旧的配置文件 (`package.json`, `claude_desktop_config.json`)

### 建议保留的文件
- 历史分析报告 (作为参考)
- `业务员机构团队对照表20251104.xlsx` (可能需要)
- 业务规则文档

### 可以归档的大文件
- `三周合并数据.csv` (23MB) - 如果不再需要可以删除
- `三周趋势分析数据.csv` (24MB) - 如果不再需要可以删除

## 当前项目状态

新的项目已经完成,使用全新的架构:

```
daylyreport/
├── backend/         # 后端服务
├── static/          # 前端资源
├── data/            # 数据目录
├── *.md             # 项目文档
└── 待处理文件夹/    # 本文件夹
```

如果旧文件不再需要,可以安全删除本文件夹。

---

*创建时间: 2025-11-06*
