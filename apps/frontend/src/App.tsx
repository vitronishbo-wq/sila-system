import React, { useState, useEffect } from 'react';
import { HashRouter, Routes, Route, Navigate } from 'react-router-dom';
import { UserRole } from '@/types';
import type { User } from '@/types';
import { authService } from '@/services/authService';
import { ProtectedRoute } from '@/components/ProtectedRoute';
import axios from 'axios';
import { withApiOrigin } from '@/utils/runtime';

// Pages
import PublicLanding from '@/pages/PublicLanding';
import Login from '@/pages/Login';
import { LoginModalProvider } from '@/hooks/useLoginModal';
import Dashboard from '@/pages/Dashboard';
import Layout from '@/components/Layout';
import PaymentsPage from '@/modules/pagamentos/PaymentsPage';
import CitizenLogin from '@/pages/CitizenLogin';
import CitizenPortal from '@/pages/CitizenPortal';
import IdentityPage from '@/pages/IdentityPage';
import RegistryPage from '@/pages/RegistryPage';
import TaxPage from '@/pages/TaxPage';
import WaterPage from '@/pages/WaterPage';
import EnergyPage from '@/pages/EnergyPage';
import EducationPage from '@/pages/EducationPage';
import EmploymentPage from '@/pages/EmploymentPage';
import LicensingPage from '@/pages/LicensingPage';
import TransportPage from '@/pages/TransportPage';
import NotariesPage from '@/pages/NotariesPage';
import BiometricEnrollmentPage from '@/pages/BiometricEnrollmentPage';
import ServiceRequestPage from '@/pages/ServiceRequestPage';
import ServiceCatalogForm from '@/pages/ServiceCatalogForm';
import UploadDocuments from '@/pages/UploadDocuments';
import MyDocuments from '@/pages/MyDocuments';
import SearchDocuments from '@/pages/SearchDocuments';
import Register from '@/pages/Register';
import QAReview from '@/pages/QAReview';
import AdminCitizens from '@/pages/AdminCitizens';
import AdminCitizenProfile from '@/pages/AdminCitizenProfile';
import AdminCitizenFuc from '@/pages/AdminCitizenFuc';
import AdminDocuments from '@/pages/AdminDocuments';
import AdminDocumentProfile from '@/pages/AdminDocumentProfile';
import AdminExports from '@/pages/AdminExports';
import AdminTerritory from '@/pages/AdminTerritory';
import AdminObservability from '@/pages/AdminObservability';

// Componente de diagnóstico (temporário)
const AuthDebugger: React.FC = () => {
  const [debugInfo, setDebugInfo] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDebug = async () => {
      try {
        const response = await axios.get(withApiOrigin('/api/debug/auth-check'));
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
    localStorage.setItem('access_token', token);
    const userData = await authService.getMe();
    setUser(userData);
    localStorage.setItem('user', JSON.stringify(userData));

    // Redirect based on role
    const pendingService = localStorage.getItem('selected_service');
    if (pendingService && userData.role === UserRole.CITIZEN) {
      const citizenServiceRoutes: Record<string, string> = {
        identity: '/citizen/services/identity',
        registry: '/citizen/services/registry',
        tax: '/citizen/services/tax',
        water: '/citizen/services/water',
        energy: '/citizen/services/energy',
        educacao: '/citizen/services/educacao',
        employment: '/citizen/services/employment',
        licensing: '/citizen/services/licensing',
        transport: '/citizen/services/transport',
        notaries: '/citizen/services/notaries'
      };
      const route = citizenServiceRoutes[pendingService] || `/citizen/portal?service=${pendingService}`;
      localStorage.removeItem('selected_service');
      window.location.hash = route;
      return;
    }

    const role = userData.role;
    const defaultRoute = role === UserRole.CITIZEN
      ? '/citizen/portal'
      : authService.getDashboardForRole(role);
    window.location.hash = defaultRoute;
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
      <LoginModalProvider>
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
        <Route path="/qa" element={<QAReview />} />

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
                  <Route path="/citizens" element={<AdminCitizens />} />
                  <Route path="/citizens/:id" element={<AdminCitizenProfile />} />
                  <Route path="/citizens/:id/fuc" element={<AdminCitizenFuc />} />
                  <Route path="/documents" element={<AdminDocuments />} />
                  <Route path="/documents/:id" element={<AdminDocumentProfile />} />
                  <Route path="/exports" element={<AdminExports />} />
                  <Route path="/payments" element={<PaymentsPage />} />
                  <Route path="/territory" element={<AdminTerritory />} />
                  <Route path="/observability" element={<AdminObservability />} />
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
                <Route path="/services/identity" element={<IdentityPage />} />
                <Route path="/services/identity/biometrics" element={<BiometricEnrollmentPage />} />
                <Route path="/services/catalog/:code" element={<ServiceCatalogForm />} />
                <Route path="/requests/new" element={<ServiceRequestPage />} />
                <Route path="/services/registry" element={<RegistryPage />} />
                <Route path="/services/tax" element={<TaxPage />} />
                <Route path="/services/water" element={<WaterPage />} />
                <Route path="/services/energy" element={<EnergyPage />} />
                <Route path="/services/educacao" element={<EducationPage />} />
                <Route path="/services/employment" element={<EmploymentPage />} />
                <Route path="/services/licensing" element={<LicensingPage />} />
                <Route path="/services/transport" element={<TransportPage />} />
                <Route path="/services/notaries" element={<NotariesPage />} />
                <Route path="/documents/upload" element={<UploadDocuments />} />
                <Route path="/documents/my" element={<MyDocuments />} />
                <Route path="/documents/search" element={<SearchDocuments />} />
                <Route path="/payments" element={<PaymentsPage />} />
              </Routes>
            </ProtectedRoute>
          }
        />

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </LoginModalProvider>
    </HashRouter>
  );
};

export default App;
