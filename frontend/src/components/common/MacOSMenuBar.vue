/**
 * macOS 风格菜单栏组件
 * 模拟 macOS 系统菜单栏
 */

<template>
  <div class="macos-menu-bar" :class="{ 'is-dark': isDarkMode }">
    <div class="menu-bar-left">
      <div class="app-icon" @click="handleAppIconClick">
        🚗
      </div>
      <nav class="menu-items">
        <div 
          v-for="menu in menus" 
          :key="menu.id"
          class="menu-item"
          :class="{ active: activeMenu === menu.id }"
          @click="handleMenuClick(menu)"
          @mouseenter="handleMenuHover(menu)"
        >
          {{ menu.title }}
          <transition name="dropdown">
            <div v-if="activeMenu === menu.id" class="dropdown-menu">
              <div 
                v-for="item in menu.items" 
                :key="item.id"
                class="dropdown-item"
                :class="{ separator: item.type === 'separator', disabled: item.disabled }"
                @click="handleMenuItemClick(item)"
              >
                <span class="item-icon" v-if="item.icon">{{ item.icon }}</span>
                <span class="item-label">{{ item.label }}</span>
                <span class="item-shortcut" v-if="item.shortcut">{{ item.shortcut }}</span>
              </div>
            </div>
          </transition>
        </div>
      </nav>
    </div>
    
    <div class="menu-bar-right">
      <div class="system-status">
        <div class="status-icons">
          <button 
            v-for="icon in statusIcons" 
            :key="icon.id"
            class="status-icon"
            :title="icon.title"
            @click="handleStatusIconClick(icon)"
          >
            {{ icon.icon }}
          </button>
        </div>
        <div class="time" @click="handleTimeClick">
          {{ currentTime }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

// 状态管理
const activeMenu = ref(null)
const currentTime = ref('')

// 主题检测
const isDarkMode = computed(() => {
  return document.documentElement.getAttribute('data-theme-mode') === 'dark'
})

// 菜单数据
const menus = ref([
  {
    id: 'app',
    title: '车险分析',
    items: [
      { id: 'about', label: '关于车险分析', icon: 'ℹ️' },
      { id: 'settings', label: '设置...', icon: '⚙️', shortcut: '⌘,' },
      { type: 'separator' },
      { id: 'hide', label: '隐藏 车险分析', shortcut: '⌘H' },
      { id: 'hide-others', label: '隐藏其他', shortcut: '⌥⌘H' },
      { id: 'show-all', label: '显示全部' },
      { type: 'separator' },
      { id: 'quit', label: '退出 车险分析', shortcut: '⌘Q' }
    ]
  },
  {
    id: 'file',
    title: '文件',
    items: [
      { id: 'new', label: '新建', icon: '📄', shortcut: '⌘N' },
      { id: 'open', label: '打开...', icon: '📁', shortcut: '⌘O' },
      { id: 'save', label: '保存', icon: '💾', shortcut: '⌘S' },
      { type: 'separator' },
      { id: 'import', label: '导入数据', icon: '📥' },
      { id: 'export', label: '导出报告', icon: '📤' }
    ]
  },
  {
    id: 'edit',
    title: '编辑',
    items: [
      { id: 'undo', label: '撤销', shortcut: '⌘Z' },
      { id: 'redo', label: '重做', shortcut: '⇧⌘Z' },
      { type: 'separator' },
      { id: 'cut', label: '剪切', shortcut: '⌘X' },
      { id: 'copy', label: '复制', shortcut: '⌘C' },
      { id: 'paste', label: '粘贴', shortcut: '⌘V' }
    ]
  },
  {
    id: 'view',
    title: '视图',
    items: [
      { id: 'fullscreen', label: '进入全屏', shortcut: '⌃⌘F' },
      { id: 'minimize', label: '最小化', shortcut: '⌘M' },
      { type: 'separator' },
      { id: 'dashboard', label: '仪表板', icon: '📊' },
      { id: 'reports', label: '报告', icon: '📈' },
      { id: 'settings', label: '设置', icon: '⚙️' }
    ]
  },
  {
    id: 'window',
    title: '窗口',
    items: [
      { id: 'close', label: '关闭窗口', shortcut: '⌘W' },
      { id: 'minimize', label: '最小化', shortcut: '⌘M' },
      { id: 'zoom', label: '缩放' },
      { type: 'separator' },
      { id: 'bring-all', label: '前置全部窗口' }
    ]
  },
  {
    id: 'help',
    title: '帮助',
    items: [
      { id: 'search', label: '搜索', shortcut: '⌘/' },
      { id: 'documentation', label: '文档', icon: '📖' },
      { id: 'feedback', label: '发送反馈', icon: '💬' },
      { type: 'separator' },
      { id: 'about', label: '关于', icon: 'ℹ️' }
    ]
  }
])

// 状态图标
const statusIcons = ref([
  { id: 'wifi', icon: '📶', title: 'Wi-Fi 已连接' },
  { id: 'battery', icon: '🔋', title: '电池: 85%' },
  { id: 'clock', icon: '⏰', title: '闹钟' },
  { id: 'user', icon: '👤', title: '用户账户' }
])

// 时间更新
let timeInterval = null

const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 事件处理
const handleAppIconClick = () => {
  console.log('应用图标点击')
  // 可以显示应用菜单
}

const handleMenuClick = (menu) => {
  activeMenu.value = activeMenu.value === menu.id ? null : menu.id
}

const handleMenuHover = (menu) => {
  // 如果已经有激活的菜单，hover 时切换
  if (activeMenu.value && activeMenu.value !== menu.id) {
    activeMenu.value = menu.id
  }
}

const handleMenuItemClick = (item) => {
  if (item.type === 'separator' || item.disabled) return
  
  console.log('菜单项点击:', item.id)
  activeMenu.value = null
  
  // 处理具体的菜单项逻辑
  switch (item.id) {
    case 'quit':
      if (confirm('确定要退出应用吗？')) {
        // 退出逻辑
        window.close()
      }
      break
    case 'settings':
      // 打开设置
      console.log('打开设置')
      break
    case 'fullscreen':
      // 全屏切换
      toggleFullscreen()
      break
    default:
      console.log(`执行操作: ${item.id}`)
  }
}

const handleStatusIconClick = (icon) => {
  console.log('状态图标点击:', icon.id)
  // 可以显示相关的状态面板
}

const handleTimeClick = () => {
  console.log('时间点击')
  // 可以显示日历或时间设置
}

// 全屏切换
const toggleFullscreen = () => {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen().catch(err => {
      console.log('无法进入全屏:', err)
    })
  } else {
    document.exitFullscreen()
  }
}

