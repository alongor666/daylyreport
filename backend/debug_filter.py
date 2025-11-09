#!/usr/bin/env python3
"""
DEBUG: 调试三级机构筛选逻辑
"""

import sys
import json
import re
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from data_processor import DataProcessor

def debug_three_level_filter():
    """调试三级机构筛选"""

    processor = DataProcessor()

    # 加载数据
    df = pd.read_csv(processor.merged_csv, encoding='utf-8-sig', low_memory=False)
    print(f"原始数据条数: {len(df)}")

    # 检查数据中的业务员
    data_staff = df['业务员'].dropna().unique()
    print(f"\n前20个数据中的业务员:")
    for staff in data_staff[:20]:
        print(f"  - {staff}")

    # 检查映射文件的键
    print(f"\n前20个映射键:")
    for key in list(processor.staff_mapping.keys())[:20]:
        print(f"  - {key}")

    # 检查达州机构
    selected_inst = '达州'
    staff_list = []

    print(f"\n=== 筛选逻辑详细过程 ('{selected_inst}') ===")
    for staff_key, staff_info in processor.staff_mapping.items():
        if staff_info.get('三级机构') == selected_inst:
            match = re.search(r'[\u4e00-\u9fa5]+', staff_key)
            if match:
                name = match.group()
                staff_list.append(name)
                print(f"  匹配: {staff_key} -> {name}")

    print(f"\n筛选出的业务员数量: {len(staff_list)}")
    print(f"业务员列表: {staff_list}")

    # 验证这些业务员在数据中是否存在
    print(f"\n=== 数据匹配验证 ===")
    data_staff_set = set()
    for staff in data_staff:
        match = re.search(r'[\u4e00-\u9fa5]+', str(staff))
        if match:
            data_staff_set.add(match.group())

    for name in staff_list[:10]:
        if name in data_staff_set:
            print(f"  ✅ {name} 在数据中存在")
        else:
            print(f"  ❌ {name} 在数据中不存在")

    print(f"\n数据中有 {len(data_staff_set)} 个独特的业务员姓名")

    # 进行筛选
    print(f"\n=== 执行筛选 ===")
    filtered_df = df.copy()

    import numpy as np
    mask = np.zeros(len(df), dtype=bool)
    count = 0
    for idx, staff in enumerate(df['业务员']):
        if pd.notna(staff):
            match = re.search(r'[\u4e00-\u9fa5]+', str(staff))
            if match and match.group() in staff_list:
                mask[idx] = True
                count += 1
                if count <= 5:
                    print(f"  匹配第 {count} 条: {staff}")

    filtered_df = df[mask]
    print(f"\n筛选后数据条数: {len(filtered_df)}")

    if len(filtered_df) == 0:
        print("\n❌ 筛选后无数据！")
        print("检查问题...")

if __name__ == '__main__':
    print("🔍 开始调试三级机构筛选逻辑...\n")
    try:
        debug_three_level_filter()
        print("\n✅ 调试完成！")
    except Exception as e:
        print(f"\n❌ 调试失败: {e}")
        import traceback
        traceback.print_exc()
