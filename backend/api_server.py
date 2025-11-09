"""
Flask API服务器 - 为前端提供数据接口
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from data_processor import DataProcessor
import sys
from pathlib import Path
import os

# 确保能找到模块
sys.path.insert(0, str(Path(__file__).parent))

# 统一静态目录到项目根的 static，以便通过后端预览静态首页
# 注意：api_server 位于 backend/ 下，需显式配置 static_folder 指向上一级目录的 static
STATIC_ROOT = Path(__file__).resolve().parent.parent / "static"
app = Flask(
    __name__,
    static_folder=str(STATIC_ROOT),  # 静态文件目录：项目根/static
    static_url_path="/static"       # 静态URL前缀
)
CORS(app)  # 允许跨域请求，支持前端开发服务器访问

# 初始化数据处理器
processor = DataProcessor()

# 允许的 period 取值（函数级中文注释）：
# - day: 当日
# - last7d: 近7天
# - last30d: 近30天
# 统一在路由层做白名单校验，避免传入非法值导致后续处理异常。
ALLOWED_PERIODS = {"day", "last7d", "last30d"}


@app.route('/', methods=['GET'])
def root_index():
    """
    根路径入口（修复 404）

    设计说明（函数级中文注释）：
    - 若存在项目根的静态首页 `static/index.html`，返回该页面用于快速预览。
    - 若静态首页不存在，则返回一个 JSON 说明，列出可用 API 与前端预览地址。
    - 这样可避免访问 `http://127.0.0.1:5001/` 返回 404 的困惑，提升可用性。

    返回：
    - HTML：静态首页（如果存在）
    - JSON：接口列表与提示信息（如果静态首页不存在）
    """
    index_file = STATIC_ROOT / 'index.html'
    if index_file.exists():
        # Flask内置方法：从配置的 static_folder 返回静态文件
        return app.send_static_file('index.html')
    # 函数级中文注释：
    # 根路径返回接口说明与前端预览地址；前端 URL 优先读取环境变量 FRONTEND_URL，其次从 VITE_PORT 构造。
    frontend_url = os.environ.get('FRONTEND_URL') or f"http://localhost:{os.environ.get('VITE_PORT', '3000')}"
    return jsonify({
        'message': '欢迎使用车险签单数据分析平台（根路径无静态首页时返回接口说明）',
        'preview': frontend_url,
        'apis': [
            'POST /api/refresh',
            'POST /api/kpi-windows',
            'POST /api/week-comparison',
            'GET  /api/filter-options',
            'GET  /api/daily-report',
            'GET  /api/week-trend',
            'GET  /api/latest-date',
            'GET  /api/health'
        ]
    })


@app.route('/api/refresh', methods=['POST'])
def refresh_data():
    """
    刷新数据 - 扫描并处理新的Excel文件
    """
    try:
        processor.scan_and_process_new_files()
        return jsonify({
            'success': True,
            'message': '数据刷新成功',
            'latest_date': processor.get_latest_date()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'数据刷新失败: {str(e)}'
        }), 500


@app.route('/api/daily-report', methods=['GET'])
def get_daily_report():
    """
    获取日报数据

    Query参数:
        date: 日期(可选,格式: YYYY-MM-DD)
    """
    date = request.args.get('date', None)

    try:
        report = processor.get_daily_report(date)

        if report is None:
            return jsonify({
                'success': False,
                'message': '未找到数据'
            }), 404

        return jsonify({
            'success': True,
            'data': report
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取日报失败: {str(e)}'
        }), 500


@app.route('/api/week-trend', methods=['GET'])
def get_week_trend():
    """
    获取周趋势数据

    Query参数:
        weeks: 周数(默认1,可选1或3)
        end_date: 结束日期(可选,格式: YYYY-MM-DD)
    """
    weeks = int(request.args.get('weeks', 1))
    end_date = request.args.get('end_date', None)

    try:
        trend = processor.get_week_trend(end_date=end_date, weeks=weeks)

        return jsonify({
            'success': True,
            'data': trend
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取趋势数据失败: {str(e)}'
        }), 500


@app.route('/api/latest-date', methods=['GET'])
def get_latest_date():
    """
    获取数据中的最新日期
    """
    try:
        latest = processor.get_latest_date()
        return jsonify({
            'success': True,
            'latest_date': latest
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取最新日期失败: {str(e)}'
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'message': 'API服务运行正常'
    })


@app.route('/api/filter-options', methods=['GET'])
def get_filter_options():
    """
    获取所有筛选器的可选值
    """
    try:
        options = processor.get_filter_options()
        return jsonify({
            'success': True,
            'data': options
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取筛选选项失败: {str(e)}'
        }), 500


@app.route('/api/policy-mapping', methods=['GET'])
def get_policy_mapping():
    """
    获取保单号→业务员→团队/机构映射

    说明：
    - 保单号作为唯一标识；通过合并清单获取保单对应业务员；
    - 再依据映射文件获取该业务员的团队简称与三级机构；
    - 返回可能存在的姓名冲突信息，供前端提示。
    """
    try:
        mapping = processor.get_policy_mapping()
        return jsonify({
            'success': True,
            'data': mapping
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取保单映射失败: {str(e)}'
        }), 500


@app.route('/api/week-comparison', methods=['POST'])
def get_week_comparison():
    """
    获取3个7天周期对比数据

    Request Body:
    {
        "metric": "premium",  // or "count"
        "filters": {
            "business_type": "xxx",  // 可选，业务类型（客户类别3）
            "三级机构": "xxx",
            "团队": "xxx",
            "业务员": "xxx",
            ...
        },
        "date": "YYYY-MM-DD",  // 可选，指定锚定日期(作为W的结束日)
        "data_scope": "exclude_correction" | "include_correction"  // 可选，数据口径，默认不含批改
    }
    """
    try:
        data = request.get_json() or {}
        metric = data.get('metric', 'premium')
        filters = data.get('filters', {})
        anchor_date = data.get('date', None)
        data_scope = data.get('data_scope', 'exclude_correction')  # 默认不含批改

        result = processor.get_week_comparison(metric=metric, filters=filters, anchor_date=anchor_date, data_scope=data_scope)

        if result is None:
            return jsonify({
                'success': False,
                'message': '未找到数据'
            }), 404

        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取周对比数据失败: {str(e)}'
        }), 500


@app.route('/api/kpi-windows', methods=['POST'])
def get_kpi_windows():
    """
    获取KPI三口径数据：当日(指定日期)、近7天(截至指定日期)、近30天(截至指定日期)

    Request Body:
        {
            "filters": {
                "business_type": "xxx",  // 可选，业务类型（客户类别3）：摩托车/挂车/特种车等
                "三级机构": "xxx",
                "团队": "xxx",
                "业务员": "xxx",
                "是否续保": "xxx",
                "是否新能源": "xxx",
                "是否过户车": "xxx",
                "是否异地车": "xxx",
                "险种大类": "xxx",
                "吨位": "xxx"
            },
            "date": "YYYY-MM-DD",  // 可选，指定日期
            "data_scope": "exclude_correction" | "include_correction"  // 可选，数据口径，默认不含批改
        }
    """
    try:
        data = request.get_json() or {}
        filters = data.get('filters', {})
        date = data.get('date', None)
        data_scope = data.get('data_scope', 'exclude_correction')  # 默认不含批改

        result = processor.get_kpi_windows(date=date, filters=filters, data_scope=data_scope)

        if result is None:
            return jsonify({
                'success': False,
                'message': '未找到数据'
            }), 404

        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取KPI数据失败: {str(e)}'
        }), 500


@app.route('/api/staff-performance-distribution', methods=['POST'])
def get_staff_performance_distribution():
    """
    获取各机构业务员业绩区间分布数据

    业绩区间划分:
    - <1万
    - 1-2万
    - 2-3万
    - 3-5万
    - >=5万

    Request Body:
        {
            "period": "day",        // 时间段: day(当日), last7d(近7天), last30d(近30天)
            "filters": {
                "三级机构": "xxx",
                "团队": "xxx",
                ...
            },
            "date": "YYYY-MM-DD",  // 可选，指定日期
            "data_scope": "exclude_correction" | "include_correction"  // 可选，数据口径，默认不含批改
        }

    Returns:
        {
            "success": true,
            "data": {
                "period": "day",
                "period_label": "当日",
                "date_range": "2025-11-08",
                "distribution": [
                    {
                        "range": "<1万",
                        "count": 15,
                        "percentage": 37.5
                    },
                    {
                        "range": "1-2万",
                        "count": 12,
                        "percentage": 30.0
                    },
                    ...
                ],
                "total_staff": 40,
                "total_premium": 1580000.50
            }
        }
    """
    try:
        data = request.get_json() or {}
        period = data.get('period', 'day')  # 可选值: day / last7d / last30d
        filters = data.get('filters', {})
        date = data.get('date', None)
        data_scope = data.get('data_scope', 'exclude_correction')  # 默认不含批改

        # 参数校验与错误返回说明（函数级中文注释）：
        # - period 必须为字符串，且在 ALLOWED_PERIODS 白名单中；否则返回 400。
        # - filters 必须为字典；否则返回 400。
        # 目的：在路由层尽早拦截无效入参，减少后端处理与 IDE 报错来源。

        # 校验 filters 类型
        if not isinstance(filters, dict):
            return jsonify({
                'success': False,
                'message': '参数错误: filters 必须为对象(JSON字典)'
            }), 400

        # 校验 period 类型
        if not isinstance(period, str):
            return jsonify({
                'success': False,
                'message': '参数错误: period 必须为字符串',
                'allowed': sorted(list(ALLOWED_PERIODS))
            }), 400

        # 归一化 period 并做白名单校验
        period = period.strip().lower()
        if period not in ALLOWED_PERIODS:
            return jsonify({
                'success': False,
                'message': '参数错误: period 仅支持 day/last7d/last30d',
                'allowed': sorted(list(ALLOWED_PERIODS))
            }), 400

        result = processor.get_staff_performance_distribution(period=period, date=date, filters=filters, data_scope=data_scope)

        if result is None:
            return jsonify({
                'success': False,
                'message': '未找到数据'
            }), 404

        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取业务员业绩分布失败: {str(e)}'
        }), 500


@app.route('/api/insurance-type-distribution', methods=['POST'])
def get_insurance_type_distribution():
    """
    获取险别组合占比分析

    Request Body:
        {
            "period": "day",        // 时间段: day(当日), last7d(近7天), last30d(近30天)
            "filters": {
                "三级机构": "xxx",
                "团队": "xxx",
                ...
            },
            "date": "YYYY-MM-DD"  // 可选，指定日期
        }

    Returns:
        {
            "success": true,
            "data": {
                "period": "day",
                "period_label": "当日",
                "date_range": "2025-11-08",
                "distribution": [
                    {
                        "type": "单交",
                        "count": 156,
                        "premium": 1250000.50,
                        "percentage": 43.8
                    },
                    ...
                ],
                "total_count": 356,
                "total_premium": 5600000.00
            }
        }
    """
    try:
        data = request.get_json() or {}
        period = data.get('period', 'day')
        filters = data.get('filters', {})
        date = data.get('date', None)
        data_scope = data.get('data_scope', 'exclude_correction')  # 默认不含批改

        # 参数校验
        if not isinstance(filters, dict):
            return jsonify({
                'success': False,
                'message': '参数错误: filters 必须为对象(JSON字典)'
            }), 400

        if not isinstance(period, str):
            return jsonify({
                'success': False,
                'message': '参数错误: period 必须为字符串',
                'allowed': sorted(list(ALLOWED_PERIODS))
            }), 400

        period = period.strip().lower()
        if period not in ALLOWED_PERIODS:
            return jsonify({
                'success': False,
                'message': '参数错误: period 仅支持 day/last7d/last30d',
                'allowed': sorted(list(ALLOWED_PERIODS))
            }), 400

        result = processor.get_insurance_type_distribution(period=period, date=date, filters=filters, data_scope=data_scope)

        if result is None:
            return jsonify({
                'success': False,
                'message': '未找到数据'
            }), 404

        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取险别组合占比失败: {str(e)}'
        }), 500


@app.route('/api/premium-range-distribution', methods=['POST'])
def get_premium_range_distribution():
    """
    获取业务员保费区间占比分析

    业绩区间划分（按业务员聚合后的保费）:
    - <0 (负保费)
    - 0-0.5万
    - 0.5-1.5万
    - 1.5-2万
    - 2-3万
    - >=3万

    Request Body:
        {
            "period": "day",        // 时间段: day(当日), last7d(近7天), last30d(近30天)
            "filters": {
                "三级机构": "xxx",
                "团队": "xxx",
                ...
            },
            "date": "YYYY-MM-DD"  // 可选，指定日期
        }

    Returns:
        {
            "success": true,
            "data": {
                "period": "day",
                "period_label": "当日",
                "date_range": "2025-11-08",
                "distribution": [
                    {
                        "range": "<0",
                        "staff_count": 2,
                        "total_premium": -5000.00,
                        "percentage": 4.2
                    },
                    {
                        "range": "0-0.5万",
                        "staff_count": 17,
                        "total_premium": 42000.50,
                        "percentage": 35.4
                    },
                    ...
                ],
                "total_staff": 48,
                "total_premium": 650000.00
            }
        }
    """
    try:
        data = request.get_json() or {}
        period = data.get('period', 'day')
        filters = data.get('filters', {})
        date = data.get('date', None)
        data_scope = data.get('data_scope', 'exclude_correction')  # 默认不含批改

        # 参数校验
        if not isinstance(filters, dict):
            return jsonify({
                'success': False,
                'message': '参数错误: filters 必须为对象(JSON字典)'
            }), 400

        if not isinstance(period, str):
            return jsonify({
                'success': False,
                'message': '参数错误: period 必须为字符串',
                'allowed': sorted(list(ALLOWED_PERIODS))
            }), 400

        period = period.strip().lower()
        if period not in ALLOWED_PERIODS:
            return jsonify({
                'success': False,
                'message': '参数错误: period 仅支持 day/last7d/last30d',
                'allowed': sorted(list(ALLOWED_PERIODS))
            }), 400

        result = processor.get_premium_range_distribution(period=period, date=date, filters=filters, data_scope=data_scope)

        if result is None:
            return jsonify({
                'success': False,
                'message': '未找到数据'
            }), 404

        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取业务员保费区间占比失败: {str(e)}'
        }), 500


@app.route('/api/renewal-type-distribution', methods=['POST'])
def get_renewal_type_distribution():
    """
    获取新转续占比分析

    Request Body:
        {
            "period": "day",        // 时间段: day(当日), last7d(近7天), last30d(近30天)
            "filters": {
                "三级机构": "xxx",
                "团队": "xxx",
                ...
            },
            "date": "YYYY-MM-DD"  // 可选，指定日期
        }

    Returns:
        {
            "success": true,
            "data": {
                "period": "day",
                "period_label": "当日",
                "date_range": "2025-11-08",
                "distribution": [
                    {
                        "type": "续保",
                        "count": 220,
                        "premium": 3450000.00,
                        "percentage": 61.8
                    },
                    {
                        "type": "新保",
                        "count": 108,
                        "premium": 1680000.00,
                        "percentage": 30.3
                    },
                    ...
                ],
                "total_count": 356,
                "total_premium": 5600000.00,
                "field_used": "是否续保"
            }
        }
    """
    try:
        data = request.get_json() or {}
        period = data.get('period', 'day')
        filters = data.get('filters', {})
        date = data.get('date', None)
        data_scope = data.get('data_scope', 'exclude_correction')  # 默认不含批改

        # 参数校验
        if not isinstance(filters, dict):
            return jsonify({
                'success': False,
                'message': '参数错误: filters 必须为对象(JSON字典)'
            }), 400

        if not isinstance(period, str):
            return jsonify({
                'success': False,
                'message': '参数错误: period 必须为字符串',
                'allowed': sorted(list(ALLOWED_PERIODS))
            }), 400

        period = period.strip().lower()
        if period not in ALLOWED_PERIODS:
            return jsonify({
                'success': False,
                'message': '参数错误: period 仅支持 day/last7d/last30d',
                'allowed': sorted(list(ALLOWED_PERIODS))
            }), 400

        result = processor.get_renewal_type_distribution(period=period, date=date, filters=filters, data_scope=data_scope)

        if result is None:
            return jsonify({
                'success': False,
                'message': '未找到数据'
            }), 404

        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取新转续占比失败: {str(e)}'
        }), 500


if __name__ == '__main__':
    import io

    # 设置输出编码为UTF-8
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    # 函数级中文注释：
    # 后端服务端口从环境变量优先读取(API_PORT/PORT)，默认 5001；
    # 前端地址从 FRONTEND_URL 或 VITE_PORT 构造，避免硬编码 5173。
    PORT = int(os.environ.get('API_PORT') or os.environ.get('PORT') or '5001')
    FRONTEND_URL = os.environ.get('FRONTEND_URL') or f"http://localhost:{os.environ.get('VITE_PORT', '3000')}"
    print("=" * 70)
    print("🚀 车险签单数据分析平台 - REST API Server")
    print("=" * 70)
    print(f"\n📡 API服务地址: http://localhost:{PORT}")
    print(f"🌐 前端开发服务器: {FRONTEND_URL} (使用 'npm run dev' 启动)")
    print("\n" + "=" * 70)
    print("\n📋 可用API接口:")
    print("  POST /api/refresh                      - 刷新数据(处理新Excel)")
    print("  POST /api/kpi-windows                  - 获取KPI三口径数据")
    print("  POST /api/week-comparison              - 获取周对比图表数据")
    print("  POST /api/insurance-type-distribution  - 获取险别组合占比")
    print("  POST /api/premium-range-distribution   - 获取业务员保费区间占比")
    print("  POST /api/renewal-type-distribution    - 获取新转续占比")
    print("  GET  /api/filter-options               - 获取筛选选项")
    print("  GET  /api/daily-report                 - 获取日报")
    print("  GET  /api/week-trend                   - 获取周趋势")
    print("  GET  /api/latest-date                  - 获取最新日期")
    print("  GET  /api/health                       - 健康检查")
    print("\n" + "=" * 70)
    print("\n💡 开发提示:")
    print(f"  - 前端开发: 访问 {FRONTEND_URL}")
    print("  - API测试: 可使用 curl/Postman 访问上述接口")
    print("  - 数据目录: backend/车险日报/")
    print("\n" + "=" * 70 + "\n")

    app.run(host='0.0.0.0', port=PORT, debug=True)
