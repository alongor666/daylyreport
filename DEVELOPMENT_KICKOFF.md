# 🚀 开发任务启动指令

> 本文档提供给新开发者或新Claude实例的完整启动指令，可直接复制使用。

---

## 📋 给Claude实例的启动指令（推荐）

```markdown
# 开发任务：车险签单数据分析平台 v2.0 前端开发

## 项目背景

这是一个车险签单数据分析平台，正在从v1.0（原生JS）升级到v2.0（Vue 3）。

**当前状态**:
- ✅ 后端API完成（Flask + Pandas，端口5001）
- ✅ 完整的v2.0文档体系（7个核心文档，约5000行）
- ✅ 技术选型确定：Vue 3 + Vite + Pinia + ECharts
- ❌ 前端代码待开发（你的任务）

## 你的任务

**阶段1**: 初始化Vue 3项目（当前任务）
**阶段2**: 开发核心组件（Dashboard, KpiCard, ChartView, FilterPanel）
**阶段3**: 集成测试和优化

## 必须遵循的规范（重要！）

**请先阅读以下文档**:
1. **CLAUDE.md** - 你的工作指南（已自动加载到你的上下文）
2. **docs/README_FOR_DEVELOPERS.md** - 开发者快速上手指南
3. **docs/ARCHITECTURE.md** - 架构设计（12章节）
4. **docs/DESIGN_SYSTEM.md** - UI/UX规范（11章节）

**关键开发原则**（来自CLAUDE.md）:
- ✅ 使用 **Vue 3 Composition API**（不是Options API）
- ✅ 使用 **Pinia** 管理状态（禁止全局变量）
- ✅ 使用 **CSS Variables** 定义颜色/间距/字体（禁止硬编码）
- ✅ 使用 **BEM命名规范** 编写CSS类名
- ✅ 使用 **Toast组件** 显示通知（禁止alert）
- ✅ 所有API调用通过 **services/api.js** 封装
- ❌ **严格禁止**: 全局变量、alert()、内联事件处理器、硬编码样式

## 技术栈

- **前端**: Vue 3 + Vite 5 + Pinia 2 + Axios + ECharts 5
- **后端**: Flask 3.0 + Pandas（保持不变，无需修改）
- **样式**: CSS Variables + BEM命名
- **端口**: 前端3000（开发）, 后端5001

## 第一个任务：初始化Vue 3项目

**请按以下步骤执行**:

### 1. 初始化项目

```bash
npm create vue@latest frontend
```

**配置选择**（重要）:
```
✔ Project name: frontend
✔ Add TypeScript? No (或Yes，可选)
✔ Add JSX Support? No
✔ Add Vue Router? No (v2.0暂不需要)
✔ Add Pinia? Yes ✅ (必选)
✔ Add Vitest? No (未来添加)
✔ Add Cypress? No
✔ Add ESLint? Yes ✅ (推荐)
```

### 2. 创建vite.config.js

配置API代理，将 `/api/*` 请求代理到后端：

```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src')
    }
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:5001',
        changeOrigin: true
      }
    }
  }
})
```

### 3. 创建目录结构

```bash
cd frontend/src
mkdir -p components/{common,dashboard} stores services assets/styles
```

**最终结构**:
```
frontend/src/
├── components/
│   ├── common/         # 通用组件（Toast, Loading）
│   └── dashboard/      # 业务组件
├── stores/             # Pinia状态管理
├── services/           # API服务层
├── assets/
│   └── styles/         # CSS变量和全局样式
├── App.vue
└── main.js
```

### 4. 创建CSS变量文件

创建 `src/assets/styles/variables.css`，参考 `docs/DESIGN_SYSTEM.md` 第3节"色彩系统"：

```css
:root {
  /* 主色 */
  --primary-500: #A855F7;
  --primary-600: #9333EA;

  /* 功能色 */
  --success-500: #10B981;
  --error-500: #EF4444;

  /* 中性色 */
  --gray-50: #F9FAFB;
  --gray-900: #111827;
  --text-primary: var(--gray-900);

  /* 间距 */
  --space-4: 1rem;
  --space-6: 1.5rem;

  /* 字体 */
  --text-base: 1rem;
  --text-2xl: 1.5rem;
}
```

### 5. 安装依赖并启动

```bash
cd frontend
npm install
npm run dev
```

**验证标准**:
- ✅ 访问 http://localhost:3000 显示Vue欢迎页
- ✅ 无控制台错误
- ✅ Vite HMR正常工作（修改代码自动刷新）
- ✅ API代理配置正确（可测试：`fetch('/api/health')`）

---

## 开发规范示例

### Vue组件规范

```vue
<!-- ✅ 正确示例 -->
<template>
  <div class="kpi-card">
    <div class="kpi-card__title">{{ title }}</div>
    <div class="kpi-card__value">{{ value }}</div>
    <button class="kpi-card__button" @click="handleClick">
      刷新
    </button>
  </div>
