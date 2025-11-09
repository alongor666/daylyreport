# 📦 文档归档 - Documentation Archive

> 本目录包含已被合并或替代的旧版文档，仅供历史参考

**归档日期**: 2025-11-08
**归档原因**: v2.0文档优化，减少冗余，提升可维护性

---

## 📋 归档文件列表

### 已合并文档

以下文档已被合并到新的文档体系中：

| 原文档 | 合并至 | 原因 |
|--------|--------|------|
| `CLAUDE.md` | [DEVELOPER_GUIDE.md](../DEVELOPER_GUIDE.md) | 开发者内容整合 |
| `README_FOR_DEVELOPERS.md` | [DEVELOPER_GUIDE.md](../DEVELOPER_GUIDE.md) | 避免重复开发文档 |
| `MIGRATION_GUIDE.md` | [DEVELOPER_GUIDE.md](../DEVELOPER_GUIDE.md) | 迁移指南作为开发指南的章节 |
| `DESIGN_PHILOSOPHY.md` | [DESIGN_GUIDE.md](../DESIGN_GUIDE.md) | 设计哲学作为设计指南的一部分 |
| `DESIGN_SYSTEM.md` | [DESIGN_GUIDE.md](../DESIGN_GUIDE.md) | 避免重复设计文档 |
| `DESIGN_UPGRADE.md` | [DESIGN_GUIDE.md](../DESIGN_GUIDE.md) | 升级说明整合到设计指南 |
| `THEME_ARCHITECTURE.md` | [THEME_SYSTEM.md](../THEME_SYSTEM.md) | 主题架构简化整合 |
| `SIMPLE_THEME_ARCHITECTURE.md` | [THEME_SYSTEM.md](../THEME_SYSTEM.md) | 简化主题架构与完整架构合并 |

---

## 🎯 优化成果

### 优化前 (v1.0)
- **文档数量**: 9个
- **总字数**: ~48,000
- **维护成本**: 高（信息分散、重复内容多）
- **新人学习曲线**: 陡峭（不知从何读起）

### 优化后 (v2.0)
- **文档数量**: 7个 核心文档 + 1个 导航中心
- **总字数**: ~34,500 (-28%)
- **维护成本**: 低（单一职责、无重复）
- **新人学习曲线**: 平缓（清晰的学习路径）

---

## 📚 新文档体系

### Tier 1: 入口文档
- [README.md](../../README.md) - 项目入口，10秒了解项目

### Tier 2: 核心文档（按角色）
- [DEVELOPER_GUIDE.md](../DEVELOPER_GUIDE.md) - 开发者完整指南
- [DESIGN_GUIDE.md](../DESIGN_GUIDE.md) - 设计系统规范
- [ARCHITECTURE.md](../ARCHITECTURE.md) - 系统架构文档
- [PRODUCT_SPEC.md](../PRODUCT_SPEC.md) - 产品需求规格
- [THEME_SYSTEM.md](../THEME_SYSTEM.md) - 主题系统文档

### Tier 3: 辅助文档
- [CONTRIBUTING.md](../../CONTRIBUTING.md) - 贡献指南
- [CHANGELOG.md](../../CHANGELOG.md) - 版本历史

### 导航中心
- [DOCS_INDEX.md](../DOCS_INDEX.md) - 完整文档索引和学习路径

---

## 🔍 如何查找旧内容

如果您需要查找旧文档中的特定内容：

### 方法1: 查看合并后的新文档
直接访问上表中"合并至"列的新文档，内容已经整合并优化。

### 方法2: 使用Git历史
```bash
# 查看某个文件的历史版本
git log --follow -- docs/archive/DESIGN_PHILOSOPHY.md

# 查看特定提交的文件内容
git show <commit-hash>:docs/DESIGN_PHILOSOPHY.md
```

### 方法3: 直接阅读归档文件
归档文件保留原始内容，可直接查看（但可能包含过时信息）。

---

## ⚠️ 重要提醒

1. **不要引用归档文档**: 归档文档不再维护，请引用新文档体系
2. **不要修改归档文档**: 如需更新内容，请修改对应的新文档
3. **归档文档可能过时**: 仅供历史参考，以新文档为准

---

## 🗑️ 删除计划

归档文档计划在 **v3.0** (2025年Q2) 后永久删除，届时：
- 保留时长: 6个月（2025-11 至 2026-05）
- 通知方式: CHANGELOG.md 中提前通知
- 备份方式: Git历史永久保留

---

## 📞 问题反馈

如果您在新文档体系中找不到原有内容：

1. 查看 [DOCS_INDEX.md](../DOCS_INDEX.md) 导航中心
2. 在新文档中搜索关键词
3. 提交Issue: `docs: 找不到XXX内容`

---

<div align="center">

**文档优化，让知识更易获取**

[返回文档首页](../DOCS_INDEX.md)

</div>
