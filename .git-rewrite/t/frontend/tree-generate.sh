#!/bin/bash

echo "🚀 Gerando estrutura completa do frontend SILA-System..."

BASE_DIR="src"

# Pastas principais
DIRS=(
  "$BASE_DIR/components"
  "$BASE_DIR/components/ui"
  "$BASE_DIR/components/layout"
  "$BASE_DIR/components/common"
  "$BASE_DIR/pages"
  "$BASE_DIR/routes"
  "$BASE_DIR/context"
  "$BASE_DIR/hooks"
  "$BASE_DIR/services"
  "$BASE_DIR/store"
  "$BASE_DIR/assets"
  "$BASE_DIR/assets/images"
  "$BASE_DIR/assets/icons"
  "$BASE_DIR/theme"
  "$BASE_DIR/utils"
  "$BASE_DIR/types"
)

# Criar diretórios
echo "📁 Criando pastas..."
for dir in "${DIRS[@]}"; do
  mkdir -p "$dir"
  echo "   ✔ $dir"
done

# Criar arquivos base
echo "📝 Criando arquivos padrão..."

# Rotas
cat <<'EOF' > "$BASE_DIR/routes/AppRoutes.tsx"
import { Routes, Route, Navigate } from "react-router-dom";
import Home from "../pages/Home";
import NotFound from "../pages/NotFound";

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}
EOF
echo "   ✔ AppRoutes.tsx criado"

# Página HOME
cat <<'EOF' > "$BASE_DIR/pages/Home.tsx"
export default function Home() {
  return (
    <div style={{ padding: 20 }}>
      <h1>SILA-System Frontend</h1>
      <p>Interface inicial carregada com sucesso.</p>
    </div>
  );
}
EOF
echo "   ✔ Home.tsx criado"

# Página NotFound
cat <<'EOF' > "$BASE_DIR/pages/NotFound.tsx"
import { Link } from "react-router-dom";

export default function NotFound() {
  return (
    <div style={{ padding: 40, textAlign: "center" }}>
      <h1>404 - Página não encontrada</h1>
      <p>A página que você procura não existe.</p>
      <Link to="/" style={{ marginTop: 20, display: "inline-block" }}>
        Voltar ao Início
      </Link>
    </div>
  );
}
EOF
echo "   ✔ NotFound.tsx criado"

# Tema global
cat <<'EOF' > "$BASE_DIR/theme/global.css"
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body, #root {
  width: 100%;
  height: 100%;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: #f5f6fa;
  color: #222;
  line-height: 1.6;
}

a {
  text-decoration: none;
  color: inherit;
}

button {
  border: none;
  background: none;
  cursor: pointer;
  font-family: inherit;
}
EOF
echo "   ✔ global.css criado"

# Helpers
cat <<'EOF' > "$BASE_DIR/utils/helpers.ts"
export const formatDate = (date: string | Date): string => {
  return new Date(date).toLocaleDateString("pt-AO", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  });
};

export const formatCurrency = (value: number): string => {
  return new Intl.NumberFormat("pt-AO", {
    style: "currency",
    currency: "AOA",
  }).format(value);
};

export const truncate = (text: string, length: number): string => {
  return text.length > length ? text.slice(0, length) + "..." : text;
};
EOF
echo "   ✔ helpers.ts criado"

# Constantes
cat <<'EOF' > "$BASE_DIR/utils/constants.ts"
export const API_BASE_URL = import.meta.env.VITE_API_BASE || "http://localhost:8000/api/v1";

export const HTTP_STATUS = {
  OK: 200,
  CREATED: 201,
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  INTERNAL_ERROR: 500,
} as const;
EOF
echo "   ✔ constants.ts criado"

# Types
cat <<'EOF' > "$BASE_DIR/types/index.ts"
export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
  status?: number;
}

export interface User {
  id: number;
  email: string;
  name: string;
  role: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
}
EOF
echo "   ✔ types/index.ts criado"

# Hooks customizados
cat <<'EOF' > "$BASE_DIR/hooks/useLocalStorage.ts"
import { useState, useEffect } from "react";

export function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error(error);
      return initialValue;
    }
  });

  const setValue = (value: T | ((val: T) => T)) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value;
      setStoredValue(valueToStore);
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.error(error);
    }
  };

  return [storedValue, setValue] as const;
}
EOF
echo "   ✔ useLocalStorage.ts criado"

# Componente Layout base
cat <<'EOF' > "$BASE_DIR/components/layout/BaseLayout.tsx"
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
EOF
echo "   ✔ BaseLayout.tsx criado"

# Contexto exemplo
cat <<'EOF' > "$BASE_DIR/context/ThemeContext.tsx"
import { createContext, useState, ReactNode } from "react";

type Theme = "light" | "dark";

interface ThemeContextType {
  theme: Theme;
  toggleTheme: () => void;
}

export const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<Theme>("light");

  const toggleTheme = () => {
    setTheme((prev) => (prev === "light" ? "dark" : "light"));
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}
EOF
echo "   ✔ ThemeContext.tsx criado"

# Index file para fácil exportação
cat <<'EOF' > "$BASE_DIR/components/index.ts"
export { default as BaseLayout } from "./layout/BaseLayout";
EOF
echo "   ✔ components/index.ts criado"

cat <<'EOF' > "$BASE_DIR/hooks/index.ts"
export { useLocalStorage } from "./useLocalStorage";
EOF
echo "   ✔ hooks/index.ts criado"

cat <<'EOF' > "$BASE_DIR/utils/index.ts"
export * from "./helpers";
export * from "./constants";
EOF
echo "   ✔ utils/index.ts criado"

# README na pasta src
cat <<'EOF' > "$BASE_DIR/README.md"
# SILA-System Frontend - Estrutura de Projeto

## 📁 Estrutura de Diretórios

```
src/
├── components/        # Componentes React reutilizáveis
│   ├── layout/       # Componentes de layout (Header, Sidebar, etc)
│   ├── ui/           # Componentes de UI genéricos (Button, Input, etc)
│   └── common/       # Componentes comuns (Cards, Modals, etc)
├── pages/            # Páginas/Views da aplicação
├── routes/           # Configuração de rotas
├── context/          # React Context (State global)
├── hooks/            # Custom Hooks
├── services/         # Serviços (API calls, etc)
├── store/            # Estado global (se usar Redux, Zustand, etc)
├── assets/           # Imagens, ícones, fonts
├── theme/            # Temas e estilos globais
├── utils/            # Funções utilitárias
├── types/            # Tipos TypeScript
├── App.tsx           # Componente root
└── main.tsx          # Ponto de entrada
```

## 🚀 Como Adicionar Novos Componentes

### Componente de UI
```
src/components/ui/Button.tsx
```

### Componente de Página
```
src/pages/Dashboard.tsx
```

### Custom Hook
```
src/hooks/useFetch.ts
```

## 📝 Convenções

- Arquivos de componentes: **PascalCase** (MyComponent.tsx)
- Arquivos de funções/utils: **camelCase** (myFunction.ts)
- Pastas: **lowercase** (components, pages, utils)
EOF
echo "   ✔ README.md criado em src/"

echo ""
echo "🎉 Estrutura do frontend criada com sucesso!"
echo ""
echo "📊 Árvore de diretórios:"
find src -type d | sed 's|[^/]*/| |g' | sort
