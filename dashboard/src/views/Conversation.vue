<template>
  <v-row no-gutters class="fill-height">
    <v-col cols="2" class="d-flex flex-column" style="border-right: 1px solid #e0e0e0;">
      <div class="pa-3">
        <v-btn block color="primary" @click="createDialog" prepend-icon="mdi-plus">新建会话</v-btn>
      </div>
      <v-divider></v-divider>
      <v-virtual-scroll :items="dialogs" height="100">
        <template v-slot:default="{ item }">
          <v-list-item :title="item.name || '未命名会话'" :subtitle="formatTime(item.created_at)"
            :active="selectedDialog?.uuid === item.uuid" @click="selectDialog(item)"
            :disabled="selectedDialog?.uuid === item.uuid">
            <template #append>
              <v-btn icon="mdi-close" variant="text" size="small" @click.stop="handleDeleteDialog(item)" />
            </template>
          </v-list-item>
        </template>
      </v-virtual-scroll>
      <v-divider></v-divider>
      <div class="pa-2 text-caption text-medium-emphasis text-center">{{ dialogs.length }} 个会话</div>
    </v-col>
    <v-col class="d-flex flex-column">
      <div v-if="!selectedDialog" class="d-flex align-center justify-center flex-grow-1 text-medium-emphasis">
        请选择或创建一个会话
      </div>
      <template v-else>
        <v-virtual-scroll ref="scrollRef" height="260px" class="pa-2" v-model="messages" :items="messages">
          <template v-slot:default="{ item, index }">
            <v-col v-if="item.role === 'user'" class="d-flex align-end flex-column">
              <div style="max-width: 70%;">
                <v-alert class="d-inline-block rounded-be-0 text-body-large" rounded="xl" color="info" density="compact"
                  style="font-size: small;">
                  {{ item.content }}
                </v-alert>
              </div>
            </v-col>
            <v-col v-else class="d-flex align-start flex-column">
              <div style="max-width: 70%;">
                <!-- 思考过程 -->
                <v-expansion-panels class="mb-4 border-s-lg" elevation="0" size="small" v-if="item.thinking"
                  :model-value="item.content ? 1 : 0">
                  <v-expansion-panel>
                    <v-expansion-panel-title style="max-width: 200px" density="compact">
                      <span class="text-warning" v-if="!item.content && loading">思考中 ...</span>
                      <span v-else class="text-info">已思考</span>
                      <template v-slot:actions>
                        <v-progress-circular v-if="!item.content && loading" indeterminate
                          size="20"></v-progress-circular>
                        <v-icon v-else>mdi-check</v-icon>
                      </template>
                    </v-expansion-panel-title>
                    <v-expansion-panel-text>
                      <p class="d-inline-block rounded-bs-0" rounded="xl" density="compact" style="font-size: small;"
                        v-html="marked(item.thinking)"></p>
                      <!-- <p style="font-size: small;">{{ item.thinking }}</p> -->
                    </v-expansion-panel-text>
                  </v-expansion-panel>
                </v-expansion-panels>

                <v-alert v-if="item.content" class="d-inline-block rounded-bs-0 px-8" rounded="xl" density="compact"
                  style="font-size: small;" v-html="marked(item.content)">
                </v-alert>
              </div>
            </v-col>
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
import API from '../api'
import { marked } from 'marked'


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
const lastLLmMsg = ref({ role: 'assistant', content: '' })


function formatTime(iso) {
  if (!iso) return ''
  const d = new Date(iso)
  return d.toLocaleString('zh-CN', { month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' })
}

async function loadDialogs() {
  try {
    const res = await API.listSessions()
    dialogs.value = res.sessions || []
  } catch (e) {
    console.error('Failed to load dialogs', e)
  }
}

async function createDialog() {
  const pid = projectId?.value
  if (!pid) return
  try {
    const dialog = await API.createSession(pid)
    dialogs.value.unshift(dialog)
    selectDialog(dialog)
  } catch (e) {
    console.error('Failed to create dialog', e)
  }
}

async function handleDeleteDialog(d) {
  try {
    await API.deleteSession(d.uuid)
    dialogs.value = dialogs.value.filter(item => item.uuid !== d.uuid)
    if (selectedDialog.value?.uuid === d.uuid) {
      selectedDialog.value = null
      messages.value = []
    }
  } catch (e) {
    console.error('Failed to delete dialog', e)
  }
}

async function selectDialog(d) {
  selectedDialog.value = d
  input.value = ''
  messages.value = []
  localStorage.setItem('session_id', d.uuid)
  let data = await API.getSessionMessages(d.uuid)
  messages.value = data.messages
}

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
  await API.queryStream(
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

:deep(::-webkit-scrollbar) {
  width: 0px;
  height: 0px;
}

/* :deep(::-webkit-scrollbar-track) {
  background: #f1f1f1;
  border-radius: 0px;
}

:deep(::-webkit-scrollbar-thumb) {
  background: grey;
  border-radius: 0px;
  transition: background 0.3s;
}

:deep(::-webkit-scrollbar-thumb:hover) {
  background: #155A9E;
} */
</style>
