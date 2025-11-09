/**
 * 主题切换器组件
 * 提供主题和模式切换功能
 */

<template>
  <div class="theme-switcher">
    <!-- 主题选择器 -->
    <div class="theme-selector">
      <button 
        class="theme-button"
        :class="{ active: isThemeSelectorOpen }"
        @click="toggleThemeSelector"
        title="选择主题"
      >
        🎨
      </button>
      
      <transition name="selector-dropdown">
        <div v-if="isThemeSelectorOpen" class="theme-dropdown">
          <div class="theme-list">
            <div 
              v-for="theme in availableThemes" 
              :key="theme.id"
              class="theme-option"
              :class="{ active: currentTheme === theme.id }"
              @click="selectTheme(theme.id)"
            >
              <div class="theme-preview">
                <div class="theme-colors">
                  <div 
                    class="color-sample primary"
                    :style="{ backgroundColor: theme.tokens.colors.primary[500] }"
                  ></div>
                  <div 
                    class="color-sample secondary"
                    :style="{ backgroundColor: theme.tokens.colors.secondary[500] }"
                  ></div>
                  <div 
                    class="color-sample accent"
                    :style="{ backgroundColor: theme.tokens.colors.semantic.success[500] }"
                  ></div>
                </div>
              </div>
              <div class="theme-info">
                <div class="theme-name">{{ theme.name }}</div>
                <div class="theme-description">{{ theme.description }}</div>
              </div>
              <div v-if="currentTheme === theme.id" class="theme-check">✓</div>
            </div>
          </div>
        </div>
      </transition>
    </div>
    
    <!-- 模式切换器 -->
    <div class="mode-switcher">
      <button 
        class="mode-button"
        :class="{ active: currentMode === 'light' }"
        @click="switchMode('light')"
        title="浅色模式"
      >
        ☀️
      </button>
      <button 
        class="mode-button"
        :class="{ active: currentMode === 'dark' }"
        @click="switchMode('dark')"
        title="深色模式"
      >
        🌙
      </button>
      <button 
        class="mode-button"
        :class="{ active: currentMode === 'auto' }"
        @click="switchMode('auto')"
        title="自动模式"
      >
        🔄
      </button>
    </div>
    
    <!-- 快速设置 -->
    <div class="quick-settings">
      <button 
        class="settings-button"
        :class="{ active: isSettingsOpen }"
        @click="toggleSettings"
        title="快速设置"
      >
        ⚙️
      </button>
      
      <transition name="settings-dropdown">
        <div v-if="isSettingsOpen" class="settings-dropdown">
          <div class="settings-group">
            <div class="setting-item">
              <label class="setting-label">
                <input 
                  type="checkbox" 
                  v-model="enableAnimations"
                  @change="toggleAnimations"
                />
                启用动画
              </label>
            </div>
            <div class="setting-item">
              <label class="setting-label">
                <input 
                  type="checkbox" 
                  v-model="enableCache"
                  @change="toggleCache"
                />
                启用缓存
              </label>
            </div>
            <div class="setting-item">
              <label class="setting-label">
                <input 
                  type="checkbox" 
                  v-model="enablePrefetch"
                  @change="togglePrefetch"
                />
                启用预加载
              </label>
            </div>
          </div>
          
          <div class="settings-group">
            <div class="setting-title">性能设置</div>
            <div class="setting-item">
              <label class="setting-label">
                性能阈值 (ms)
                <input 
                  type="range" 
                  v-model.number="performanceThreshold"
                  min="50"
                  max="500"
                  step="50"
                  @change="updatePerformanceThreshold"
                />
                <span class="setting-value">{{ performanceThreshold }}ms</span>
              </label>
            </div>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, inject, onMounted, onUnmounted } from 'vue'

// 注入主题系统
const themeSystem = inject('themeSystem')
const { currentTheme, currentMode, switchTheme, switchMode } = themeSystem ? themeSystem.getEngine() : { 
  currentTheme: ref('default'), 
  currentMode: ref('light'), 
  switchTheme: () => {}, 
  switchMode: () => {} 
}

// 状态管理
const isThemeSelectorOpen = ref(false)
const isSettingsOpen = ref(false)

// 设置选项
const enableAnimations = ref(true)
const enableCache = ref(true)
const enablePrefetch = ref(true)
const performanceThreshold = ref(100)

