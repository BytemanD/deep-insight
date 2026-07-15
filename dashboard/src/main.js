import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'
import 'vuetify/styles' // 确保这个在前面
// import './styles/youth.scss' // 你的自定义样式放在后面

const app = createApp(App)
app.use(router)
app.use(vuetify)
app.mount('#app')