// 点击外部关闭菜单
const handleClickOutside = (event) => {
  const menuBar = document.querySelector('.macos-menu-bar')
  if (menuBar && !menuBar.contains(event.target)) {
    activeMenu.value = null
  }
}

// 生命周期
onMounted(() => {
  updateTime()
  timeInterval = setInterval(updateTime, 1000)
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  if (timeInterval) {
    clearInterval(timeInterval)
  }
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.macos-menu-bar {
  height: 28px;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 16px;
  font-size: 13px;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Helvetica Neue', Arial, sans-serif;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  user-select: none;
  -webkit-user-select: none;
  transition: all 0.2s ease;
}

.macos-menu-bar.is-dark {
  background: rgba(30, 30, 32, 0.8);
  border-bottom-color: rgba(255, 255, 255, 0.1);
  color: #ffffff;
}

.menu-bar-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.app-icon {
  font-size: 16px;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.app-icon:hover {
  background: rgba(0, 0, 0, 0.05);
}

.is-dark .app-icon:hover {
  background: rgba(255, 255, 255, 0.1);
}

.menu-items {
  display: flex;
  align-items: center;
  gap: 4px;
}

.menu-item {
  position: relative;
  padding: 4px 8px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: 400;
}

.menu-item:hover {
  background: rgba(0, 0, 0, 0.05);
}

.is-dark .menu-item:hover {
  background: rgba(255, 255, 255, 0.1);
}

.menu-item.active {
  background: rgba(0, 122, 255, 0.1);
  color: #007AFF;
}

.is-dark .menu-item.active {
  background: rgba(0, 122, 255, 0.2);
  color: #0A84FF;
}

.menu-bar-right {
  display: flex;
  align-items: center;
}

.system-status {
  display: flex;
  align-items: center;
  gap: 12px;
}

.status-icons {
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-icon {
  background: none;
  border: none;
  font-size: 14px;
  padding: 4px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
  color: inherit;
}

.status-icon:hover {
  background: rgba(0, 0, 0, 0.05);
}

.is-dark .status-icon:hover {
  background: rgba(255, 255, 255, 0.1);
}

.time {
  font-weight: 500;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.time:hover {
  background: rgba(0, 0, 0, 0.05);
}

.is-dark .time:hover {
  background: rgba(255, 255, 255, 0.1);
}

/* 下拉菜单 */
.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  min-width: 200px;
  padding: 4px 0;
  z-index: 1001;
  margin-top: 4px;
}

.is-dark .dropdown-menu {
  background: rgba(40, 40, 42, 0.95);
  border-color: rgba(255, 255, 255, 0.1);
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 13px;
}

.dropdown-item:hover:not(.disabled):not(.separator) {
  background: rgba(0, 122, 255, 0.1);
}

.is-dark .dropdown-item:hover:not(.disabled):not(.separator) {
  background: rgba(10, 132, 255, 0.2);
}

.dropdown-item.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.dropdown-item.separator {
  height: 1px;
  background: rgba(0, 0, 0, 0.1);
  margin: 4px 12px;
  padding: 0;
  cursor: default;
}

.is-dark .dropdown-item.separator {
  background: rgba(255, 255, 255, 0.1);
}

.item-icon {
  font-size: 14px;
  width: 16px;
  text-align: center;
}

.item-label {
  flex: 1;
}

.item-shortcut {
  font-size: 11px;
  color: #8E8E93;
  margin-left: auto;
}

.is-dark .item-shortcut {
  color: #8E8E93;
}

/* 动画 */
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.dropdown-enter-from {
  opacity: 0;
  transform: translateY(-10px) scale(0.95);
}

.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-10px) scale(0.95);
}

/* 响应式调整 */
@media (max-width: 768px) {
  .macos-menu-bar {
    padding: 0 12px;
    font-size: 12px;
  }
  
  .menu-bar-left {
    gap: 12px;
  }
  
  .menu-item {
    padding: 4px 6px;
  }
  
  .status-icons {
    gap: 6px;
  }
}
</style>