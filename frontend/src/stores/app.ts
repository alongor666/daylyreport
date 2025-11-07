import { defineStore } from 'pinia';

export const useAppStore = defineStore('app', {
  state: () => ({
    initializedAt: new Date().toISOString()
  }),
  getters: {
    welcomeMessage: (state) => `前端环境初始化于 ${state.initializedAt}`
  }
});
