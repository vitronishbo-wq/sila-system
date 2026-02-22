import React, { useState, useEffect } from 'react';
import { HashRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { User, UserRole } from './types';
import { authService } from './services/authService';
import { ProtectedRoute } from './components/ProtectedRoute';
import axios from 'axios';

// Pages
import PublicLanding from './pages/PublicLanding';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Layout from './components/Layout';
import PaymentsPage from './modules/pagamentos/PaymentsPage';
import CitizenLogin from './pages/CitizenLogin';
import CitizenPortal from './pages/CitizenPortal';
import Register from './pages/Register';

// Componente de diagnóstico (temporário)
const AuthDebugger: React.FC = () => {
  const [debugInfo, setDebugInfo] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDebug = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/debug/auth-check');
        setDebugInfo(response.data);
      } catch (error) {
        console.error('Erro no debug:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDebug();
  }, []);

  if (loading) return (
    <div className="p-8 font-mono">
      <div className="animate-spin inline-block w-4 h-4 border-2 border-yellow-500 rounded-full mr-2"></div>
      Diagnosticando...
    </div>
  );

  return (
    <div className="p-8 font-mono bg-slate-900 text-green-400 min-h-screen">
      <h2 className="text-xl font-bold mb-4 border-b border-green-800 pb-2">🔍 Diagnóstico de Autenticação</h2>
      <pre className="bg-black p-4 rounded overflow-auto mb-4">{JSON.stringify(debugInfo, null, 2)}</pre>
      {debugInfo?.recommended_dashboard && (
        <div className="mt-4 p-4 border border-green-800 rounded">
          <h3 className="text-lg font-bold">Dashboard Recomendado:</h3>
          <p className="mb-2">Baseado no seu papel: <span className="text-yellow-500 font-bold">{debugInfo.user?.role}</span></p>
          <a
            href={`#${debugInfo.recommended_dashboard}`}
            className="inline-block bg-green-700 text-white px-4 py-2 rounded hover:bg-green-600 transition"
          >
            Ir para {debugInfo.recommended_dashboard}
          </a>
        </div>
      )}
    </div>
  );
};

// Componente de redirecionamento inteligente
const SmartRedirect: React.FC = () => {
  const [redirectTo, setRedirectTo] = useState<string | null>(null);

  useEffect(() => {
    const checkAuth = async () => {
      const user = await authService.getMe().catch(() => null);
      if (user) {
        setRedirectTo(authService.getDashboardForRole(user.role));
      } else {
        setRedirectTo('/login');
      }
    };
    checkAuth();
  }, []);

  if (!redirectTo) return (
    <div className="min-h-screen flex items-center justify-center bg-slate-900 text-white">
      <div className="animate-pulse text-lg">Redirecionando...</div>
    </div>
  );

  return <Navigate to={redirectTo} replace />;
};

const App: React.FC = () => {
  const [user, setUser] = useState<User | null>(() => {
    const saved = localStorage.getItem('user');
    return saved ? JSON.parse(saved) : null;
  });

  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const initAuth = async () => {
      const token = localStorage.getItem('token');
      if (token) {
        try {
          const userData = await authService.getMe();
          setUser(userData);
          localStorage.setItem('user', JSON.stringify(userData));
        } catch (err) {
          localStorage.clear();
          setUser(null);
        }
      }
      setIsLoading(false);
    };
    initAuth();
  }, []);

  const handleLoginSuccess = async (token: string) => {
    localStorage.setItem('token', token);
    const userData = await authService.getMe();
    setUser(userData);
    localStorage.setItem('user', JSON.stringify(userData));

    // Redirect based on role
    window.location.hash = authService.getDashboardForRole(userData.role);
  };

  const handleLogout = () => {
    localStorage.clear();
    setUser(null);
    window.location.hash = '/';
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-slate-900 text-white">
        <i className="fa-solid fa-circle-notch fa-spin text-4xl text-yellow-500 mb-4"></i>
        <p className="text-lg font-medium animate-pulse">SILA System - A carregar...</p>
      </div>
    );
  }

  return (
    <HashRouter>
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<PublicLanding />} />
        <Route path="/login" element={
          user ? <Navigate to="/dashboard" /> : <Login onLoginSuccess={handleLoginSuccess} />
        } />
        <Route path="/citizen/login" element={
          user ? <Navigate to="/dashboard" /> : <CitizenLogin onLoginSuccess={handleLoginSuccess} onBackClick={() => window.location.hash = '/'} />
        } />
        <Route path="/register" element={<Register />} />

        {/* Diagnostic Route */}
        <Route path="/debug-auth" element={<AuthDebugger />} />

        {/* Smart Redirect to Role Dashboard */}
        <Route path="/dashboard" element={<SmartRedirect />} />
        <Route path="/smart-redirect" element={<SmartRedirect />} />

        {/* Protected Admin Channel */}
        <Route
          path="/admin/*"
          element={
            <ProtectedRoute 
              user={user}
              requiredRole={[
                UserRole.ADMIN_SUPER,
                UserRole.ADMIN_CENTRAL,
                UserRole.ADMIN_PROVINCIAL,
                UserRole.ADMIN_MUNICIPAL,
                UserRole.ADMIN_COMMUNAL
              ]}>
              <Layout user={user!} onLogout={handleLogout}>
                <Routes>
                  <Route path="/" element={<Dashboard user={user!} />} />
                  <Route path="/citizens" element={<div className="p-8"><h2 className="text-2xl font-bold">Módulo de Cidadãos em construção</h2></div>} />
                  <Route path="/documents" element={<div className="p-8"><h2 className="text-2xl font-bold">Módulo de Documentos em construção</h2></div>} />
                  <Route path="/payments" element={<PaymentsPage />} />
                  <Route path="/territory" element={<div className="p-8"><h2 className="text-2xl font-bold">Hierarquia de Territórios em construção</h2></div>} />
                  <Route path="/observability" element={<div className="p-8"><h2 className="text-2xl font-bold">Observabilidade em construção</h2></div>} />
                </Routes>
              </Layout>
            </ProtectedRoute>
          }
        />

        {/* Protected Citizen Channel */}
        <Route
          path="/citizen/*"
          element={
            <ProtectedRoute user={user} requiredRole={[UserRole.CITIZEN]}>
              <Routes>
                <Route path="/portal" element={<CitizenPortal onLogout={handleLogout} />} />
              </Routes>
            </ProtectedRoute>
          }
        />

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </HashRouter>
  );
};

export default App;
