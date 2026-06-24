<template>
  <v-container fluid class="pa-4">
    <div class="d-flex align-center mb-2">
      <h2 class="text-h5">文档管理</h2>
      <v-spacer />
      <v-btn color="primary" prepend-icon="mdi-refresh" variant="text" :loading="loading" @click="loadDocs">
        刷新
      </v-btn>
    </div>

    <v-alert v-if="error" type="error" closable class="mb-2" @click:close="error = ''">
      {{ error }}
    </v-alert>

    <v-data-table
      :headers="headers"
      :items="docs"
      :loading="loading"
      loading-text="加载中..."
      no-data-text="暂无文档"
      hover
      density="compact"
      class="doc-table"
    >
      <template #item.name="{ item }">
        <div class="d-flex align-center">
          <v-icon icon="mdi-file-document-outline" class="mr-2" color="primary" />
          <span class="doc-name">{{ item.name }}</span>
        </div>
      </template>
      <template #item.created="{ item }">
        <span class="text-no-wrap">{{ item.metadata?.created || '-' }}</span>
      </template>
    </v-data-table>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'

const headers = [
  { title: '文件名', key: 'name', sortable: true },
  { title: '创建时间', key: 'created', sortable: true },
]

const docs = ref([])
const loading = ref(false)
const error = ref('')

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

onMounted(loadDocs)
</script>

<style scoped>
.doc-table :deep(table) {
  table-layout: fixed;
  width: 100%;
}
.doc-table :deep(colgroup) {
  display: none;
}
.doc-table :deep(th:first-child),
.doc-table :deep(td:first-child) {
  width: auto;
}
.doc-table :deep(th:last-child),
.doc-table :deep(td:last-child) {
  width: 160px;
}
.doc-name {
  word-break: break-all;
  line-height: 1.3;
}
</style>
