# 设计系统 - 车险签单数据分析平台 v2.0

**文档版本**: 1.0
**更新日期**: 2025-11-07
**设计师**: AI Assistant
**状态**: 设计完成，待实施

---

## 目录

1. [概述](#1-概述)
2. [设计原则](#2-设计原则)
3. [色彩系统](#3-色彩系统)
4. [字体系统](#4-字体系统)
5. [间距系统](#5-间距系统)
6. [组件库](#6-组件库)
7. [图标系统](#7-图标系统)
8. [动画规范](#8-动画规范)
9. [响应式设计](#9-响应式设计)
10. [无障碍设计](#10-无障碍设计)
11. [暗色模式](#11-暗色模式)

---

## 1. 概述

### 1.1 设计系统定位

本设计系统为**车险签单数据分析平台v2.0**提供统一的视觉语言和交互规范，确保：

- **一致性**: 所有页面/组件风格统一
- **高效性**: 设计师和开发者快速协作
- **可维护性**: 易于扩展和修改
- **可访问性**: 符合WCAG 2.1 AA标准

### 1.2 设计灵感

- **主题**: 现代商务 + 数据可视化
- **风格**: Material Design 3 + 渐变美学
- **色调**: 紫色系（专业、科技、信任）
- **参考**: Ant Design, Material UI, Tailwind CSS

### 1.3 设计工具

- **原型工具**: Figma / Sketch
- **配色工具**: Coolors, Adobe Color
- **图标库**: Heroicons, Material Icons
- **字体**: Inter, PingFang SC

---

## 2. 设计原则

### 2.1 核心原则

#### 1. 清晰 (Clarity)

- 信息层级分明，主次清晰
- 避免过度装饰，专注数据展示
- 使用适当的对比度和留白

#### 2. 一致 (Consistency)

- 统一的颜色、字体、间距
- 相同功能使用相同交互模式
- 遵循用户心智模型

#### 3. 高效 (Efficiency)

- 减少用户操作步骤
- 关键信息一屏展示
- 快速加载和响应

#### 4. 美观 (Aesthetics)

- 渐变色彩增强视觉层次
- 柔和的阴影和圆角
- 流畅的动画过渡

#### 5. 包容 (Inclusive)

- 支持多种屏幕尺寸
- 无障碍访问（键盘、屏幕阅读器）
- 色盲友好的配色

### 2.2 数据可视化原则

1. **准确性**: 数据表达必须准确，避免误导
2. **简洁性**: 去除图表杂音（Chart Junk）
3. **对比性**: 使用颜色和大小强调重点数据
4. **上下文**: 提供充分的图例和标签
5. **交互性**: 支持悬停、缩放、筛选

---

## 3. 色彩系统

### 3.1 主色调 (Primary Colors)

#### 紫色渐变（品牌主色）

```css
/* CSS变量定义 */
:root {
  /* 主紫色 */
  --primary-50:  #FAF5FF;
  --primary-100: #F3E8FF;
  --primary-200: #E9D5FF;
  --primary-300: #D8B4FE;
  --primary-400: #C084FC;
  --primary-500: #A855F7;  /* 基准色 */
  --primary-600: #9333EA;
  --primary-700: #7E22CE;
  --primary-800: #6B21A8;
  --primary-900: #581C87;

  /* 渐变 */
  --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  --gradient-primary-hover: linear-gradient(135deg, #5568d3 0%, #663d8f 100%);
}
```

**使用场景**:
- 按钮背景、进度条
- KPI卡片边框强调
- 图表主色
- 链接和高亮

**示例**:
```vue
<button class="btn-primary">刷新数据</button>
<div class="kpi-card" style="border-left: 4px solid var(--primary-500)"></div>
```

---

### 3.2 功能色 (Semantic Colors)

#### 成功色（绿色）

```css
:root {
  --success-50:  #F0FDF4;
  --success-100: #DCFCE7;
  --success-500: #10B981;  /* 基准色 */
  --success-700: #047857;
}
```

**使用场景**: 数据上升、目标达成、成功提示

#### 警告色（橙色）

```css
:root {
  --warning-50:  #FFFBEB;
  --warning-100: #FEF3C7;
  --warning-500: #F59E0B;  /* 基准色 */
  --warning-700: #B45309;
}
```

**使用场景**: 接近目标、需要注意的指标

#### 错误色（红色）

```css
:root {
  --error-50:  #FEF2F2;
  --error-100: #FEE2E2;
  --error-500: #EF4444;  /* 基准色 */
  --error-700: #B91C1C;
}
```

**使用场景**: 数据下降、错误提示、删除操作

#### 信息色（蓝色）

```css
:root {
  --info-50:  #EFF6FF;
  --info-100: #DBEAFE;
  --info-500: #3B82F6;  /* 基准色 */
  --info-700: #1D4ED8;
}
```

**使用场景**: 提示信息、帮助文档、中性通知

---

### 3.3 中性色 (Neutral Colors)

```css
:root {
  /* 灰度 */
  --gray-50:  #F9FAFB;
  --gray-100: #F3F4F6;
  --gray-200: #E5E7EB;
  --gray-300: #D1D5DB;
  --gray-400: #9CA3AF;
  --gray-500: #6B7280;
  --gray-600: #4B5563;
  --gray-700: #374151;
  --gray-800: #1F2937;
  --gray-900: #111827;

  /* 语义化别名 */
  --text-primary:   var(--gray-900);  /* 主要文本 */
  --text-secondary: var(--gray-600);  /* 次要文本 */
  --text-disabled:  var(--gray-400);  /* 禁用文本 */
  --text-inverse:   #FFFFFF;          /* 反色文本（深色背景） */

  --bg-primary:     #FFFFFF;          /* 主背景 */
  --bg-secondary:   var(--gray-50);   /* 次背景 */
  --bg-tertiary:    var(--gray-100);  /* 三级背景 */

  --border-light:   var(--gray-200);  /* 浅边框 */
  --border-medium:  var(--gray-300);  /* 中边框 */
  --border-dark:    var(--gray-400);  /* 深边框 */
}
```

**使用场景**:
- 文本颜色（标题、正文、提示）
- 背景颜色（卡片、面板、输入框）
- 边框和分割线

---

### 3.4 图表配色

#### 柱状图/折线图配色

```css
:root {
  /* 3色组合（最近、上周、前周） */
  --chart-color-1: #667eea;  /* 主紫 */
  --chart-color-2: #f093fb;  /* 粉紫 */
  --chart-color-3: #4facfe;  /* 亮蓝 */

  /* 5色组合（多维度对比） */
  --chart-palette-1: #667eea;
  --chart-palette-2: #f093fb;
  --chart-palette-3: #4facfe;
  --chart-palette-4: #43e97b;
  --chart-palette-5: #fa709a;

  /* 8色组合（机构对比） */
  --chart-palette: [
    '#667eea', '#f093fb', '#4facfe', '#43e97b',
    '#fa709a', '#feca57', '#ff6b6b', '#a29bfe'
  ];
}
```

**ECharts配置示例**:

```javascript
const chartColors = [
  '#667eea', '#f093fb', '#4facfe', '#43e97b'
]

const option = {
  color: chartColors,
  series: [
    {
      type: 'bar',
      itemStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: '#667eea' },
          { offset: 1, color: '#764ba2' }
        ])
      }
    }
  ]
}
```

#### 热力图配色

```css
:root {
  --heatmap-cold:   #4facfe;  /* 低值 - 蓝色 */
  --heatmap-medium: #f093fb;  /* 中值 - 紫色 */
  --heatmap-hot:    #fa709a;  /* 高值 - 粉色 */
}
```

---

### 3.5 颜色使用规范

#### 对比度要求（WCAG 2.1 AA）

| 文本大小 | 最小对比度 | 示例 |
|---------|-----------|------|
| 正文（<18px） | 4.5:1 | `gray-900` on `white` ✅ |
| 大文本（≥18px） | 3:1 | `gray-700` on `white` ✅ |
| UI元素 | 3:1 | `primary-500` on `white` ✅ |

**工具**: [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)

#### 颜色搭配禁忌

❌ **避免**:
- 红色 + 绿色（色盲不友好）
- 纯黑 `#000000` 文本（过于刺眼）
- 低对比度组合（如浅灰on白底）

✅ **推荐**:
- 深灰 `#1F2937` 替代纯黑
- 蓝色 + 橙色（对比鲜明）
- 紫色 + 绿色（互补色）

---

## 4. 字体系统

### 4.1 字体家族

#### 主字体（西文）

```css
:root {
  --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI",
               "Helvetica Neue", Arial, sans-serif;
}
```

**特点**: 系统字体栈，跨平台一致性

#### 主字体（中文）

```css
:root {
  --font-zh: "PingFang SC", "Microsoft YaHei",
             "微软雅黑", "Hiragino Sans GB", sans-serif;
}
```

**特点**: macOS/iOS用苹方，Windows用微软雅黑

#### 等宽字体（数字/代码）

```css
:root {
  --font-mono: "SF Mono", "Consolas", "Monaco",
               "Courier New", monospace;
}
```

**使用场景**: 保单号、数据表格、代码块

---

### 4.2 字号体系

采用**1.25倍**增长比例（Major Third Scale）

```css
:root {
  --text-xs:   0.75rem;  /* 12px */
  --text-sm:   0.875rem; /* 14px */
  --text-base: 1rem;     /* 16px - 基准 */
  --text-lg:   1.125rem; /* 18px */
  --text-xl:   1.25rem;  /* 20px */
  --text-2xl:  1.5rem;   /* 24px */
  --text-3xl:  1.875rem; /* 30px */
  --text-4xl:  2.25rem;  /* 36px */
  --text-5xl:  3rem;     /* 48px */
}
```

**使用场景**:

| 字号 | 使用场景 | 示例 |
|------|---------|------|
| `text-xs` | 辅助说明、时间戳 | "最后更新: 2分钟前" |
| `text-sm` | 次要信息、表单标签 | 筛选器标签 |
| `text-base` | 正文、按钮 | 正文段落 |
| `text-lg` | 小标题、强调文本 | 卡片标题 |
| `text-xl` | 二级标题 | 区块标题 |
| `text-2xl` | 一级标题 | 页面标题 |
| `text-3xl` | KPI数值 | 签单保费数值 |
| `text-4xl` | 首屏大标题 | Dashboard标题 |

---

### 4.3 字重体系

```css
:root {
  --font-light:      300;
  --font-normal:     400;
  --font-medium:     500;
  --font-semibold:   600;
  --font-bold:       700;
  --font-extrabold:  800;
}
```

**使用规范**:
- `normal (400)`: 正文
- `medium (500)`: 次要标题
- `semibold (600)`: 主要标题
- `bold (700)`: 数据强调（KPI数值）

---

### 4.4 行高体系

```css
:root {
  --leading-none:   1;      /* 紧密 - 数字 */
  --leading-tight:  1.25;   /* 紧凑 - 标题 */
  --leading-snug:   1.375;
  --leading-normal: 1.5;    /* 正常 - 正文 */
  --leading-relaxed: 1.625;
  --leading-loose:  2;      /* 松散 - 长文 */
}
```

**最佳实践**:
- 标题: `leading-tight (1.25)`
- 正文: `leading-normal (1.5)`
- 长文: `leading-relaxed (1.625)`

---

### 4.5 字体样式示例

```vue
<template>
  <!-- 页面标题 -->
  <h1 class="text-4xl font-bold text-primary leading-tight">
    车险签单数据分析平台
  </h1>

  <!-- 区块标题 -->
  <h2 class="text-2xl font-semibold text-gray-900 leading-tight">
    本周签单趋势
  </h2>

  <!-- KPI数值 -->
  <div class="text-3xl font-bold text-gray-900 leading-none font-mono">
    205,000
  </div>

  <!-- 正文 -->
  <p class="text-base text-gray-700 leading-normal">
    当前筛选条件: 成都地区，新能源车
  </p>

  <!-- 辅助文本 -->
  <span class="text-sm text-gray-500">
    最后更新: 2025-11-07 14:30
  </span>
</template>
```

---

## 5. 间距系统

### 5.1 间距比例

采用**4px基准**的8点网格系统

```css
:root {
  --space-0:  0;
  --space-1:  0.25rem;  /* 4px */
  --space-2:  0.5rem;   /* 8px */
  --space-3:  0.75rem;  /* 12px */
  --space-4:  1rem;     /* 16px - 基准 */
  --space-5:  1.25rem;  /* 20px */
  --space-6:  1.5rem;   /* 24px */
  --space-8:  2rem;     /* 32px */
  --space-10: 2.5rem;   /* 40px */
  --space-12: 3rem;     /* 48px */
  --space-16: 4rem;     /* 64px */
  --space-20: 5rem;     /* 80px */
  --space-24: 6rem;     /* 96px */
}
```

---

### 5.2 组件内间距

```css
/* 按钮 */
.btn {
  padding: var(--space-2) var(--space-6); /* 8px 24px */
}

.btn-sm {
  padding: var(--space-1) var(--space-4); /* 4px 16px */
}

.btn-lg {
  padding: var(--space-3) var(--space-8); /* 12px 32px */
}

/* 卡片 */
.card {
  padding: var(--space-6); /* 24px */
}

.card-compact {
  padding: var(--space-4); /* 16px */
}

/* 输入框 */
.input {
  padding: var(--space-2) var(--space-3); /* 8px 12px */
}
```

---

### 5.3 布局间距

```css
/* 栅格间距 */
.grid {
  gap: var(--space-6); /* 24px */
}

.grid-tight {
  gap: var(--space-4); /* 16px */
}

.grid-loose {
  gap: var(--space-8); /* 32px */
}

/* 垂直节奏 */
.section {
  margin-bottom: var(--space-8); /* 32px */
}

.section-lg {
  margin-bottom: var(--space-12); /* 48px */
}
```

---

### 5.4 响应式间距

```css
/* 移动端缩小间距 */
@media (max-width: 768px) {
  .card {
    padding: var(--space-4); /* 24px → 16px */
  }

  .section {
    margin-bottom: var(--space-6); /* 32px → 24px */
  }
}
```

---

## 6. 组件库

### 6.1 按钮 (Button)

#### 主按钮

```vue
<button class="btn btn-primary">
  刷新数据
</button>

<style scoped>
.btn {
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary {
  background: var(--gradient-primary);
  color: white;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
}

.btn-primary:active {
  transform: translateY(0);
}
</style>
```

#### 次要按钮

```vue
<button class="btn btn-secondary">
  重置筛选
</button>

<style scoped>
.btn-secondary {
  background: white;
  color: var(--gray-700);
  border: 2px solid var(--gray-300);
}

.btn-secondary:hover {
  border-color: var(--primary-500);
  color: var(--primary-600);
}
</style>
```

#### 文本按钮

```vue
<button class="btn btn-text">
  查看详情
</button>

<style scoped>
.btn-text {
  background: transparent;
  color: var(--primary-600);
  padding: 8px 16px;
}

.btn-text:hover {
  background: var(--primary-50);
}
</style>
```

---

### 6.2 KPI卡片 (KpiCard)

```vue
<template>
  <div class="kpi-card">
    <div class="kpi-icon">📊</div>
    <div class="kpi-content">
      <div class="kpi-label">签单总保费</div>
      <div class="kpi-value">20.5万</div>
      <div class="kpi-trend kpi-trend--up">
        ↑ 12.5%
      </div>
    </div>
  </div>
</template>

<style scoped>
.kpi-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  border-left: 4px solid var(--primary-500);
}

.kpi-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.kpi-icon {
  font-size: 48px;
  line-height: 1;
}

.kpi-label {
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: 8px;
}

.kpi-value {
  font-size: 36px;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1;
  margin-bottom: 8px;
  font-family: var(--font-mono);
}

.kpi-trend {
  font-size: 14px;
  font-weight: 600;
}

.kpi-trend--up {
  color: var(--success-500);
}

.kpi-trend--down {
  color: var(--error-500);
}

.kpi-trend--neutral {
  color: var(--text-secondary);
}
</style>
```

---

### 6.3 Toast通知

```vue
<template>
  <Transition name="toast">
    <div v-if="visible" :class="['toast', `toast--${type}`]">
      <div class="toast-icon">{{ icons[type] }}</div>
      <div class="toast-content">
        <div class="toast-title">{{ title }}</div>
        <div v-if="message" class="toast-message">{{ message }}</div>
      </div>
      <button class="toast-close" @click="close">×</button>
    </div>
  </Transition>
</template>

<style scoped>
.toast {
  position: fixed;
  top: 20px;
  right: 20px;
  min-width: 320px;
  max-width: 480px;
  background: white;
  border-radius: 12px;
  padding: 16px 20px;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  z-index: 9999;
}

.toast--success {
  border-left: 4px solid var(--success-500);
}

.toast--error {
  border-left: 4px solid var(--error-500);
}

.toast--warning {
  border-left: 4px solid var(--warning-500);
}

.toast--info {
  border-left: 4px solid var(--info-500);
}

.toast-icon {
  font-size: 24px;
  line-height: 1;
}

.toast-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.toast-message {
  font-size: 14px;
  color: var(--text-secondary);
}

.toast-close {
  margin-left: auto;
  background: transparent;
  border: none;
  font-size: 24px;
  color: var(--text-secondary);
  cursor: pointer;
  line-height: 1;
  padding: 0;
}

.toast-close:hover {
  color: var(--text-primary);
}

/* 动画 */
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  transform: translateX(100%);
  opacity: 0;
}

.toast-leave-to {
  transform: translateY(-20px);
  opacity: 0;
}
</style>
```

---

### 6.4 筛选面板

```vue
<template>
  <div class="filter-panel">
    <div class="filter-header">
      <h3>数据筛选</h3>
      <button class="btn-text" @click="reset">重置</button>
    </div>

    <div class="filter-tags" v-if="activeTags.length">
      <span v-for="tag in activeTags" :key="tag" class="filter-tag">
        {{ tag }}
        <button @click="removeTag(tag)">×</button>
      </span>
    </div>

    <div class="filter-grid">
      <div class="filter-item">
        <label>三级机构</label>
        <select v-model="filters.institution">
          <option value="">全部</option>
          <option value="成都">成都</option>
          <option value="绵阳">绵阳</option>
        </select>
      </div>

      <!-- 更多筛选项... -->
    </div>

    <button class="btn btn-primary" @click="apply">
      应用筛选
    </button>
  </div>
</template>

<style scoped>
.filter-panel {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.filter-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}

.filter-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  background: var(--primary-50);
  color: var(--primary-700);
  border-radius: 16px;
  font-size: 14px;
}

.filter-tag button {
  background: transparent;
  border: none;
  color: var(--primary-700);
  cursor: pointer;
  font-size: 18px;
  line-height: 1;
  padding: 0;
}

.filter-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 20px;
}

.filter-item label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: 8px;
}

.filter-item select {
  width: 100%;
  padding: 10px 12px;
  border: 2px solid var(--border-light);
  border-radius: 8px;
  font-size: 14px;
  color: var(--text-primary);
  background: white;
  cursor: pointer;
  transition: border-color 0.2s;
}

.filter-item select:hover {
  border-color: var(--primary-300);
}

.filter-item select:focus {
  outline: none;
  border-color: var(--primary-500);
  box-shadow: 0 0 0 3px var(--primary-50);
}
</style>
```

---

## 7. 图标系统

### 7.1 图标库选择

推荐使用 **Heroicons** 或 **Material Icons**

```bash
npm install @heroicons/vue
```

### 7.2 图标使用示例

```vue
<script setup>
import { ArrowPathIcon, FunnelIcon, CheckCircleIcon } from '@heroicons/vue/24/outline'
</script>

<template>
  <!-- 刷新按钮 -->
  <button class="btn-icon">
    <ArrowPathIcon class="icon" />
  </button>

  <!-- 筛选器 -->
  <FunnelIcon class="icon-sm" />

  <!-- 成功提示 -->
  <CheckCircleIcon class="icon-success" />
</template>

<style scoped>
.icon {
  width: 20px;
  height: 20px;
}

.icon-sm {
  width: 16px;
  height: 16px;
}

.icon-success {
  width: 24px;
  height: 24px;
  color: var(--success-500);
}
</style>
```

### 7.3 自定义图标

```vue
<!-- 保费图标 -->
<svg class="icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-width="2"/>
  <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="2"/>
  <path d="M2 12L12 17L12 22" stroke="currentColor" stroke-width="2"/>
</svg>
```

---

## 8. 动画规范

### 8.1 过渡时间

```css
:root {
  --duration-fast:   150ms;  /* 快速交互 */
  --duration-base:   200ms;  /* 基础过渡 */
  --duration-slow:   300ms;  /* 复杂动画 */
  --duration-slower: 500ms;  /* 页面切换 */
}
```

### 8.2 缓动函数

```css
:root {
  --ease-in:     cubic-bezier(0.4, 0, 1, 1);
  --ease-out:    cubic-bezier(0, 0, 0.2, 1);
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);
}
```

### 8.3 常用动画

#### Hover悬停

```css
.btn {
  transition: all var(--duration-base) var(--ease-out);
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
}
```

#### 淡入淡出

```vue
<Transition name="fade">
  <div v-if="visible">内容</div>
</Transition>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity var(--duration-base) var(--ease-out);
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
```

#### 滑入滑出

```vue
<Transition name="slide">
  <div v-if="visible">侧边栏</div>
</Transition>

<style>
.slide-enter-active,
.slide-leave-active {
  transition: transform var(--duration-slow) var(--ease-in-out);
}

.slide-enter-from {
  transform: translateX(-100%);
}

.slide-leave-to {
  transform: translateX(100%);
}
</style>
```

#### Skeleton加载

```css
@keyframes skeleton-loading {
  0% {
    background-position: -200px 0;
  }
  100% {
    background-position: calc(200px + 100%) 0;
  }
}

.skeleton {
  background: linear-gradient(
    90deg,
    var(--gray-200) 0%,
    var(--gray-100) 50%,
    var(--gray-200) 100%
  );
  background-size: 200px 100%;
  animation: skeleton-loading 1.5s ease-in-out infinite;
}
```

---

## 9. 响应式设计

### 9.1 断点系统

```css
:root {
  --breakpoint-xs: 320px;   /* 小手机 */
  --breakpoint-sm: 640px;   /* 手机 */
  --breakpoint-md: 768px;   /* 平板 */
  --breakpoint-lg: 1024px;  /* 小笔记本 */
  --breakpoint-xl: 1280px;  /* 桌面 */
  --breakpoint-2xl: 1536px; /* 大屏 */
}
```

### 9.2 移动端优先

```css
/* 基础样式（移动端） */
.container {
  padding: var(--space-4);
}

/* 平板及以上 */
@media (min-width: 768px) {
  .container {
    padding: var(--space-6);
  }
}

/* 桌面及以上 */
@media (min-width: 1024px) {
  .container {
    padding: var(--space-8);
    max-width: 1400px;
    margin: 0 auto;
  }
}
```

### 9.3 响应式组件

#### KPI卡片栅格

```vue
<style scoped>
.kpi-grid {
  display: grid;
  grid-template-columns: 1fr; /* 移动端单列 */
  gap: var(--space-4);
}

@media (min-width: 640px) {
  .kpi-grid {
    grid-template-columns: repeat(2, 1fr); /* 平板2列 */
  }
}

@media (min-width: 1024px) {
  .kpi-grid {
    grid-template-columns: repeat(4, 1fr); /* 桌面4列 */
    gap: var(--space-6);
  }
}
</style>
```

#### 响应式字体

```css
.hero-title {
  font-size: clamp(24px, 5vw, 48px);
}
```

---

## 10. 无障碍设计

### 10.1 键盘导航

```vue
<button
  class="btn"
  @click="handleClick"
  @keydown.enter="handleClick"
  @keydown.space.prevent="handleClick"
>
  操作
</button>
```

### 10.2 ARIA属性

```vue
<div
  role="button"
  tabindex="0"
  :aria-label="label"
  :aria-pressed="active"
>
  {{ text }}
</div>
```

### 10.3 焦点样式

```css
button:focus-visible {
  outline: 2px solid var(--primary-500);
  outline-offset: 2px;
}
```

---

## 11. 暗色模式（未来）

```css
/* 亮色模式（默认） */
:root {
  --bg-primary: #FFFFFF;
  --text-primary: #111827;
}

/* 暗色模式 */
:root[data-theme="dark"] {
  --bg-primary: #1F2937;
  --text-primary: #F9FAFB;
  --primary-500: #A78BFA; /* 调整为更柔和的紫色 */
}
```

---

## 附录

### A. 完整CSS变量表

```css
/* variables.css */
:root {
  /* 颜色 */
  --primary-500: #A855F7;
  --success-500: #10B981;
  --warning-500: #F59E0B;
  --error-500: #EF4444;
  --info-500: #3B82F6;

  /* 字体 */
  --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  --text-base: 1rem;

  /* 间距 */
  --space-4: 1rem;
  --space-6: 1.5rem;

  /* 动画 */
  --duration-base: 200ms;
  --ease-out: cubic-bezier(0, 0, 0.2, 1);

  /* 断点 */
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
}
```

### B. 设计资源

- **Figma设计稿**: `figma.com/file/your-design`
- **图标库**: [Heroicons](https://heroicons.com/)
- **配色工具**: [Coolors](https://coolors.co/)
- **字体**: [Google Fonts](https://fonts.google.com/)

### C. 参考设计系统

- [Ant Design](https://ant.design/)
- [Material Design 3](https://m3.material.io/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Chakra UI](https://chakra-ui.com/)

---

**文档维护**: 每次UI组件更新时同步更新
**审核周期**: 每月review一次
**反馈渠道**: 设计师群/GitHub Issues
