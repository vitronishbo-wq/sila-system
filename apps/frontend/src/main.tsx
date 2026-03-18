import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import keycloak from './auth/keycloak'

const rootElement = document.getElementById('root');

if (!rootElement) {
  throw new Error('Falha ao encontrar o elemento root. Verifique seu index.html.');
}

keycloak.init({
  onLoad: "login-required"
}).then(auth => {
  if (!auth) {
    window.location.reload()
    return
  }
  console.log("Authenticated")

  createRoot(rootElement).render(
    <StrictMode>
      <App />
    </StrictMode>,
  )
}).catch(error => {
  console.error("Keycloak init failed", error)
})
