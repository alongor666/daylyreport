/**
 * 主题模式切换器 - 简化版
 * 提供护眼模式和暗黑模式的快速切换
 */

<template>
  <div class="theme-toggle-container">
    <!-- 主要切换按钮 -->
    <div class="main-toggle">
      <button 
        class="toggle-button"
        :class="{ 'eye-care': currentMode === 'eye-care', 'dark': currentMode === 'dark' }"
        @click="handleToggle"
        :title="toggleTitle"
        :disabled="isLoading"
      >
        <span class="toggle-icon">{{ toggleIcon }}</span>
        <span class="toggle-text">{{ toggleText }}</span>
      </button>
    </div>
    
    <!-- 模式指示器 -->
    <div class="mode-indicator">
      <div class="indicator-item" :class="{ active: currentMode === 'eye-care' }">
        <span class="indicator-icon">😊</span>
        <span class="indicator-label">护眼</span>
      </div>
      <div class="indicator-divider"></div>
      <div class="indicator-item" :class="{ active: currentMode === 'dark' }">
        <span class="indicator-icon">🌙</span>
        <span class="indicator-label">暗黑</span>
      </div>
    </div>
    
    <!-- 系统偏好显示 -->
    <div class="system-preference" v-if="showSystemPreference">
      <span class="preference-label">系统偏好:</span>
      <span class="preference-value">{{ systemPreferenceText }}</span>
    </div>
    
    <!-- 快速设置 -->
    <div class="quick-settings">
      <button 
        class="settings-button"
        :class="{ active: showSettings }"
        @click="toggleSettings"
        title="设置"
      >
        ⚙️
      </button>
      
      <transition name="settings-slide">
        <div v-if="showSettings" class="settings-panel">
          <div class="settings-group">
            <h4 class="settings-title">显示设置</h4>
            <label class="setting-item">
              <input 
                type="checkbox" 
                v-model="enableTransitions"
                @change="updateTransitions"
              />
              <span class="setting-label">启用过渡动画</span>
            </label>
            <label class="setting-item">
              <input 
                type="checkbox" 
                v-model="respectSystem"
                @change="updateSystemPreference"
              />
              <span class="setting-label">跟随系统偏好</span>
            </label>
          </div>
          
          <div class="settings-group">
            <h4 class="settings-title">性能设置</h4>
            <label class="setting-item">
              <input 
                type="checkbox" 
                v-model="enableReducedMotion"
                @change="updateReducedMotion"
              />
              <span class="setting-label">减少动画 (护眼)</span>
            </label>
          </div>
          
          <div class="settings-group">
            <h4 class="settings-title">快捷键</h4>
            <div class="shortcut-info">
              <kbd>Alt + T</kbd> 切换主题<br>
              <kbd>Alt + E</kbd> 护眼模式<br>
              <kbd>Alt + D</kbd> 暗黑模式
            </div>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useThemeSwitch, useSystemPreference } from '@/themes-simple/composables'

// 主题系统
const { currentMode, switchMode, toggleMode, isLoading } = useThemeSwitch()
const { systemPreference, respectsSystem } = useSystemPreference()

// 状态管理
const showSettings = ref(false)
const enableTransitions = ref(true)
const enableReducedMotion = ref(false)

// 计算属性
const toggleIcon = computed(() => {
  return currentMode.value === 'eye-care' ? '😊' : '🌙'
})

const toggleText = computed(() => {
  return currentMode.value === 'eye-care' ? '护眼模式' : '暗黑模式'
})

const toggleTitle = computed(() => {
  return `切换到${currentMode.value === 'eye-care' ? '暗黑' : '护眼'}模式`
})

const systemPreferenceText = computed(() => {
  return systemPreference.value === 'dark' ? '深色 🌙' : '浅色 ☀️'
})

const showSystemPreference = computed(() => {
  return respectsSystem.value && systemPreference.value !== currentMode.value
})