// 可用主题
const availableThemes = computed(() => {
  return themeSystem?.getEngine()?.getAvailableThemes() || [
    {
      id: 'default',
      name: '默认主题',
      description: '简洁现代的基础主题',
      tokens: {
        colors: {
          primary: { 500: '#3b82f6' },
          secondary: { 500: '#64748b' },
          semantic: { success: { 500: '#22c55e' } }
        }
      }
    },
    {
      id: 'macos',
      name: 'macOS 风格',
      description: 'Apple macOS 风格主题',
      tokens: {
        colors: {
          primary: { 500: '#007AFF' },
          secondary: { 500: '#8E8E93' },
          semantic: { success: { 500: '#34C759' } }
        }
      }
    },
    {
      id: 'material',
      name: 'Material Design 3',
      description: 'Google Material Design 3 风格',
      tokens: {
        colors: {
          primary: { 500: '#1F6EF0' },
          secondary: { 500: '#6A87B4' },
          semantic: { success: { 500: '#198C19' } }
        }
      }
    }
  ]
})

// 主题名称映射
const themeNames = {
  'default': '默认主题',
  'macos': 'macOS 风格',
  'material': 'Material Design 3'
}

// 事件处理
const toggleThemeSelector = () => {
  isThemeSelectorOpen.value = !isThemeSelectorOpen.value
  if (isThemeSelectorOpen.value) {
    isSettingsOpen.value = false
  }
}

const toggleSettings = () => {
  isSettingsOpen.value = !isSettingsOpen.value
  if (isSettingsOpen.value) {
    isThemeSelectorOpen.value = false
  }
}

const selectTheme = async (themeId) => {
  try {
    await switchTheme(themeId)
    isThemeSelectorOpen.value = false
    console.log(`主题已切换到: ${themeId}`)
  } catch (error) {
    console.error('主题切换失败:', error)
  }
}

const switchMode = async (mode) => {
  try {
    await themeSystem?.getEngine()?.switchMode(mode)
    console.log(`模式已切换到: ${mode}`)
  } catch (error) {
    console.error('模式切换失败:', error)
  }
}

const toggleAnimations = () => {
  // 更新动画设置
  document.documentElement.style.setProperty(
    '--animation-duration-normal', 
    enableAnimations.value ? '200ms' : '0ms'
  )
  console.log(`动画已${enableAnimations.value ? '启用' : '禁用'}`)
}

const toggleCache = () => {
  // 这里可以连接到主题引擎的缓存设置
  console.log(`缓存已${enableCache.value ? '启用' : '禁用'}`)
}

const togglePrefetch = () => {
  // 这里可以连接到主题引擎的预加载设置
  console.log(`预加载已${enablePrefetch.value ? '启用' : '禁用'}`)
}

const updatePerformanceThreshold = () => {
  // 这里可以连接到主题引擎的性能设置
  console.log(`性能阈值已设置为: ${performanceThreshold.value}ms`)
}

// 点击外部关闭下拉菜单
const handleClickOutside = (event) => {
  const themeSwitcher = document.querySelector('.theme-switcher')
  if (themeSwitcher && !themeSwitcher.contains(event.target)) {
    isThemeSelectorOpen.value = false
    isSettingsOpen.value = false
  }
}

// 生命周期
onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  
  // 加载保存的设置
  const savedSettings = localStorage.getItem('theme-settings')
  if (savedSettings) {
    try {
      const settings = JSON.parse(savedSettings)
      enableAnimations.value = settings.enableAnimations ?? true
      enableCache.value = settings.enableCache ?? true
      enablePrefetch.value = settings.enablePrefetch ?? true
      performanceThreshold.value = settings.performanceThreshold ?? 100
    } catch (error) {
      console.warn('加载主题设置失败:', error)
    }
  }
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  
  // 保存设置
  const settings = {
    enableAnimations: enableAnimations.value,
    enableCache: enableCache.value,
    enablePrefetch: enablePrefetch.value,
    performanceThreshold: performanceThreshold.value
  }
  localStorage.setItem('theme-settings', JSON.stringify(settings))
})
</script>

<style scoped>
.theme-switcher {
  position: fixed;
  top: 60px;
  right: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  z-index: 1000;
  font-family: var(--typography-fontFamily-sans);
}

/* 主题选择器 */
.theme-selector {
  position: relative;
}

.theme-button {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  border: 1px solid var(--colors-border-light);
  background: var(--colors-background-elevated);
  font-size: 18px;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: var(--shadows-sm);
  display: flex;
  align-items: center;
  justify-content: center;
}

