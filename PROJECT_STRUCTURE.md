# 项目目录结构

## 📂 当前项目结构(清理后)

```
daylyreport/
│
├── 📁 backend/                          后端服务目录
│   ├── data_processor.py               数据处理核心模块
│   └── api_server.py                   Flask API服务器
│
├── 📁 static/                           前端资源目录
│   ├── index.html                      主页面
│   ├── 📁 css/
│   │   └── style.css                   样式文件
│   └── 📁 js/
│       └── app.js                      应用逻辑
│
├── 📁 data/                             数据目录(用户放Excel文件)
│   ├── README.md                       数据目录说明
│   └── 📁 processed/                    已处理文件归档(自动生成)
│
├── 📁 .claude/                          Claude配置目录
│
├── 📁 .git/                             Git版本控制
│
├── 📁 待处理文件夹/                     旧文件存档
│   └── README.md                       待处理文件说明
│
├── 📄 车险清单_2025年10-11月_合并.csv    主数据文件(系统维护)
├── 📄 业务员机构团队归属.json            业务员映射数据
│
├── 📄 requirements.txt                  Python依赖清单
├── 📄 start_server.bat                  Windows启动脚本
├── 📄 .gitignore                        Git忽略配置
│
└── 📄 文档文件/
    ├── README.md                        项目文档(主)
    ├── QUICKSTART.md                    快速启动指南
    ├── USAGE_GUIDE.md                   详细使用指南
    ├── PROJECT_SUMMARY.md               项目技术总结
    ├── DEMO.md                          演示指南
    └── PROJECT_STRUCTURE.md             本文档
```

---

## 📋 文件说明

### 核心文件

| 文件路径 | 大小 | 说明 | 修改频率 |
|---------|------|------|----------|
| `backend/data_processor.py` | 12KB | 数据处理核心,负责Excel清洗和KPI计算 | 需要修改目标值时 |
| `backend/api_server.py` | 5KB | Flask API服务器,提供数据接口 | 需要增加接口时 |
| `static/index.html` | 4KB | 主页面HTML | 需要修改布局时 |
| `static/css/style.css` | 15KB | 样式文件,定义界面外观 | 需要改样式时 |
| `static/js/app.js` | 18KB | 前端逻辑,处理数据和图表 | 需要改功能时 |
| `requirements.txt` | 61B | Python依赖包列表 | 很少修改 |
| `start_server.bat` | 897B | Windows启动脚本 | 很少修改 |

### 数据文件

| 文件路径 | 大小 | 说明 | 修改方式 |
|---------|------|------|----------|
| `车险清单_2025年10-11月_合并.csv` | 20MB | 主数据文件,包含所有历史数据 | 系统自动维护 |
| `业务员机构团队归属.json` | 31KB | 业务员与机构团队的映射关系 | 手动更新 |
| `data/*.xlsx` | - | 待处理的Excel文件 | 用户每日放入 |
| `data/processed/*.xlsx` | - | 已处理的Excel文件归档 | 系统自动移动 |

### 文档文件

| 文件名 | 大小 | 用途 | 适合读者 |
|--------|------|------|----------|
| `README.md` | 5KB | 项目介绍、安装、使用、API文档 | 所有人 |
| `QUICKSTART.md` | 6KB | 30秒快速启动指南 | 新用户 |
| `USAGE_GUIDE.md` | 6KB | 详细使用指南、场景演示 | 日常用户 |
| `PROJECT_SUMMARY.md` | 15KB | 技术架构、算法、性能分析 | 开发者 |
| `DEMO.md` | 8KB | 演示脚本和讲解要点 | 演示者 |
| `PROJECT_STRUCTURE.md` | 本文档 | 目录结构说明 | 维护者 |

---

## 🗂️ 目录功能说明

### 1. backend/ - 后端服务目录

**用途:** 包含所有Python后端代码

**核心模块:**
- `data_processor.py`: 数据处理引擎
  - Excel读取和转换
  - 数据清洗和去重
  - KPI计算
  - 趋势数据生成

- `api_server.py`: Web服务器
  - Flask应用配置
  - RESTful API接口
  - 静态文件服务
  - CORS跨域支持

**启动方式:**
```bash
cd backend
python api_server.py
```

---

### 2. static/ - 前端资源目录

