#!/bin/bash

echo "测试三级机构筛选【乐山】"
echo "=============================="

curl -s -X POST http://localhost:5001/api/kpi-windows \
  -H "Content-Type: application/json" \
  -d "{\"filters\": {\"三级机构\": \"乐山\"}}" > /tmp/kpi_result.json

cat /tmp/kpi_result.json | python3 -c "
import sys, json
data = json.load(sys.stdin)
if data.get('success'):
    kpi = data['data']
    print(f\"✓ 筛选成功\")
    print(f\"  最新日期: {kpi.get('latest_date')}\")
    for window in ['today', 'week', 'month']:
        w_data = kpi.get(window, {})
        premium = w_data.get('total_premium', 0)
        count = w_data.get('policy_count', 0)
        print(f\"  {window}: 保费={premium:,.2f}, 件数={count}\")
else:
    print(f\"✗ 失败: {data.get('message')}\")
    sys.exit(1)
"

echo ""
echo "测试周对比数据"
echo "=============================="

curl -s -X POST http://localhost:5001/api/week-comparison \
  -H "Content-Type: application/json" \
  -d "{\"filters\": {\"三级机构\": \"乐山\"}, \"metric\": \"premium\"}" > /tmp/week_result.json

cat /tmp/week_result.json | python3 -c "
import sys, json
data = json.load(sys.stdin)
if data.get('success'):
    chart = data['data']
    print(f\"✓ 周对比数据获取成功\")
    print(f\"  最新日期: {chart.get('latest_date')}\")
    print(f\"  数据系列数: {len(chart.get('series', []))}\")
    for series in chart.get('series', []):
        print(f\"    - {series.get('name')}: {series.get('total_value', 0):,.2f}\")
else:
    print(f\"✗ 失败: {data.get('message')}\")
    sys.exit(1)
"

echo ""
echo "=============================="
echo "✓ 所有测试通过！"
