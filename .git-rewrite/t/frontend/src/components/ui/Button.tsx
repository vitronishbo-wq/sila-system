import { ReactNode, CSSProperties } from "react";

interface ButtonProps {
  children: ReactNode;
  variant?: "primary" | "secondary" | "danger";
  size?: "sm" | "md" | "lg";
  onClick?: () => void;
  disabled?: boolean;
  type?: "button" | "submit" | "reset";
  style?: CSSProperties;
}

const variants = {
  primary: { background: "#6366f1", color: "white" },
  secondary: { background: "#e5e7eb", color: "#374151" },
  danger: { background: "#dc2626", color: "white" },
};

const sizes = {
  sm: { padding: "8px 12px", fontSize: "0.875rem" },
  md: { padding: "12px 16px", fontSize: "1rem" },
  lg: { padding: "16px 20px", fontSize: "1.125rem" },
};

export default function Button({
  children,
  variant = "primary",
  size = "md",
  onClick,
  disabled,
  type = "button",
  style,
}: ButtonProps) {
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      style={{
        ...variants[variant],
        ...sizes[size],
        borderRadius: "8px",
        border: "none",
        cursor: disabled ? "not-allowed" : "pointer",
        opacity: disabled ? 0.6 : 1,
        fontWeight: "500",
        transition: "all 0.2s",
        ...style,
      }}
    >
      {children}
    </button>
  );
}