// 事件处理
const handleToggle = async () => {
  if (isLoading.value) return
  await toggleMode()
}

const toggleSettings = () => {
  showSettings.value = !showSettings.value
}

const updateTransitions = () => {
  document.documentElement.style.setProperty(
    '--transition-duration',
    enableTransitions.value ? '0.2s' : '0s'
  )
}

const updateSystemPreference = () => {
  // 这里可以连接到主题引擎的系统偏好设置
  console.log('系统偏好设置:', respectsSystem.value)
}

const updateReducedMotion = () => {
  document.documentElement.style.setProperty(
    '--animation-duration',
    enableReducedMotion.value ? '0.01ms' : '0.2s'
  )
}

// 键盘快捷键
const handleKeydown = (event) => {
  // Alt + T 切换主题
  if (event.altKey && event.key === 't') {
    event.preventDefault()
    toggleMode()
  }
  
  // Alt + E 护眼模式
  if (event.altKey && event.key === 'e') {
    event.preventDefault()
    switchMode('eye-care')
  }
  
  // Alt + D 暗黑模式
  if (event.altKey && event.key === 'd') {
    event.preventDefault()
    switchMode('dark')
  }
}

// 生命周期
onMounted(() => {
  document.addEventListener('keydown', handleKeydown)
  
  // 初始化设置
  enableTransitions.value = true
  enableReducedMotion.value = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  
  // 应用减少动画设置
  if (enableReducedMotion.value) {
    updateReducedMotion()
  }
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
})
</script>

<style scoped>
.theme-toggle-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1000;
  font-family: var(--typography-fontFamily-sans);
}

/* 主要切换按钮 */
.main-toggle {
  margin-bottom: 12px;
}

.toggle-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  border: 1px solid var(--colors-border-medium);
  border-radius: 12px;
  background: var(--colors-background-elevated);
  color: var(--colors-text-primary);
  cursor: pointer;
  transition: all 0.2s ease-out;
  font-size: var(--typography-fontSize-base);
  font-weight: var(--typography-fontWeight-medium);
  box-shadow: var(--shadows-sm);
  min-width: 140px;
  justify-content: center;
}

.toggle-button:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadows-md);
  border-color: var(--colors-accent-primary);
}

.toggle-button.eye-care {
  background: linear-gradient(135deg, #fefcf3 0%, #f8f4e9 100%);
  border-color: #d4a574;
}

.toggle-button.dark {
  background: linear-gradient(135deg, #1a1a1a 0%, #262626 100%);
  border-color: #a3907c;
  color: #e8e8e8;
}

.toggle-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.toggle-icon {
  font-size: 1.2em;
}

.toggle-text {
  font-size: var(--typography-fontSize-sm);
}

/* 模式指示器 */
.mode-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  background: var(--colors-background-elevated);
  border: 1px solid var(--colors-border-medium);
  border-radius: 8px;
  padding: 8px;
  box-shadow: var(--shadows-sm);
  margin-bottom: 12px;
}

.indicator-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 8px 12px;
  border-radius: 6px;
  transition: all 0.2s ease-out;
  min-width: 60px;
}

.indicator-item.active {
  background: var(--colors-accent-primary);
  color: white;
}

.indicator-item:not(.active) {
  opacity: 0.6;
  cursor: pointer;
}

.indicator-item:not(.active):hover {
  opacity: 0.8;
  background: var(--colors-background-secondary);
}

.indicator-icon {
  font-size: 1.2em;
}

.indicator-label {
  font-size: var(--typography-fontSize-xs);
  font-weight: var(--typography-fontWeight-medium);
}

.indicator-divider {
  width: 1px;
  height: 24px;
  background: var(--colors-border-light);
}

/* 系统偏好显示 */
.system-preference {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: var(--colors-background-secondary);
  border: 1px solid var(--colors-border-light);
  border-radius: 6px;
  font-size: var(--typography-fontSize-xs);
  color: var(--colors-text-secondary);
}

