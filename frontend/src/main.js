import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'

import './assets/styles/variables.css'
import './assets/styles/base.css'

const app = createApp(App)

app.use(createPinia())

app.mount('#app')
