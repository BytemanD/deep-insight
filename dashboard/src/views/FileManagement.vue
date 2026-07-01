<template>
  <v-container fluid class="pa-4">
    <div class="d-flex align-center mb-2">
      <h2 class="text-h5">文档管理</h2>
      <v-spacer />
      <v-btn color="primary" prepend-icon="mdi-upload" variant="text" :loading="uploading" @click="dialog = true">
        上传文件
      </v-btn>
      <v-btn color="primary" prepend-icon="mdi-refresh" variant="text" :loading="loading" @click="loadDocs">
        刷新
      </v-btn>
    </div>

    <v-alert v-if="error" type="error" closable class="mb-2" @click:close="error = ''">
      {{ error }}
    </v-alert>

    <v-data-table :headers="headers" :items="docs" :loading="loading" loading-text="加载中..." no-data-text="暂无文档" hover
      density="compact">
      <template #item.name="{ item }">
        <span class="doc-name">{{ item.name }}</span>
      </template>
      <template #item.file_size="{ item }">
        <span class="text-no-wrap">{{ formatSize(item.file_size) }}</span>
      </template>
      <template #item.status="{ item }">
        <v-chip :color="statusColor(item.status)" size="small">{{ statusLabel(item.status) }}</v-chip>
      </template>
      <template #item.created_at="{ item }">
        <span class="text-no-wrap">{{ formatDate(item.created_at) }}</span>
      </template>
    </v-data-table>

    <v-dialog v-model="dialog" max-width="500">
      <v-card>
        <v-card-title>上传文档</v-card-title>
        <v-card-text>
          <v-file-input v-model="file" label="选择文件" accept=".txt,.md,.json,.csv,.xml,.yaml,.yml" show-size
            :disabled="uploading" :rules="[fileSizeRule]" @update:model-value="fileError = ''" />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="dialog = false" :disabled="uploading">取消</v-btn>
          <v-btn color="primary" variant="elevated" :loading="uploading" :disabled="!canUpload"
            @click="uploadFile">
            上传
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../api'

const headers = [
  { title: '文件名', key: 'name', sortable: true },
  { title: '大小', key: 'file_size', sortable: true },
  { title: '状态', key: 'status', sortable: true },
  { title: '创建时间', key: 'created_at', sortable: true },
]

const docs = ref([])
const loading = ref(false)
const error = ref('')
const dialog = ref(false)
const file = ref(null)
const uploading = ref(false)
const fileError = ref('')
const canUpload = computed(() => file.value && file.value.size > 0)

function fileSizeRule(v) {
  if (!v) return true
  if (v.size === 0) {
    fileError.value = '请选择非空文件'
    return '请选择非空文件'
  }
  fileError.value = ''
  return true
}

function formatSize(bytes) {
  if (!bytes) return '-'
  const units = ['B', 'KB', 'MB', 'GB']
  let i = 0
  let size = bytes
  while (size >= 1024 && i < units.length - 1) {
    size /= 1024
    i++
  }
  return `${size.toFixed(i === 0 ? 0 : 1)} ${units[i]}`
}

function formatDate(dateStr) {
  if (!dateStr) return '-'
  const d = new Date(dateStr)
  return d.toLocaleString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' })
}

function statusColor(status) {
  const map = { pending: 'warning', parsing: 'info', parsed: 'success', failed: 'error' }
  return map[status] || 'grey'
}

function statusLabel(status) {
  const map = { pending: '待解析', parsing: '解析中', parsed: '解析完成', failed: '解析失败' }
  return map[status] || status
}

async function loadDocs() {
  loading.value = true
  error.value = ''
  try {
    const data = await api.listDocs()
    docs.value = data.docs
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

async function uploadFile() {
  if (!file.value) return
  if (file.value.size === 0) {
    fileError.value = '请选择非空文件'
    return
  }
  uploading.value = true
  error.value = ''
  try {
    const res = await api.uploadDoc(file.value)
    if (!res.ok) {
      const msg = await res.text().catch(() => res.statusText)
      throw new Error(msg)
    }
    dialog.value = false
    file.value = null
    await loadDocs()
  } catch (e) {
    error.value = e.message
  } finally {
    uploading.value = false
  }
}

onMounted(loadDocs)
</script>

<style scoped>
.doc-name {
  word-break: break-all;
  line-height: 1.3;
}
</style>
