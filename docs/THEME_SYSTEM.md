# 主题系统 - 跨平台主题解决方案

> 轻量级、高性能的网页端主题系统，支持护眼模式和暗黑模式

**适用场景**: Web应用、跨OS兼容（Windows、macOS、信创系统）
**最后更新**: 2025-11-08

---

## 🎯 快速开始

### 30秒集成

```javascript
// main.js
import { SimpleThemePlugin } from '@/themes-simple'

app.use(SimpleThemePlugin, {
  defaultMode: 'eye-care',
  enableTransitions: true
})
```

```vue
<!-- App.vue -->
<template>
  <div :data-theme-mode="currentMode">
    <ThemeModeToggle />
    <RouterView />
  </div>
</template>

<script setup>
import { useThemeSwitch } from '@/themes-simple'

const { currentMode } = useThemeSwitch()
</script>
```

---

## 🎨 主题模式

### 护眼模式 (Eye-Care Mode)

**设计理念**: 基于眼科医学研究，减少蓝光刺激

**核心特性**:
- 🛡️ 减少蓝光 - 温暖的米白色背景 `#fefcf3`
- 👁️ 降低对比度 - 避免强烈黑白对比
- 📖 增加行高 - 1.6 行高减少视觉疲劳
- 🌈 柔和色彩 - 不刺眼的颜色搭配

**颜色配置**:
```typescript
background: {
  primary: '#fefcf3',      // 温暖米白
  secondary: '#f8f4e9',    // 浅米色
  elevated: '#ffffff',     // 纯白
}
text: {
  primary: '#3a3a3a',      // 深灰（降低对比度）
  secondary: '#5a5a5a',
  muted: '#8a8a8a',
}
```

### 暗黑模式 (Dark Mode)

**设计理念**: 夜间使用，最大程度减少屏幕亮度

**核心特性**:
- 🌑 纯黑背景 - `#0d0d0d`
- 💡 高对比文字 - 确保夜间清晰可读
- 🌊 深色阴影 - 增强层次感
- 🎨 柔和色彩 - 避免过饱和颜色

**颜色配置**:
```typescript
background: {
  primary: '#0d0d0d',      // 纯黑
  secondary: '#1a1a1a',    // 近黑
  elevated: '#262626',     // 深灰
}
text: {
  primary: '#f0f0f0',      // 亮白
  secondary: '#c0c0c0',
  muted: '#909090',
}
```

---

## 🔧 API参考

### 组合式API

```typescript
// 主题切换
const { currentMode, switchMode, toggleMode } = useThemeSwitch()

// 样式获取
const { baseThemeStyles, cardStyles, buttonStyles } = useThemeStyles()

// 组件主题化
const { getButtonVariantStyles } = useComponentTheme()
```

### 完整示例

```vue
<template>
  <div class="app-container" :data-theme-mode="currentMode">
    <!-- 主题切换器 -->
    <button @click="toggleMode">
      {{ currentMode === 'eye-care' ? '🌙 切换暗黑' : '☀️ 切换护眼' }}
    </button>

    <!-- 主题化按钮 -->
    <button :style="buttonStyles">
      主题化按钮
    </button>

    <!-- 主题化卡片 -->
    <div :style="cardStyles">
      <h3>主题化卡片</h3>
    </div>
  </div>
</template>

<script setup>
import { useThemeSwitch, useThemeStyles } from '@/themes-simple'

const { currentMode, toggleMode } = useThemeSwitch()
const { buttonStyles, cardStyles } = useThemeStyles()
</script>
```

---

## ⚡ 性能优化

### 关键指标

- **包大小**: < 25KB
- **初始化时间**: < 50ms
- **内存占用**: < 1MB
- **切换性能**: < 200ms

### 优化策略

1. **CSS变量** - 避免重复样式计算
2. **智能缓存** - 主题配置本地缓存
3. **按需加载** - 只加载当前主题
4. **事件节流** - 防止频繁切换

---

## 🌐 跨OS适配

### Windows优化
```css
.windows {
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
}
```

### macOS优化
```css
.macos {
  color-profile: display-p3;
  font-family: -apple-system, 'SF Pro Display';
}
```

### 信创系统优化
```css
.linux {
  font-family: system-ui, sans-serif;
  text-rendering: optimizeSpeed;
}
```

---

## 📚 参考资源

- [完整架构文档](SIMPLE_THEME_ARCHITECTURE.md)
- [设计指南](DESIGN_GUIDE.md)
- [开发者文档](DEVELOPER_GUIDE.md)

---

**设计原则**: 够用就好，简洁高效
**适用场景**: 快速集成主题功能的项目
**技术标准**: Web标准、跨平台兼容
