<template>
  <div class="app-container" :data-theme-mode="currentMode" :data-os="osType">
    <!-- 主题切换器 -->
    <ThemeModeToggle />
    
    <!-- 主要内容 -->
    <main class="main-content">
      <!-- 页面标题 -->
      <header class="page-header">
        <div class="theme-indicator">
          <span class="mode-icon">{{ modeIcon }}</span>
          <h1 class="page-title">跨操作系统主题系统</h1>
          <p class="mode-description">{{ modeDescription }}</p>
        </div>
        <p class="os-info">当前系统: {{ osType }} | 浏览器: {{ browserInfo.name }}</p>
      </header>
      
      <!-- 主题化组件展示 -->
      <section class="demo-section">
        <h2 class="section-title">🎨 主题化组件展示</h2>
        
        <!-- 按钮组件 -->
        <div class="component-demo">
          <h3 class="demo-title">按钮组件</h3>
          <div class="button-group">
            <button 
              v-for="variant in buttonVariants" 
              :key="variant"
              :class="getButtonClass(variant)"
              :style="getButtonVariantStyles(variant)"
              @click="handleButtonClick(variant)"
            >
              {{ variant }} 按钮
            </button>
          </div>
        </div>
        
        <!-- 卡片组件 -->
        <div class="component-demo">
          <h3 class="demo-title">卡片组件</h3>
          <div class="card-grid">
            <div 
              v-for="variant in cardVariants" 
              :key="variant"
              :class="getCardClass(variant)"
              :style="getCardVariantStyles(variant)"
            >
              <h4 class="card-title">{{ variant }} 卡片</h4>
              <p class="card-content">这是一个{{ variant }}风格的卡片组件，展示了不同主题下的视觉效果。</p>
              <div class="card-footer">
                <span class="card-date">{{ currentDate }}</span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 输入框组件 -->
        <div class="component-demo">
          <h3 class="demo-title">输入框组件</h3>
          <div class="input-group">
            <input 
              v-for="state in inputStates" 
              :key="state"
              :class="getInputClass(state)"
              :style="getInputStateStyles(state)"
              :placeholder="`${state}状态输入框`"
            />
          </div>
        </div>
        
        <!-- 系统信息 -->
        <div class="component-demo">
          <h3 class="demo-title">系统信息</h3>
          <div class="info-grid">
            <div class="info-card">
              <h4>当前模式</h4>
              <p>{{ currentModeName }}</p>
            </div>
            <div class="info-card">
              <h4>系统偏好</h4>
              <p>{{ systemPreference }}</p>
            </div>
            <div class="info-card">
              <h4>性能状态</h4>
              <p>{{ performanceStatus }}</p>
            </div>
            <div class="info-card">
              <h4>颜色色域</h4>
              <p>{{ colorGamut }}</p>
            </div>
          </div>
        </div>
        
        <!-- 护眼特性说明 -->
        <div v-if="currentMode === 'eye-care'" class="eye-care-info">
          <h3 class="demo-title">🛡️ 护眼特性</h3>
          <ul class="feature-list">
            <li>✅ 减少蓝光：使用暖色调背景</li>
            <li>✅ 降低对比度：避免强烈黑白对比</li>
            <li>✅ 增加行高：减少视觉疲劳</li>
            <li>✅ 柔和色彩：使用不刺眼的颜色</li>
            <li>✅ 优化字体：系统原生字体渲染</li>
          </ul>
        </div>
        
        <!-- 暗黑特性说明 -->
        <div v-if="currentMode === 'dark'" class="dark-mode-info">
          <h3 class="demo-title">🌙 暗黑特性</h3>
          <ul class="feature-list">
            <li>✅ 纯黑背景：最大程度减少亮度</li>
            <li>✅ 高对比文字：确保清晰可读</li>
            <li>✅ 深色阴影：增强层次感</li>
            <li>✅ 柔和色彩：避免过饱和颜色</li>
            <li>✅ 系统适配：根据OS优化显示</li>
          </ul>
        </div>
      </section>
    </main>
    
    <!-- 底部信息 -->
    <footer class="app-footer">
      <p>跨操作系统主题系统 - 支持 Windows、macOS、信创系统</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { 
  useThemeSwitch, 
  useThemeIndicator, 
  useComponentTheme,
  useThemeStyles,
  useSystemPreference
} from '@/themes-simple/composables'
import ThemeModeToggle from '@/components/simple/ThemeModeToggle.vue'

// 主题系统
const { currentMode, switchMode, toggleMode } = useThemeSwitch()
const { modeIcon, modeDescription } = useThemeThemeIndicator()
const { getButtonVariantStyles, getCardVariantStyles, getInputStateStyles, getThemeClass } = useComponentTheme()
const { cardStyles, buttonStyles, inputStyles } = useThemeStyles()
const { systemPreference } = useSystemPreference()