</template>

<script setup>
import { computed } from 'vue'

// Props定义
const props = defineProps({
  title: {
    type: String,
    required: true
  },
  value: {
    type: Number,
    default: 0
  }
})

// Emits定义
const emit = defineEmits(['refresh'])

// 方法
const handleClick = () => {
  emit('refresh')
}

// 计算属性
const formattedValue = computed(() => {
  return props.value.toLocaleString()
})
</script>

<style scoped>
/* BEM命名 + CSS变量 */
.kpi-card {
  padding: var(--space-6);
  background: white;
  border-radius: 12px;
}

.kpi-card__title {
  font-size: var(--text-base);
  color: var(--text-secondary);
}

.kpi-card__value {
  font-size: var(--text-2xl);
  color: var(--text-primary);
  font-weight: 700;
}

.kpi-card__button {
  padding: var(--space-2) var(--space-4);
  background: var(--primary-500);
  color: white;
}
</style>
```

### Pinia Store规范

```javascript
// ✅ 正确示例 - stores/app.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAppStore = defineStore('app', () => {
  // State
  const loading = ref(false)
  const latestDate = ref(null)

  // Getters
  const displayDate = computed(() => {
    return latestDate.value || '加载中...'
  })

  // Actions
  const setLoading = (value) => {
    loading.value = value
  }

  const setLatestDate = (date) => {
    latestDate.value = date
  }

  return {
    loading,
    latestDate,
    displayDate,
    setLoading,
    setLatestDate
  }
})
```

### 错误示例（禁止）

```javascript
// ❌ 错误 - 全局变量
let currentData = {}  // 禁止！

// ❌ 错误 - alert
alert('数据刷新成功')  // 禁止！应使用Toast

// ❌ 错误 - 内联事件
<button onclick="handleClick()">  // 禁止！应使用@click

