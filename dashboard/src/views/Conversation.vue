<template>
  <v-row no-gutters class="fill-height">
    <v-col cols="3" class="d-flex flex-column" style="border-right: 1px solid #e0e0e0;">
      <div class="pa-3">
        <v-btn block color="primary" @click="createDialog">+ 新建会话</v-btn>
      </div>
      <v-divider></v-divider>
      <v-list density="compact" nav class="overflow-y-auto flex-grow-1">
        <v-list-item v-for="d in dialogs" :key="d.uuid" :title="d.name || '未命名会话'"
          :subtitle="formatTime(d.created_at)" :active="selectedDialog?.uuid === d.uuid" @click="selectDialog(d)">
          <template #append>
            <v-btn icon="mdi-close" variant="text" size="small" @click.stop="handleDeleteDialog(d)" />
          </template>
        </v-list-item>
      </v-list>
      <v-divider></v-divider>
      <div class="pa-2 text-caption text-medium-emphasis text-center">{{ dialogs.length }} 个会话</div>
    </v-col>

    <v-col cols="9" class="d-flex flex-column">
      <div v-if="!selectedDialog" class="d-flex align-center justify-center flex-grow-1 text-medium-emphasis">
        请选择或创建一个会话
      </div>
      <template v-else>
        <div ref="scrollRef" class="flex-grow-1 overflow-y-auto pa-4">
          <div v-for="(item, i) in messages" :key="i"
            :class="['d-flex mb-3', item.role === 'user' ? 'justify-end' : 'justify-start']">
            <v-card :subtitle="item.role === 'user' ? '你' : 'AI'"
              :class="['pa-3', item.role === 'user' ? 'bg-primary' : 'bg-surface-variant']"
              :max-width="isMobile ? '85%' : '70%'" rounded="lg">
              <div class="text-body-2" style="white-space: pre-wrap; word-break: break-word; min-width: 200px;">
                {{ item.content }}
              </div>
            </v-card>
          </div>
          <v-card v-if="loading" class="bg-surface-variant pa-3">loading</v-card>
        </div>
        <v-divider></v-divider>
        <v-footer class="pa-4">
          <v-text-field v-model="input" variant="outlined" density="compact" placeholder="输入消息..." hide-details
            :disabled="loading || !selectedDialog" @keydown.enter.prevent="send">
            <template #append-inner>
              <v-btn icon="mdi-send" variant="text" color="primary" :loading="loading" :disabled="!input.trim()"
                @click="send" />
            </template>
          </v-text-field>
        </v-footer>
      </template>
    </v-col>
  </v-row>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import { useDisplay } from 'vuetify'
import api from '../api'

const { smAndDown } = useDisplay()
const isMobile = smAndDown

const input = ref('')
const loading = ref(false)
const messages = ref([])
const scrollRef = ref(null)
const dialogs = ref([])
const selectedDialog = ref(null)

function formatTime(iso) {
  if (!iso) return ''
  const d = new Date(iso)
  return d.toLocaleString('zh-CN', { month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' })
}

async function loadDialogs() {
  const projectId = localStorage.getItem('project_id')
  if (!projectId) return
  try {
    const res = await api.listDialogs(projectId)
    dialogs.value = res.dialogs || []
  } catch (e) {
    console.error('Failed to load dialogs', e)
  }
}

async function createDialog() {
  const projectId = localStorage.getItem('project_id')
  if (!projectId) return
  try {
    const dialog = await api.createDialog(projectId)
    dialogs.value.unshift(dialog)
    selectDialog(dialog)
  } catch (e) {
    console.error('Failed to create dialog', e)
  }
}

async function handleDeleteDialog(d) {
  try {
    await api.deleteDialog(d.uuid)
    dialogs.value = dialogs.value.filter(item => item.uuid !== d.uuid)
    if (selectedDialog.value?.uuid === d.uuid) {
      selectedDialog.value = null
      messages.value = []
    }
  } catch (e) {
    console.error('Failed to delete dialog', e)
  }
}

function selectDialog(d) {
  selectedDialog.value = d
  messages.value = []
  input.value = ''
}

async function send() {
  const text = input.value.trim()
  if (!text || loading.value) return

  messages.value.push({ role: 'user', content: text })
  input.value = ''
  loading.value = true

  await nextTick()
  scrollToBottom()

  try {
    const data = await api.query(text)
    messages.value.push({ role: 'assistant', content: data.answer })
  } catch (e) {
    messages.value.push({ role: 'assistant', content: `错误: ${e.message}` })
  } finally {
    loading.value = false
    await nextTick()
    scrollToBottom()
  }
}

function scrollToBottom() {
  setTimeout(() => {
    const el = scrollRef.value
    if (el) el.scrollTop = el.scrollHeight
  }, 50)
}

onMounted(() => {
  loadDialogs()
})

watch(() => localStorage.getItem('project_id'), () => {
  selectedDialog.value = null
  messages.value = []
  loadDialogs()
})
</script>

<style scoped>
.fill-height {
  height: calc(100vh - 64px);
}
</style>
