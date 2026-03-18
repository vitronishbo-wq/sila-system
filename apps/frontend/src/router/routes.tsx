import { Routes, Route, Navigate } from "react-router-dom";
import { ProtectedRoute } from "@/components/Auth/ProtectedRoute";
import { AdminRoute } from "@/components/Auth/AdminRoute";
import Login from "../pages/Login";
import PortalSelection from "../pages/PortalSelection";
import CitizenDashboard from "../pages/CitizenDashboard";
import NotificationPage from "../pages/Notifications";
import { MyDocuments } from "../pages/MyDocuments";
import { UploadDocuments } from "../pages/UploadDocuments";
import { AdminStatistics } from "../pages/AdminStatistics";
import { SearchDocuments } from "../pages/SearchDocuments";
import { SearchDeepResults } from "../pages/SearchDeepResults";
import { AdminAuditViewer } from "../pages/AdminAuditViewer";
import { AdminDashboard } from "../modules/admin/components/AdminDashboard";
import { MeteorologyPage } from "../modules/meteorologia/pages/MeteorologyPage";
import { IdentityPage } from "../pages/IdentityPage";
import { BiometricEnrollmentPage } from "../pages/BiometricEnrollmentPage";
import Unauthorized from "../pages/Unauthorized";

export default function AppRoutes() {
  return (
    <Routes>
      {/* Rota Pública */}
      <Route path="/login" element={<Login />} />
      <Route path="/unauthorized" element={<Unauthorized />} />

      {/* Rotas Protegidas (Cidadão/Geral) */}
      <Route element={<ProtectedRoute />}>
        <Route path="/portal" element={<PortalSelection />} />
        <Route path="/citizen" element={<CitizenDashboard />} />
        <Route path="/notifications" element={<NotificationPage />} />
        <Route path="/documents" element={<MyDocuments />} />
        <Route path="/citizen/documents" element={<MyDocuments />} />
        <Route path="/upload" element={<UploadDocuments />} />
        <Route path="/search" element={<SearchDocuments />} />
        <Route path="/search/deep" element={<SearchDeepResults />} />
        <Route path="/identity" element={<IdentityPage />} />
        <Route path="/biometric-enrollment" element={<BiometricEnrollmentPage />} />
      </Route>

      {/* Rotas Administrativas */}
      <Route element={<AdminRoute />}>
        <Route path="/admin/dashboard" element={<AdminDashboard />} />
        <Route path="/admin/statistics" element={<AdminStatistics />} />
        <Route path="/admin/audit" element={<AdminAuditViewer />} />
        <Route path="/meteorologia" element={<MeteorologyPage />} />
      </Route>

      {/* Redirecionamento Padrão */}
      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  );
}