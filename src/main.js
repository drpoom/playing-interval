import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import { vLongpress } from './directives/longpress.js'

const app = createApp(App)
app.directive('longpress', vLongpress)
app.mount('#app')