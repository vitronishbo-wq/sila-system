import { useState } from "react";

interface SidebarProps {
  isOpen?: boolean;
  onClose?: () => void;
  activePath?: string;
}

interface MenuItem {
  label: string;
  path: string;
  icon: string;
}

const menuItems: MenuItem[] = [
  { label: "Dashboard", path: "/dashboard", icon: "📊" },
  { label: "Documentos", path: "/documents", icon: "📄" },
  { label: "Usuários", path: "/users", icon: "👥" },
  { label: "Serviços", path: "/services", icon: "🔧" },
  { label: "Relatórios", path: "/reports", icon: "📈" },
  { label: "Configurações", path: "/settings", icon: "⚙️" },
];

export default function Sidebar({ isOpen = true, onClose, activePath = "/dashboard" }: SidebarProps) {
  return (
    <aside
      style={{
        width: "280px",
        background: "white",
        borderRight: "1px solid #e5e7eb",
        height: "calc(100vh - 64px)",
        overflowY: "auto",
        padding: "1rem 0",
        display: isOpen ? "block" : "none",
        position: "fixed",
        left: 0,
        top: "64px",
        zIndex: 40,
      }}
    >
      <nav style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}>
        {menuItems.map((item) => {
          const isActive = activePath === item.path;
          return (
            <button
              key={item.path}
              onClick={() => {
                window.location.href = item.path;
                onClose?.();
              }}
              style={{
                background: isActive ? "#f0f4ff" : "transparent",
                color: isActive ? "#6366f1" : "#6b7280",
                border: "none",
                padding: "1rem 1.5rem",
                textAlign: "left",
                cursor: "pointer",
                fontSize: "1rem",
                fontWeight: isActive ? "600" : "400",
                borderLeft: isActive ? "4px solid #6366f1" : "4px solid transparent",
                transition: "all 0.2s",
              }}
              onMouseEnter={(e) => {
                if (!isActive) {
                  (e.target as HTMLButtonElement).style.background = "#f9fafb";
                }
              }}
              onMouseLeave={(e) => {
                if (!isActive) {
                  (e.target as HTMLButtonElement).style.background = "transparent";
                }
              }}
            >
              <span style={{ marginRight: "0.75rem" }}>{item.icon}</span>
              {item.label}
            </button>
          );
        })}
      </nav>
    </aside>
  );
}
