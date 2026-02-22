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
