#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CSV 字段分析器

功能：
- 读取指定 CSV 文件，分析每个字段的类型、常见格式、取值范围；
- 对文本型字段，穷举所有唯一取值（含计数）；
- 输出 Markdown 文档，便于审阅与归档。

使用：
- 直接运行本脚本，会分析项目根目录下的 `车险清单_2025年10-11月_合并.csv` 并在 `开发文档/` 生成同名字段说明文档；
- 也可通过命令行参数指定输入/输出路径。
"""

import csv
import os
import re
from datetime import datetime
from collections import Counter, defaultdict
from typing import List, Dict, Tuple, Optional, Any, Type, Union


# -----------------------------
# 类型与格式识别辅助
# -----------------------------

def _is_missing(value: str) -> bool:
    """判断是否为空/缺失值（中文函数级注释）

    说明：
    - 将常见空值标记（空串、NA、N/A、null、None、-）视作缺失；
    - 去除前后空白后进行匹配。
    """
    if value is None:
        return True
    v = str(value).strip()
    return v == "" or v.lower() in {"na", "n/a", "null", "none"} or v == "-"


def _strip_thousand_sep(s: str) -> str:
    """移除千分位分隔符与空格（中文函数级注释）

    说明：
    - 去除常见的千分位逗号与空格，保留小数点与负号；
    - 不修改百分号与货币符号，由上层逻辑分别检测。
    """
    return s.replace(",", "").replace(" ", "")


def _detect_date(value: str) -> Optional[Tuple[datetime, str, bool]]:
    """检测日期/时间格式并解析为 datetime（中文函数级注释）

    返回：
    - (parsed_datetime, format_string, has_time) 或 None

    支持格式示例：
    - YYYY-MM-DD, YYYY/MM/DD, YYYY.MM.DD
    - YYYY-MM-DD HH:MM[:SS], YYYY/MM/DD HH:MM[:SS]
    - YYYYMMDD
    """
    if not isinstance(value, str):
        return None
    v = value.strip()
    if not v:
        return None
    formats = [
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%Y.%m.%d",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d %H:%M:%S",
        "%Y/%m/%d %H:%M",
        "%Y/%m/%d %H:%M:%S",
        "%Y%m%d",
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(v, fmt)
            has_time = any(token in fmt for token in ["%H", "%M", "%S"])
            return dt, fmt, has_time
        except Exception:
            continue
    return None


def _classify_numeric(value: str) -> Optional[Dict[str, Any]]:
    """识别数值、百分比与货币，并返回分类信息（中文函数级注释）

    返回：
    - dict: {category, numeric_value, format, currency_symbol}
      - category ∈ {"integer","float","percentage","currency"}
      - numeric_value: 浮点表示的数值
      - format: 粗略格式描述，如“无小数/两位小数/千分位/含%/含¥”
      - currency_symbol: 若为货币，记录符号或单位
    - None: 非数值型

    识别策略：
    - 先识别百分比（带 %），再识别货币（¥/￥/元/RMB/CNY/$/HK$ 等）；
    - 移除千分位分隔符后尝试解析整数/浮点；
    - 保留原始格式线索用于报告。
    """
    if not isinstance(value, str):
        return None
    raw = value.strip()
    if raw == "":
        return None

    # 百分比
    m = re.match(r"^\s*([-+]?\d+(?:\.\d+)?)\s*%\s*$", raw)
    if m:
        num = float(m.group(1))
        return {
            "category": "percentage",
            "numeric_value": num,
            "format": "百分比（含%）",
            "currency_symbol": None,
        }

    # 货币：常见中文/英文符号与单位
    currency_patterns = [
        (r"^(¥|￥|RMB|CNY|HK\$|\$)?\s*([-+]?\d[\d,]*(?:\.\d+)?)\s*(元|人民币)?$", True),
    ]
    for pat, _ in currency_patterns:
        m = re.match(pat, raw, re.IGNORECASE)
        if m:
            symbol = m.group(1) or (m.group(3) if m.group(3) else None)
            num_str = _strip_thousand_sep(m.group(2))
            try:
                num = float(num_str)
                fmt = "货币（含符号/单位/千分位）" if "," in m.group(2) else "货币（含符号/单位）"
                return {
                    "category": "currency",
                    "numeric_value": num,
                    "format": fmt,
                    "currency_symbol": symbol,
                }
            except Exception:
                pass

    # 纯数字（整数/浮点，允许千分位）
    cleaned = _strip_thousand_sep(raw)
    # 整数
    if re.match(r"^[-+]?\d+$", cleaned):
        try:
            num = int(cleaned)
            fmt = "整数（无小数{}）".format("，含千分位" if "," in raw else "")
            return {
                "category": "integer",
                "numeric_value": float(num),
                "format": fmt,
                "currency_symbol": None,
            }
        except Exception:
            pass
    # 浮点
    if re.match(r"^[-+]?\d*\.\d+$", cleaned) or re.match(r"^[-+]?\d+\.\d*$", cleaned):
        try:
            num = float(cleaned)
            fmt = "浮点数（含小数{}）".format("，含千分位" if "," in raw else "")
            return {
                "category": "float",
                "numeric_value": num,
                "format": fmt,
                "currency_symbol": None,
            }
        except Exception:
            pass

    return None


def _summarize_column(values: List[str]) -> Dict[str, Any]:
    """对单列数据进行类型归类与统计（中文函数级注释）

    输入：
    - values：某字段的原始字符串列表

    输出：
    - 包含类型计数、格式集合、范围（数值/日期/文本长度）、唯一值等的综合摘要
    """
    missing = 0
    type_counts = Counter()
    formats = Counter()
    currency_symbols = Counter()
    numeric_min, numeric_max = None, None
    date_min, date_max = None, None
    has_time_flag = False
    text_counter = Counter()
    text_len_min, text_len_max = None, None

    for raw in values:
        if _is_missing(raw):
            missing += 1
            continue
        # 日期/时间识别
        d = _detect_date(str(raw))
        if d:
            dt, fmt, has_time = d
            type_counts["datetime" if has_time else "date"] += 1
            formats[fmt] += 1
            has_time_flag = has_time_flag or has_time
            date_min = dt if date_min is None or dt < date_min else date_min
            date_max = dt if date_max is None or dt > date_max else date_max
            continue

        # 数值/百分比/货币识别
        num_info = _classify_numeric(str(raw))
        if num_info:
            cat = num_info["category"]
            type_counts[cat] += 1
            formats[num_info["format"]] += 1
            if cat == "currency" and num_info.get("currency_symbol"):
                currency_symbols[num_info["currency_symbol"]] += 1
            val = num_info["numeric_value"]
            numeric_min = val if numeric_min is None or val < numeric_min else numeric_min
            numeric_max = val if numeric_max is None or val > numeric_max else numeric_max
            continue

        # 文本
        s = str(raw).strip()
        type_counts["text"] += 1
        text_counter[s] += 1
        l = len(s)
        text_len_min = l if text_len_min is None or l < text_len_min else text_len_min
        text_len_max = l if text_len_max is None or l > text_len_max else text_len_max

    total = len(values)
    non_missing = total - missing

    # 最终类型判定优先级
    final_type = None
    if type_counts["date"] + type_counts["datetime"] == non_missing and non_missing > 0:
        final_type = "日期时间" if type_counts["datetime"] > 0 else "日期"
    elif type_counts["percentage"] == non_missing and non_missing > 0:
        final_type = "百分比"
    elif type_counts["currency"] == non_missing and non_missing > 0:
        final_type = "货币"
    elif (type_counts["integer"] + type_counts["float"]) == non_missing and non_missing > 0:
        final_type = "数值（整数/浮点）" if (type_counts["integer"] > 0 and type_counts["float"] > 0) else ("整数" if type_counts["integer"] > 0 else "浮点数")
    else:
        final_type = "文本"

    return {
        "total": total,
        "missing": missing,
        "non_missing": non_missing,
        "type_counts": type_counts,
        "final_type": final_type,
        "formats": formats,
        "currency_symbols": currency_symbols,
        "numeric_min": numeric_min,
        "numeric_max": numeric_max,
        "date_min": date_min,
        "date_max": date_max,
        "has_time": has_time_flag,
        "text_counter": text_counter,
        "text_len_min": text_len_min,
        "text_len_max": text_len_max,
    }


def _is_sensitive_field(name: str) -> bool:
    """判断字段是否为敏感字段（中文函数级注释）

    说明：
    - 为保护隐私与合规，以下字段的“文本明细穷举”将被隐藏；
    - 采用关键字匹配，覆盖可能的同义字段名（如“车牌号/号牌号码”）。

    隐藏范围：
    - 被保险人、投保人
    - 车牌号码/车牌号/号牌号码
    - 车架号码/车架号/VIN
    - 发动机号码/发动机号
    - 批单号码/批单号
    - 续保号码/续保单号
    - 行驶证车主（含同义词：行驶证持有人/行驶证所有人）
    """
    if not isinstance(name, str):
        return False
    n = name.strip()
    keywords = [
        "被保险人",
        "投保人",
        "车牌号码",
        "车牌号",
        "号牌号码",
        "车架号码",
        "车架号",
        "VIN",
        "发动机号码",
        "发动机号",
        "批单号码",
        "批单号",
        "续保号码",
        "续保单号",
        "行驶证车主",
        "行驶证持有人",
        "行驶证所有人",
    ]
    return any(k in n for k in keywords)


def _is_detail_masked_field(name: str) -> bool:
    """判断字段是否仅屏蔽“文本明细”（中文函数级注释）

    说明：
    - 与 `_is_sensitive_field`（章节删除）不同，本函数用于保留章节但屏蔽文本穷举明细；
    - 当前仅针对“客户名称”类字段进行屏蔽，以减少敏感信息暴露风险。

    屏蔽范围：
    - 客户名称（含可能同义：客户姓名/客户名称）
    """
    if not isinstance(name, str):
        return False
    n = name.strip()
    keywords = [
        "客户名称",
        "客户姓名",
    ]
    return any(k in n for k in keywords)


def _sniff_dialect(file_path: str) -> Union[str, csv.Dialect, Type[csv.Dialect]]:
    """自动检测 CSV 方言（分隔符/引号）（中文函数级注释）

    说明：
    - 使用 `csv.Sniffer` 从前 4KB 样本推断分隔符与引号；
    - 若检测失败，退回默认逗号分隔。
    """
    with open(file_path, "r", encoding="utf-8-sig") as f:
        sample = f.read(4096)
    try:
        # 说明：部分类型检查器将 sniff 返回值视为 Dialect 的类型（类）而非实例，
        # 但 `csv.reader` 可接受字符串名称、Dialect 类或实例。此处直接返回原值，
        # 并在回退时使用内置的 'excel' 方言名称以保证兼容性。
        dialect = csv.Sniffer().sniff(sample)
        return dialect
    except Exception:
        # 使用内置方言名称回退，避免返回类型与注解不匹配问题。
        return "excel"


def _read_csv(file_path: str) -> Tuple[List[str], List[List[str]]]:
    """读取 CSV 文件并返回表头与数据行（中文函数级注释）

    输入：
    - file_path：CSV 文件路径

    输出：
    - (headers, rows)：表头列表与数据行列表（每行为字符串列表）
    """
    dialect = _sniff_dialect(file_path)
    with open(file_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f, dialect)
        rows = list(reader)
    if not rows:
        return [], []
    headers = rows[0]
    data_rows = rows[1:]
    return headers, data_rows


def _generate_markdown(
    file_name: str,
    headers: List[str],
    column_summaries: Dict[str, Dict[str, Any]],
) -> str:
    """生成 Markdown 文档内容（中文函数级注释）

    说明：
    - 顶部写入文件信息与总览；
    - 每个字段生成独立小节，包含类型、格式、范围与文本穷举（含计数）。
    - 合规要求：命中敏感字段（如被保险人/投保人/车牌/车架/发动机/批单/续保等），完全跳过该字段章节（永久删除）。
    """
    total_rows = max((column_summaries.get(headers[0], {}).get("total", 0)), 0) if headers else 0
    lines: List[str] = []
    lines.append(f"# 字段说明：{file_name}")
    lines.append("")
    lines.append("> 本文档根据 CSV 内容自动生成，列出每个字段的类型、格式与值域；文本类字段穷举全部取值用于数据核查。")
    lines.append("")
    lines.append(f"- 总行数：{total_rows}")
    lines.append(f"- 字段数：{len(headers)}")
    lines.append("")

    for col in headers:
        # 合规：敏感字段章节直接跳过（不写入到文档中）
        if _is_sensitive_field(col):
            continue
        s = column_summaries[col]
        lines.append(f"## 字段：{col}")
        lines.append("")
        lines.append(f"- 类型：{s['final_type']}")
        # 格式集合
        if s["formats"]:
            fmt_list = [f"{fmt}（{cnt}次）" for fmt, cnt in s["formats"].most_common()]
            lines.append(f"- 格式：{'；'.join(fmt_list)}")
        else:
            lines.append("- 格式：无明显格式特征")
        # 货币符号
        if s["currency_symbols"]:
            sym_list = [f"{sym}（{cnt}次）" for sym, cnt in s["currency_symbols"].most_common()]
            lines.append(f"- 货币符号/单位：{'；'.join(sym_list)}")
        # 缺失值
        miss_pct = (s["missing"] / s["total"] * 100) if s["total"] > 0 else 0.0
        lines.append(f"- 缺失值：{s['missing']}（{miss_pct:.2f}%）")
        # 范围
        if s["final_type"] in {"整数", "浮点数", "数值（整数/浮点）", "百分比", "货币"}:
            if s["numeric_min"] is not None and s["numeric_max"] is not None:
                lines.append(f"- 值域范围：{s['numeric_min']} ~ {s['numeric_max']}")
        elif s["final_type"] in {"日期", "日期时间"}:
            if s["date_min"] is not None and s["date_max"] is not None:
                dt_min = s["date_min"].strftime("%Y-%m-%d %H:%M:%S") if s["has_time"] else s["date_min"].strftime("%Y-%m-%d")
                dt_max = s["date_max"].strftime("%Y-%m-%d %H:%M:%S") if s["has_time"] else s["date_max"].strftime("%Y-%m-%d")
                lines.append(f"- 值域范围：{dt_min} ~ {dt_max}")
        else:  # 文本
            if s["text_len_min"] is not None and s["text_len_max"] is not None:
                lines.append(f"- 文本长度范围：{s['text_len_min']} ~ {s['text_len_max']}")

        # 文本穷举
        if s["final_type"] == "文本":
            if _is_detail_masked_field(col):
                # 合规：仅屏蔽文本明细，但保留章节与统计信息
                lines.append("- 隐私字段：已省略具体取值明细。")
            else:
                unique_count = len(s["text_counter"]) 
                lines.append(f"- 取值全集（共 {unique_count} 项，含计数）：")
                # 为避免单行过长，按字典序输出：值（计数）
                for val in sorted(s["text_counter"].items(), key=lambda x: (x[0])):
                    safe_val = val[0] if val[0] != "" else "<空字符串>"
                    lines.append(f"  - {safe_val}（{val[1]}）")

        lines.append("")

    return "\n".join(lines)


def _analyze_csv(file_path: str) -> Tuple[List[str], Dict[str, Dict[str, Any]]]:
    """对 CSV 文件执行列级分析并返回摘要（中文函数级注释）

    输入：
    - file_path：CSV 文件路径

    输出：
    - (headers, column_summaries)：表头与每列摘要字典
    """
    headers, rows = _read_csv(file_path)
    if not headers:
        return [], {}

    columns: Dict[str, List[str]] = {h: [] for h in headers}
    for row in rows:
        # 对齐长度不足的行（填充空串）
        if len(row) < len(headers):
            row = row + [""] * (len(headers) - len(row))
        for i, h in enumerate(headers):
            columns[h].append(row[i])

    summaries: Dict[str, Dict[str, Any]] = {}
    for h, vals in columns.items():
        summaries[h] = _summarize_column(vals)
    return headers, summaries


def write_markdown(output_path: str, content: str) -> None:
    """写入 Markdown 文件（中文函数级注释）

    说明：
    - 确保输出目录存在；
    - 将生成内容写入指定路径（UTF-8）。
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)