// 组件数据
const buttonVariants = ['primary', 'secondary', 'ghost']
const cardVariants = ['elevated', 'outlined', 'flat']
const inputStates = ['normal', 'focus', 'error', 'disabled']

// 系统信息
const osType = ref('unknown')
const browserInfo = ref({ name: 'unknown', version: '0' })
const colorGamut = ref('sRGB')
const performanceStatus = ref('良好')
const currentDate = computed(() => new Date().toLocaleDateString('zh-CN'))

// 计算属性
const currentModeName = computed(() => {
  return currentMode.value === 'eye-care' ? '护眼模式' : '暗黑模式'
})

// 样式生成函数
const getButtonClass = (variant) => {
  return getThemeClass('theme-button', variant)
}

const getCardClass = (variant) => {
  return getThemeClass('theme-card', variant)
}

const getInputClass = (state) => {
  return getThemeClass('theme-input', state)
}

// 事件处理
const handleButtonClick = (variant) => {
  console.log(`点击了 ${variant} 按钮`)
  // 这里可以添加更多交互逻辑
}

// 生命周期
onMounted(async () => {
  console.log('🔧 简化主题系统已加载')
  console.log('当前模式:', currentMode.value)
  console.log('系统偏好:', systemPreference.value)
  
  // 检测系统信息
  if (navigator.userAgent) {
    const ua = navigator.userAgent.toLowerCase()
    if (ua.includes('mac')) {
      osType.value = 'macOS'
    } else if (ua.includes('win')) {
      osType.value = 'Windows'
    } else if (ua.includes('linux')) {
      osType.value = 'Linux'
    }
    
    // 浏览器检测
    if (ua.includes('chrome') || ua.includes('edg')) {
      browserInfo.value = { name: 'Chrome/Edge', version: 'latest', engine: 'Blink' }
    } else if (ua.includes('firefox')) {
      browserInfo.value = { name: 'Firefox', version: 'latest', engine: 'Gecko' }
    } else if (ua.includes('safari') && !ua.includes('chrome')) {
      browserInfo.value = { name: 'Safari', version: 'latest', engine: 'WebKit' }
    }
    
    // 色域检测
    if (window.matchMedia) {
      if (window.matchMedia('(color-gamut: p3)').matches) {
        colorGamut.value = 'P3'
      } else if (window.matchMedia('(color-gamut: rec2020)').matches) {
        colorGamut.value = 'Rec2020'
      }
    }
  }
})
</script>

<style scoped>
/* 基础主题样式 */
.app-container {
  min-height: 100vh;
  background: var(--colors-background-primary);
  color: var(--colors-text-primary);
  font-family: var(--typography-fontFamily-sans);
  transition: background-color 0.3s ease, color 0.3s ease;
}

.main-content {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

/* 页面头部 */
.page-header {
  text-align: center;
  margin-bottom: 3rem;
  padding: 2rem;
  background: var(--colors-background-secondary);
  border-radius: var(--components-card-borderRadius);
}

.theme-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.mode-icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.page-title {
  font-size: var(--typography-fontSize-2xl);
  font-weight: var(--typography-fontWeight-bold);
  margin-bottom: 0.5rem;
  color: var(--colors-text-primary);
}

.mode-description {
  font-size: var(--typography-fontSize-base);
  color: var(--colors-text-secondary);
}

.os-info {
  font-size: var(--typography-fontSize-sm);
  color: var(--colors-text-muted);
  margin-top: 1rem;
}

/* 演示区域 */
.demo-section {
  margin-bottom: 3rem;
}

.section-title {
  font-size: var(--typography-fontSize-xl);
  font-weight: var(--typography-fontWeight-semibold);
  margin-bottom: 1.5rem;
  color: var(--colors-text-primary);
  text-align: center;
}

.component-demo {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: var(--colors-background-secondary);
  border-radius: var(--components-card-borderRadius);
  box-shadow: var(--shadows-sm);
}

.demo-title {
  font-size: var(--typography-fontSize-lg);
  font-weight: var(--typography-fontWeight-medium);
  margin-bottom: 1rem;
  color: var(--colors-text-primary);
}

/* 按钮组件 */
.button-group {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.theme-button {
  border: none;
  cursor: pointer;
  outline: none;
  transition: all 0.2s ease-out;
  font-size: var(--typography-fontSize-base);
  font-weight: var(--typography-fontWeight-medium);
}

.theme-button--primary {
  background: var(--colors-accent-primary);
  color: white;
  box-shadow: var(--shadows-sm);
}

.theme-button--primary:hover {
  background: var(--colors-accent-secondary);
  transform: translateY(-1px);
  box-shadow: var(--shadows-md);
}

.theme-button--secondary {
  background: transparent;
  color: var(--colors-accent-primary);
  border: 1px solid var(--colors-accent-primary);
}

.theme-button--secondary:hover {
  background: var(--colors-accent-primary);
  color: white;
}

.theme-button--ghost {
  background: transparent;
  color: var(--colors-text-primary);
  border: 1px solid var(--colors-border-medium);
}

.theme-button--ghost:hover {
  background: var(--colors-background-secondary);
  border-color: var(--colors-accent-primary);
}

/* 卡片组件 */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.theme-card {
  transition: all 0.2s ease-out;
}

.theme-card--elevated {
  box-shadow: var(--shadows-md);
  border: none;
}

.theme-card--elevated:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadows-lg);
}

