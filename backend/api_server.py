"""
Flask API服务器 - 为前端提供数据接口
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from data_processor import DataProcessor
import sys
from pathlib import Path

# 确保能找到模块
sys.path.insert(0, str(Path(__file__).parent))

# 获取项目根目录
project_root = Path(__file__).parent.parent

app = Flask(__name__,
            static_folder=str(project_root / 'static'),
            static_url_path='/static')
CORS(app)  # 允许跨域请求

# 初始化数据处理器
processor = DataProcessor()


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


@app.route('/api/week-comparison', methods=['POST'])
def get_week_comparison():
    """
    获取3个7天周期对比数据

    Request Body:
    {
        "metric": "premium",  // or "count"
        "filters": {
            "三级机构": "xxx",
            "团队": "xxx",
            ...
        },
        "date": "YYYY-MM-DD"  // 可选，指定锚定日期(作为W的结束日)
    }
    """
    try:
        data = request.get_json() or {}
        metric = data.get('metric', 'premium')
        filters = data.get('filters', {})
        anchor_date = data.get('date', None)

        result = processor.get_week_comparison(metric=metric, filters=filters, anchor_date=anchor_date)

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


@app.route('/api/kpi-windows', methods=['GET'])
def get_kpi_windows():
    """
    获取KPI三口径数据：当日(指定日期)、近7天(截至指定日期)、近30天(截至指定日期)

    Query参数:
        date: 指定日期(可选,格式: YYYY-MM-DD)，默认最新日期
    """
    date = request.args.get('date', None)

    try:
        result = processor.get_kpi_windows(date)

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


@app.route('/')
def index():
    """重定向到主页"""
    return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    import io

    # 设置输出编码为UTF-8
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    PORT = 5001  # macOS的AirPlay Receiver可能占用5000端口
    print("=" * 60)
    print("启动每日签单平台趋势分析API服务器")
    print("=" * 60)
    print(f"访问地址: http://localhost:{PORT}")
    print(f"前端页面: http://localhost:{PORT}/static/index.html")
    print("=" * 60)
    print("\n可用接口:")
    print("  POST /api/refresh          - 刷新数据(处理新Excel)")
    print("  GET  /api/daily-report     - 获取日报")
    print("  GET  /api/week-trend       - 获取周趋势")
    print("  GET  /api/latest-date      - 获取最新日期")
    print("  GET  /api/health           - 健康检查")
    print("\n" + "=" * 60)

    app.run(host='0.0.0.0', port=PORT, debug=True)
