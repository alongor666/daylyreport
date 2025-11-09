#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
本脚本基于本地xlsx文件，按日生成车险业绩日报，并输出多维度汇总。

设计原则：
- 稳健：兼容不同Excel列名与表结构，自动识别工作表与日期。
- 可维护：函数清晰、注释中文，参数化输入输出路径与日期范围。
- 管理视角：输出总览与常用维度（机构、渠道、险种）的聚合报表。

使用示例：
python3 local_xlsx_reporting/generate_daily_report.py \
  --input-dir "/Users/.../车险签单清单_2025年3月" \
  --start-date 2025-03-08 --end-date 2025-03-25 \
  --output "日报汇总-20250308-20250325.xlsx"

支持 --per-day-files 单独输出每日文件；支持 --dry-run 仅扫描列名与文件。
"""

import argparse
import os
import re
from datetime import datetime, date
from typing import List, Optional, Dict, Tuple

import pandas as pd


# =========================
# 配置与列名映射
# =========================

# 兼容多种中文列名，统一到标准字段名
COLUMN_SYNONYMS: Dict[str, List[str]] = {
    "保单号": ["保单号", "保单号码", "保单编号"],
    "批单号": ["批单号", "批单号码", "批单编号"],
    "业务类型": ["业务类型", "单据类型", "类型"],
    "批单类型": ["批单类型", "批改类型", "批改原因"],
    "险种名称": ["险种名称", "险种", "保险险种"],
    "出单日期": ["出单日期", "起保日期", "签单日期", "承保日期"],
    "所属机构": ["所属机构", "机构名称", "归属机构", "归属部门", "机构"],
    "渠道名称": ["渠道名称", "渠道", "出单渠道", "渠道类别"],
    "承保保费": ["承保保费", "保费", "保费金额", "实收保费", "保费合计"],
    "车辆种类": ["车辆种类", "车辆类型", "车型分类", "车辆用途"],
    "车牌号": ["车牌号", "号牌号码", "车牌号码"],
    "车架号": ["车架号", "车架号码", "VIN", "VIN码"],
    "客户名称": ["客户名称", "被保险人", "投保人", "客户"],
}


# =========================
# 工具函数
# =========================

def ensure_dir(path: str) -> None:
    """确保输出目录存在。

    参数：
    - path: 输出文件路径或目录路径
    """
    out_dir = os.path.dirname(path) if os.path.splitext(path)[1] else path
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)


def is_target_file(filename: str) -> bool:
    """判断是否为目标文件：形如『保批单业务报表-YYYYMMDD.xlsx』。

    说明：仅匹配顶层文件，忽略『混乱/』目录。
    """
    return bool(re.match(r"^保批单业务报表-\d{8}\.xlsx$", filename))


def parse_date_from_filename(filename: str) -> Optional[date]:
    """从文件名解析日期，格式YYYYMMDD。

    示例：保批单业务报表-20250318.xlsx -> 2025-03-18
    """
    m = re.match(r"^保批单业务报表-(\d{8})\.xlsx$", filename)
    if not m:
        return None
    dt_str = m.group(1)
    try:
        return datetime.strptime(dt_str, "%Y%m%d").date()
    except Exception:
        return None


def pick_best_sheet(xls: pd.ExcelFile) -> str:
    """选择最可能的数据工作表。

    策略：
    - 优先选择名称包含『业务』『数据』『报表』的sheet。
    - 其次选择列数最多的sheet。
    """
    candidates = []
    for name in xls.sheet_names:
        low = name.lower()
        score = 0
        if any(k in low for k in ["业务", "数据", "报表", "明细"]):
            score += 10
        try:
            df = xls.parse(name, nrows=5)
            score += df.shape[1]
        except Exception:
            pass
        candidates.append((name, score))
    candidates.sort(key=lambda x: x[1], reverse=True)
    return candidates[0][0] if candidates else xls.sheet_names[0]


def find_excel_files(input_dir: str) -> List[str]:
    """扫描目录，找到所有目标xlsx文件。

    参数：
    - input_dir: 输入目录

    返回：
    - 文件绝对路径列表
    """
    files = []
    for entry in os.listdir(input_dir):
        full = os.path.join(input_dir, entry)
        if os.path.isdir(full):
            # 忽略『混乱』子目录，以免混入其他险种杂表
            if os.path.basename(full) == "混乱":
                continue
            # 顶层策略：仅处理顶层标准命名文件，不递归
            continue
        if is_target_file(entry):
            files.append(full)
    files.sort()
    return files


def _match_column(columns: List[str], synonyms: List[str]) -> Optional[str]:
    """在给定列名列表中，匹配同义列名，返回实际存在的列名。

    说明：采用大小写与空白鲁棒匹配。
    """
    norm = {c.strip().lower(): c for c in columns}
    for s in synonyms:
        key = s.strip().lower()
        if key in norm:
            return norm[key]
    # 宽松包含式匹配（例如『号牌号码』包含『车牌』）
    for s in synonyms:
        for c in columns:
            if s.lower() in c.strip().lower():
                return c
    return None


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """将DataFrame列统一映射为标准字段名。

    返回：新DataFrame，包含尽可能多的标准列；保留原列以便溯源。
    """
    df2 = df.copy()
    col_map = {}
    cols = list(df2.columns)
    for std_name, syns in COLUMN_SYNONYMS.items():
        m = _match_column(cols, syns)
        if m:
            col_map[m] = std_name
    if col_map:
        df2.rename(columns=col_map, inplace=True)
    return df2


def to_numeric_safe(series: pd.Series) -> pd.Series:
    """安全地将列转为数值，无法转换的视为0。
    """
    return pd.to_numeric(series, errors="coerce").fillna(0.0)


def classify_risk(df: pd.DataFrame) -> pd.DataFrame:
    """根据『险种名称』粗略分类为『交强险』『商业险』『未知险种』。

    规则：
    - 含『交强』视为交强险
    - 含『商业』视为商业险
    - 其他为未知险种
    """
    df2 = df.copy()
    if "险种名称" in df2.columns:
        low = df2["险种名称"].astype(str).str.lower()
        df2["险种类别"] = pd.Series("未知险种", index=df2.index)
        df2.loc[low.str.contains("交强"), "险种类别"] = "交强险"
        df2.loc[low.str.contains("商业"), "险种类别"] = "商业险"
    else:
        df2["险种类别"] = "未知险种"
    return df2


def assign_signed_premium(df: pd.DataFrame) -> pd.DataFrame:
    """生成签单保费（带符号），批单退保/作废为负，批增/加费为正，其余按原值。

    说明：
    - 基础保费列优先使用『承保保费』，若不存在则尝试『保费』『实收保费』等同义列。
    - 批单类型含『退』『注销』『作废』 -> 负；含『批增』『加费』『调整增加』 -> 正。
    - 无批单类型时，业务类型为『保单』按正值处理。
    """
    df2 = df.copy()
    base_col = None
    for c in ["承保保费", "保费", "保费金额", "实收保费", "保费合计"]:
        if c in df2.columns:
            base_col = c
            break
    if base_col is None:
        # 若完全找不到保费列，创建为0
        df2["签单保费"] = 0.0
        return df2

    premium = to_numeric_safe(df2[base_col])
    signed = premium.copy()

    # 优先依据批单类型
    if "批单类型" in df2.columns:
        t = df2["批单类型"].astype(str)
        neg_mask = t.str.contains("退|注销|作废|撤销|退保")
        pos_mask = t.str.contains("批增|加费|增加|调整增加|上调")
        signed = premium
        signed = signed.where(~neg_mask, -premium)
        signed = signed.where(~pos_mask, premium.abs())

    # 其次依据业务类型
    elif "业务类型" in df2.columns:
        bt = df2["业务类型"].astype(str)
        is_policy = bt.str.contains("保单")
        is_endorse = bt.str.contains("批")
        signed = premium.where(is_policy, premium)
        signed = signed.where(~is_endorse, premium)  # 无批单类型，批单默认按原值

    df2["签单保费"] = signed.fillna(0.0)
    return df2


def tag_report_date(df: pd.DataFrame, file_date: Optional[date]) -> pd.DataFrame:
    """打上『报告日期』，优先使用『出单日期』，否则使用文件名日期。

    日期格式统一为日期型（YYYY-MM-DD）。
    """
    df2 = df.copy()
    if "出单日期" in df2.columns:
        # 尝试多格式解析
        def parse_dt(x):
            if pd.isna(x):
                return None
            try:
                return pd.to_datetime(x).date()
            except Exception:
                for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y%m%d", "%m/%d/%Y"):
                    try:
                        return datetime.strptime(str(x), fmt).date()
                    except Exception:
                        continue
                return None

        dates = df2["出单日期"].apply(parse_dt)
        df2["报告日期"] = dates.fillna(file_date if file_date else pd.NaT)
    else:
        df2["报告日期"] = file_date
    return df2


def load_one_file(path: str) -> Tuple[pd.DataFrame, Optional[date]]:
    """读取一个Excel文件，自动选择sheet并标准化列，返回DataFrame与文件名日期。
    """
    fname = os.path.basename(path)
    fdate = parse_date_from_filename(fname)
    try:
        xls = pd.ExcelFile(path)
        sheet = pick_best_sheet(xls)
        df = xls.parse(sheet, dtype=str)
    except Exception as e:
        raise RuntimeError(f"读取Excel失败: {path}, 错误: {e}")

    df = standardize_columns(df)
    df = classify_risk(df)
    df = assign_signed_premium(df)
    df = tag_report_date(df, fdate)
    return df, fdate


def filter_by_date_range(df: pd.DataFrame, start: date, end: date) -> pd.DataFrame:
    """按闭区间[start, end]过滤『报告日期』。
    """
    d = df.copy()
    d["报告日期"] = pd.to_datetime(d["报告日期"]).dt.date
    mask = (d["报告日期"] >= start) & (d["报告日期"] <= end)
    return d.loc[mask]


def compute_daily_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """计算每日报表核心指标（件数、保费、交强/商业拆分）。

    输出列：
    - 日期
    - 原保件数、批单件数、总件数
    - 原保保费、批单保费净额、净保费
    - 交强保费、商业保费
    """
    if df.empty:
        return pd.DataFrame(columns=[
            "日期", "原保件数", "批单件数", "总件数",
            "原保保费", "批单保费净额", "净保费",
            "交强保费", "商业保费"
        ])

    d = df.copy()
    d["报告日期"] = pd.to_datetime(d["报告日期"]).dt.date

    # 件数统计
    is_policy = d["业务类型"].astype(str).str.contains("保单") if "业务类型" in d.columns else pd.Series(False, index=d.index)
    is_endorse = d["业务类型"].astype(str).str.contains("批") if "业务类型" in d.columns else pd.Series(False, index=d.index)

    # 保费
    premium_signed = to_numeric_safe(d["签单保费"]) if "签单保费" in d.columns else pd.Series(0.0, index=d.index)

    # 交强/商业
    risk = d["险种类别"].astype(str) if "险种类别" in d.columns else pd.Series("未知险种", index=d.index)
    comp_mask = risk.str.contains("商业")
    mtpl_mask = risk.str.contains("交强")

    grp = d.groupby("报告日期")
    out = pd.DataFrame({
        "原保件数": grp.apply(lambda g: is_policy.loc[g.index].sum()),
        "批单件数": grp.apply(lambda g: is_endorse.loc[g.index].sum()),
        "总件数": grp.size(),
        "原保保费": grp.apply(lambda g: premium_signed.loc[g.index].where(is_policy.loc[g.index], 0).sum()),
        "批单保费净额": grp.apply(lambda g: premium_signed.loc[g.index].where(is_endorse.loc[g.index], 0).sum()),
        "净保费": grp.apply(lambda g: premium_signed.loc[g.index].sum()),
        "交强保费": grp.apply(lambda g: premium_signed.loc[g.index].where(mtpl_mask.loc[g.index], 0).sum()),
        "商业保费": grp.apply(lambda g: premium_signed.loc[g.index].where(comp_mask.loc[g.index], 0).sum()),
    })

    out.reset_index(inplace=True)
    out.rename(columns={"报告日期": "日期"}, inplace=True)
    return out


def aggregate_dimensions(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """生成常用维度汇总：机构、渠道、险种×日期的保费与件数。

    返回：包含 DataFrame 的字典：{"机构": df1, "渠道": df2, "险种": df3}
    """
    if df.empty:
        empty = pd.DataFrame(columns=["日期", "维度", "件数", "保费"])
        return {"机构": empty.copy(), "渠道": empty.copy(), "险种": empty.copy()}

    d = df.copy()
    d["报告日期"] = pd.to_datetime(d["报告日期"]).dt.date
    premium_signed = to_numeric_safe(d["签单保费"]) if "签单保费" in d.columns else pd.Series(0.0, index=d.index)

    def agg_by(col: str, title: str) -> pd.DataFrame:
        dim_col = col if col in d.columns else None
        if dim_col is None:
            return pd.DataFrame(columns=["日期", "维度", "件数", "保费"])
        g = d.groupby(["报告日期", dim_col])
        res = pd.DataFrame({
            "件数": g.size(),
            "保费": g.apply(lambda g_: premium_signed.loc[g_.index].sum()),
        }).reset_index()
        res.rename(columns={"报告日期": "日期", dim_col: "维度"}, inplace=True)
        res["维度类型"] = title
        return res

    by_org = agg_by("所属机构", "机构")
    by_chn = agg_by("渠道名称", "渠道")
    by_risk = agg_by("险种类别", "险种")

    return {"机构": by_org, "渠道": by_chn, "险种": by_risk}


def export_report(
    daily_metrics: pd.DataFrame,
    dims: Dict[str, pd.DataFrame],
    output_path: str,
) -> None:
    """导出Excel报表：总览、机构、渠道、险种三张表。

    参数：
    - daily_metrics: 每日指标表
    - dims: 维度聚合表字典
    - output_path: 输出Excel文件路径
    """
    ensure_dir(output_path)
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        daily_metrics.sort_values("日期").to_excel(writer, sheet_name="总览", index=False)
        dims.get("机构", pd.DataFrame()).sort_values(["日期", "维度"]).to_excel(writer, sheet_name="机构", index=False)
        dims.get("渠道", pd.DataFrame()).sort_values(["日期", "维度"]).to_excel(writer, sheet_name="渠道", index=False)
        dims.get("险种", pd.DataFrame()).sort_values(["日期", "维度"]).to_excel(writer, sheet_name="险种", index=False)


def export_per_day_files(df: pd.DataFrame, output_dir: str) -> None:
    """为每一天单独导出一个Excel明细文件，便于日常流转与复核。

    文件命名：『日报明细-YYYYMMDD.xlsx』。
    """
    ensure_dir(output_dir)
    df2 = df.copy()
    df2["报告日期"] = pd.to_datetime(df2["报告日期"]).dt.date
    for rdate, g in df2.groupby("报告日期"):
        fname = os.path.join(output_dir, f"日报明细-{rdate.strftime('%Y%m%d')}.xlsx")
        with pd.ExcelWriter(fname, engine="openpyxl") as writer:
            g.to_excel(writer, sheet_name="明细", index=False)


def dry_run(input_dir: str, start: Optional[date], end: Optional[date]) -> None:
    """Dry-run模式：仅扫描文件与列名，打印识别到的sheet与字段，不做导出。
    """
    files = find_excel_files(input_dir)
    if not files:
        print("未发现符合命名的xlsx文件。")
        return
    print(f"发现 {len(files)} 个文件：")
    for p in files:
        fname = os.path.basename(p)
        fdate = parse_date_from_filename(fname)
        print(f"- {fname} (日期: {fdate})")
        try:
            xls = pd.ExcelFile(p)
            sheet = pick_best_sheet(xls)
            df = xls.parse(sheet, nrows=5, dtype=str)
            df_std = standardize_columns(df)
            merged_cols = sorted(set(df.columns) | set(df_std.columns))
            print(f"  选中Sheet: {sheet}")
            print(f"  原始列: {list(df.columns)}")
            print(f"  标准化后含标准列: {[c for c in df_std.columns if c in COLUMN_SYNONYMS]}")
        except Exception as e:
            print(f"  读取失败: {e}")
    if start and end:
        print(f"日期范围: {start} 至 {end}")


def run_pipeline(input_dir: str, start: date, end: date, output_path: str, per_day_dir: Optional[str] = None) -> None:
    """完整管道：读取全部文件、按日期过滤、计算指标、导出报表与每日文件（可选）。
    """
    files = find_excel_files(input_dir)
    if not files:
        raise RuntimeError("未发现任何目标xlsx文件，请检查目录与命名。")

    frames = []
    for p in files:
        df, fdate = load_one_file(p)
        frames.append(df)
    all_df = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    rng_df = filter_by_date_range(all_df, start, end)

    daily = compute_daily_metrics(rng_df)
    dims = aggregate_dimensions(rng_df)
    export_report(daily, dims, output_path)

    if per_day_dir:
        export_per_day_files(rng_df, per_day_dir)


def parse_args() -> argparse.Namespace:
    """解析命令行参数。"""
    parser = argparse.ArgumentParser(description="本地xlsx车险日报生成器")
    parser.add_argument("--input-dir", required=True, help="输入目录（含每日xlsx文件）")
    parser.add_argument("--start-date", required=False, help="开始日期，格式YYYY-MM-DD")
    parser.add_argument("--end-date", required=False, help="结束日期，格式YYYY-MM-DD")
    parser.add_argument("--output", required=False, default="日报汇总.xlsx", help="输出汇总Excel文件路径")
    parser.add_argument("--per-day-files", required=False, help="每日明细输出目录（可选）")
    parser.add_argument("--dry-run", action="store_true", help="仅扫描文件与列名，不导出")
    return parser.parse_args()


def main():
    """主入口：根据参数运行dry-run或完整报表生成。"""
    args = parse_args()

    start = datetime.strptime(args.start_date, "%Y-%m-%d").date() if args.start_date else None
    end = datetime.strptime(args.end_date, "%Y-%m-%d").date() if args.end_date else None

    if args.dry_run:
        dry_run(args.input_dir, start, end)
        return

    if not start or not end:
        raise SystemExit("非dry-run模式需要提供 --start-date 与 --end-date")

    run_pipeline(
        input_dir=args.input_dir,
        start=start,
        end=end,
        output_path=args.output,
        per_day_dir=args.per_day_files,
    )
    print(f"已完成：{args.output}")


if __name__ == "__main__":
    main()