**用途:** 包含所有前端文件(HTML/CSS/JS)

**子目录:**
- `css/`: 样式文件
- `js/`: JavaScript应用逻辑

**特点:**
- 无框架依赖(原生JS)
- 响应式设计
- 现代化UI

---

### 3. data/ - 数据目录

**用途:** 用户放置Excel文件的地方

**工作流程:**
1. 用户将Excel文件复制到此目录
2. 点击网页"刷新数据"按钮
3. 系统自动处理并移动到 `processed/` 子目录

**注意事项:**
- 只支持 `.xlsx` 和 `.xls` 格式
- 文件名可以任意
- 系统会自动去重

---

### 4. 待处理文件夹/ - 旧文件存档

**用途:** 存放项目清理时移出的旧文件

**内容分类:**
- 旧的分析脚本
- 测试文件
- 历史报告
- 大数据文件(47MB)

**处理建议:**
- 定期查看是否还需要
- 不需要的可以删除
- 重要文档可以归档

---

## 📦 依赖说明

### Python依赖(requirements.txt)

```
flask==3.0.0           # Web框架
flask-cors==4.0.0      # 跨域支持
pandas==2.1.4          # 数据处理
openpyxl==3.1.2        # Excel读取
```

### 前端依赖(CDN)

```
ECharts 5.4.3          # 图表库(通过CDN加载)
```

---

## 🔧 配置文件

### .gitignore

忽略以下文件/目录:
- `__pycache__/`
- `*.pyc`
- `.DS_Store`
- `node_modules/`
- `.env`

---

## 📈 数据流向

```
用户操作
  ↓
Excel文件 → data/
  ↓
点击"刷新数据"
  ↓
backend/data_processor.py
  ├─ 读取Excel
  ├─ 清洗数据
  ├─ 去重合并
  └─ 保存CSV
  ↓
车险清单_2025年10-11月_合并.csv
  ↓
backend/api_server.py
  ├─ 计算KPI
  └─ 生成趋势
  ↓
API接口(/api/*)
  ↓
static/js/app.js
  ├─ 更新KPI卡片
  └─ 绘制图表
  ↓
用户查看结果
```

---

## 💾 磁盘使用情况

| 目录/文件 | 大小 | 说明 |
|----------|------|------|
| `backend/` | ~20KB | 后端代码 |
| `static/` | ~40KB | 前端代码 |
| `data/` | 变化 | 待处理文件 |
| `待处理文件夹/` | 47MB | 旧文件(可删除) |
| `车险清单_2025年10-11月_合并.csv` | 20MB | 主数据 |
| 文档(*.md) | ~50KB | 项目文档 |
| **总计** | ~70MB | 含旧文件 |
| **总计(清理后)** | ~20MB | 不含旧文件 |

---

## 🎯 关键文件路径速查

### 修改日目标值
```
backend/data_processor.py  (第140行左右)
daily_target = 200000  # 修改这里
```

### 修改图表颜色
```
static/css/style.css  (搜索 "linear-gradient")
```

### 修改自动刷新间隔
```
static/js/app.js  (第24行左右)
setInterval(..., 5 * 60 * 1000)  # 5分钟
```

### 修改服务器端口
```
backend/api_server.py  (最后一行)
app.run(host='0.0.0.0', port=5000, debug=True)
```

---

## 🚀 快速操作

### 查看项目结构
```bash
ls -la
```

### 查看文件大小
```bash
du -sh *
```

### 清理旧文件(释放空间)
```bash
rm -rf 待处理文件夹
```

### 备份主数据
```bash
cp 车险清单_2025年10-11月_合并.csv 车险清单_备份_20251106.csv
```

---

## ✅ 项目完整性检查清单

- [ ] `backend/` 目录存在且包含2个py文件
- [ ] `static/` 目录存在且包含index.html和子目录
- [ ] `data/` 目录存在(可以为空)
- [ ] `requirements.txt` 文件存在
- [ ] `start_server.bat` 文件存在
- [ ] `车险清单_2025年10-11月_合并.csv` 文件存在
- [ ] `业务员机构团队归属.json` 文件存在
- [ ] 至少有README.md等3个文档文件

---

**目录结构已优化,项目更加清晰!** ✨

*最后更新: 2025-11-06*
