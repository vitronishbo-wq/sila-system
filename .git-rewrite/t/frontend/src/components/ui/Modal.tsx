import { useState, ReactNode } from "react";

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: ReactNode;
  footer?: ReactNode;
}

export default function Modal({
  isOpen,
  onClose,
  title,
  children,
  footer,
}: ModalProps) {
  if (!isOpen) return null;

  return (
    <>
      <div
        style={{
          position: "fixed",
          inset: 0,
          background: "rgba(0,0,0,0.5)",
          zIndex: 40,
        }}
        onClick={onClose}
      />
      <div
        style={{
          position: "fixed",
          top: "50%",
          left: "50%",
          transform: "translate(-50%, -50%)",
          background: "white",
          borderRadius: "12px",
          boxShadow: "0 25px 50px rgba(0,0,0,0.3)",
          zIndex: 50,
          maxWidth: "500px",
          width: "90%",
          maxHeight: "80vh",
          overflowY: "auto",
        }}
      >
        {title && (
          <div
            style={{
              padding: "1.5rem",
              borderBottom: "1px solid #e5e7eb",
              fontWeight: "600",
              fontSize: "1.25rem",
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
            }}
          >
            {title}
            <button
              onClick={onClose}
              style={{
                background: "none",
                border: "none",
                fontSize: "1.5rem",
                cursor: "pointer",
                color: "#6b7280",
              }}
            >
              ×
            </button>
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
              display: "flex",
              gap: "1rem",
              justifyContent: "flex-end",
            }}
          >
            {footer}
          </div>
        )}
      </div>
    </>
  );
}
