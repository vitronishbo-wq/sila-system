import { useState, useEffect } from 'react'
import { Toaster, toast } from 'react-hot-toast'
import DashboardLayout from './components/layout/DashboardLayout'
import DashboardPage from './modules/dashboard/DashboardPage'

function App() {
  const [token, setToken] = useState(localStorage.getItem('access_token'))
  const [user, setUser] = useState<any>(null)
  const [email, setEmail] = useState('admin@sila.gov.ao')
  const [password, setPassword] = useState('adm123')

  useEffect(() => {
    if (token) {
      fetch('http://localhost:8000/api/v1/auth/me', {
        headers: { Authorization: `Bearer ${token}` }
      })
        .then(r => r.ok ? r.json() : null)
        .then(setUser)
        .catch(() => {
          localStorage.removeItem('access_token')
          setToken(null)
        })
    }
  }, [token])

  const login = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const res = await fetch('http://localhost:8000/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      })
      const data = await res.json()
      if (res.ok) {
        localStorage.setItem('access_token', data.access_token)
        setToken(data.access_token)
        toast.success('Bem-vindo ao SILA-System!')
      } else {
        toast.error(data.detail || 'Credenciais inválidas')
      }
    } catch {
      toast.error('Erro de conexão')
    }
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    setToken(null)
    setUser(null)
    toast.success('Até à próxima!')
  }

  if (!token || !user) {
    return (
      <div style={{
        minHeight:'100vh',
        background:'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
        display:'flex',
        alignItems:'center',
        justifyContent:'center'
      }}>
        <div style={{
          background:'white',
          padding:'4rem',
          borderRadius:'24px',
          boxShadow:'0 25px 60px rgba(0,0,0,0.3)',
          width:'440px',
          textAlign:'center'
        }}>
          <h1 style={{fontSize:'3.5rem', fontWeight:'bold', color:'#4f46e5', marginBottom:'2rem'}}>
            SILA-System
          </h1>
          <form onSubmit={login} style={{display:'grid', gap:'1.2rem'}}>
            <input value={email} onChange={e=>setEmail(e.target.value)} placeholder="Email" required
              style={{padding:'18px', borderRadius:'12px', border:'1px solid #e5e7eb', fontSize:'1.1rem'}} />
            <input type="password" value={password} onChange={e=>setPassword(e.target.value)} placeholder="Senha" required
              style={{padding:'18px', borderRadius:'12px', border:'1px solid #e5e7eb', fontSize:'1.1rem'}} />
            <button type="submit" style={{
              padding:'18px',
              background:'#6366f1',
              color:'white',
              border:'none',
              borderRadius:'12px',
              fontSize:'1.3rem',
              fontWeight:'bold',
              cursor:'pointer'
            }}>
              Entrar
            </button>
          </form>
          <p style={{marginTop:'2rem', color:'#6b7280'}}>
            admin@sila.gov.ao • adm123
          </p>
        </div>
        <Toaster position="top-right" />
      </div>
    )
  }

  return (
    <DashboardLayout userName={user?.name || user?.email} onLogout={logout}>
      <DashboardPage />
    </DashboardLayout>
  )
}

export default App
