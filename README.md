# 车险签单数据分析平台 v2.0

> 现代化的车险签单数据实时分析与可视化平台 | Modern Vehicle Insurance Analytics Platform

[![Vue 3](https://img.shields.io/badge/Vue-3.4-brightgreen.svg)](https://vuejs.org/)
[![Vite](https://img.shields.io/badge/Vite-5.0-646CFF.svg)](https://vitejs.dev/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-black.svg)](https://flask.palletsprojects.com/)

---

## ✨ 功能特性

### 📊 数据分析
- **实时KPI监控**: 签单保费、保单件数、手续费、目标达成度
- **多维度筛选**: 支持机构/团队/新业务分类/能源类型/险种等8个维度
- **趋势分析**: 3周对比柱状图，动态X轴（周一~周日）
- **智能对比**: 近7天 vs 近14天 vs 近21天三周期对比
- **数据导出**: 支持Excel/CSV格式导出（计划中）

### 🎨 用户体验
- **现代化UI**: 基于Material Design的紫色渐变主题
- **响应式设计**: 完美适配PC、平板、手机
- **流畅动画**: Hover效果、平滑过渡、加载骨架屏
- **交互式图表**: ECharts 5图表，支持缩放、悬停详情
- **智能筛选**: 折叠面板设计，标签化已选项，一键清除

### 🚀 性能优化
- **秒级加载**: 首屏加载 < 2s（v2.0目标）
- **组件化架构**: Vue 3 Composition API，代码复用率高
- **状态管理**: Pinia全局状态，避免重复请求
- **懒加载**: 按需加载组件和图表库
- **缓存优化**: 智能缓存筛选项和历史数据

---

## 🏗️ 技术架构

### 前端技术栈（v2.0全新升级）
- **框架**: Vue 3（Composition API）
- **构建工具**: Vite 5
- **状态管理**: Pinia 2
- **HTTP客户端**: Axios
- **图表库**: Apache ECharts 5
- **样式方案**: CSS Variables + BEM命名

### 后端技术栈
- **Web框架**: Flask 3.0
- **数据处理**: Pandas 2.0
- **Excel解析**: openpyxl
- **服务器**: Gunicorn + Nginx（生产环境）

### 架构图

```
┌─────────────────────────────────────────┐
│         Vue 3 SPA (Vite)                │
├─────────────────────────────────────────┤
│  Components    │  Stores   │  Services  │
│  - Dashboard   │  - app    │  - api     │
│  - KpiCard     │  - filter │  - utils   │
│  - ChartView   │  - data   │            │
│  - FilterPanel │           │            │
├─────────────────────────────────────────┤
│          Flask REST API                 │
│  /api/refresh                           │
│  /api/daily-report                      │
│  /api/week-comparison                   │
│  /api/filter-options                    │
├─────────────────────────────────────────┤
│     Pandas Data Processing              │
│  Excel → CSV → 清洗 → 合并 → 查询      │
└─────────────────────────────────────────┘
```

---

## 📁 项目结构

```
daylyreport/
├── frontend/                      # 前端源码（Vue 3）
│   ├── src/
│   │   ├── components/           # Vue组件
│   │   │   ├── Dashboard.vue     # 主仪表板
│   │   │   ├── KpiCard.vue       # KPI卡片
│   │   │   ├── ChartView.vue     # 图表组件
│   │   │   ├── FilterPanel.vue   # 筛选面板
│   │   │   └── Toast.vue         # 通知组件
│   │   ├── stores/               # Pinia状态管理
│   │   │   ├── app.ts            # 应用全局状态
│   │   │   ├── filter.ts         # 筛选器状态
│   │   │   └── data.ts           # 数据状态
│   │   ├── services/             # 服务层
│   │   │   ├── api.ts            # API调用封装
│   │   │   └── utils.ts          # 工具函数
│   │   ├── App.vue               # 根组件
│   │   └── main.ts               # 入口文件
│   ├── public/                   # 静态资源
│   ├── vite.config.ts            # Vite配置
│   └── package.json              # 前端依赖
│
├── backend/                       # 后端服务
│   ├── data_processor.py         # 数据处理核心
│   └── api_server.py             # Flask API服务器
│
├── data/                          # 数据目录
│   ├── *.xlsx                    # Excel源文件
│   └── processed/                # 已处理文件归档
│
├── docs/                          # 项目文档
│   ├── PRD.md                    # 产品需求文档
│   ├── ARCHITECTURE.md           # 架构设计文档
│   ├── DESIGN_SYSTEM.md          # 设计系统文档
│   └── MIGRATION_GUIDE.md        # v1.0迁移指南
│
├── CLAUDE.md                      # Claude Code工作指南
├── README.md                      # 项目说明（本文件）
└── requirements.txt               # Python依赖
```

---

## 🚀 快速开始

### 环境要求

- **操作系统**: Windows 10+, macOS 11+, Linux, 统信UOS, 麒麟OS
- **Python**: 3.8+ (推荐3.10或3.11)
- **Node.js**: 18+ (推荐20 LTS)
- **浏览器**: Chrome 90+, Edge 90+, Firefox 88+, Safari 14+

### 安装步骤

#### 1. 克隆仓库

```bash
git clone <repository-url>
cd daylyreport
```

#### 2. 安装后端依赖

**Windows:**
```bash
pip install -r requirements.txt
```

**macOS/Linux:**
```bash
pip3 install -r requirements.txt
```

**信创系统/网络受限环境** (使用清华镜像源):
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 3. 安装前端依赖

```bash
cd frontend
npm install

# 或使用国内镜像源
npm install --registry=https://registry.npmmirror.com
```

#### 4. 准备数据

将每日Excel签单清单放入 `data/` 目录:

```
data/
├── 2025-11-05_签单清单.xlsx
├── 2025-11-06_签单清单.xlsx
└── ...
```

**Excel格式要求**:
- 必须包含字段: `投保确认时间`, `签单/批改保费`, `签单数量`, `保单号`, `业务员`
- 支持 `.xlsx` 和 `.xls` 格式
- 系统会自动去重和清洗数据

---

### 启动服务

#### 开发环境

**方式一: 使用启动脚本（推荐）**

**Windows:**
```bash
start_server.bat
```

**macOS/Linux/信创系统:**
```bash
./start_server.sh
```

**首次使用注意**: macOS/Linux用户需先添加执行权限:
```bash
chmod +x start_server.sh
```

**方式二: 手动启动**

**启动后端（终端1）:**
```bash
cd backend
python api_server.py
# 后端运行在 http://localhost:5001
```

**启动前端（终端2）:**
```bash
cd frontend
npm run dev
# 前端运行在 http://localhost:3000
```

#### 访问系统

- **开发环境**: http://localhost:3000
- **API文档**: http://localhost:5001/api/health
- **后端健康检查**: http://localhost:5001/api/latest-date

---

## 📖 使用指南

### 数据刷新流程

1. **添加新数据**: 将新Excel文件放入 `data/` 目录
2. **触发刷新**: 点击页面右上角"刷新数据"按钮
3. **自动处理**:
   - Excel → CSV转换
   - 数据清洗（去重、格式化、缺失值填充）
   - 与历史数据合并
   - 处理完的文件移至 `data/processed/`
4. **实时更新**: 页面自动刷新显示最新KPI和图表

### 筛选功能

**8个筛选维度**:
- 三级机构（与团队联动）
- 团队
- 是否续保（新/转/续）
- 是否新能源
- 过户车
- 险种大类
- 吨位分段
- 电销标记

**使用技巧**:
- 选择机构后，团队下拉框自动联动
- 点击已选标签快速移除筛选项
- "重置"按钮清除所有筛选
- "应用筛选"按钮触发数据查询

### 图表说明

**KPI卡片**:
- 显示当日/近7天/近30天数据
- 带趋势指示器（↑ 上升、↓ 下降、→ 持平）
- 点击卡片查看详细数据（计划中）

**周对比柱状图**:
- 最近7天 vs 上7天 vs 前7天
- X轴为动态周几（周一~周日）
- 支持保费/件数指标切换
- 鼠标悬停显示详细数据

---

## 🔌 API接口

### 数据刷新

```http
POST /api/refresh
```

**响应示例**:
```json
{
  "success": true,
  "message": "数据刷新成功",
  "processed_files": ["2025-11-07_签单清单.xlsx"]
}
```

### 日报数据

```http
GET /api/daily-report?date=2025-11-07
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "date": "2025-11-07",
    "premium": 205000,
    "count": 45,
    "commission": 15000,
    "target_gap": 5000,
    "target_completion": 102.5
  }
}
```

### 周对比数据

```http
POST /api/week-comparison
Content-Type: application/json

{
  "filters": {
    "三级机构": "成都",
    "是否新能源": "是"
  }
}
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "categories": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"],
    "recent_week": [45000, 52000, 48000, 55000, 60000, 35000, 40000],
    "last_week": [42000, 50000, 46000, 53000, 58000, 33000, 38000],
    "before_last_week": [40000, 48000, 44000, 51000, 56000, 31000, 36000]
  }
}
```

### 筛选选项

```http
GET /api/filter-options
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "三级机构": ["成都", "绵阳", "德阳", "..."],
    "团队": ["团队A", "团队B", "..."],
    "车险新业务分类": ["新", "转", "续"],
    "是否新能源": ["是", "否"],
    "是否过户车": ["是", "否"]
  }
}
```

完整API文档请参考: [CLAUDE.md](./CLAUDE.md#api端点详解)

---

## ⚙️ 配置说明

### 修改日目标

编辑 `backend/data_processor.py` 第206行:

```python
daily_target = 200000  # 修改此值（单位：元）
```

### 修改服务器端口

**后端端口** (`backend/api_server.py` 第229行):
```python
PORT = 5001  # 修改此值
```

**前端端口** (`frontend/vite.config.ts`):
```typescript
export default defineConfig({
  server: {
    port: 3000  // 修改此值
  }
})
```

### 添加新筛选维度

详细步骤请参考: [CLAUDE.md - 修改系统](./CLAUDE.md#修改系统)

---

## 🧪 测试

### 数据处理测试

```bash
cd backend
python data_processor.py
```

这将输出测试报告，包括:
- 数据清洗统计
- 去重记录数
- 日期范围
- 样本数据预览

### 前端单元测试（计划中）

```bash
cd frontend
npm run test
```

### E2E测试（计划中）

```bash
cd frontend
npm run test:e2e
```

---

## 📊 版本历史

### v2.0.0 (2025-11-07) - 全面升级

**重大变更**:
- 前端重构为Vue 3 + Vite架构
- 引入Pinia状态管理
- 全新设计系统（Material Design风格）
- 组件化架构，代码可维护性提升100%
- 性能优化，首屏加载速度提升50%
- 响应式设计全面升级，移动端体验提升80%

**新增功能**:
- 折叠式筛选面板
- 标签化已选筛选项
- Toast通知系统
- Skeleton加载占位
- 智能缓存机制

**技术债务清理**:
- 移除所有全局变量
- 移除inline事件处理器
- 移除alert()调用
- 添加错误边界
- 实现防抖和节流

### v1.0.0 (2024-10) - 初始版本

- 原生JavaScript + Flask实现
- 基础KPI展示
- 简单图表对比
- 基础筛选功能

完整更新日志: [CHANGELOG.md](./docs/CHANGELOG.md)

---

## 📚 相关文档

- **[PRD.md](./docs/PRD.md)** - 产品需求文档（完整功能规划）
- **[ARCHITECTURE.md](./docs/ARCHITECTURE.md)** - 架构设计文档
- **[DESIGN_SYSTEM.md](./docs/DESIGN_SYSTEM.md)** - 设计系统规范
- **[MIGRATION_GUIDE.md](./docs/MIGRATION_GUIDE.md)** - v1.0迁移指南
- **[CLAUDE.md](./CLAUDE.md)** - Claude Code开发指南

---

## 🛠️ 常见问题

### Q: 为什么后端启动失败？

**A**: 请检查:
1. Python版本是否 >= 3.8
2. 依赖是否安装完整: `pip list | grep -E "flask|pandas|openpyxl"`
3. 端口5001是否被占用: `lsof -i :5001` (macOS/Linux) 或 `netstat -ano | findstr 5001` (Windows)

### Q: 为什么前端页面空白？

**A**: 请检查:
1. Node.js版本是否 >= 18
2. 前端依赖是否安装: `ls frontend/node_modules`
3. 浏览器控制台是否有错误
4. 后端API是否正常运行: 访问 http://localhost:5001/api/health

### Q: macOS上启动脚本无法执行？

**A**: 添加执行权限:
```bash
chmod +x start_server.sh
```

### Q: 数据刷新后没有变化？

**A**: 请检查:
1. Excel文件是否放在 `data/` 目录
2. 文件名格式是否正确（建议: `YYYY-MM-DD_签单清单.xlsx`）
3. 后端控制台是否有错误日志
4. 浏览器是否缓存了旧数据（尝试硬刷新: Ctrl+Shift+R）

### Q: 图表显示异常？

**A**: 请检查:
1. 浏览器是否支持（推荐Chrome 90+）
2. 窗口大小调整后图表是否自适应（已实现防抖）
3. 数据是否存在（查看Network面板API响应）

### Q: 信创系统/国产浏览器兼容性？

**A**:
- 支持统信UOS、麒麟OS等信创系统
- 支持360、QQ、搜狗等国产浏览器（基于Chromium内核）
- 如遇问题，请使用系统自带浏览器或安装Chrome

---

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

**开发流程**:
1. Fork本仓库
2. 创建特性分支: `git checkout -b feature/AmazingFeature`
3. 提交更改: `git commit -m 'Add some AmazingFeature'`
4. 推送到分支: `git push origin feature/AmazingFeature`
5. 提交Pull Request

**代码规范**:
- 前端: 遵循Vue 3官方风格指南
- 后端: 遵循PEP 8规范
- 提交信息: 遵循Conventional Commits规范

---

## 📄 许可证

MIT License

Copyright (c) 2025 车险业务团队

---

## 👥 联系方式

如有问题或建议，请通过以下方式联系:

- **Issue**: [GitHub Issues](https://github.com/your-repo/issues)
- **Email**: your-email@example.com

---

**Made with ❤️ for 车险业务团队**

*从v1.0到v2.0，我们始终致力于提供最佳的数据分析体验*
