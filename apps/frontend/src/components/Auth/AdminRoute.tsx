import { ProtectedRoute } from "@/components/Auth/ProtectedRoute";

export const AdminRoute = () => <ProtectedRoute allowedLevels={["CENTRAL"]} />;
