import { useState } from 'react'
import Editor from "@monaco-editor/react"
import './App.css'

function App() {
  const [code, setCode] = useState("")
  const [language, setLanguage] = useState("python")
  const [result, setResult] = useState("")
  const [loading, setLoading] = useState(false)
  const [copied, setCopied] = useState(false)
  const [theme, setTheme] = useState('light')
  const [darkMode, setDarkMode] = useState(false)

  const handleSubmit = async () => {
    setLoading(true)
    setResult("")
    setCopied(false)

    try {
      const res = await fetch("https://code-humanizer-backend.onrender.com/humanize", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ code, language })
      })
      const data = await res.json()
      setResult(data.humanized_code)
    } catch (err) {
      setResult("# Error: Failed to humanize code.")
    } finally {
      setLoading(false)
    }
  }

  const handleCopy = () => {
    navigator.clipboard.writeText(result)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const monacoLangMap = {
    python: "python",
    java: "java",
    cpp: "cpp",
    javascript: "javascript"
  }

  const handleThemeToggle = () => {
    const newTheme = darkMode ? 'light' : 'vs-dark'
    setTheme(newTheme)
    setDarkMode(!darkMode)
  }

  return (
    <div className={`container ${darkMode ? 'dark' : ''}`}>
      <h1>AI Code Humanizer</h1>

      <div className='controls'>
        <select value={language} onChange={(e) => setLanguage(e.target.value)}>
          <option value="python">Python</option>
          <option value="java">Java</option>
          <option value="cpp">C++</option>
          <option value="javascript">JavaScript</option>
        </select>
        <button onClick={handleSubmit} disabled={loading}>
          {loading ? "Humanizing..." : "Humanize Code"}
        </button>
        <button onClick={handleThemeToggle}>
          {darkMode ? "☀ Light Mode" : "🌙 Dark Mode"}
        </button>
      </div>

      <div className='editor-box'>
        <Editor
          height="300px"
          defaultLanguage='python'
          language={monacoLangMap[language]}
          value={code}
          onChange={(val) => setCode(val || "")}
          theme={theme}
          options={{
            fontSize: 14,
            minimap: { enabled: false },
            lineNumbers: "on",
          }}
        />
      </div>

      <h3>Humanized Output:</h3>

      {loading ? (
        <div className='spinner'>Please wait...</div>
      ) : (
        <>
          <div className='copy-bar'>
            <button onClick={handleCopy}>
              {copied ? "Copied!" : "Copy Code"}
            </button>
          </div>
          <Editor
            height="300px"
            language={monacoLangMap[language]}
            value={result}
            theme={theme}
            options={{
              fontSize: 14,
              readOnly: true,
              minimap: { enabled: false },
              lineNumbers: "on",
            }}
          />
        </>
      )}
    </div>
  )
}

export default App