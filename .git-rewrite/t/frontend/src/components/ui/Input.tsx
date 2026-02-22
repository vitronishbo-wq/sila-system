import { InputHTMLAttributes, CSSProperties } from "react";

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  containerStyle?: CSSProperties;
}

export default function Input({
  label,
  error,
  containerStyle,
  ...props
}: InputProps) {
  return (
    <div style={{ display: "flex", flexDirection: "column", ...containerStyle }}>
      {label && (
        <label
          style={{
            marginBottom: "8px",
            fontWeight: "500",
            color: "#374151",
            fontSize: "0.875rem",
          }}
        >
          {label}
        </label>
      )}
      <input
        style={{
          padding: "12px",
          borderRadius: "8px",
          border: error ? "2px solid #dc2626" : "1px solid #e5e7eb",
          fontSize: "1rem",
          fontFamily: "inherit",
          transition: "all 0.2s",
        }}
        {...props}
      />
      {error && (
        <span
          style={{
            marginTop: "4px",
            fontSize: "0.875rem",
            color: "#dc2626",
          }}
        >
          {error}
        </span>
      )}
    </div>
  );
}
