const BASE = '/api/v1'

class API {
  async request(url, options = {}) {
    const projectId = localStorage.getItem('project_id') || ''
    const headers = {
      'Content-Type': 'application/json',
      ...(projectId ? { 'X-Project-Id': projectId } : {}),
      ...options.headers,
    }
    const res = await fetch(`${BASE}${url}`, {
      ...options,
      headers,
    })
    if (!res.ok) {
      const msg = await res.text().catch(() => res.statusText)
      throw new Error(`API ${res.status}: ${msg}`)
    }
    return res.json()
  }

  listDocs() {
    return this.request('/docs')
  }

  listProjects() {
    return this.request('/projects')
  }

  query(text) {
    return this.request('/query', {
      method: 'POST',
      body: JSON.stringify({ text }),
    })
  }

  listDialogs(projectUuid) {
    const params = projectUuid ? `?project_uuid=${encodeURIComponent(projectUuid)}` : ''
    return this.request(`/dialogs${params}`)
  }

  createDialog(projectUuid, name) {
    return this.request('/dialogs', {
      method: 'POST',
      body: JSON.stringify({ project_uuid: projectUuid, name }),
    })
  }

  deleteDialog(uuid) {
    return this.request(`/dialogs/${uuid}`, { method: 'DELETE' })
  }
}

export default new API()
