const BASE = '/api/v1'

class API {
  async request(url, options = {}) {
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers,
    }
    const projectId = localStorage.getItem('project_id')
    const sessionId = localStorage.getItem('session_id')
    if (projectId) {
      headers['X-Project-Id'] = projectId
    }
    if (sessionId) {
      headers['X-Session-Id'] = sessionId
    }

    const res = await fetch(`${BASE}${url}`, {
      ...options,
      headers,
    })
    if (!res.ok) {
      const msg = await res.text().catch(() => res.statusText)
      throw new Error(`API ${res.status}: ${msg}`)
    }
    console.log('API', res)
    if (res.status === 204) {
      return {}
    } else {
      return res.json()
    }
  }
  async stream_request(url, options = {}) {
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers,
    }
    const projectId = localStorage.getItem('project_id')
    const sessionId = localStorage.getItem('session_id')
    if (projectId) {
      headers['X-Project-Id'] = projectId
    }
    if (sessionId) {
      headers['X-Session-Id'] = sessionId
    }
    // 获取 reader
    const reader = response.body.getReader();
    // 使用 TextDecoder 将二进制流转换为字符串
    const decoder = new TextDecoder();
    while (true) {
      // 读取数据块 (done 表示是否结束, value 是 Uint8Array)
      const { done, value } = await reader.read();

      if (done) {
        console.log('流结束');
        break;
      }

      // 解码当前块
      const chunk = decoder.decode(value, { stream: true });

      // 处理数据（注意：这里可能收到的是不完整的消息，需要按分隔符切割）
      console.log('收到原始数据:', chunk);

      // 假设数据是以 \n\n 分隔的（SSE 格式）
      console.log('收到数据:', chunk);
      // processChunk(chunk);
    }

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
  chat(text) {
    return this.stream_request('/query', {
      method: 'POST',
      body: JSON.stringify({ text }),
    })
  }
  queryStream(text, onChunk, onDone, onError) {
    const projectId = localStorage.getItem('project_id') || ''
    const headers = {
      'Content-Type': 'application/json',
      ...(projectId ? { 'X-Project-Id': projectId } : {}),
    }
    fetch(`${BASE}/query`, {
      method: 'POST',
      headers,
      body: JSON.stringify({ text }),
    }).then(async (res) => {
      if (!res.ok) {
        const msg = await res.text().catch(() => res.statusText)
        throw new Error(`API ${res.status}: ${msg}`)
      }
      const reader = res.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''
      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() || ''
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6)
            if (data === '[DONE]') {
              onDone && onDone()
              return
            }
            try {
              const parsed = JSON.parse(data)
              if (parsed.type === 'thinking') {
                onChunk && onChunk(parsed.content, 'thinking')
                continue
              }
              if (parsed.type === 'text') {
                onChunk && onChunk(parsed.content, 'text')
              } else if (parsed.type === 'error') {
                onError && onError(parsed.content, 'error')
              }
            } catch {
              onChunk && onChunk(data, 'error')
            }
          }
        }
      }
      onDone && onDone()
    }).catch((e) => {
      onError && onError(e.message)
    })
  }

  listSessions() {
    return this.request(`/sessions`)
  }

  createSession(projectUuid, name) {
    return this.request('/sessions', {
      method: 'POST',
      body: JSON.stringify({ project_uuid: projectUuid, name }),
    })
  }

  deleteSession(uuid) {
    return this.request(`/sessions/${uuid}`, { method: 'DELETE' })
  }
}

export default new API()
