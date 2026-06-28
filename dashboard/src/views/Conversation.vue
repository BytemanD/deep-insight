<template>
  <v-row no-gutters class="fill-height">
    <v-col cols="2" class="d-flex flex-column" style="border-right: 1px solid #e0e0e0;">
      <div class="pa-3">
        <v-btn block color="primary" @click="createDialog">+ 新建会话</v-btn>
      </div>
      <v-divider></v-divider>
      <v-list density="compact" nav class="overflow-y-auto flex-grow-1">
        <v-list-item v-for="d in dialogs" :key="d.uuid" :title="d.name || '未命名会话'" :subtitle="formatTime(d.created_at)"
          :active="selectedDialog?.uuid === d.uuid" @click="selectDialog(d)">
          <template #append>
            <v-btn icon="mdi-close" variant="text" size="small" @click.stop="handleDeleteDialog(d)" />
          </template>
        </v-list-item>
      </v-list>
      <v-divider></v-divider>

      <div class="pa-2 text-caption text-medium-emphasis text-center">{{ dialogs.length }} 个会话</div>
    </v-col>
    <v-col class="d-flex flex-column">
      <div v-if="!selectedDialog" class="d-flex align-center justify-center flex-grow-1 text-medium-emphasis">
        请选择或创建一个会话
      </div>
      <template v-else>
        <v-virtual-scroll ref="scrollRef" height="260px" item-height="32" v-model="messages" :items="messages">
          <template v-slot:default="{ item, index }">
            <div :class="['d-flex mb-3', item.role === 'user' ? 'justify-end' : 'justify-start']">
              <v-card :class="['pa-3', item.role === 'user' ? 'bg-primary' : 'bg-surface-variant']"
                :max-width="isMobile ? '85%' : '70%'" rounded="lg" density="compact">
                <v-expansion-panels v-if="item.thinking" density="compact" theme="dark" class="mb-4">
                  <v-expansion-panel>
                    <v-expansion-panel-title v-if="!item.content">
                      <span>思考中 ...</span>
                      <template v-slot:actions>
                        <div class="d-flex align-center">
                          <v-progress-circular indeterminate color="primary" size="24" width="2" />
                        </div>
                      </template>
                    </v-expansion-panel-title>
                    <v-expansion-panel-title v-else>
                      <span>思考</span>
                    </v-expansion-panel-title>

                    <v-expansion-panel-text>
                      {{ item.thinking }}
                    </v-expansion-panel-text>
                  </v-expansion-panel>
                  <!-- 加载状态：显示转圈圈 -->
                </v-expansion-panels>
                <div class="text-body-2" style="white-space: pre-wrap; word-break: break-word; min-width: 200px;">
                  {{ item.content }}
                </div>
              </v-card>
            </div>
          </template>

        </v-virtual-scroll>
        <v-divider></v-divider>
        <v-footer class="">
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
import { ref, inject, onMounted, watch, nextTick } from 'vue'
import { useDisplay } from 'vuetify'
import api from '../api'

const { smAndDown } = useDisplay()
const isMobile = smAndDown

const input = ref('')
const loading = ref(false)
const messages = ref([])
const scrollRef = ref(null)
const projectId = inject('projectId')
const dialogs = ref([])
const selectedDialog = ref(null)
const showTooltip = ref(true)
function formatTime(iso) {
  if (!iso) return ''
  const d = new Date(iso)
  return d.toLocaleString('zh-CN', { month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' })
}

async function loadDialogs() {
  try {
    const res = await api.listSessions()
    dialogs.value = res.sessions || []
  } catch (e) {
    console.error('Failed to load dialogs', e)
  }
}

async function createDialog() {
  const pid = projectId?.value
  if (!pid) return
  try {
    const dialog = await api.createSession(pid)
    dialogs.value.unshift(dialog)
    selectDialog(dialog)
  } catch (e) {
    console.error('Failed to create dialog', e)
  }
}

async function handleDeleteDialog(d) {
  try {
    await api.deleteSession(d.uuid)
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
  localStorage.setItem('session_id', d.uuid)
}
const lastLLmMsg = ref({ role: 'assistant', content: '' })

async function send() {
  const text = input.value.trim()
  if (!text || loading.value) return

  messages.value.push({ role: 'user', content: text })
  input.value = ''
  loading.value = true

  await nextTick()
  scrollToBottom()

  lastLLmMsg.value.content = ''
  // const assistantMsg = { role: 'assistant', content: '' }
  messages.value.push({ role: 'assistant', content: '', thinking: '' })

  let hasError = false
  await api.queryStream(
    text,
    (chunk, type) => {
      if (type === 'thinking') {
        messages.value[messages.value.length - 1].thinking += chunk
      } else {
        messages.value[messages.value.length - 1].content += chunk
      }
      scrollToBottom()
    },
    () => {
      loading.value = false
      scrollToBottom()
    },
    (error) => {
      if (!hasError) {
        hasError = true
        messages.value[messages.value.length - 1].content = `错误: ${error}`
        loading.value = false
        scrollToBottom()
      }
    },
  )
}

function scrollToBottom() {
  const el = scrollRef.value
  if (el && el.$el.scrollTop < el.$el.scrollHeight) {
    el.$el.scrollTop = el.$el.scrollHeight
  }
}

onMounted(() => {
  loadDialogs()
})

watch(projectId, (newVal, oldVal) => {
  if (newVal && newVal !== oldVal) {
    selectedDialog.value = null
    messages.value = []
    loadDialogs()
  }
})
</script>

<style scoped>
.fill-height {
  height: calc(100vh - 64px);
}
</style>