.preference-label {
  font-weight: var(--typography-fontWeight-medium);
}

.preference-value {
  color: var(--colors-accent-primary);
}

/* 快速设置 */
.quick-settings {
  position: relative;
}

.settings-button {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  border: 1px solid var(--colors-border-medium);
  background: var(--colors-background-elevated);
  color: var(--colors-text-primary);
  cursor: pointer;
  transition: all 0.2s ease-out;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.settings-button:hover {
  background: var(--colors-background-secondary);
  border-color: var(--colors-accent-primary);
}

.settings-button.active {
  background: var(--colors-accent-primary);
  color: white;
}

.settings-panel {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 8px;
  background: var(--colors-background-elevated);
  border: 1px solid var(--colors-border-medium);
  border-radius: 8px;
  box-shadow: var(--shadows-lg);
  padding: 16px;
  min-width: 200px;
  max-width: 250px;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.settings-group {
  margin-bottom: 16px;
}

.settings-group:last-child {
  margin-bottom: 0;
}

.settings-title {
  font-size: var(--typography-fontSize-xs);
  font-weight: var(--typography-fontWeight-semibold);
  color: var(--colors-text-secondary);
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.setting-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 0;
  cursor: pointer;
  transition: all 0.2s ease-out;
}

.setting-item:hover {
  background: var(--colors-background-secondary);
  margin: 0 -8px;
  padding: 6px 8px;
  border-radius: 4px;
}

.setting-item input[type="checkbox"] {
  margin: 0;
  cursor: pointer;
}

.setting-label {
  font-size: var(--typography-fontSize-sm);
  color: var(--colors-text-primary);
  cursor: pointer;
  flex: 1;
}

.shortcut-info {
  font-size: var(--typography-fontSize-xs);
  color: var(--colors-text-muted);
  line-height: 1.4;
}

.shortcut-info kbd {
  background: var(--colors-background-secondary);
  border: 1px solid var(--colors-border-medium);
  border-radius: 3px;
  padding: 2px 4px;
  font-family: var(--typography-fontFamily-mono);
  font-size: 10px;
  margin-right: 4px;
}

/* 动画 */
.settings-slide-enter-active,
.settings-slide-leave-active {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.settings-slide-enter-from {
  opacity: 0;
  transform: translateY(-10px) scale(0.95);
}

.settings-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px) scale(0.95);
}

/* 深色模式适配 */
[data-theme-mode="dark"] .toggle-button.eye-care {
  background: linear-gradient(135deg, #2a2a2a 0%, #333333 100%);
  border-color: #a3907c;
  color: #e8e8e8;
}

[data-theme-mode="dark"] .mode-indicator {
  background: rgba(30, 30, 32, 0.8);
  border-color: rgba(255, 255, 255, 0.1);
}

[data-theme-mode="dark"] .settings-panel {
  background: rgba(30, 30, 32, 0.9);
  border-color: rgba(255, 255, 255, 0.1);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .theme-toggle-container {
    top: 10px;
    right: 10px;
  }
  
  .toggle-button {
    min-width: 120px;
    padding: 10px 16px;
  }
  
  .mode-indicator {
    flex-direction: column;
    gap: 4px;
  }
  
  .indicator-divider {
    width: 100%;
    height: 1px;
  }
  
  .settings-panel {
    min-width: 180px;
    max-width: 200px;
  }
}

/* 护眼模式特殊样式 */
[data-theme-mode="eye-care"] .toggle-button {
  background: linear-gradient(135deg, #fefcf3 0%, #f8f4e9 100%);
  border-color: #d4a574;
  color: #3a3a3a;
}

[data-theme-mode="eye-care"] .mode-indicator {
  background: rgba(254, 252, 243, 0.9);
  border-color: rgba(212, 165, 116, 0.3);
}

[data-theme-mode="eye-care"] .settings-panel {
  background: rgba(254, 252, 243, 0.95);
  border-color: rgba(212, 165, 116, 0.3);
}
</style>