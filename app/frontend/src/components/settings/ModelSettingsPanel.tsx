import { useEffect, useState } from 'react'
import { settingsApi } from '../../services/settingsApi'

export function ModelSettingsPanel() {
  const [text, setText] = useState('加载中...')

  useEffect(() => {
    settingsApi
      .getLLMSettings()
      .then((v) => setText(`${v.llm_provider} / ${v.llm_model}`))
      .catch(() => setText('模型设置读取失败'))
  }, [])

  return <div style={{ padding: 8, fontSize: 12, color: '#666' }}>模型: {text}</div>
}