def main(input_path: Optional[str] = None, output_path: Optional[str] = None) -> None:
    """主入口：执行 CSV 分析并生成字段说明文档（中文函数级注释）

    参数：
    - input_path：输入 CSV 路径，默认使用项目根目录下的车险清单文件；
    - output_path：输出 Markdown 文档路径，默认写入开发文档目录。

    行为：
    - 分析每列的数据类型、格式、范围；
    - 文本列穷举所有取值（含计数）；
    - 控制台打印结果路径与摘要信息。
    """
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    default_input = os.path.join(project_root, "车险清单_2025年10-11月_合并.csv")
    default_output = os.path.join(project_root, "开发文档", "车险清单_2025年10-11月_合并-字段说明.md")

    input_file = input_path or default_input
    output_file = output_path or default_output

    if not os.path.exists(input_file):
        print(f"[错误] 找不到输入文件：{input_file}")
        return

    headers, summaries = _analyze_csv(input_file)
    if not headers:
        print("[警告] CSV 文件为空或无表头，未生成文档。")
        return

    md = _generate_markdown(os.path.basename(input_file), headers, summaries)
    write_markdown(output_file, md)
    total_rows = next(iter(summaries.values())).get("total", 0) if summaries else 0
    print(f"[完成] 文档已生成：{output_file} ；总行数：{total_rows}，字段数：{len(headers)}")


if __name__ == "__main__":
    # 支持从命令行传参：python3 scripts/csv_field_profiler.py [input_csv] [output_md]
    import sys
    args = sys.argv[1:]
    inp = args[0] if len(args) >= 1 else None
    outp = args[1] if len(args) >= 2 else None
    main(inp, outp)