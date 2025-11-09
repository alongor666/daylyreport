#!/usr/bin/env python3
"""
测试三级机构筛选功能
"""

import sys
import json
from pathlib import Path

# 确保能找到数据处理器
sys.path.insert(0, str(Path(__file__).parent))

from data_processor import DataProcessor

def test_three_level_filter():
    """测试三级机构筛选"""

    # 初始化数据处理器
    processor = DataProcessor()

    # 测试1: 无筛选条件
    print("=" * 70)
    print("测试1: 无筛选条件")
    print("=" * 70)
    result1 = processor.get_kpi_windows(date=None, filters={})
    if result1:
        premium_7d_no_filter = result1['premium']['last7d']
        print(f"近7天保费: {premium_7d_no_filter:,.2f}")
    else:
        print("无数据")
        return

    # 测试2: 筛选达州三级机构
    print("\n" + "=" * 70)
    print("测试2: 筛选三级机构='达州'")
    print("=" * 70)
    filters = {"三级机构": "达州"}
    result2 = processor.get_kpi_windows(date=None, filters=filters)

    premium_7d_dazhou = 0
    if result2:
        premium_7d_dazhou = result2['premium']['last7d']
        print(f"近7天保费: {premium_7d_dazhou:,.2f}")

        # 验证筛选是否有效
        if premium_7d_dazhou < premium_7d_no_filter:
            reduction = (premium_7d_no_filter - premium_7d_dazhou) / premium_7d_no_filter * 100
            print(f"✅ 筛选有效！保费减少了 {reduction:.2f}%")
        elif premium_7d_dazhou > 0:
            print(f"数据量减少，筛选有效！")
        else:
            print("⚠️  筛选似乎没有生效，数据量没有明显变化")

        # 显示验证信息
        validation = result2.get('validation', {})
        if validation:
            print(f"\n验证信息:")
            print(f"  - 未匹配业务员: {validation.get('unmatched_count', 0)} 个")
            if validation.get('policy_consistency'):
                print(f"  - 保单不一致: {validation['policy_consistency'].get('mismatch_count', 0)} 个")
    else:
        print("⚠️  筛选后无数据返回")

    # 测试3: 筛选德阳
    print("\n" + "=" * 70)
    print("测试3: 筛选三级机构='德阳'")
    print("=" * 70)
    filters = {"三级机构": "德阳"}
    result3 = processor.get_kpi_windows(date=None, filters=filters)

    premium_7d_deyang = 0
    if result3:
        premium_7d_deyang = result3['premium']['last7d']
        print(f"近7天保费: {premium_7d_deyang:,.2f}")

    # 汇总结果
    print("\n" + "=" * 70)
    print("汇总结果:")
    print("=" * 70)
    print(f"无筛选:     {premium_7d_no_filter:>15,.2f}")
    print(f"达州:       {premium_7d_dazhou:>15,.2f}")
    print(f"德阳:       {premium_7d_deyang:>15,.2f}")

    if premium_7d_no_filter > 0:
        dazhou_pct = (premium_7d_dazhou/premium_7d_no_filter)*100 if premium_7d_dazhou > 0 else 0
        deyang_pct = (premium_7d_deyang/premium_7d_no_filter)*100 if premium_7d_deyang > 0 else 0
        print(f"\n达州占比:   {dazhou_pct:>15.2f}%")
        print(f"德阳占比:   {deyang_pct:>15.2f}%")

if __name__ == '__main__':
    print("🧪 开始测试三级机构筛选功能...\n")
    try:
        test_three_level_filter()
        print("\n✅ 测试完成！")
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
