import path from 'node:path';
import { defineConfig, loadEnv } from 'vite';
import vue from '@vitejs/plugin-vue';

// 函数级中文注释：
// 1) 读取 .env 环境变量以实现端口与代理目标的灵活化，避免硬编码。
//    - VITE_PORT: 前端开发端口，默认 3000
//    - VITE_API_TARGET: 后端 API 代理目标，例如 http://localhost:5001
// 2) 为兼容当前 TypeScript 的 module 目标（可能不支持 import.meta），
//    取消对 import.meta.url 的使用，别名解析改为 path.resolve(process.cwd(), 'src')。
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const port = Number(env.VITE_PORT) || 3000
  const apiTarget = env.VITE_API_TARGET || 'http://localhost:5001'

  return {
    plugins: [vue()],
    resolve: {
      alias: {
        // 使用进程工作目录解析到 src，避免 import.meta 在某些 TS 配置下的诊断报错
        '@': path.resolve(process.cwd(), 'src')
      }
    },
    server: {
      port,
      proxy: {
        '/api': {
          target: apiTarget,
          changeOrigin: true
        }
      }
    }
  }
});
