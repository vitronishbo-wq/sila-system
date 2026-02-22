import { ReactNode } from "react";
import { Navigate } from "react-router-dom";

interface RoleGuardProps {
  allowedRoles: string[];
  userRole: string;
  children: ReactNode;
}

export default function RoleGuard({ allowedRoles, userRole, children }: RoleGuardProps) {
  if (!allowedRoles.includes(userRole)) {
    return <Navigate to="/" replace />;
  }
  return <>{children}</>;
}