// ❌ 错误 - 硬编码样式
.card {
  padding: 24px;  // 禁止！应使用 var(--space-6)
  color: #667eea; // 禁止！应使用 var(--primary-500)
}
```

---

## 后续任务（按顺序）

完成初始化后，按以下顺序开发：

1. ✅ **初始化项目**（第一个任务，上述内容）
2. 创建设计系统基础
   - `assets/styles/variables.css` - CSS变量
   - `assets/styles/reset.css` - CSS重置
   - `assets/styles/global.css` - 全局样式
3. 创建通用组件
   - `components/common/Toast.vue` - 通知组件
   - `components/common/Loading.vue` - 加载组件
4. 创建Pinia stores
   - `stores/app.js` - 应用全局状态
   - `stores/filter.js` - 筛选器状态
   - `stores/data.js` - 数据状态
5. 创建API服务层
   - `services/api.js` - Axios封装和拦截器
6. 开发主要组件
   - `components/Header.vue` - 页面头部
   - `components/dashboard/KpiCard.vue` - KPI卡片
   - `components/dashboard/ChartView.vue` - 图表容器
   - `components/dashboard/FilterPanel.vue` - 筛选面板
   - `components/Dashboard.vue` - 主仪表板（容器组件）
7. 集成测试
   - 前后端联调
   - 功能测试
   - 响应式测试
8. 性能优化
   - 懒加载
   - 代码分割
   - 图表优化

---

## 关键文档链接

### 必读文档（按优先级）

1. **[CLAUDE.md](CLAUDE.md)** - 开发规范和技术细节（已自动加载）
2. **[docs/README_FOR_DEVELOPERS.md](docs/README_FOR_DEVELOPERS.md)** - 开发者上手指南
3. **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** - 架构设计（12章节）
4. **[docs/DESIGN_SYSTEM.md](docs/DESIGN_SYSTEM.md)** - UI/UX规范（11章节）

### 参考文档

- **[docs/PRD.md](docs/PRD.md)** - 产品需求文档
- **[docs/MIGRATION_GUIDE.md](docs/MIGRATION_GUIDE.md)** - v1.0→v2.0迁移指南
- **[CHANGELOG.md](CHANGELOG.md)** - 版本历史
- **[HOW_TO_ENSURE_CONSISTENCY.md](HOW_TO_ENSURE_CONSISTENCY.md)** - 多终端协作

### v1.0参考（已归档）

- **[docs/v1.0-archived/](docs/v1.0-archived/)** - v1.0文档（仅供参考，已过时）

---

## 遇到问题？

### 优先级1: 查文档

90%的问题文档都有答案：
- 组件如何设计？→ `docs/DESIGN_SYSTEM.md` 第6节
- API如何调用？→ `CLAUDE.md` 中的"API端点详解"
- 状态如何管理？→ `docs/ARCHITECTURE.md` 第7节

### 优先级2: 查看v1.0实现

```bash
cat docs/v1.0-archived/README.md  # 了解v1.0架构
cat static/js/app.js              # 查看v1.0逻辑（仅参考）
```

### 优先级3: 提问

- GitHub Issues
- 内部技术群
- 联系技术负责人

---

## 成功标准

开发完成后，系统应该满足：

### 功能性

- ✅ 所有功能正常运行（KPI展示、图表、筛选）
- ✅ 前后端API调用正常
- ✅ 数据刷新功能正常
- ✅ 筛选器联动正常

### 性能

- ✅ 首屏加载 < 2s
- ✅ 图表渲染 < 500ms
- ✅ 交互响应 < 100ms

### 代码质量

- ✅ 通过ESLint检查（无error）
- ✅ 无控制台错误/警告
- ✅ 遵循CLAUDE.md中的所有规范
- ✅ 使用CSS变量，无硬编码

### 用户体验

- ✅ 移动端适配良好（320px-2560px）
- ✅ 交互流畅，动画平滑
- ✅ 错误提示友好
- ✅ Loading状态明确

---

## 开始开发！

请先执行以下步骤：

1. **阅读文档**（15分钟）
   ```bash
   cat docs/README_FOR_DEVELOPERS.md
   cat CLAUDE.md | head -100
   ```

2. **初始化项目**（10分钟）
   ```bash
   npm create vue@latest frontend
   # 按上述配置选择
   ```

3. **启动验证**（5分钟）
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **告诉我进度**
   每完成一个步骤，请报告结果和遇到的问题。

**祝开发顺利！🚀**
```

---

## 📋 给人类开发者的启动指令（完整版）

```markdown
# 车险签单数据分析平台 v2.0 开发任务

## 项目背景

我们正在将车险签单数据分析平台从v1.0（原生JavaScript）全面升级到v2.0（Vue 3架构）。

**当前进度**:
- ✅ 后端API完成（Flask + Pandas，无需改动）
- ✅ 完整的v2.0文档体系（PRD/架构/设计系统/迁移指南等7个核心文档）
- ✅ 技术选型确定（Vue 3 + Vite + Pinia）
- ❌ 前端代码待开发（你的任务）

## 环境要求

- **Node.js**: 18+ (推荐20 LTS)
- **Python**: 3.8+ (推荐3.10/3.11)
- **Git**: 最新版本
- **浏览器**: Chrome 90+, Edge 90+, Firefox 88+, Safari 14+
- **操作系统**: Windows 10+, macOS 11+, Linux, 信创系统

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/alongor666/daylyreport.git
cd daylyreport
```

### 2. 必读文档（30分钟）

**请按顺序阅读**:

1. **[docs/README_FOR_DEVELOPERS.md](docs/README_FOR_DEVELOPERS.md)** (10分钟)
   - 文档导航
   - 开发流程
   - 常见错误避免

