import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import '@/assets/style/reset.css'
// import '@/assets/style/index.css'
import '@/assets/style/global.css'
import App from './App.jsx'

const root = createRoot(document.getElementById('root')) // 처음 한 번만 실행
root.render(
  <StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </StrictMode>
)
