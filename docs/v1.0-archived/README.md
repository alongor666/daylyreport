# v1.0 文档归档

> 这些文档描述的是v1.0（原生JavaScript）版本的系统，已于2025-11-08归档。

---

## ⚠️ 重要提示

**这些文档已过时，仅供历史参考！**

当前系统版本是 **v2.0**，技术栈已全面升级为 **Vue 3 + Vite + Pinia**。

### 请查看最新文档

- **[README.md](../../README.md)** - v2.0项目总览和快速开始
- **[CLAUDE.md](../../CLAUDE.md)** - v2.0开发指南（Claude Code必读）
- **[docs/](../)** - v2.0完整文档体系

---

## 📚 归档文件列表

### v1.0 文档说明

| 文档 | 原用途 | 为何归档 |
|------|--------|---------|
| **DEMO.md** | v1.0演示指南 | 端口5000→5001，static目录已废弃 |
| **PROJECT_STRUCTURE.md** | v1.0目录结构 | 缺少frontend/目录，描述原生JS结构 |
| **PROJECT_SUMMARY.md** | v1.0项目总结 | 描述原生JS技术实现，无Vue 3 |
| **QUICKSTART.md** | v1.0快速启动 | 端口5000，Windows路径硬编码 |
| **USAGE_GUIDE.md** | v1.0使用指南 | 描述static/index.html而非Vue SPA |

---

## 🔄 v1.0 → v2.0 主要变更

### 技术栈对比

| 组件 | v1.0 | v2.0 |
|------|------|------|
| **前端框架** | 原生JavaScript | Vue 3 (Composition API) |
| **构建工具** | 无 | Vite 5 |
| **状态管理** | 全局变量 | Pinia 2 |
| **HTTP客户端** | XMLHttpRequest | Axios |
| **样式方案** | 内联样式 + CSS | CSS Variables + BEM |
| **目录结构** | `static/` | `frontend/src/` |
| **开发服务器** | Flask直接托管 | Vite Dev Server + 代理 |
| **端口** | 5000 | 前端3000 / 后端5001 |

### 架构变更

**v1.0**:
```
static/
  ├── index.html (单页HTML)
  ├── css/style.css
  └── js/app.js (全局变量、内联事件)
```

**v2.0**:
```
frontend/
  └── src/
      ├── components/ (Vue组件)
      ├── stores/     (Pinia状态)
      ├── services/   (API封装)
      └── App.vue
```

---

## 📖 如何查看v1.0历史代码

### 查看Git历史

```bash
# 查看v1.0时期的代码
git log --before="2025-11-07" --oneline

# 切换到v1.0标签（如果存在）
git checkout v1.0-backup

# 返回最新版本
git checkout main
```

### 查看v1.0文件内容

```bash
# 查看归档的文档
cat docs/v1.0-archived/QUICKSTART.md

# 查看v1.0时期的代码
git show v1.0-backup:static/js/app.js
```

---

## 🚀 迁移到v2.0

如果您需要从v1.0迁移到v2.0，请参考：

- **[docs/MIGRATION_GUIDE.md](../MIGRATION_GUIDE.md)** - 详细的迁移指南
- **[CHANGELOG.md](../../CHANGELOG.md)** - 完整的版本变更日志

---

## 📅 归档信息

- **归档日期**: 2025-11-08
- **归档原因**: v2.0全面升级，技术栈从原生JS变更为Vue 3
- **v1.0最后提交**: `eed826f - Initial GitHub upload: project files`
- **v2.0文档完成**: `v2.0-docs-complete` 标签

---

## 🔗 相关链接

- **v2.0文档**: [docs/](../)
- **迁移指南**: [docs/MIGRATION_GUIDE.md](../MIGRATION_GUIDE.md)
- **架构设计**: [docs/ARCHITECTURE.md](../ARCHITECTURE.md)
- **更新日志**: [CHANGELOG.md](../../CHANGELOG.md)

---

**维护者**: AI Assistant (Claude)
**最后更新**: 2025-11-08
