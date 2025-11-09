#!/usr/bin/env python3
"""
测试三级机构和团队筛选功能
"""
import requests
import json

BASE_URL = "http://localhost:5001"

def test_filter_options():
    """测试获取筛选选项"""
    print("=" * 80)
    print("1. 获取筛选选项")
    print("=" * 80)

    response = requests.get(f"{BASE_URL}/api/filter-options")
    data = response.json()

    if data.get('success'):
        options = data['data']
        institutions = options.get('机构团队映射', {}).get('三级机构', [])
        print(f"✓ 可用的三级机构 ({len(institutions)} 个):")
        for inst in institutions[:5]:
            print(f"  - {inst}")
        if len(institutions) > 5:
            print(f"  ... 还有 {len(institutions) - 5} 个")
        return institutions
    else:
        print(f"✗ 获取筛选选项失败: {data.get('message')}")
        return []

def test_institution_filter(institution):
    """测试三级机构筛选"""
    print("\n" + "=" * 80)
    print(f"2. 测试三级机构筛选: {institution}")
    print("=" * 80)

    # 测试 KPI 数据
    payload = {
        "filters": {
            "三级机构": institution
        }
    }

    print(f"\n请求: POST /api/kpi-windows")
    print(f"筛选条件: {json.dumps(payload, ensure_ascii=False)}")

    response = requests.post(f"{BASE_URL}/api/kpi-windows", json=payload)

    print(f"状态码: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            kpi_data = data['data']
            print(f"✓ KPI数据获取成功")
            print(f"  - 最新日期: {kpi_data.get('latest_date')}")

            # 显示各指标数据
            for window in ['today', 'week', 'month']:
                window_data = kpi_data.get(window, {})
                premium = window_data.get('total_premium', 0)
                count = window_data.get('policy_count', 0)
                print(f"  - {window}: 保费={premium:,.2f}, 件数={count}")
        else:
            print(f"✗ API返回失败: {data.get('message')}")
    else:
        print(f"✗ 请求失败: {response.text[:200]}")

    # 测试周对比数据
    print(f"\n请求: POST /api/week-comparison")
    response = requests.post(f"{BASE_URL}/api/week-comparison", json=payload)

    print(f"状态码: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            chart_data = data['data']
            print(f"✓ 周对比数据获取成功")
            print(f"  - 最新日期: {chart_data.get('latest_date')}")
            print(f"  - 数据系列数: {len(chart_data.get('series', []))}")

            for series in chart_data.get('series', []):
                name = series.get('name', 'N/A')
                total = series.get('total_value', 0)
                print(f"  - {name}: {total:,.2f}")
        else:
            print(f"✗ API返回失败: {data.get('message')}")
    else:
        print(f"✗ 请求失败: {response.text[:200]}")

def test_team_filter():
    """测试团队筛选"""
    print("\n" + "=" * 80)
    print("3. 测试团队筛选")
    print("=" * 80)

    # 先获取可用的团队
    response = requests.get(f"{BASE_URL}/api/filter-options")
    data = response.json()

    if not data.get('success'):
        print("✗ 无法获取筛选选项")
        return

    teams = []
    for inst_data in data['data']['机构团队映射']['三级机构'].values():
        if isinstance(inst_data, dict):
            teams.extend(inst_data.get('teams', []))

    if not teams:
        print("✗ 没有找到可用的团队")
        return

    # 测试第一个团队
    test_team = teams[0]
    print(f"\n测试团队: {test_team}")

    payload = {
        "filters": {
            "团队": test_team
        }
    }

    response = requests.post(f"{BASE_URL}/api/kpi-windows", json=payload)

    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            kpi_data = data['data']
            print(f"✓ 团队筛选成功")
            print(f"  - 最新日期: {kpi_data.get('latest_date')}")

            window_data = kpi_data.get('today', {})
            premium = window_data.get('total_premium', 0)
            count = window_data.get('policy_count', 0)
            print(f"  - 当日数据: 保费={premium:,.2f}, 件数={count}")
        else:
            print(f"✗ API返回失败: {data.get('message')}")
    else:
        print(f"✗ 请求失败: {response.text[:200]}")

if __name__ == "__main__":
    print("\n🧪 开始测试三级机构和团队筛选功能\n")

    # 1. 获取筛选选项
    institutions = test_filter_options()

    # 2. 测试三级机构筛选（使用第一个机构）
    if institutions:
        test_institution = institutions[0]
        test_institution_filter(test_institution)

    # 3. 测试团队筛选
    test_team_filter()

    print("\n" + "=" * 80)
    print("✓ 测试完成")
    print("=" * 80)
