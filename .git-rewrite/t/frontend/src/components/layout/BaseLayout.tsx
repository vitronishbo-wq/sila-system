import { ReactNode } from "react";

interface BaseLayoutProps {
  children: ReactNode;
}

export default function BaseLayout({ children }: BaseLayoutProps) {
  return (
    <div style={{ display: "flex", flexDirection: "column", minHeight: "100vh" }}>
      <header
        style={{
          background: "white",
          padding: "1rem 2rem",
          boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
        }}
      >
        <h1 style={{ fontSize: "1.5rem", color: "#6366f1" }}>SILA-System</h1>
      </header>
      <main style={{ flex: 1, padding: "2rem" }}>
        {children}
      </main>
      <footer
        style={{
          background: "#f9fafb",
          padding: "1rem 2rem",
          textAlign: "center",
          borderTop: "1px solid #e5e7eb",
          fontSize: "0.875rem",
          color: "#6b7280",
        }}
      >
        © 2025 SILA-System. Todos os direitos reservados.
      </footer>
    </div>
  );
}
