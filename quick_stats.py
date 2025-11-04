#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速统计脚本 - 生成关键业务指标
"""

import pandas as pd
import numpy as np

def quick_stats():
    """生成快速统计报告"""
    file_path = "/Users/xuechenglong/Library/CloudStorage/GoogleDrive-alongor0512@gmail.com/我的云端硬盘/WPS+iMac/车险签单清单_2025年3月/保批单业务报表-20250325.xlsx"
    
    try:
        # 读取主要工作表
        df = pd.read_excel(file_path, sheet_name='车险保批单报表')
        
        print("=" * 60)
        print("车险保批单业务快速统计报告")
        print("=" * 60)
        print(f"数据日期: 2025-03-25")
        print(f"总记录数: {len(df):,}")
        print(f"总字段数: {len(df.columns)}")
        print()
        
        # 核心业务指标
        print("【核心业务指标】")
        print("-" * 40)
        
        # 险种分布
        print("险种大类分布:")
        险种分布 = df['险种大类'].value_counts()
        for 险种, 数量 in 险种分布.items():
            占比 = 数量 / len(df) * 100
            print(f"  {险种}: {数量:,} ({占比:.1f}%)")
        print()
        
        # 续保情况
        print("续保情况分布:")
        续保分布 = df['是否续保'].value_counts()
        for 续保, 数量 in 续保分布.items():
            占比 = 数量 / len(df) * 100
            print(f"  {续保}: {数量:,} ({占比:.1f}%)")
        print()
        
        # 客户类别
        print("客户类别分布 (TOP 5):")
        客户分布 = df['客户类别'].value_counts().head(5)
        for 客户, 数量 in 客户分布.items():
            占比 = 数量 / len(df) * 100
            print(f"  {客户}: {数量:,} ({占比:.1f}%)")
        print()
        
        # 财务指标
        print("【财务指标】")
        print("-" * 40)
        
        # 保费统计
        总保费 = df['签单保费'].sum()
        平均保费 = df['签单保费'].mean()
        保费中位数 = df['签单保费'].median()
        print(f"签单保费总额: {总保费:,.2f} 元")
        print(f"平均保费: {平均保费:.2f} 元")
        print(f"保费中位数: {保费中位数:.2f} 元")
        print()
        
        # 保额统计
        总保额 = df['签单保额'].sum()
        平均保额 = df['签单保额'].mean()
        print(f"签单保额总额: {总保额:,.2f} 元")
        print(f"平均保额: {平均保额:.2f} 元")
        print()
        
        # 手续费统计
        总手续费 = df['手续费'].sum()
        平均手续费 = df['手续费'].mean()
        print(f"手续费总额: {总手续费:,.2f} 元")
        print(f"平均手续费: {平均手续费:.2f} 元")
        print()
        
        # 地理分布
        print("【地理分布】")
        print("-" * 40)
        
        print("三级机构分布 (TOP 5):")
        机构分布 = df['三级机构'].value_counts().head(5)
        for 机构, 数量 in 机构分布.items():
            占比 = 数量 / len(df) * 100
            print(f"  {机构}: {数量:,} ({占比:.1f}%)")
        print()
        
        # 车辆特征
        print("【车辆特征】")
        print("-" * 40)
        
        # 新能源车辆
        新能源数量 = (df['是否新能源'] == '是').sum()
        新能源占比 = 新能源数量 / len(df) * 100
        print(f"新能源车辆: {新能源数量:,} ({新能源占比:.1f}%)")
        
        # 网约车
        网约车数量 = (df['是否网约车'] == '是').sum()
        网约车占比 = 网约车数量 / len(df) * 100
        print(f"网约车: {网约车数量:,} ({网约车占比:.1f}%)")
        
        # 过户车
        过户车数量 = (df['是否过户车'] == '是').sum()
        过户车占比 = 过户车数量 / len(df) * 100
        print(f"过户车: {过户车数量:,} ({过户车占比:.1f}%)")
        print()
        
        # 车辆使用年限
        平均年限 = df['车辆使用年限'].mean()
        最大年限 = df['车辆使用年限'].max()
        最小年限 = df['车辆使用年限'].min()
        print(f"车辆使用年限: 平均{平均年限:.1f}年，范围{最小年限}-{最大年限}年")
        print()
        
        # 业务来源
        print("【业务来源分布】")
        print("-" * 40)
        业务来源分布 = df['业务来源'].value_counts()
        for 来源, 数量 in 业务来源分布.items():
            占比 = 数量 / len(df) * 100
            print(f"  {来源}: {数量:,} ({占比:.1f}%)")
        print()
        
        # 异常值提醒
        print("【异常值提醒】")
        print("-" * 40)
        
        # 负值保费
        负保费数量 = (df['签单保费'] < 0).sum()
        if 负保费数量 > 0:
            print(f"负值保费记录: {负保费数量:,}条")
            负保费总额 = df[df['签单保费'] < 0]['签单保费'].sum()
            print(f"负值保费总额: {负保费总额:,.2f}元")
        
        # 负值保额
        负保额数量 = (df['签单保额'] < 0).sum()
        if 负保额数量 > 0:
            print(f"负值保额记录: {负保额数量:,}条")
        
        # 零手续费
        零手续费数量 = (df['手续费'] == 0).sum()
        零手续费占比 = 零手续费数量 / len(df) * 100
        print(f"零手续费记录: {零手续费数量:,} ({零手续费占比:.1f}%)")
        
        print()
        print("=" * 60)
        print("统计完成")
        print("=" * 60)
        
    except Exception as e:
        print(f"分析过程中出错: {e}")

if __name__ == "__main__":
    quick_stats()