#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import sys
from typing import Optional

import pandas as pd

# 兼容作为脚本直接执行时的导入路径
try:
    from .generate_daily_report import (
        standardize_columns,
        assign_signed_premium,
        pick_best_sheet,
    )
except ImportError:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from generate_daily_report import (  # type: ignore
        standardize_columns,
        assign_signed_premium,
        pick_best_sheet,
    )


def dedup_by_policy(input_path: str, output_path: Optional[str] = None) -> str:
    xls = pd.ExcelFile(input_path)
    sheet = pick_best_sheet(xls)
    df = xls.parse(sheet)

    original_rows = len(df)
    df = standardize_columns(df)

    # 如果没有保单号列，直接输出原表到新文件
    if "保单号" not in df.columns:
        out = (
            output_path
            if output_path
            else os.path.join(
                os.path.dirname(input_path),
                os.path.splitext(os.path.basename(input_path))[0] + "_dedup.xlsx",
            )
        )
        with pd.ExcelWriter(out, engine="xlsxwriter") as w:
            df.to_excel(w, index=False, sheet_name=sheet)
        print(f"OUTPUT={out}")
        print(f"ORIGINAL_ROWS={original_rows}")
        print(f"NEW_ROWS={len(df)}")
        print("REMOVED_DUPLICATES=0")
        return out

    df = assign_signed_premium(df)

    # 排序规则：先按出单日期，后按签单保费绝对值，保留最后一条
    if "出单日期" in df.columns:
        df["_dt"] = pd.to_datetime(df["出单日期"], errors="coerce")
    else:
        df["_dt"] = pd.NaT

    signed = pd.to_numeric(df.get("签单保费", 0.0), errors="coerce").fillna(0.0)
    df["_abs"] = signed.abs()

    df = df.sort_values(["_dt", "_abs"], ascending=[True, True])
    df_dedup = df.drop_duplicates(subset=["保单号"], keep="last")

    removed = original_rows - len(df_dedup)
    df_dedup = df_dedup.drop(columns=["_dt", "_abs"], errors="ignore")

    out = (
        output_path
        if output_path
        else os.path.join(
            os.path.dirname(input_path),
            os.path.splitext(os.path.basename(input_path))[0] + "_dedup.xlsx",
        )
    )
    with pd.ExcelWriter(out, engine="xlsxwriter") as w:
        df_dedup.to_excel(w, index=False, sheet_name=sheet)

    print(f"OUTPUT={out}")
    print(f"ORIGINAL_ROWS={original_rows}")
    print(f"NEW_ROWS={len(df_dedup)}")
    print(f"REMOVED_DUPLICATES={removed}")
    return out


def main():
    parser = argparse.ArgumentParser(description="按保单号去重并保存副本")
    parser.add_argument("--input", required=True, help="输入xlsx文件路径")
    parser.add_argument("--output", required=False, help="输出xlsx文件路径")
    args = parser.parse_args()

    try:
        out = dedup_by_policy(args.input, args.output)
        print("STATUS=OK")
    except Exception as e:
        print(f"STATUS=ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()