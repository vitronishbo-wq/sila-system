import { ProtectedRoute } from "./ProtectedRoute";

export const AdminRoute = () => <ProtectedRoute allowedLevels={["CENTRAL"]} />;
