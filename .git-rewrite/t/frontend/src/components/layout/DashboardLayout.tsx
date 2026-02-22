import { ReactNode, useState } from "react";
import Navbar from "./Navbar";
import Sidebar from "./Sidebar";

interface DashboardLayoutProps {
  children: ReactNode;
  userName?: string;
  onLogout?: () => void;
}

export default function DashboardLayout({
  children,
  userName,
  onLogout,
}: DashboardLayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  return (
    <div style={{ display: "flex", flexDirection: "column", minHeight: "100vh" }}>
      <Navbar userName={userName} onLogout={onLogout} />

      <div style={{ display: "flex", flex: 1 }}>
        <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

        <main
          style={{
            flex: 1,
            marginLeft: sidebarOpen ? "280px" : "0",
            background: "#f9fafb",
            overflowY: "auto",
            padding: "2rem",
            transition: "margin-left 0.3s",
          }}
        >
          {children}
        </main>
      </div>
    </div>
  );
}
