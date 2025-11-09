#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
车险业务数据结构分析工具
分析Excel文件中的车险业务数据结构
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

def analyze_excel_structure(file_path):
    """分析Excel文件的数据结构"""
    print(f"正在分析文件: {file_path}")
    print("=" * 60)
    
    try:
        # 读取Excel文件
        excel_file = pd.ExcelFile(file_path)
        
        print(f"Excel文件包含的工作表: {excel_file.sheet_names}")
        print("\n" + "="*60)
        
        # 分析每个工作表
        for sheet_name in excel_file.sheet_names:
            print(f"\n工作表: {sheet_name}")
            print("-" * 40)
            
            # 读取工作表数据
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            
            # 基本信息
            print(f"数据行数: {len(df)}")
            print(f"数据列数: {len(df.columns)}")
            
            # 列名分析
            print(f"\n所有列名:")
            for i, col in enumerate(df.columns, 1):
                print(f"{i:2d}. {col}")
            
            # 数据类型分析
            print(f"\n数据类型分布:")
            type_counts = df.dtypes.value_counts()
            for dtype, count in type_counts.items():
                print(f"  {dtype}: {count}列")
            
            # 数值列统计
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if numeric_cols:
                print(f"\n数值列 ({len(numeric_cols)}个):")
                for col in numeric_cols[:10]:  # 只显示前10个
                    print(f"  {col}")
                if len(numeric_cols) > 10:
                    print(f"  ... 还有 {len(numeric_cols)-10} 个数值列")
            
            # 日期列分析
            date_cols = []
            for col in df.columns:
                if 'date' in str(col).lower() or '时间' in str(col) or '日期' in str(col):
                    date_cols.append(col)
                elif df[col].dtype == 'object':
                    # 尝试转换为日期
                    try:
                        pd.to_datetime(df[col].dropna().head())
                        date_cols.append(col)
                    except:
                        pass
            
            if date_cols:
                print(f"\n可能的日期列 ({len(date_cols)}个):")
                for col in date_cols:
                    print(f"  {col}")
            
            # 机构相关列
            org_keywords = ['机构', '公司', '分公司', '支公司', '部门', 'org', 'company']
            org_cols = []
            for col in df.columns:
                if any(keyword in str(col) for keyword in org_keywords):
                    org_cols.append(col)
            
            if org_cols:
                print(f"\n机构相关列 ({len(org_cols)}个):")
                for col in org_cols:
                    print(f"  {col}")
            
            # 车险特有列
            car_keywords = ['车', '险', '保', '续保', '新保', '车辆', '使用性质', '车型']
            car_cols = []
            for col in df.columns:
                if any(keyword in str(col) for keyword in car_keywords):
                    car_cols.append(col)
            
            if car_cols:
                print(f"\n车险相关列 ({len(car_cols)}个):")
                for col in car_cols:
                    print(f"  {col}")
            
            # 关键业务指标分析
            business_keywords = ['保费', '保额', '手续费', '佣金', '金额', '收入', '成本', '利润']
            business_cols = []
            for col in df.columns:
                if any(keyword in str(col) for keyword in business_keywords):
                    business_cols.append(col)
            
            if business_cols:
                print(f"\n业务指标列 ({len(business_cols)}个):")
                for col in business_cols:
                    print(f"  {col}")
                    # 显示基本统计信息
                    if col in numeric_cols:
                        print(f"    范围: {df[col].min():.2f} - {df[col].max():.2f}")
                        print(f"    均值: {df[col].mean():.2f}")
            
            print("\n" + "="*60)
    
    except Exception as e:
        print(f"分析文件时出错: {e}")

def main():
    # 分析日报汇总文件
    daily_report = "日报汇总-20250308-20250325.xlsx"
    if os.path.exists(daily_report):
        print("分析日报汇总文件...")
        analyze_excel_structure(daily_report)
    
    # 分析单个日报文件
    sample_file = "保批单业务报表-20250325.xlsx"
    if os.path.exists(sample_file):
        print(f"\n分析样本日报文件: {sample_file}")
        analyze_excel_structure(sample_file)

if __name__ == "__main__":
    main()