@echo off
chcp 65001 >nul
echo ========================================
echo    每日签单平台趋势分析系统
echo ========================================
echo.

echo [1/3] 检查Python环境...
python --version
if errorlevel 1 (
    echo ❌ 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)
echo ✓ Python环境正常
echo.

echo [2/3] 检查依赖包...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo 📦 安装依赖包...
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
)
echo ✓ 依赖包已安装
echo.

echo [3/3] 启动API服务器...
echo.
echo ========================================
echo  服务器地址: http://localhost:5000
echo  网页访问: http://localhost:5000/static/index.html
echo ========================================
echo.
echo 按 Ctrl+C 停止服务器
echo.

cd backend
python api_server.py

pause
