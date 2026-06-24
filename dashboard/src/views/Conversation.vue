<template>
  <v-row>
    <v-col cols="1" style="padding: 20px 20px">
      <v-btn>+ 新建会话</v-btn>
    </v-col>
    <v-col cols="11" style="">
      <v-virtual-scroll ref="scrollRef" :items="messages" height="600" item-height="48"
        style="border: 1px solid #e0e0e0; padding: 20px 20px;">
        <template #default="{ item }">
          <div :class="['d-flex mb-3', item.role === 'user' ? 'justify-end' : 'justify-start']">
            <v-card :subtitle="item.role === 'user' ? '你' : 'AI'"
              :class="['pa-3', item.role === 'user' ? 'bg-primary' : 'bg-surface-variant']"
              :max-width="isMobile ? '85%' : '70%'" rounded="lg">
              <div class="text-body-2" style="white-space: pre-wrap; word-break: break-word; min-width: 200px;">
                {{ item.content }}
              </div>
            </v-card>
          </div>
        </template>
      </v-virtual-scroll>
      <v-card v-if="loading">loading</v-card>
      <v-divider></v-divider>
      <v-footer>
        <v-text-field v-model="input" variant="outlined" density="compact" placeholder="输入消息..." hide-details
          :disabled="loading" @keydown.enter.prevent="send">
          <template #append-inner>
            <v-btn icon="mdi-send" variant="text" color="primary" :loading="loading" :disabled="!input.trim()"
              @click="send" />
          </template>
        </v-text-field>

      </v-footer>
    </v-col>
  </v-row>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import { useDisplay } from 'vuetify'
import api from '../api'

const { smAndDown } = useDisplay()
const isMobile = smAndDown

const input = ref('')
const loading = ref(false)
const messages = ref([])
const scrollRef = ref(null)

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
    const el = scrollRef.value?.$el
    if (el) el.scrollTop = el.scrollHeight
  }, 50)
}
</script>

<style scoped>
.fill-height {
  height: calc(100vh - 64px);
}
</style>
