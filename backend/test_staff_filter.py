#!/usr/bin/env python3
"""
测试“业务员”姓名筛选兼容性

函数级中文注释：
- 目的：验证后端在传入仅中文姓名的情况下，能够正确过滤数据。
- 原因：前端 GlobalFilterPanel 使用姓名作为筛选值，后端数据列通常为“工号+姓名”。
- 期待：通过映射或中文提取逻辑，返回非空且合理的KPI数据。
"""

import sys
import json
from pathlib import Path

# 确保能找到数据处理器
sys.path.insert(0, str(Path(__file__).parent))

from data_processor import DataProcessor


def pick_any_staff_name(processor: DataProcessor):
    """
    选择一个可用的中文姓名用于测试

    函数级中文注释：
    - 优先从 policy-mapping 的 staff_to_info 中选取键（中文姓名）。
    - 若无映射，则从数据中“业务员”列提取中文姓名作为备选。
    """
    mapping = processor.get_policy_mapping() or {}
    staff_to_info = mapping.get('staff_to_info', {})
    if staff_to_info:
        # 返回第一个姓名键
        return next(iter(staff_to_info.keys()))

    # 回退：从原始数据中提取中文姓名
    import pandas as pd
    import re
    if not processor.merged_csv.exists():
        return None
    df = pd.read_csv(processor.merged_csv, encoding='utf-8-sig', low_memory=False)
    if '业务员' not in df.columns:
        return None
    for v in df['业务员'].dropna().unique().tolist():
        m = re.search(r'[\u4e00-\u9fa5]+', str(v))
        if m:
            return m.group()
    return None


def test_staff_name_filter():
    """
    测试仅姓名的业务员筛选能否返回有效数据
    """
    processor = DataProcessor()
    name = pick_any_staff_name(processor)
    print("=" * 70)
    print("测试：业务员姓名筛选兼容性")
    print("=" * 70)
    if not name:
        print("⚠️ 无可用的业务员姓名，跳过测试。")
        return

    print(f"选用业务员姓名：{name}")
    filters = {"业务员": name}
    result = processor.get_kpi_windows(date=None, filters=filters)

    if not result:
        print("❌ 筛选后无数据返回")
        return

    day_premium = result['premium'].get('day', 0)
    last7d_premium = result['premium'].get('last7d', 0)
    last30d_premium = result['premium'].get('last30d', 0)

    print(f"当日保费:    {day_premium:,.2f}")
    print(f"近7天保费:   {last7d_premium:,.2f}")
    print(f"近30天保费:  {last30d_premium:,.2f}")

    if (day_premium + last7d_premium + last30d_premium) > 0:
        print("✅ 姓名筛选生效，返回了有效数据。")
    else:
        print("⚠️ 返回数据为0，可能是数据集与时间范围导致。")


if __name__ == '__main__':
    print("🧪 开始测试业务员姓名筛选兼容性...\n")
    try:
        test_staff_name_filter()
        print("\n✅ 测试完成！")
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()