2. **[CLAUDE.md](CLAUDE.md)** (15分钟)
   - 技术栈和架构
   - 组件设计规范
   - API文档

3. **根据任务选读**:
   - 开发UI组件 → [docs/DESIGN_SYSTEM.md](docs/DESIGN_SYSTEM.md)
   - 了解架构 → [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
   - 了解需求 → [docs/PRD.md](docs/PRD.md)

### 3. 安装依赖

**后端**（保持运行）:
```bash
# macOS/Linux
pip3 install -r requirements.txt
cd backend
python3 api_server.py

# Windows
pip install -r requirements.txt
cd backend
python api_server.py

# 后端运行在 http://localhost:5001
```

**前端**（第一个任务）:
```bash
# 当前前端还未初始化
# 你的第一个任务就是搭建Vue 3环境
npm create vue@latest frontend
```

### 4. 开发环境配置

**VSCode推荐插件**:
- Volar (Vue 3官方)
- ESLint
- Prettier
- Vue VSCode Snippets

**Chrome推荐插件**:
- Vue Devtools

## 开发规范（重要！）

### ✅ 必须遵守

- **框架**: Vue 3 Composition API（不是Options API）
- **状态管理**: Pinia（禁止全局变量、localStorage直接操作）
- **样式**: CSS Variables + BEM命名（禁止内联样式、硬编码颜色）
- **通知**: Toast组件（禁止alert、confirm、prompt）
- **API调用**: 通过services/api.js封装（禁止直接fetch）
- **组件命名**: PascalCase（如KpiCard.vue）
- **CSS类名**: BEM（如kpi-card__value）

### ❌ 严格禁止

- ❌ 全局变量
- ❌ `alert()`, `confirm()`, `prompt()`
- ❌ 内联事件处理器（`onclick`等）
- ❌ 硬编码的颜色、间距、字体大小
- ❌ 直接操作DOM（除非必要）

## 第一个任务：初始化Vue 3项目

**目标**: 搭建Vue 3 + Vite开发环境

**步骤**:

1. **运行初始化命令**
   ```bash
   npm create vue@latest frontend
   ```

2. **配置选择**（重要）
   ```
   ✔ Project name: frontend
   ✔ Add TypeScript? No (或Yes，看团队偏好)
   ✔ Add JSX Support? No
   ✔ Add Vue Router? No (v2.0暂不需要)
   ✔ Add Pinia? Yes ✅ (必选！)
   ✔ Add Vitest? No (未来添加)
   ✔ Add Cypress? No
   ✔ Add ESLint? Yes ✅ (强烈推荐)
   ```

3. **安装依赖**
   ```bash
   cd frontend
   npm install
   ```

4. **配置Vite代理**
   创建/修改 `vite.config.js`:
   ```javascript
   import { defineConfig } from 'vite'
   import vue from '@vitejs/plugin-vue'
   import path from 'path'

   export default defineConfig({
     plugins: [vue()],
     resolve: {
       alias: {
         '@': path.resolve(__dirname, 'src')
       }
     },
     server: {
       port: 3000,
       proxy: {
         '/api': {
           target: 'http://localhost:5001',
           changeOrigin: true
         }
       }
     }
   })
   ```

5. **创建目录结构**
   ```bash
   cd src
   mkdir -p components/common components/dashboard stores services assets/styles
   ```

6. **启动开发服务器**
   ```bash
   npm run dev
   ```

**验证成功标准**:
- ✅ 访问 http://localhost:3000 显示Vue欢迎页
- ✅ 控制台无错误
- ✅ 修改代码自动热更新
- ✅ API代理正常（可在控制台测试：`fetch('/api/health')`）

## 后续任务（按顺序）

### 第1周：基础搭建

1. ✅ 初始化Vue 3项目（上述任务）
2. 创建设计系统基础
   - CSS变量文件（参考DESIGN_SYSTEM.md）
   - 全局样式
3. 创建通用组件
   - Toast通知组件
   - Loading加载组件
4. 创建Pinia stores
   - app.js - 应用全局状态
   - filter.js - 筛选器状态
   - data.js - 数据状态
5. 创建API服务层
   - api.js - Axios配置和拦截器

### 第2周：核心功能

6. 开发Header组件
7. 开发KpiCard组件（4个KPI卡片）
8. 开发ChartView组件（ECharts集成）
9. 开发FilterPanel组件（筛选面板）
10. 开发Dashboard主页面（容器组件）

### 第3周：测试优化

11. 前后端联调测试
12. 响应式适配（移动端）
13. 性能优化（懒加载、代码分割）
14. ESLint检查和修复
15. 用户验收测试

## 关键文档快速链接

- **开发规范**: [CLAUDE.md](CLAUDE.md)
- **快速上手**: [docs/README_FOR_DEVELOPERS.md](docs/README_FOR_DEVELOPERS.md)
- **架构设计**: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) (12章节)
- **设计系统**: [docs/DESIGN_SYSTEM.md](docs/DESIGN_SYSTEM.md) (11章节)
- **产品需求**: [docs/PRD.md](docs/PRD.md)
- **迁移指南**: [docs/MIGRATION_GUIDE.md](docs/MIGRATION_GUIDE.md)
- **版本历史**: [CHANGELOG.md](CHANGELOG.md)