.theme-card--outlined {
  box-shadow: none;
  border: 1px solid var(--colors-border-medium);
}

.theme-card--outlined:hover {
  border-color: var(--colors-accent-primary);
}

.theme-card--flat {
  box-shadow: none;
  border: none;
}

.theme-card--flat:hover {
  background: var(--colors-background-elevated);
}

.card-title {
  font-size: var(--typography-fontSize-lg);
  font-weight: var(--typography-fontWeight-semibold);
  margin-bottom: 0.5rem;
  color: var(--colors-text-primary);
}

.card-content {
  color: var(--colors-text-secondary);
  margin-bottom: 1rem;
  line-height: var(--typography-lineHeight-normal);
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: var(--typography-fontSize-sm);
  color: var(--colors-text-muted);
}

.card-date {
  font-weight: var(--typography-fontWeight-medium);
}

/* 输入框组件 */
.input-group {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.theme-input {
  border: 1px solid var(--colors-border-medium);
  outline: none;
  font-size: var(--typography-fontSize-base);
  font-family: var(--typography-fontFamily-sans);
  transition: all 0.2s ease-out;
}

.theme-input--normal {
  border-color: var(--colors-border-medium);
}

.theme-input--normal:focus {
  border-color: var(--colors-accent-primary);
  box-shadow: 0 0 0 2px rgba(139, 115, 85, 0.2);
}

.theme-input--focus {
  border-color: var(--colors-accent-primary);
  box-shadow: 0 0 0 2px rgba(139, 115, 85, 0.2);
}

.theme-input--error {
  border-color: var(--colors-semantic-error);
  background-color: rgba(184, 106, 94, 0.1);
}

.theme-input--disabled {
  opacity: 0.6;
  cursor: not-allowed;
  background-color: var(--colors-background-secondary);
}

/* 信息网格 */
.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.info-card {
  padding: 1rem;
  background: var(--colors-background-secondary);
  border-radius: var(--components-card-borderRadius);
  text-align: center;
  border: 1px solid var(--colors-border-light);
}

.info-card h4 {
  font-size: var(--typography-fontSize-sm);
  color: var(--colors-text-secondary);
  margin-bottom: 0.5rem;
  font-weight: var(--typography-fontWeight-medium);
}

.info-card p {
  font-size: var(--typography-fontSize-lg);
  font-weight: var(--typography-fontWeight-semibold);
  color: var(--colors-text-primary);
}

/* 特性说明 */
.eye-care-info,
.dark-mode-info {
  margin-top: 2rem;
  padding: 1.5rem;
  background: var(--colors-background-secondary);
  border-radius: var(--components-card-borderRadius);
  border-left: 4px solid var(--colors-accent-primary);
}

.feature-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.feature-list li {
  padding: 0.5rem 0;
  color: var(--colors-text-secondary);
  font-size: var(--typography-fontSize-base);
  line-height: var(--typography-lineHeight-normal);
}

/* 底部信息 */
.app-footer {
  text-align: center;
  padding: 2rem;
  background: var(--colors-background-secondary);
  border-top: 1px solid var(--colors-border-light);
  margin-top: 2rem;
}

.app-footer p {
  color: var(--colors-text-muted);
  font-size: var(--typography-fontSize-sm);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .main-content {
    padding: 1rem;
  }
  
  .page-header {
    padding: 1.5rem;
  }
  
  .page-title {
    font-size: var(--typography-fontSize-xl);
  }
  
  .button-group {
    flex-direction: column;
  }
  
  .card-grid {
    grid-template-columns: 1fr;
  }
  
  .info-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* 动画优化 */
@media (prefers-reduced-motion: reduce) {
  * {
    transition-duration: 0.01ms !important;
    animation-duration: 0.01ms !important;
  }
}

/* 高对比度模式适配 */
@media (prefers-contrast: high) {
  .app-container {
    --colors-text-primary: #000000;
    --colors-text-secondary: #333333;
    --colors-border-medium: #666666;
  }
}
</style>