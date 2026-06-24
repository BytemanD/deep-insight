const BASE = '/api/v1'

class API {
  async request(url, options = {}) {
    const res = await fetch(`${BASE}${url}`, {
      headers: { 'Content-Type': 'application/json', ...options.headers },
      ...options,
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

  query(text) {
    return this.request('/query', {
      method: 'POST',
      body: JSON.stringify({ text }),
    })
  }
}

export default new API()
