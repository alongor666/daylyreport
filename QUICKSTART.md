# 🚀 快速启动指南

## 30秒快速启动

```bash
# 1. 进入项目目录
cd "d:\WPS+iMac\车险签单清单_2025年3月\daylyreport"

# 2. 安装依赖(首次运行)
pip install -r requirements.txt

# 3. 启动服务器
start_server.bat

# 4. 打开浏览器
# 访问: http://localhost:5000
```

完成! 🎉

---

## 目录结构一览

```
daylyreport/
│
├── 📁 backend/                      后端服务
│   ├── data_processor.py           数据处理核心
│   └── api_server.py               API服务器
│
├── 📁 static/                       前端资源
│   ├── index.html                  主页面
│   ├── css/style.css               样式文件
│   └── js/app.js                   应用逻辑
│
├── 📁 data/                         数据目录
│   ├── *.xlsx                      ← 放Excel文件到这里
│   └── processed/                  已处理文件归档
│
├── 📄 车险清单_2025年10-11月_合并.csv  主数据文件
├── 📄 业务员机构团队归属.json          业务员映射
│
├── 📄 requirements.txt             Python依赖
├── 📄 start_server.bat             启动脚本
├── 📄 README.md                    项目文档
├── 📄 USAGE_GUIDE.md               使用指南
├── 📄 PROJECT_SUMMARY.md           项目总结
├── 📄 DEMO.md                      演示指南
└── 📄 QUICKSTART.md                本文档
```

---

## 核心文件说明

### 后端文件

| 文件 | 作用 | 何时修改 |
|------|------|----------|
| `backend/data_processor.py` | 数据处理逻辑 | 修改目标值、增加字段 |
| `backend/api_server.py` | API接口服务 | 增加新接口 |

### 前端文件

| 文件 | 作用 | 何时修改 |
|------|------|----------|
| `static/index.html` | 页面结构 | 修改布局、增加组件 |
| `static/css/style.css` | 页面样式 | 修改颜色、字体、布局 |
| `static/js/app.js` | 业务逻辑 | 修改图表、增加功能 |

### 配置文件

| 文件 | 作用 | 何时修改 |
|------|------|----------|
| `requirements.txt` | Python依赖 | 增加新的Python包 |
| `start_server.bat` | 启动脚本 | 修改端口、启动参数 |

---

## 常用操作速查

### 启动服务

```bash
start_server.bat
```

或手动启动:

```bash
cd backend
python api_server.py
```

### 停止服务

在命令行窗口按 `Ctrl+C`

### 重启服务

停止服务(Ctrl+C) → 重新运行 `start_server.bat`

### 查看日志

服务器日志直接显示在命令行窗口中。

### 修改端口

编辑 `backend/api_server.py` 最后一行:

```python
app.run(host='0.0.0.0', port=5000, debug=True)
                         ^^^^修改这里
```

### 修改日目标

编辑 `backend/data_processor.py` 第140行左右:

```python
daily_target = 200000  # 修改这个值
```

---

## API接口速查

| 接口 | 方法 | 功能 | 示例 |
|------|------|------|------|
| `/` | GET | 主页面 | http://localhost:5000 |
| `/api/refresh` | POST | 刷新数据 | `curl -X POST http://localhost:5000/api/refresh` |
| `/api/daily-report` | GET | 获取日报 | http://localhost:5000/api/daily-report |
| `/api/week-trend?weeks=1` | GET | 获取7天趋势 | http://localhost:5000/api/week-trend?weeks=1 |
| `/api/week-trend?weeks=3` | GET | 获取3周趋势 | http://localhost:5000/api/week-trend?weeks=3 |
| `/api/latest-date` | GET | 获取最新日期 | http://localhost:5000/api/latest-date |
| `/api/health` | GET | 健康检查 | http://localhost:5000/api/health |

---

## 测试API

### 使用curl测试

```bash
# 健康检查
curl http://localhost:5000/api/health

# 获取日报
curl http://localhost:5000/api/daily-report

# 获取7天趋势
curl http://localhost:5000/api/week-trend?weeks=1

# 刷新数据
curl -X POST http://localhost:5000/api/refresh
```

### 使用浏览器测试

直接在浏览器地址栏访问:

```
http://localhost:5000/api/health
http://localhost:5000/api/daily-report
http://localhost:5000/api/week-trend?weeks=1
```

---

## 故障排查速查

| 问题 | 可能原因 | 解决方法 |
|------|----------|----------|
| 服务器启动失败 | 缺少依赖包 | `pip install -r requirements.txt` |
| 页面无法访问 | 端口被占用 | 修改端口或关闭占用程序 |
| 显示"加载中..." | 后端未启动 | 检查命令行窗口是否有错误 |
| 数据不更新 | data目录为空 | 将Excel文件放入data目录 |
| 图表显示异常 | 浏览器缓存 | 按Ctrl+F5强制刷新 |
| 数据格式错误 | Excel字段不匹配 | 检查Excel是否包含必需字段 |

---

## 日常使用流程

### 每日数据更新(30秒)

1. 将今天的Excel文件复制到 `data/` 目录
2. 打开网页 http://localhost:5000
3. 点击"刷新数据"按钮
4. 等待3-5秒,完成!

### 查看趋势(10秒)

1. 打开网页 http://localhost:5000
2. 观察顶部KPI卡片
3. 查看趋势图表
4. 切换7天/3周视图

### 导出数据(5秒)

直接打开 `车险清单_2025年10-11月_合并.csv` 文件即可。

---

## 快捷键

| 按键 | 功能 |
|------|------|
| `F5` | 刷新页面 |
| `Ctrl+F5` | 强制刷新(清除缓存) |
| `F12` | 打开开发者工具 |
| `Ctrl+C` | 停止服务器 |

---

## 相关文档

- 📘 [README.md](README.md) - 项目介绍和完整文档
- 📗 [USAGE_GUIDE.md](USAGE_GUIDE.md) - 详细使用指南
- 📕 [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - 项目技术总结
- 📙 [DEMO.md](DEMO.md) - 演示指南

---

## 技术支持

遇到问题?

1. 查看 [USAGE_GUIDE.md](USAGE_GUIDE.md) 常见问题章节
2. 查看后端命令行窗口的错误信息
3. 按F12查看浏览器控制台的错误信息
4. 联系技术支持团队

---

## 下一步

✅ **系统已就绪!**

可以开始使用了:

1. 将Excel文件放入 `data/` 目录
2. 访问 http://localhost:5000
3. 点击"刷新数据"
4. 查看最新的业务数据!

---

**祝使用愉快!** 📊✨

*最后更新: 2025-11-06*
