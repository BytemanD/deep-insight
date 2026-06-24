import { createRouter, createWebHistory } from 'vue-router'
import Conversation from '../views/Conversation.vue'
import FileManagement from '../views/FileManagement.vue'

const routes = [
  { path: '/', redirect: '/conversation' },
  { path: '/conversation', name: 'Conversation', component: Conversation, meta: { title: '对话' } },
  { path: '/files', name: 'FileManagement', component: FileManagement, meta: { title: '文档管理' } },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
