<template>
  <v-app>
    <v-app-bar app elevation="1" color="primary-darken-1">
      <v-app-bar-nav-icon @click="drawer = !drawer" />
      <v-app-bar-title>Deep Insight</v-app-bar-title>
      <v-spacer />
      <v-select v-model="selectedProject" :items="projects" item-title="name" item-value="uuid" density="compact"
        variant="solo" hide-details prepend-inner-icon="mdi-layers-outline" style="min-width: 160px; max-width: 220px"
        @update:model-value="onProjectChange">
      </v-select>
      <v-btn icon="mdi-theme-light-dark" @click="toggleTheme" />
    </v-app-bar>

    <v-navigation-drawer v-model="drawer" app :permanent="!isMobile" :temporary="isMobile" :rail="!isMobile && !drawer"
      @click="expandDrawer" width="200">
      <!-- <v-list-item class="px-2" title="Deep Insight" subtitle="知识库">
        <template #prepend>
          <v-avatar color="primary" class="text-white">DI</v-avatar>
        </template>
</v-list-item>
<v-divider /> -->

      <v-list nav>
        <v-list-item prepend-icon="mdi-chat" title="对话" :to="{ name: 'Conversation' }"
          :active="route.name === 'Conversation'" color="primary" slim />
        <v-list-item prepend-icon="mdi-file-document-multiple" title="文档管理" :to="{ name: 'FileManagement' }"
          :active="route.name === 'FileManagement'" color="primary" slim />
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, computed, onMounted, provide } from 'vue'
import { useRoute } from 'vue-router'
import { useTheme, useDisplay } from 'vuetify'
import api from './api'

const route = useRoute()
const theme = useTheme()
const { smAndDown } = useDisplay()
const isMobile = computed(() => smAndDown.value)
const drawer = ref(true)

const projects = ref([])
const selectedProject = ref(null)
provide('projectId', selectedProject)

onMounted(async () => {
  try {
    const res = await api.listProjects()
    console.log('xxxxxxxxxxx', res)
    projects.value = res.projects
    selectInitialProject()
  } catch (e) {
    console.error('Failed to load projects', e)
  }
})

function selectInitialProject() {
  if (!projects.value.length) return
  const saved = localStorage.getItem('project_id')
  if (saved && projects.value.some(p => p.uuid === saved)) {
    selectedProject.value = saved
  } else {
    selectedProject.value = projects.value[0].uuid
    localStorage.setItem('project_id', selectedProject.value)
  }
}

function onProjectChange(val) {
  if (val) {
    localStorage.setItem('project_id', val)
  }
}

function toggleTheme() {
  theme.global.name.value = theme.global.name.value === 'light' ? 'dark' : 'light'
}

function expandDrawer() {
  if (!isMobile.value && !drawer.value) {
    drawer.value = true
  }
}
</script>
