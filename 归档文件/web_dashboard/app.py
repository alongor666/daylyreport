#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
本应用提供一个本地可视化网页，用于对目录中的xlsx车险签单日报进行现代化图表展示。

技术栈：
- 后端：Flask（本地API，读取xlsx并聚合数据）
- 前端：ECharts + 原生JS，苹果发布会风格极简深色UI

运行方式：
python3 web_dashboard/app.py
然后在浏览器访问 http://127.0.0.1:8000/

环境变量：
- REPORT_INPUT_DIR：可选，指定xlsx输入目录；未提供时使用默认工作目录。
"""

import os
import sys
from datetime import datetime, date
from typing import Dict, List, Optional, Tuple

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import pandas as pd
import os
from typing import Tuple

# 为了复用已实现的读取与聚合逻辑，将工作根目录加入Python路径
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

try:
    from local_xlsx_reporting.generate_daily_report import (
        find_excel_files,
        load_one_file,
        filter_by_date_range,
        compute_daily_metrics,
        aggregate_dimensions,
        parse_date_from_filename,
    )
except Exception as e:
    raise RuntimeError(f"无法导入报表逻辑模块，请确认路径：{e}")


app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# 内存缓存：按文件与结果集加速
PER_FILE_CACHE: Dict[str, pd.DataFrame] = {}
PER_FILE_META: Dict[str, Tuple[float, int]] = {}
AGG_CACHE: Dict[Tuple[str, str, str], object] = {}


def get_input_dir() -> str:
    """获取输入目录。

    优先使用环境变量 REPORT_INPUT_DIR；否则默认到项目工作目录中的『车险签单清单_2025年3月』。
    """
    env_dir = os.environ.get("REPORT_INPUT_DIR")
    if env_dir and os.path.isdir(env_dir):
        return env_dir
    # 默认目录：与当前工作空间一致
    default_dir = os.path.join(PROJECT_ROOT, "车险签单清单_2025年3月")
    if os.path.isdir(default_dir):
        return default_dir
    # 兜底：使用当前工作目录
    return os.getcwd()


def scan_files_and_range(input_dir: str) -> Tuple[List[str], Optional[date], Optional[date]]:
    """扫描目录中的目标xlsx文件，并基于文件名推导日期范围（最小/最大）。"""
    files = find_excel_files(input_dir)
    dates: List[date] = []
    for p in files:
        fname = os.path.basename(p)
        d = parse_date_from_filename(fname)
        if d:
            dates.append(d)
    start = min(dates) if dates else None
    end = max(dates) if dates else None
    return files, start, end


def serialize_df(df) -> List[Dict]:
    """将DataFrame序列化为列表字典，便于JSON响应。"""
    return df.to_dict(orient="records")


def list_files_in_range(input_dir: str, start: date, end: date) -> List[str]:
    """
    根据文件名中的日期，仅选择所需区间内的xlsx文件。
    这样避免无谓读取所有文件，大幅降低IO与解析开销。
    """
    files, _, _ = scan_files_and_range(input_dir)
    selected: List[str] = []
    for p in files:
        fname = os.path.basename(p)
        d = parse_date_from_filename(fname)
        if d and (start <= d <= end):
            selected.append(p)
    return selected


def load_file_cached(path: str) -> pd.DataFrame:
    """
    读取单个xlsx文件并进行缓存：
    - 以文件的修改时间与大小作为签名；若未变更则复用缓存的DataFrame。
    - 显著减少重复请求时的解析时间。
    """
    try:
        st = os.stat(path)
        sig = (st.st_mtime, st.st_size)
    except Exception:
        sig = None
    if sig and (path in PER_FILE_META) and (PER_FILE_META[path] == sig) and (path in PER_FILE_CACHE):
        return PER_FILE_CACHE[path]
    df, _ = load_one_file(path)
    PER_FILE_META[path] = sig
    PER_FILE_CACHE[path] = df
    return df


def build_dataframe(start_date: str, end_date: str):
    """
    构建并返回指定日期范围内的标准化DataFrame。
    仅加载文件名日期位于区间内的xlsx，并进行内存缓存。
    参数格式：YYYY-MM-DD
    """
    input_dir = get_input_dir()
    start = datetime.strptime(start_date, "%Y-%m-%d").date()
    end = datetime.strptime(end_date, "%Y-%m-%d").date()
    selected = list_files_in_range(input_dir, start, end)
    if not selected:
        return pd.DataFrame()
    frames = [load_file_cached(p) for p in selected]
    all_df = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    rng_df = filter_by_date_range(all_df, start, end)
    return rng_df


@app.route("/")
def index():
    """首页：渲染可视化页面模板。"""
    return render_template("index.html")


@app.route("/api/meta")
def api_meta():
    """元信息接口：返回当前扫描的文件数与可用日期范围。"""
    input_dir = get_input_dir()
    files, start, end = scan_files_and_range(input_dir)
    return jsonify({
        "input_dir": input_dir,
        "file_count": len(files),
        "start": start.isoformat() if start else None,
        "end": end.isoformat() if end else None,
    })


@app.route("/api/daily")
def api_daily():
    """每日指标接口：基于日期范围汇总每日原保/批单件数与保费、净保费、交强/商业拆分。"""
    start_str = request.args.get("start")
    end_str = request.args.get("end")
    if not start_str or not end_str:
        return jsonify({"error": "缺少start或end参数，格式YYYY-MM-DD"}), 400
    # 结果缓存命中直接返回
    key = ("daily", start_str, end_str)
    if key in AGG_CACHE:
        return jsonify(AGG_CACHE[key])
    df = build_dataframe(start_str, end_str)
    if df is None or df.empty:
        return jsonify([])
    daily = compute_daily_metrics(df)
    AGG_CACHE[key] = serialize_df(daily)
    return jsonify(AGG_CACHE[key])


@app.route("/api/dim")
def api_dim():
    """维度聚合接口：type可选org/channel/risk，返回日期×维度的件数与保费。"""
    dim_type = request.args.get("type", "org")
    start_str = request.args.get("start")
    end_str = request.args.get("end")
    if not start_str or not end_str:
        return jsonify({"error": "缺少start或end参数，格式YYYY-MM-DD"}), 400
    # 结果缓存命中直接返回
    key_cache = (f"dim:{dim_type}", start_str, end_str)
    if key_cache in AGG_CACHE:
        return jsonify(AGG_CACHE[key_cache])
    df = build_dataframe(start_str, end_str)
    if df is None or df.empty:
        return jsonify([])
    dims = aggregate_dimensions(df)

    key_map = {"org": "机构", "channel": "渠道", "risk": "险种"}
    key = key_map.get(dim_type, "机构")
    out = dims.get(key, pd.DataFrame())
    # 提供总汇总按维度排序（保费降序）
    if not out.empty:
        try:
            out_sorted = out.copy()
            out_sorted["保费"] = pd.to_numeric(out_sorted["保费"], errors="coerce").fillna(0)
            out_sorted = out_sorted.sort_values(["日期", "保费"], ascending=[True, False])
            out_records = serialize_df(out_sorted)
            AGG_CACHE[key_cache] = out_records
            return jsonify(out_records)
        except Exception:
            out_records = serialize_df(out)
            AGG_CACHE[key_cache] = out_records
            return jsonify(out_records)
    AGG_CACHE[key_cache] = []
    return jsonify([])


@app.route("/api/kpi")
def api_kpi():
    """
    返回所选日期区间的关键指标KPI。
    指标包含：净保费、原保保费、批单保费净额、原保件数、批单件数、总件数、交强保费、商业保费、商业占比、交强占比。
    参数：start、end（YYYY-MM-DD）
    """
    start = request.args.get("start")
    end = request.args.get("end")
    if not start or not end:
        return jsonify({"error": "缺少start或end参数，格式YYYY-MM-DD"}), 400
    # 缓存命中
    key = ("kpi", start, end)
    if key in AGG_CACHE:
        return jsonify(AGG_CACHE[key])
    df = build_dataframe(start, end)
    if df is None or df.empty:
        AGG_CACHE[key] = {}
        return jsonify(AGG_CACHE[key])

    # 数值列安全转换
    for col in ["签单保费", "原保保费", "批单保费净额"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
        else:
            df[col] = 0

    # 件数标记
    is_policy = df.get("是否原保", pd.Series(False, index=df.index))
    is_endorse = df.get("是否批单", pd.Series(False, index=df.index))
    policy_cnt = int(pd.to_numeric(is_policy, errors="coerce").fillna(0).sum())
    endorse_cnt = int(pd.to_numeric(is_endorse, errors="coerce").fillna(0).sum())
    total_cnt = int(len(df))

    net_premium = float(df["签单保费"].sum())
    orig_premium = float(df["原保保费"].sum())
    endorse_net = float(df["批单保费净额"].sum())

    # 险种拆分
    risk_col = df.get("险种名称")
    if risk_col is None:
        df["险种名称"] = "未知"
        risk_col = df["险种名称"]
    mtpl_premium = float(df.loc[risk_col == "交强险", "签单保费"].sum())
    comm_premium = float(df.loc[risk_col == "商业险", "签单保费"].sum())

    comm_ratio = float(comm_premium / net_premium) if net_premium else 0.0
    mtpl_ratio = float(mtpl_premium / net_premium) if net_premium else 0.0

    out = {
        "净保费": net_premium,
        "原保保费": orig_premium,
        "批单保费净额": endorse_net,
        "原保件数": policy_cnt,
        "批单件数": endorse_cnt,
        "总件数": total_cnt,
        "交强保费": mtpl_premium,
        "商业保费": comm_premium,
        "商业占比": comm_ratio,
        "交强占比": mtpl_ratio
    }
    AGG_CACHE[key] = out
    return jsonify(out)


@app.route("/api/quality")
def api_quality():
    """
    返回数据质量检查结果，包括负保费记录与重复保单号记录。
    参数：start、end（YYYY-MM-DD）
    """
    start = request.args.get("start")
    end = request.args.get("end")
    if not start or not end:
        return jsonify({"error": "缺少start或end参数，格式YYYY-MM-DD"}), 400
    df = build_dataframe(start, end)
    if df is None or df.empty:
        return jsonify({"negative": [], "duplicates": [], "duplicate_count": 0})

    # 准备列
    work = pd.DataFrame({
        "报告日期": df.get("报告日期"),
        "所属机构": df.get("所属机构"),
        "渠道名称": df.get("渠道名称"),
        "保单号": df.get("保单号"),
        "批单号": df.get("批单号"),
        "签单保费": pd.to_numeric(df.get("签单保费"), errors="coerce").fillna(0),
        "险种名称": df.get("险种名称"),
    })

    # 负保费记录
    negative_df = work[work["签单保费"] < 0].copy()
    negative = negative_df.fillna("").to_dict(orient="records")

    # 重复保单号记录
    if "保单号" in work.columns:
        dup_mask = work["保单号"].duplicated(keep=False)
        dup_df = work[dup_mask].copy().sort_values("保单号")
        duplicates = dup_df.fillna("").to_dict(orient="records")
        duplicate_count = int(work["保单号"].duplicated().sum())
    else:
        duplicates = []
        duplicate_count = 0

    return jsonify({
        "negative": negative,
        "duplicates": duplicates,
        "duplicate_count": duplicate_count
    })


@app.route("/api/monthly")
def api_monthly():
    """
    返回月度净保费汇总（单位为原值，前端显示为万元）。
    参数：start、end（YYYY-MM-DD）
    """
    start = request.args.get("start")
    end = request.args.get("end")
    if not start or not end:
        return jsonify({"error": "缺少start或end参数，格式YYYY-MM-DD"}), 400
    key = ("monthly", start, end)
    if key in AGG_CACHE:
        return jsonify(AGG_CACHE[key])
    df = build_dataframe(start, end)
    if df is None or df.empty:
        AGG_CACHE[key] = []
        return jsonify(AGG_CACHE[key])

    # 数值列与月份列
    df["签单保费"] = pd.to_numeric(df.get("签单保费"), errors="coerce").fillna(0)
    date_col = pd.to_datetime(df.get("报告日期"), errors="coerce")
    df["月份"] = date_col.dt.to_period("M").astype(str)

    monthly = (
        df.groupby("月份", as_index=False)["签单保费"].sum().sort_values("月份")
    )
    out = serialize_df(monthly)
    AGG_CACHE[key] = out
    return jsonify(out)


def create_app() -> Flask:
    """工厂函数：返回Flask应用实例，用于扩展或测试。"""
    return app


if __name__ == "__main__":
    # 启动本地服务
    app.run(host="127.0.0.1", port=8000, debug=False)