## 开发技巧

### 如何查找答案

1. **组件设计问题** → `docs/DESIGN_SYSTEM.md` 第6节"组件库"
2. **API调用问题** → `CLAUDE.md` "API端点详解"部分
3. **状态管理问题** → `docs/ARCHITECTURE.md` 第7节"状态管理"
4. **样式问题** → `docs/DESIGN_SYSTEM.md` 第3-5节（色彩/字体/间距）

### 代码示例位置

所有文档都包含详细的代码示例：
- Vue组件示例 → DESIGN_SYSTEM.md
- Pinia Store示例 → ARCHITECTURE.md
- API调用示例 → CLAUDE.md

## 遇到问题？

### 自助排查

1. **先查文档**（90%问题都有答案）
2. **查看v1.0实现**（`docs/v1.0-archived/`仅供参考）
3. **查看Git历史**（`git log --oneline`）

### 提问渠道

1. **GitHub Issues** - 技术问题、Bug报告
2. **内部技术群** - 快速咨询
3. **技术负责人** - 架构决策、紧急问题

## 成功标准

开发完成后，请确认：

### 功能性（必须全部通过）

- [ ] 所有功能正常运行
- [ ] 前后端API调用正常
- [ ] 数据刷新功能正常
- [ ] 筛选器联动正常
- [ ] 图表交互正常

### 性能（必须达标）

- [ ] 首屏加载 < 2s
- [ ] 图表渲染 < 500ms
- [ ] TTI (Time to Interactive) < 3s

### 代码质量（必须通过）

- [ ] `npm run lint` 无error
- [ ] 无控制台错误/警告
- [ ] 遵循CLAUDE.md所有规范
- [ ] 无硬编码颜色/间距/字体

### 用户体验（必须良好）

- [ ] 移动端适配（320px-2560px）
- [ ] 交互流畅，动画平滑
- [ ] 错误提示友好
- [ ] Loading状态明确

## 联系方式

- **项目负责人**: [姓名/邮箱]
- **技术支持**: [技术群/邮箱]
- **GitHub**: https://github.com/alongor666/daylyreport

---

**准备好了？开始你的第一个任务吧！🚀**

1. 阅读 `docs/README_FOR_DEVELOPERS.md` (10分钟)
2. 初始化Vue 3项目 (15分钟)
3. 报告进度和问题

**祝开发顺利！**
```

---

## 💡 使用建议

### 这个文件已经创建了

我刚刚创建了 **[DEVELOPMENT_KICKOFF.md](DEVELOPMENT_KICKOFF.md)**，您可以：

1. **直接发给开发者**:
   ```
   "请查看DEVELOPMENT_KICKOFF.md，按照说明开始开发"
   ```

2. **给新Claude实例**:
   ```
   "请阅读DEVELOPMENT_KICKOFF.md中的'给Claude实例的启动指令'部分，
   然后开始初始化Vue 3项目"
   ```

3. **发给团队**:
   ```
   "车险项目v2.0开发启动，详见仓库根目录的DEVELOPMENT_KICKOFF.md"
   ```

要我现在提交这个文件到Git吗？