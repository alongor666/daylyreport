#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析车险业务的三级机构结构
"""

import pandas as pd
import numpy as np

def analyze_institution_structure():
    """分析机构结构"""
    print("正在分析机构结构...")
    print("=" * 60)
    
    try:
        # 读取机构工作表
        df = pd.read_excel("日报汇总-20250308-20250325.xlsx", sheet_name="机构")
        
        print(f"机构数据总行数: {len(df)}")
        print(f"机构数据列数: {len(df.columns)}")
        
        # 分析维度列
        print(f"\n维度列的唯一值:")
        dimensions = df['维度'].unique()
        print(f"总共有 {len(dimensions)} 个不同机构/维度")
        
        print(f"\n前20个机构/维度:")
        for i, dim in enumerate(dimensions[:20], 1):
            print(f"{i:2d}. {dim}")
        
        if len(dimensions) > 20:
            print(f"... 还有 {len(dimensions)-20} 个机构")
        
        # 分析维度类型
        print(f"\n维度类型分布:")
        dim_type_counts = df['维度类型'].value_counts()
        for dim_type, count in dim_type_counts.items():
            print(f"  {dim_type}: {count} 条记录")
        
        # 按维度类型分组显示机构
        print(f"\n按维度类型分组的机构:")
        for dim_type in df['维度类型'].unique():
            print(f"\n{dim_type}:")
            type_dimensions = df[df['维度类型'] == dim_type]['维度'].unique()
            for i, dim in enumerate(type_dimensions[:10], 1):
                print(f"  {i}. {dim}")
            if len(type_dimensions) > 10:
                print(f"  ... 还有 {len(type_dimensions)-10} 个")
        
        # 分析日期分布
        print(f"\n日期分布:")
        date_counts = df['日期'].value_counts().sort_index()
        print(f"数据时间范围: {date_counts.index.min()} 到 {date_counts.index.max()}")
        print(f"共有 {len(date_counts)} 个不同日期")
        
        # 显示前几天的数据
        print(f"\n前几天的机构数据统计:")
        for date in date_counts.head(3).index:
            day_data = df[df['日期'] == date]
            print(f"\n{date.strftime('%Y-%m-%d')}:")
            print(f"  总记录数: {len(day_data)}")
            print(f"  总件数: {day_data['件数'].sum()}")
            print(f"  总保费: {day_data['保费'].sum():,.2f}")
            print(f"  机构数: {len(day_data['维度'].unique())}")
        
        # 分析保费分布
        print(f"\n保费统计分析:")
        premium_stats = df['保费'].describe()
        print(premium_stats)
        
        # 找出保费最高的机构
        print(f"\n保费最高的前10个机构 (总保费):")
        inst_premium = df.groupby('维度')['保费'].sum().sort_values(ascending=False)
        for i, (inst, premium) in enumerate(inst_premium.head(10).items(), 1):
            print(f"{i:2d}. {inst}: {premium:,.2f}")
        
        # 找出件数最高的机构
        print(f"\n件数最高的前10个机构 (总件数):")
        inst_count = df.groupby('维度')['件数'].sum().sort_values(ascending=False)
        for i, (inst, count) in enumerate(inst_count.head(10).items(), 1):
            print(f"{i:2d}. {inst}: {count}")
        
    except Exception as e:
        print(f"分析机构结构时出错: {e}")

def analyze_risk_types():
    """分析险种结构"""
    print("\n" + "="*60)
    print("正在分析险种结构...")
    print("="*60)
    
    try:
        # 读取险种工作表
        df = pd.read_excel("日报汇总-20250308-20250325.xlsx", sheet_name="险种")
        
        print(f"险种数据总行数: {len(df)}")
        
        # 分析维度列 (险种)
        print(f"\n险种类型:")
        risk_types = df['维度'].unique()
        print(f"总共有 {len(risk_types)} 种不同险种")
        
        for i, risk in enumerate(risk_types, 1):
            risk_data = df[df['维度'] == risk]
            total_premium = risk_data['保费'].sum()
            total_count = risk_data['件数'].sum()
            print(f"{i:2d}. {risk}: 保费 {total_premium:,.2f}, 件数 {total_count}")
        
        # 分析时间趋势
        print(f"\n主要险种的时间趋势 (前5天):")
        main_risks = ['交强险', '商业险'] if any('交' in r for r in risk_types) else risk_types[:2]
        
        for risk in main_risks:
            risk_data = df[df['维度'] == risk].sort_values('日期')
            print(f"\n{risk}:")
            for _, row in risk_data.head(5).iterrows():
                print(f"  {row['日期'].strftime('%m-%d')}: 保费 {row['保费']:,.2f}, 件数 {row['件数']}")
        
    except Exception as e:
        print(f"分析险种结构时出错: {e}")

def suggest_trend_analysis_fields():
    """建议适合趋势分析的字段"""
    print("\n" + "="*60)
    print("日签单趋势分析建议字段")
    print("="*60)
    
    suggestions = {
        "核心指标": [
            "净保费 (最适合趋势分析)",
            "原保保费 (新保单业务)", 
            "商业保费 (商业险部分)",
            "交强保费 (交强险部分)"
        ],
        "业务规模": [
            "总件数 (业务量趋势)",
            "原保件数 (新保单件数)",
            "批单件数 (批改业务量)"
        ],
        "机构维度": [
            "各分公司保费趋势",
            "各支公司保费趋势",
            "机构排名变化趋势"
        ],
        "险种维度": [
            "交强险保费趋势",
            "商业险保费趋势",
            "各险种占比变化"
        ],
        "时间维度建议": [
            "按日趋势 (每日签单情况)",
            "周度汇总 (周趋势分析)",
            "月度汇总 (月度趋势)",
            "同比环比 (同期对比)"
        ]
    }
    
    for category, fields in suggestions.items():
        print(f"\n{category}:")
        for field in fields:
            print(f"  • {field}")
    
    print(f"\n建议的趋势分析图表类型:")
    chart_suggestions = [
        "折线图 - 日保费趋势",
        "柱状图 - 各机构对比",
        "堆积图 - 险种构成变化",
        "双轴图 - 保费+件数趋势",
        "热力图 - 各机构每日表现"
    ]
    
    for chart in chart_suggestions:
        print(f"  • {chart}")

if __name__ == "__main__":
    analyze_institution_structure()
    analyze_risk_types()
    suggest_trend_analysis_fields()