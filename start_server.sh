#!/bin/bash

# 设置UTF-8编码
export LANG=zh_CN.UTF-8
export LC_ALL=zh_CN.UTF-8

echo "========================================"
echo "   每日签单平台趋势分析系统"
echo "========================================"
echo ""

echo "[1/3] 检查Python环境..."
if ! command -v python3 &> /dev/null
then
    if ! command -v python &> /dev/null
    then
        echo "❌ 未找到Python，请先安装Python 3.8+"
        exit 1
    else
        PYTHON_CMD=python
    fi
else
    PYTHON_CMD=python3
fi

$PYTHON_CMD --version
echo "✓ Python环境正常"
echo ""

echo "[2/3] 检查依赖包..."
if ! $PYTHON_CMD -c "import flask" 2>/dev/null; then
    echo "📦 安装依赖包..."
    $PYTHON_CMD -m pip install -r requirements.txt
fi
echo "✓ 依赖包已安装"
echo ""

echo "[3/3] 启动API服务器..."
echo ""
echo "========================================"
echo "  服务器地址: http://localhost:5000"
echo "  网页访问: http://localhost:5000/static/index.html"
echo "========================================"
echo ""
echo "按 Ctrl+C 停止服务器"
echo ""

cd backend
$PYTHON_CMD api_server.py
