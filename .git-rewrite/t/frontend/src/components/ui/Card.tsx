import { ReactNode, CSSProperties } from "react";

interface CardProps {
  children: ReactNode;
  title?: string;
  footer?: ReactNode;
  style?: CSSProperties;
}

export default function Card({
  children,
  title,
  footer,
  style,
}: CardProps) {
  return (
    <div
      style={{
        background: "white",
        borderRadius: "12px",
        boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
        overflow: "hidden",
        ...style,
      }}
    >
      {title && (
        <div
          style={{
            padding: "1.5rem",
            borderBottom: "1px solid #e5e7eb",
            fontWeight: "600",
            fontSize: "1.1rem",
            color: "#1f2937",
          }}
        >
          {title}
        </div>
      )}
      <div style={{ padding: "1.5rem" }}>
        {children}
      </div>
      {footer && (
        <div
          style={{
            padding: "1.5rem",
            borderTop: "1px solid #e5e7eb",
            background: "#f9fafb",
          }}
        >
          {footer}
        </div>
      )}
    </div>
  );
}
