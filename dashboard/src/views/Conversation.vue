<template>
  <v-row no-gutters class="fill-height">
    <v-col xl="1" lg="2" sm="3" class="d-flex flex-column" style="border-right: 1px solid #e0e0e0;">
      <div class="pa-3">
        <v-btn block color="primary" size="large" @click="createDialog" rounded prepend-icon="mdi-plus">新建会话</v-btn>
      </div>
      <div class="pa-2 text-caption text-medium-emphasis text-center">{{ dialogs.length }} 个会话</div>
      <v-divider></v-divider>
      <v-virtual-scroll :items="dialogs" height="100" class="sidebar-scroll">
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
    </v-col>
    <v-col class="d-flex flex-column" xl="11" lg="10" sm="9">
      <div v-if="!selectedDialog" class="d-flex align-center justify-center flex-grow-1 text-medium-emphasis">
        请选择或创建一个会话
      </div>
      <template v-else>
        <v-virtual-scroll ref="scrollRef" height="260px" class="pa-2" v-model="messages" :items="messages"
          id="conversation">
          <template v-slot:default="{ item, index }">
            <v-col v-if="item.role === 'user'" class="d-flex align-end flex-column">
              <div style="max-width: 70%;">
                <v-alert class="d-inline-block rounded-te-0 text-body-large" rounded="xl" color="info" density="compact"
                  style="font-size: small;">
                  {{ item.content }}
                </v-alert>
              </div>
            </v-col>
            <v-col v-else class="d-flex align-start flex-column">
              <div style="max-width: 70%; word-break: break-all; overflow-x: visible;">
                <!-- 思考过程 -->
                <v-expansion-panels class="mb-1 border-s-lg" elevation="0" v-if="item.thinking">
                  <v-expansion-panel>
                    <v-expansion-panel-title style="" density="compact">
                      <span class="text-warning" v-if="!item.content && loading">思考中</span>
                      <span v-else class="text-info">已思考</span>
                      <template v-slot:actions>
                        <ThinkingDots v-if="!item.content && loading" />
                        <v-icon v-else>mdi-check</v-icon>
                      </template>
                    </v-expansion-panel-title>
                    <v-expansion-panel-text style="">
                      <p class="d-inline-block" density="compact" style="font-size: small;"
                        v-html="marked(item.thinking)">
                      </p>
                      <!-- <p style="font-size: small;">{{ item.thinking }}</p> -->
                    </v-expansion-panel-text>
                  </v-expansion-panel>
                </v-expansion-panels>
                <v-card v-if="item.content" class="rounded-ts-0 px-2" variant="tonal" rounded="xl">
                  <v-alert v-if="item.type === 'error'" variant="text" type="error" density="compact">
                    {{ item.content }}
                  </v-alert>
                  <v-card-text v-else v-html="marked(item.content)">
                  </v-card-text>
                </v-card>

                <!-- <v-alert v-if="item.content" class="d-inline-block rounded-bs-0 px-8" rounded="xl" density="compact"
                  style="font-size: small;" v-html="marked(item.content)">
                </v-alert>
                <div
                  style="border: 2px solid red; width: 500px; white-space: pre-wrap; word-break: break-all; overflow-x: wrap;">
                  <v-alert>{{ marked(item.content) }}</v-alert>
                  <v-alert v-html="marked(item.content)"></v-alert>
                </div> -->
              </div>
            </v-col>
          </template>

        </v-virtual-scroll>

        <v-footer class="pb-1  px-10" height="auto" style="flex: 0 0 auto;">
          <v-col>
            <v-textarea v-model="input" variant="outlined" placeholder="随便问点什么(Enter 发送, Shift+Enter 换行)..."
              hide-details :disabled="loading || !selectedDialog" @keydown.enter="onEnter" rows="2" auto-grow
              :max-rows="4" class="pa-4 pb-0">
              <template #append-inner>
                <v-btn icon="mdi-send" variant="text" color="primary" :loading="loading" :disabled="!input.trim()"
                  @click="send" class="pl-4" />
              </template>
            </v-textarea>
            <div class="d-flex flex-row-reverse mb-1 px-4" style="width: 100%;">
              <v-sheet>
                <v-select v-model="selectedModel" :items="models" item-title="label" item-value="value"
                  density="compact" variant="text" hide-details class="model-selector" />
              </v-sheet>
            </div>
          </v-col>
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
import ThinkingDots from '../components/ThinkingDots.vue'


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

const models = ref([])
const selectedModel = ref(localStorage.getItem('selected_model') || '')

async function loadModels() {
  try {
    const res = await API.listModels()
    models.value = res.models || []
    if (!selectedModel.value && models.value.length) {
      selectedModel.value = models.value[0].value
    }
  } catch (e) {
    console.error('Failed to load models', e)
  }
}


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
  proxyLinks()
}

function onEnter(e) {
  if (e.shiftKey) return
  e.preventDefault()
  send()
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
  localStorage.setItem('selected_model', selectedModel.value)
  await API.queryStream(
    text,
    selectedModel.value,
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
    (error, type) => {
      if (!hasError) {
        hasError = true
        messages.value[messages.value.length - 1].content = error
        messages.value[messages.value.length - 1].type = type || 'error'
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

function proxyLinks() {
  console.log('proxy links ...')
  document.getElementById('conversation').addEventListener('click', function (e) {
    // 检查点击的是否是 a 标签
    const link = e.target.closest('a');
    if (!link) return;
    // 阻止默认跳转
    e.preventDefault();
    // 获取文件链接
    const fileUrl = link.getAttribute('href');
    console.log('download', fileUrl)
    window.open(`/api/v1/docs/download?path=${fileUrl}`, '_self')
  });
}

onMounted(async () => {
  await loadModels()
  await loadDialogs()
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

.compact-input {
  margin: 0;
}

:deep(.compact-input .v-field) {
  min-height: 32px;
}

:deep(.compact-input .v-field__input) {
  padding-top: 2px;
  padding-bottom: 2px;
  min-height: 24px;
  font-size: 0.875rem;
}

:deep(.compact-input .v-field__append-inner) {
  padding-top: 2px;
  padding-bottom: 2px;
}

:deep(.send-btn) {
  margin: -6px;
}

.toolbar {
  border-top: 1px solid rgba(var(--v-border-color), 0.3);
  background: rgba(var(--v-theme-on-surface), 0.02);
}

.model-selector {
  min-width: 140px;
}

:deep(.model-selector .v-field) {
  min-height: 28px;
}

:deep(.model-selector .v-field__input) {
  padding-top: 2px;
  padding-bottom: 2px;
  font-size: 0.75rem;
  min-height: 24px;
}

#conversation ::-webkit-scrollbar {
  width: 0px;
  height: 0px;
}

/* .sidebar-scroll {
  scrollbar-width: thin;
} */

.sidebar-scroll::-webkit-scrollbar {
  width: 4px;
}

.sidebar-scroll::-webkit-scrollbar-thumb {
  background: rgba(var(--v-theme-on-surface), 0.12);
  border-radius: 2px;
}

.sidebar-scroll::-webkit-scrollbar-track {
  background: transparent;
}

:deep(.v-textarea textarea::-webkit-scrollbar) {
  width: 6px;
}

:deep(.v-textarea textarea::-webkit-scrollbar-thumb) {
  background: rgba(var(--v-theme-on-surface), 0.2);
  border-radius: 3px;
}

:deep(.v-textarea textarea::-webkit-scrollbar-track) {
  background: transparent;
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
