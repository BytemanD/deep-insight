<template>
  <v-app>
    <v-navigation-drawer width="200" permanent :rail-width="60" :rail="drawer ? false : true">
      <template v-slot:prepend>
        <v-list-item v-if="drawer" class="pl-3 py-2" title="Deep Insight">
          <template v-slot:prepend>
            <v-avatar color="primary" class="text-white" size="32" variant="flat">DI</v-avatar>
          </template>
        </v-list-item>
        <v-list-item v-else class="pl-3 py-2">
          <v-avatar color="primary" class="text-white" size="32" variant="flat">DI</v-avatar>
        </v-list-item>

      </template>
      <v-divider />

      <v-list nav>
        <v-list-item prepend-icon="mdi-chat" title="对话" :to="{ name: 'Conversation' }"
          :active="route.name === 'Conversation'" color="primary" slim />
        <v-list-item prepend-icon="mdi-file-document-multiple" title="文档管理" :to="{ name: 'FileManagement' }"
          :active="route.name === 'FileManagement'" color="primary" slim />
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <v-app-bar density="compact" flat
        style="background: linear-gradient(135deg, rgb(var(--v-theme-primary)), rgb(var(--v-theme-accent)))">
        <v-app-bar-nav-icon color="white" @click="drawer = !drawer" />
        <v-toolbar-title>
          <v-select v-model="selectedProject" :items="projects" item-title="name" item-value="uuid" density="compact"
            variant="solo" hide-details prepend-inner-icon="mdi-layers-outline"
            style="min-width: 140px; max-width: 200px" @update:model-value="onProjectChange">
          </v-select>
        </v-toolbar-title>
        <v-btn icon="mdi-plus" @click="projectDialog = true" />
        <v-btn icon="mdi-theme-light-dark" @click="toggleTheme" />
      </v-app-bar>

      <router-view :key="selectedProject" />

      <v-dialog v-model="projectDialog" max-width="400">
        <v-card>
          <v-card-title>创建项目</v-card-title>
          <v-card-text>
            <v-text-field v-model="projectName" label="项目名称" variant="outlined" hide-details autofocus
              @keyup.enter="createProject" />
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn variant="text" @click="projectDialog = false">取消</v-btn>
            <v-btn color="primary" variant="elevated" :loading="projectCreating" :disabled="!projectName"
              @click="createProject">创建</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
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

const projectDialog = ref(false)
const projectName = ref('')
const projectCreating = ref(false)

async function createProject() {
  if (!projectName.value) return
  projectCreating.value = true
  try {
    const res = await api.createProject(projectName.value)
    projects.value.push(res)
    selectedProject.value = res.uuid
    localStorage.setItem('project_id', res.uuid)
    projectDialog.value = false
    projectName.value = ''
  } catch (e) {
    console.error('Failed to create project', e)
  } finally {
    projectCreating.value = false
  }
}

function toggleTheme() {
  theme.global.name.value = theme.global.name.value === 'light' ? 'dark' : 'light'
}

</script>
