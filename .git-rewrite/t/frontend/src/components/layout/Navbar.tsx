import { useState } from "react";

interface NavbarProps {
  onLogout?: () => void;
  userName?: string;
}

export default function Navbar({ onLogout, userName }: NavbarProps) {
  const [showDropdown, setShowDropdown] = useState(false);

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    onLogout?.();
    window.location.href = "/login";
  };

  return (
    <nav
      style={{
        background: "white",
        borderBottom: "1px solid #e5e7eb",
        padding: "0 2rem",
        height: "64px",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        boxShadow: "0 2px 4px rgba(0,0,0,0.05)",
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: "1rem" }}>
        <div
          style={{
            width: "40px",
            height: "40px",
            background: "#6366f1",
            borderRadius: "8px",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            color: "white",
            fontWeight: "bold",
            fontSize: "1.2rem",
          }}
        >
          S
        </div>
        <h1 style={{ fontSize: "1.3rem", color: "#1f2937", margin: 0 }}>
          SILA-System 2025
        </h1>
      </div>

      <div style={{ display: "flex", alignItems: "center", gap: "2rem" }}>
        <div
          style={{
            position: "relative",
          }}
        >
          <button
            onClick={() => setShowDropdown(!showDropdown)}
            style={{
              background: "none",
              border: "none",
              cursor: "pointer",
              fontSize: "1rem",
              color: "#6b7280",
              display: "flex",
              alignItems: "center",
              gap: "0.5rem",
            }}
          >
            👤 {userName || "Admin"}
            <span style={{ fontSize: "0.8rem" }}>▼</span>
          </button>

          {showDropdown && (
            <div
              style={{
                position: "absolute",
                top: "100%",
                right: 0,
                background: "white",
                border: "1px solid #e5e7eb",
                borderRadius: "8px",
                marginTop: "0.5rem",
                boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
                minWidth: "150px",
                zIndex: 50,
              }}
            >
              <button
                onClick={() => window.location.href = "/profile"}
                style={{
                  display: "block",
                  width: "100%",
                  padding: "0.75rem 1rem",
                  border: "none",
                  background: "none",
                  textAlign: "left",
                  cursor: "pointer",
                  borderBottom: "1px solid #e5e7eb",
                }}
              >
                Perfil
              </button>
              <button
                onClick={handleLogout}
                style={{
                  display: "block",
                  width: "100%",
                  padding: "0.75rem 1rem",
                  border: "none",
                  background: "none",
                  textAlign: "left",
                  cursor: "pointer",
                  color: "#dc2626",
                }}
              >
                Sair
              </button>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
}
