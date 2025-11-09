#!/usr/bin/env python3
import pandas as pd
import sys
import os

# 测试读取Excel文件
excel_files = [f for f in os.listdir('.') if f.endswith('.xlsx')]

if excel_files:
    print(f"发现 {len(excel_files)} 个Excel文件:")
    for file in excel_files[:3]:  # 只测试前3个文件
        print(f"\n测试读取文件: {file}")
        try:
            # 读取Excel文件
            df = pd.read_excel(file)
            print(f"  成功读取！形状: {df.shape}")
            print(f"  列名: {list(df.columns[:5])}")  # 显示前5列
            if len(df) > 0:
                print(f"  第一行数据: {df.iloc[0].tolist()[:3]}")  # 显示前3个字段
        except Exception as e:
            print(f"  读取失败: {e}")
else:
    print("当前目录没有找到Excel文件")

print("\nExcel读取测试完成！")