.theme-button:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadows-md);
}

.theme-button.active {
  border-color: var(--colors-primary-500);
  background: var(--colors-primary-50);
}

.theme-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 8px;
  background: var(--colors-background-elevated);
  border: 1px solid var(--colors-border-light);
  border-radius: 12px;
  box-shadow: var(--shadows-xl);
  padding: 8px;
  min-width: 280px;
  max-height: 400px;
  overflow-y: auto;
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
}

.theme-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.theme-option {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.theme-option:hover {
  background: var(--colors-background-secondary);
}

.theme-option.active {
  background: var(--colors-primary-50);
  border: 1px solid var(--colors-primary-200);
}

.theme-preview {
  flex-shrink: 0;
}

.theme-colors {
  display: flex;
  gap: 2px;
}

.color-sample {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.theme-info {
  flex: 1;
  min-width: 0;
}

.theme-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--colors-text-primary);
  margin-bottom: 2px;
}

.theme-description {
  font-size: 12px;
  color: var(--colors-text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.theme-check {
  color: var(--colors-primary-500);
  font-weight: bold;
  font-size: 16px;
}

/* 模式切换器 */
.mode-switcher {
  display: flex;
  gap: 8px;
  background: var(--colors-background-elevated);
  border: 1px solid var(--colors-border-light);
  border-radius: 12px;
  padding: 4px;
  box-shadow: var(--shadows-sm);
}

.mode-button {
  flex: 1;
  padding: 8px 12px;
  border: none;
  background: transparent;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.mode-button:hover {
  background: var(--colors-background-secondary);
}

.mode-button.active {
  background: var(--colors-primary-500);
  color: white;
}

/* 快速设置 */
.quick-settings {
  position: relative;
}

.settings-button {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  border: 1px solid var(--colors-border-light);
  background: var(--colors-background-elevated);
  font-size: 18px;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: var(--shadows-sm);
  display: flex;
  align-items: center;
  justify-content: center;
}

.settings-button:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadows-md);
}

.settings-button.active {
  border-color: var(--colors-primary-500);
  background: var(--colors-primary-50);
}

.settings-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 8px;
  background: var(--colors-background-elevated);
  border: 1px solid var(--colors-border-light);
  border-radius: 12px;
  box-shadow: var(--shadows-xl);
  padding: 16px;
  min-width: 250px;
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
}

.settings-group {
  margin-bottom: 16px;
}

.settings-group:last-child {
  margin-bottom: 0;
}

.setting-title {
  font-size: 12px;
  font-weight: 600;
  color: var(--colors-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 8px;
}

.setting-item {
  margin-bottom: 8px;
}

.setting-item:last-child {
  margin-bottom: 0;
}

.setting-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: var(--colors-text-primary);
  cursor: pointer;
}

.setting-label input[type="checkbox"] {
  margin: 0;
}

.setting-label input[type="range"] {
  flex: 1;
  margin: 0 8px;
}

.setting-value {
  font-size: 12px;
  color: var(--colors-text-secondary);
  min-width: 40px;
  text-align: right;
}

/* 动画 */
.selector-dropdown-enter-active,
.selector-dropdown-leave-active {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.selector-dropdown-enter-from {
  opacity: 0;
  transform: translateY(-10px) scale(0.95);
}

.selector-dropdown-leave-to {
  opacity: 0;
  transform: translateY(-10px) scale(0.95);
}

.settings-dropdown-enter-active,
.settings-dropdown-leave-active {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.settings-dropdown-enter-from {
  opacity: 0;
  transform: translateY(-10px) scale(0.95);
}

.settings-dropdown-leave-to {
  opacity: 0;
  transform: translateY(-10px) scale(0.95);
}

/* 深色模式适配 */
@media (prefers-color-scheme: dark) {
  .theme-button,
  .settings-button {
    background: rgba(30, 30, 32, 0.8);
    color: white;
  }
  
  .theme-dropdown,
  .settings-dropdown {
    background: rgba(30, 30, 32, 0.9);
    border-color: rgba(255, 255, 255, 0.1);
  }
  
  .mode-switcher {
    background: rgba(30, 30, 32, 0.8);
    border-color: rgba(255, 255, 255, 0.1);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .theme-switcher {
    right: 10px;
    top: 50px;
  }
  
  .theme-dropdown {
    min-width: 240px;
  }
  
  .settings-dropdown {
    min-width: 200px;
  }
}
</style>