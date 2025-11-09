# 🤝 贡献指南 - Contributing Guide

> 感谢您考虑为「车险签单数据分析平台」贡献代码！我们欢迎任何形式的贡献。

**语言 Language**: [中文](#中文版本) | [English](#english-version)

---

## 中文版本

### 📋 目录

- [行为准则](#行为准则)
- [我能做什么贡献](#我能做什么贡献)
- [开发流程](#开发流程)
- [代码规范](#代码规范)
- [提交规范](#提交规范)
- [Pull Request流程](#pull-request流程)
- [测试要求](#测试要求)

---

### 🤗 行为准则

参与本项目即表示您同意遵守我们的行为准则：

- ✅ **尊重他人** - 包容不同观点和经验
- ✅ **建设性反馈** - 批评代码而非个人
- ✅ **协作优先** - 寻求共识而非对抗
- ✅ **专业态度** - 保持友善、专业的沟通
- ❌ **零容忍** - 不接受任何形式的骚扰、歧视、攻击性言论

---

### 💡 我能做什么贡献

#### 🐛 报告Bug

**步骤**:
1. 检查 [Issues](https://github.com/your-repo/issues) 确认未被报告
2. 使用Bug模板创建Issue
3. 包含详细信息：
   - 复现步骤
   - 预期行为 vs 实际行为
   - 环境信息（浏览器、OS、Node/Python版本）
   - 截图或错误日志

**示例**:
```markdown
**Bug描述**: KPI卡片数据刷新后显示NaN

**复现步骤**:
1. 访问 http://localhost:3000
2. 点击"刷新数据"按钮
3. 签单保费卡片显示NaN

**预期行为**: 应显示数字如"20.5万"

**环境**:
- 浏览器: Chrome 120.0
- OS: macOS 14.0
- Node: v18.17.0
```

#### ✨ 提出新功能

**步骤**:
1. 先创建 [Discussion](https://github.com/your-repo/discussions) 讨论可行性
2. 获得维护者认可后创建Feature Request Issue
3. 包含：用户故事、业务价值、UI原型（如有）

**示例**:
```markdown
**功能需求**: 支持自定义日期范围查询

**用户故事**:
作为业务分析师，我希望能选择任意日期范围（如2024-10-01到2024-10-15）查看数据，
这样我可以分析特定时间段的业务表现。

**业务价值**:
- 提升数据分析灵活性
- 减少手动数据导出工作量

**UI原型**:
[附件: date-range-picker-mockup.png]
```

#### 📝 改进文档

欢迎以下文档贡献：
- 修复错别字、语法错误
- 补充使用示例
- 翻译文档（中英双语）
- 增加FAQ条目

**提交方式**: 直接提交Pull Request

#### 🔧 提交代码

见下方 [开发流程](#开发流程)

---

### 🛠️ 开发流程

#### 1. Fork并克隆仓库

```bash
# Fork仓库到你的GitHub账号
# 然后克隆你的Fork
git clone https://github.com/YOUR_USERNAME/daylyreport.git
cd daylyreport

# 添加上游远程仓库
git remote add upstream https://github.com/original-owner/daylyreport.git
```

#### 2. 创建分支

**分支命名规范**:
```bash
# 新功能
git checkout -b feature/date-range-picker

# Bug修复
git checkout -b fix/kpi-card-nan-issue

# 文档更新
git checkout -b docs/update-api-reference

# 重构
git checkout -b refactor/optimize-chart-rendering
```

#### 3. 安装依赖

```bash
# 前端依赖
npm install

# 后端依赖
pip install -r requirements.txt

# 推荐使用虚拟环境
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

#### 4. 开发

```bash
# 终端1: 启动前端开发服务器
npm run dev
# 访问 http://localhost:5173

# 终端2: 启动后端API服务器
cd backend
python api_server.py
# API地址 http://localhost:5001
```

#### 5. 测试

```bash
# 前端测试（未来）
npm run test
npm run test:e2e

# 后端测试（未来）
pytest backend/tests/
```

#### 6. 提交代码

见下方 [提交规范](#提交规范)

---

### 📐 代码规范

#### 前端规范 (Vue 3)

**组件命名**: PascalCase
```vue
<!-- ✅ 正确 -->
<KpiCard />
<DateRangePicker />

<!-- ❌ 错误 -->
<kpiCard />
<date-range-picker />
```

**Props定义**: 必须包含类型和默认值
```javascript
// ✅ 正确
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

// ❌ 错误
const props = defineProps(['title', 'value'])
```

**样式**: 使用scoped + CSS变量
```vue
<!-- ✅ 正确 -->
<style scoped>
.card {
  padding: var(--space-4);
  background: var(--bg-primary);
  border-radius: var(--radius-lg);
}
</style>

<!-- ❌ 错误 -->
<style>
.card {
  padding: 16px;
  background: #ffffff;
  border-radius: 12px;
}
</style>
```

#### 后端规范 (Flask)

**函数文档**: 使用Google风格docstring
```python
# ✅ 正确
def get_kpi_data(date: str = None) -> dict:
    """获取KPI三口径数据

    Args:
        date: 查询日期，格式YYYY-MM-DD，默认最新日期

    Returns:
        包含premium/policy_count/commission的字典

    Raises:
        ValueError: 日期格式错误时
    """
    pass
```

**类型注解**: 所有公开函数必须有类型注解
```python
# ✅ 正确
def process_data(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    pass

# ❌ 错误
def process_data(df, filters):
    pass
```

#### 通用规范

**文件命名**: kebab-case
```
✅ kpi-card.vue, data-service.js, api-server.py
❌ KpiCard.vue, dataService.js, ApiServer.py
```

**变量命名**: camelCase (JS) / snake_case (Python)
```javascript
// ✅ JavaScript
const userName = 'Alice'
const fetchUserData = () => {}

// ❌ JavaScript
const user_name = 'Alice'
const FetchUserData = () => {}
```

```python
# ✅ Python
user_name = 'Alice'
def fetch_user_data():
    pass

# ❌ Python
userName = 'Alice'
def fetchUserData():
    pass
```

---

### 📝 提交规范

采用 [Conventional Commits](https://www.conventionalcommits.org/) 规范

#### 提交消息格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Type类型**:
- `feat`: 新功能
- `fix`: Bug修复
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构（既非新增功能也非修复Bug）
- `perf`: 性能优化
- `test`: 增加测试
- `chore`: 构建工具、依赖更新

**Scope范围**:
- `frontend`: 前端相关
- `backend`: 后端相关
- `api`: API接口
- `ui`: UI组件
- `docs`: 文档
- `deps`: 依赖

**示例**:

```bash
# 新功能
git commit -m "feat(frontend): add date range picker component"

# Bug修复
git commit -m "fix(backend): resolve NaN issue in KPI calculation"

# 文档更新
git commit -m "docs: update API reference for /api/kpi-windows"

# 重构
git commit -m "refactor(ui): extract chart config into utils"

# 多行提交消息
git commit -m "feat(api): add data export endpoint

- Support CSV and Excel formats
- Add date range filtering
- Include error handling for large datasets

Closes #42"
```

#### ❌ 不好的提交消息

```bash
git commit -m "update"
git commit -m "fix bug"
git commit -m "WIP"
git commit -m "修复了一个问题"
```

---

### 🔀 Pull Request流程

#### 1. 更新你的分支

```bash
# 拉取上游最新代码
git fetch upstream
git rebase upstream/main

# 解决冲突（如果有）
git add .
git rebase --continue

# 强制推送到你的Fork
git push origin feature/your-feature --force
```

#### 2. 创建Pull Request

**标题格式**: 与提交消息一致
```
feat(frontend): add date range picker component
```

**描述模板**:
```markdown
## 📋 变更说明

**关联Issue**: Closes #42

**变更类型**:
- [ ] 🐛 Bug修复
- [x] ✨ 新功能
- [ ] 📝 文档更新
- [ ] 🔨 重构

## 🎯 变更内容

- 新增日期范围选择器组件 (DateRangePicker.vue)
- 集成到Dashboard筛选面板
- 添加日期验证逻辑

## 🧪 测试计划

- [x] 手动测试日期选择功能
- [x] 测试无效日期输入处理
- [ ] 添加单元测试（待补充）

## 📸 截图

[附件: date-picker-screenshot.png]

## ⚠️ 破坏性变更

无

## 📝 检查清单

- [x] 代码遵循项目规范
- [x] 提交消息符合Conventional Commits
- [x] 已更新相关文档
- [x] 已手动测试功能
- [ ] 已添加单元测试（未来要求）
```

#### 3. Code Review

**维护者将检查**:
- 代码质量和规范
- 功能完整性
- 测试覆盖率（未来）
- 文档完整性
- 无破坏性变更（或已标注）

**贡献者需要**:
- 及时响应Review意见
- 修改后更新PR
- 保持PR聚焦单一功能

#### 4. 合并

满足以下条件后合并：
- ✅ 所有Review意见已解决
- ✅ CI/CD检查通过（未来）
- ✅ 至少1名维护者批准
- ✅ 无冲突

---

### 🧪 测试要求

#### 当前阶段（v2.0）

**手动测试即可**，需确保：
- 功能正常工作
- 无控制台错误
- 跨浏览器兼容（Chrome/Firefox/Safari）

#### 未来要求（v2.1+）

**前端单元测试** (Vitest):
```javascript
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import KpiCard from '@/components/KpiCard.vue'

describe('KpiCard', () => {
  it('renders title correctly', () => {
    const wrapper = mount(KpiCard, {
      props: { title: '签单保费', value: 200000 }
    })
    expect(wrapper.text()).toContain('签单保费')
  })
})
```

**后端单元测试** (pytest):
```python
def test_get_kpi_data():
    """测试KPI数据获取"""
    result = get_kpi_data('2025-11-05')
    assert 'premium' in result
    assert result['premium']['day'] > 0
```

---

## English Version

### 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute](#how-can-i-contribute)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Testing Requirements](#testing-requirements)

---

### 🤗 Code of Conduct

By participating in this project, you agree to abide by our code of conduct:

- ✅ **Be Respectful** - Embrace diverse perspectives and experiences
- ✅ **Constructive Feedback** - Critique code, not people
- ✅ **Collaborative Spirit** - Seek consensus, not confrontation
- ✅ **Professional Attitude** - Maintain friendly, professional communication
- ❌ **Zero Tolerance** - No harassment, discrimination, or offensive behavior

---

### 💡 How Can I Contribute

#### 🐛 Reporting Bugs

**Steps**:
1. Check [Issues](https://github.com/your-repo/issues) to avoid duplicates
2. Create an issue using the Bug template
3. Include detailed information:
   - Reproduction steps
   - Expected vs actual behavior
   - Environment info (browser, OS, Node/Python version)
   - Screenshots or error logs

**Example**:
```markdown
**Bug Description**: KPI card displays NaN after data refresh

**Steps to Reproduce**:
1. Visit http://localhost:3000
2. Click "Refresh Data" button
3. Premium card shows NaN

**Expected Behavior**: Should display number like "205,000"

**Environment**:
- Browser: Chrome 120.0
- OS: macOS 14.0
- Node: v18.17.0
```

#### ✨ Suggesting Features

**Steps**:
1. Start a [Discussion](https://github.com/your-repo/discussions) to explore feasibility
2. After maintainer approval, create Feature Request issue
3. Include: user story, business value, UI mockups (if any)

#### 📝 Improving Documentation

Welcome documentation contributions:
- Fix typos and grammar errors
- Add usage examples
- Translate docs (Chinese/English)
- Expand FAQ

**Submission**: Direct Pull Request

#### 🔧 Contributing Code

See [Development Workflow](#development-workflow)

---

### 🛠️ Development Workflow

#### 1. Fork and Clone

```bash
# Fork the repository to your GitHub account
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/daylyreport.git
cd daylyreport

# Add upstream remote
git remote add upstream https://github.com/original-owner/daylyreport.git
```

#### 2. Create Branch

**Branch naming convention**:
```bash
# New feature
git checkout -b feature/date-range-picker

# Bug fix
git checkout -b fix/kpi-card-nan-issue

# Documentation
git checkout -b docs/update-api-reference

# Refactoring
git checkout -b refactor/optimize-chart-rendering
```

#### 3. Install Dependencies

```bash
# Frontend dependencies
npm install

# Backend dependencies (recommended: use virtual environment)
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

#### 4. Develop

```bash
# Terminal 1: Start frontend dev server
npm run dev
# Visit http://localhost:5173

# Terminal 2: Start backend API server
cd backend
python api_server.py
# API at http://localhost:5001
```

#### 5. Test

```bash
# Frontend tests (future)
npm run test
npm run test:e2e

# Backend tests (future)
pytest backend/tests/
```

#### 6. Commit

See [Commit Guidelines](#commit-guidelines)

---

### 📐 Coding Standards

#### Frontend (Vue 3)

**Component Naming**: PascalCase
```vue
<!-- ✅ Correct -->
<KpiCard />
<DateRangePicker />

<!-- ❌ Incorrect -->
<kpiCard />
<date-range-picker />
```

**Props Definition**: Must include type and default
```javascript
// ✅ Correct
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

// ❌ Incorrect
const props = defineProps(['title', 'value'])
```

#### Backend (Flask)

**Function Documentation**: Google-style docstrings
```python
# ✅ Correct
def get_kpi_data(date: str = None) -> dict:
    """Retrieve KPI data for three time windows

    Args:
        date: Query date in YYYY-MM-DD format, defaults to latest

    Returns:
        Dictionary containing premium/policy_count/commission

    Raises:
        ValueError: If date format is invalid
    """
    pass
```

**Type Hints**: Required for all public functions
```python
# ✅ Correct
def process_data(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    pass

# ❌ Incorrect
def process_data(df, filters):
    pass
```

---

### 📝 Commit Guidelines

Follow [Conventional Commits](https://www.conventionalcommits.org/) specification

#### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation update
- `style`: Code formatting (no functional change)
- `refactor`: Code refactoring (neither feature nor fix)
- `perf`: Performance optimization
- `test`: Add tests
- `chore`: Build tools, dependency updates

**Scopes**:
- `frontend`: Frontend-related
- `backend`: Backend-related
- `api`: API endpoints
- `ui`: UI components
- `docs`: Documentation
- `deps`: Dependencies

**Examples**:

```bash
# New feature
git commit -m "feat(frontend): add date range picker component"

# Bug fix
git commit -m "fix(backend): resolve NaN issue in KPI calculation"

# Documentation
git commit -m "docs: update API reference for /api/kpi-windows"

# Multi-line commit
git commit -m "feat(api): add data export endpoint

- Support CSV and Excel formats
- Add date range filtering
- Include error handling for large datasets

Closes #42"
```

---

### 🔀 Pull Request Process

#### 1. Update Your Branch

```bash
# Fetch latest upstream code
git fetch upstream
git rebase upstream/main

# Resolve conflicts (if any)
git add .
git rebase --continue

# Force push to your fork
git push origin feature/your-feature --force
```

#### 2. Create Pull Request

**Title Format**: Same as commit message
```
feat(frontend): add date range picker component
```

**Description Template**:
```markdown
## 📋 Changes

**Related Issue**: Closes #42

**Change Type**:
- [ ] 🐛 Bug fix
- [x] ✨ New feature
- [ ] 📝 Documentation
- [ ] 🔨 Refactoring

## 🎯 What Changed

- Added DateRangePicker component
- Integrated into Dashboard filter panel
- Added date validation logic

## 🧪 Testing

- [x] Manual testing of date selection
- [x] Tested invalid date input handling
- [ ] Added unit tests (future)

## 📸 Screenshots

[Attachment: date-picker-screenshot.png]

## ⚠️ Breaking Changes

None

## 📝 Checklist

- [x] Code follows project conventions
- [x] Commit messages follow Conventional Commits
- [x] Documentation updated
- [x] Manually tested
- [ ] Unit tests added (future requirement)
```

#### 3. Code Review

**Maintainers will check**:
- Code quality and conventions
- Feature completeness
- Test coverage (future)
- Documentation completeness
- No breaking changes (or properly marked)

**Contributors should**:
- Respond to review comments promptly
- Update PR after making changes
- Keep PR focused on single feature

#### 4. Merge

PR will be merged when:
- ✅ All review comments resolved
- ✅ CI/CD checks pass (future)
- ✅ At least 1 maintainer approval
- ✅ No conflicts

---

### 🧪 Testing Requirements

#### Current Stage (v2.0)

**Manual testing is sufficient**, ensure:
- Functionality works as expected
- No console errors
- Cross-browser compatibility (Chrome/Firefox/Safari)

#### Future Requirements (v2.1+)

**Frontend Unit Tests** (Vitest):
```javascript
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import KpiCard from '@/components/KpiCard.vue'

describe('KpiCard', () => {
  it('renders title correctly', () => {
    const wrapper = mount(KpiCard, {
      props: { title: 'Premium', value: 200000 }
    })
    expect(wrapper.text()).toContain('Premium')
  })
})
```

**Backend Unit Tests** (pytest):
```python
def test_get_kpi_data():
    """Test KPI data retrieval"""
    result = get_kpi_data('2025-11-05')
    assert 'premium' in result
    assert result['premium']['day'] > 0
```

---

## 📞 联系方式 - Contact

- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)
- **Email**: tech-support@example.com

---

<div align="center">

**感谢您的贡献！Thank you for contributing!**

Made with ❤️ by the community

</div>
