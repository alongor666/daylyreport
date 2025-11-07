# 开发者指南 - 如何使用本项目文档

> 📚 本文档专为**新加入的开发者**或**新的Claude Code实例**设计，帮助快速理解项目结构和开发流程。

---

## 🚀 快速开始（5分钟上手）

### 第一次打开项目？

1. **先读这个文件** ← 你正在读
2. **然后读** [CLAUDE.md](../CLAUDE.md) - Claude Code工作指南（必读）
3. **最后读** [README.md](../README.md) - 项目总览和快速开始

### 如果你是Claude Code实例

**CLAUDE.md已经被自动加载到你的上下文中**，你应该：

1. ✅ 遵循CLAUDE.md中的所有开发规范
2. ✅ 使用文档中定义的技术栈和架构模式
3. ✅ 参考API文档和组件设计进行开发
4. ✅ 在开始编码前检查相关设计文档

---

## 📖 文档导航

### 核心文档（必读）

| 文档 | 用途 | 何时阅读 |
|------|------|---------|
| **[CLAUDE.md](../CLAUDE.md)** | Claude Code工作指南 | 🔴 **开始任何工作前必读** |
| **[README.md](../README.md)** | 项目总览、快速开始 | 第一次了解项目时 |
| **[PRD.md](PRD.md)** | 产品需求文档 | 需要了解功能需求时 |

### 设计文档（开发前参考）

| 文档 | 用途 | 何时阅读 |
|------|------|---------|
| **[ARCHITECTURE.md](ARCHITECTURE.md)** | 架构设计（前后端/API/部署） | 设计新功能或重构时 |
| **[DESIGN_SYSTEM.md](DESIGN_SYSTEM.md)** | UI/UX设计规范 | 开发UI组件时 |
| **[MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)** | v1.0→v2.0迁移指南 | 进行迁移工作时 |

### 变更记录

| 文档 | 用途 | 何时阅读 |
|------|------|---------|
| **[CHANGELOG.md](../CHANGELOG.md)** | 版本历史和路线图 | 需要了解版本变更时 |

---

## 🗺️ 文档阅读路径

### 路径1: 我是新开发者

```
README.md (了解项目)
    ↓
CLAUDE.md (开发规范)
    ↓
PRD.md (功能需求)
    ↓
ARCHITECTURE.md (技术架构)
    ↓
DESIGN_SYSTEM.md (UI规范)
    ↓
开始开发 🎉
```

### 路径2: 我是新的Claude实例

```
CLAUDE.md (已自动加载 ✅)
    ↓
根据用户请求查阅对应文档
    ↓
遵循文档规范进行开发
```

### 路径3: 我要做v1.0→v2.0迁移

```
MIGRATION_GUIDE.md (迁移步骤)
    ↓
ARCHITECTURE.md (新架构理解)
    ↓
DESIGN_SYSTEM.md (新设计规范)
    ↓
执行迁移 + 测试验证
```

### 路径4: 我要开发新功能

```
PRD.md (确认需求范围)
    ↓
ARCHITECTURE.md (确认架构模式)
    ↓
DESIGN_SYSTEM.md (确认设计规范)
    ↓
CLAUDE.md (查看开发命令和组件设计)
    ↓
开始编码
```

---

## 🎯 关键开发原则（来自CLAUDE.md）

以下是CLAUDE.md中最重要的开发原则，请务必遵守：

### 1. 技术栈（不可改变）

- **前端**: Vue 3 + Vite 5 + Pinia 2 + Axios + ECharts 5
- **后端**: Flask 3.0 + Pandas（保持不变）
- **样式**: CSS Variables + BEM命名

### 2. 目录结构（必须遵循）

```
frontend/src/
  ├── components/     ← Vue组件
  ├── stores/         ← Pinia状态管理
  ├── services/       ← API服务层
  └── assets/styles/  ← CSS变量和样式

backend/
  ├── api_server.py      ← Flask路由
  └── data_processor.py  ← 数据处理
```

### 3. 组件规范

