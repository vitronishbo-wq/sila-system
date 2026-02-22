
import { useEffect, useState } from "react";
import { useDashboardStats } from "../services/dashboard";
import BarChart from "../modules/BarChart";
import AlertList from "../modules/AlertList";

interface User {
  id: string;
  email: string;
  name: string;
  roles: string[];
  status: string;
  permissions: string[];
}

export default function Dashboard() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {

    export default function Dashboard() {
      const [user, setUser] = useState<User | null>(null);
      const [loadingUser, setLoadingUser] = useState(true);
      const { documentsByMonth, activeUsers, alerts, loading: loadingStats } = useDashboardStats();

      useEffect(() => {
        const fetchUser = async () => {
          try {
            const token = localStorage.getItem("access_token");
            const res = await fetch("http://localhost:8000/api/v1/auth/me", {
              headers: { Authorization: `Bearer ${token}` },
            });
            if (res.ok) {
              setUser(await res.json());
            }
          } catch (err) {
            console.error(err);
          } finally {
            setLoadingUser(false);
          }
        };
        if (localStorage.getItem("access_token")) {
          fetchUser();
        } else {
          setLoadingUser(false);
        }
      }, []);

      if (loadingUser || loadingStats) {
        return (
          <div style={{ padding: "2rem", textAlign: "center" }}>
            <p>Carregando...</p>
          </div>
        );
      }

      return (
        <div style={{ padding: "2rem" }}>
          <h1>Dashboard</h1>
          <AlertList alerts={alerts} />
          {user ? (
            <div>
              <p>Bem-vindo, <strong>{user.name}</strong>!</p>
              <p>Email: {user.email}</p>
              <p>Roles: {user.roles.join(", ")}</p>
            </div>
          ) : (
            <p>Não autenticado</p>
          )}
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
              gap: "1.5rem",
              marginTop: "2rem",
            }}
          >
            {[
              { title: "Documentos", value: documentsByMonth.reduce((acc, d) => acc + d.value, 0), color: "#3b82f6" },
              { title: "Usuários Ativos", value: activeUsers, color: "#10b981" },
            ].map((card) => (
              <div
                key={card.title}
                style={{
                  background: "white",
                  padding: "1.5rem",
                  borderRadius: "12px",
                  boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
                  textAlign: "center",
                }}
              >
                <p style={{ color: "#6b7280", fontSize: "0.9rem" }}>{card.title}</p>
                <p
                  style={{
                    fontSize: "2.5rem",
                    fontWeight: "bold",
                    color: card.color,
                    marginTop: "0.5rem",
                  }}
                >
                  {card.value}
                </p>
              </div>
            ))}
          </div>
          <div style={{ marginTop: 32 }}>
            <h2 style={{ fontSize: 18, marginBottom: 12 }}>Documentos por mês</h2>
            <BarChart data={documentsByMonth} />
          </div>
        </div>
      );
    }
