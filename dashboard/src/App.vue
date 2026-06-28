<template>
  <v-app>
    <v-app-bar app elevation="1" color="primary-darken-1">
      <v-app-bar-nav-icon @click="drawer = !drawer" />
      <v-app-bar-title>Deep Insight</v-app-bar-title>
      <v-select
        v-model="selectedProject"
        :items="projects"
        item-title="name"
        item-value="uuid"
        label="项目"
        density="compact"
        variant="outlined"
        hide-details
        clearable
        class="ml-4"
        style="max-width: 200px"
        @update:model-value="onProjectChange"
      />
      <v-spacer />
      <v-btn icon="mdi-theme-light-dark" @click="toggleTheme" />
    </v-app-bar>

    <v-navigation-drawer v-model="drawer" app :permanent="!isMobile" :temporary="isMobile" :rail="!isMobile && !drawer"
      @click="expandDrawer">
      <v-list-item class="px-2" title="Deep Insight" subtitle="知识库">
        <template #prepend>
          <v-avatar color="primary" class="text-white">DI</v-avatar>
        </template>
      </v-list-item>

      <v-divider />

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
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useTheme, useDisplay } from 'vuetify'
import api from './api'

const route = useRoute()
const theme = useTheme()
const { smAndDown } = useDisplay()
const isMobile = computed(() => smAndDown.value)
const drawer = ref(true)

const projects = ref([])
const selectedProject = ref(localStorage.getItem('project_id') || null)

onMounted(async () => {
  try {
    const res = await api.listProjects()
    projects.value = res.projects
  } catch (e) {
    console.error('Failed to load projects', e)
  }
})

function onProjectChange(val) {
  if (val) {
    localStorage.setItem('project_id', val)
  } else {
    localStorage.removeItem('project_id')
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