- **命名**: PascalCase (如 `KpiCard.vue`)
- **Props**: 必须定义类型和默认值
- **样式**: 使用 `<style scoped>` + CSS变量
- **事件**: 使用 kebab-case (如 `@update:value`)

### 4. 状态管理

- ❌ **禁止**: 全局变量、localStorage直接操作
- ✅ **使用**: Pinia stores (app/filter/data)

### 5. API调用

- ❌ **禁止**: `fetch()`, `XMLHttpRequest`
- ✅ **使用**: `services/api.js` 中封装的Axios方法

### 6. 用户交互

- ❌ **禁止**: `alert()`, `confirm()`, `prompt()`
- ✅ **使用**: Toast通知组件

---

## 🔧 开发环境设置

### 前端开发

```bash
# 安装依赖
cd frontend
npm install

# 启动开发服务器 (http://localhost:3000)
npm run dev

# 构建生产版本
npm run build
```

### 后端开发

```bash
# 启动后端 (http://localhost:5001)
cd backend
python3 api_server.py

# 或使用启动脚本（macOS/Linux）
./start_server.sh
```

### 全栈开发

**开发模式**（推荐）：
```bash
# 终端1: 启动后端
cd backend && python3 api_server.py

# 终端2: 启动前端
cd frontend && npm run dev

# 访问 http://localhost:3000
# API请求自动代理到 http://localhost:5001
```

---

## 📝 开发流程示例

### 场景1: 新增一个KPI卡片

