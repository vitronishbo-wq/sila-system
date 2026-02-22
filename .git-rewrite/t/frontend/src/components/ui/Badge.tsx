import { ReactNode } from "react";

interface BadgeProps {
  children: ReactNode;
  variant?: "success" | "warning" | "error" | "info";
}

const variants = {
  success: { background: "#d1fae5", color: "#065f46" },
  warning: { background: "#fef3c7", color: "#b45309" },
  error: { background: "#fee2e2", color: "#991b1b" },
  info: { background: "#dbeafe", color: "#1e40af" },
};

export default function Badge({ children, variant = "info" }: BadgeProps) {
  return (
    <span
      style={{
        ...variants[variant],
        padding: "4px 12px",
        borderRadius: "20px",
        fontSize: "0.875rem",
        fontWeight: "500",
        display: "inline-block",
      }}
    >
      {children}
    </span>
  );
}