1. **查阅文档**:
   - [DESIGN_SYSTEM.md - 组件库 - KPI卡片](DESIGN_SYSTEM.md#62-kpi卡片-kpicard)
   - [CLAUDE.md - 组件设计 - KpiCard](../CLAUDE.md#组件设计)

2. **创建组件**: `frontend/src/components/NewKpiCard.vue`

3. **遵循规范**:
   ```vue
   <template>
     <div class="kpi-card">
       <!-- 使用CSS变量 -->
       <div class="kpi-card__value">{{ value }}</div>
     </div>
   </template>

   <script setup>
   // 定义Props
   const props = defineProps({
     value: {
       type: Number,
       required: true
     }
   })
   </script>

   <style scoped>
   .kpi-card {
     padding: var(--space-6);
     border-radius: var(--radius-lg);
     /* 使用BEM命名 */
   }
   </style>
   ```

4. **集成到Dashboard**: 在 `Dashboard.vue` 中引入

5. **测试验证**: 检查样式、交互、响应式

### 场景2: 修改API端点

1. **查阅文档**:
   - [ARCHITECTURE.md - API设计](ARCHITECTURE.md#8-api设计)
   - [CLAUDE.md - API端点](../CLAUDE.md#后端api端点)

2. **修改后端**: `backend/api_server.py`

3. **更新文档**: 同步更新CLAUDE.md中的API文档

4. **前端调用**: 在 `services/api.js` 中添加方法

5. **测试**: 使用 `curl` 或Postman测试API

---

## ⚠️ 常见错误和避免方法

### 错误1: 不遵循CSS变量

❌ **错误**:
```css
.card {
  padding: 24px;  /* 硬编码 */
  color: #667eea; /* 硬编码颜色 */
}
```

✅ **正确**:
```css
.card {
  padding: var(--space-6);
  color: var(--primary-500);
}
```

### 错误2: 使用全局变量

❌ **错误**:
```javascript
let currentFilters = {}  // 全局变量
```

✅ **正确**:
```javascript
import { useFilterStore } from '@/stores/filter'
const filterStore = useFilterStore()
```

### 错误3: 内联事件处理器

❌ **错误**:
```html
<button onclick="handleClick()">点击</button>
```

✅ **正确**:
```vue
<button @click="handleClick">点击</button>
```

### 错误4: 使用alert

❌ **错误**:
```javascript
alert('数据刷新成功')
```

✅ **正确**:
```javascript
import { useToast } from '@/composables/useToast'
const toast = useToast()
toast.success('数据刷新成功')
```

---

## 🤝 多终端协作指南

### 如何确保不同Claude实例使用相同文档？

1. **提交到Git** (已完成 ✅)
   ```bash
   git add .
   git commit -m "docs: 更新文档"
   git push origin main
   ```

2. **其他终端拉取**
   ```bash
   git pull origin main
   ```

3. **验证CLAUDE.md已更新**
   ```bash
   cat CLAUDE.md | head -20
   ```

4. **新的Claude实例会自动读取最新CLAUDE.md**
   - CLAUDE.md在项目根目录
   - Claude Code会自动加载并遵循

### 如何通知其他开发者？

1. **创建PR**: 提交Pull Request并描述变更
2. **发消息**: 通知团队成员拉取最新代码
3. **查看CHANGELOG**: 让他们查看CHANGELOG.md了解变更

---

## 📊 文档版本管理

### 当前版本

- **文档版本**: v2.0-docs-complete
- **最后更新**: 2025-11-07
- **Git标签**: `v2.0-docs-complete`

### 查看文档历史

```bash
# 查看所有文档相关提交
git log --oneline --grep="docs"

# 查看特定文档的变更历史
git log -p docs/PRD.md

# 查看所有标签
git tag -l
```

### 恢复到特定文档版本

```bash
# 恢复到文档完成时的状态
git checkout v2.0-docs-complete

# 查看后返回最新
git checkout main
```

---

## 🔍 常见问题FAQ

### Q1: CLAUDE.md和README.md有什么区别？

- **CLAUDE.md**: 给Claude Code看的，包含详细开发规范、命令、架构
- **README.md**: 给用户看的，包含项目介绍、快速开始、使用指南

### Q2: 我要修改文档怎么办？

1. 修改对应的.md文件
2. 提交到Git: `git commit -m "docs: 更新XXX文档"`
3. 推送到远程: `git push`
4. 通知团队成员

### Q3: 新的Claude实例会自动读取CLAUDE.md吗？

**是的！** Claude Code会自动读取项目根目录的CLAUDE.md文件，并将其作为工作指南。

### Q4: 如果文档和代码冲突怎么办？

**优先级**: 代码 > CLAUDE.md > 其他文档

原因: CLAUDE.md是实时维护的开发指南，应该反映最新的代码实践。

### Q5: 我可以不遵循文档规范吗？

**不可以！** 这些规范是为了确保：
- 代码一致性
- 团队协作效率
- 可维护性
- 新人上手速度

---

## 📚 扩展阅读

### Vue 3官方文档
- [Vue 3指南](https://vuejs.org/guide/)
- [Composition API](https://vuejs.org/guide/extras/composition-api-faq.html)
- [单文件组件](https://vuejs.org/guide/scaling-up/sfc.html)

### Pinia官方文档
- [Pinia入门](https://pinia.vuejs.org/getting-started.html)
- [定义Store](https://pinia.vuejs.org/core-concepts/)

### Vite官方文档
- [Vite指南](https://vitejs.dev/guide/)
- [配置参考](https://vitejs.dev/config/)

### Flask官方文档
- [Flask快速开始](https://flask.palletsprojects.com/en/3.0.x/quickstart/)
- [Blueprints](https://flask.palletsprojects.com/en/3.0.x/blueprints/)

---

## 💬 获取帮助

如果你遇到问题：

1. **先查文档**: 90%的问题文档都有答案
2. **查看CHANGELOG**: 可能是已知问题或新特性
3. **提Issue**: GitHub Issues
4. **联系团队**: 内部技术群

---

## ✅ 检查清单：我准备好开发了吗？

使用此清单确认你已准备就绪：

- [ ] 已阅读 [README.md](../README.md)
- [ ] 已阅读 [CLAUDE.md](../CLAUDE.md)
- [ ] 已了解技术栈（Vue 3 + Vite + Pinia + Flask）
- [ ] 已理解目录结构
- [ ] 已配置开发环境（Node.js + Python）
- [ ] 已成功启动前后端服务
- [ ] 已查阅相关设计文档（ARCHITECTURE/DESIGN_SYSTEM）
- [ ] 已了解Git工作流程

**如果全部打勾 → 开始开发吧！🚀**

---

**文档维护者**: AI Assistant (Claude)
**最后更新**: 2025-11-07
**问题反馈**: GitHub Issues
