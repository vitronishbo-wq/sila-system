/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
    // Caminhos relativos à raiz do projeto frontend para garantir a varredura das classes
    "../../apps/frontend/index.html",
    "../../apps/frontend/src/**/*.{js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: "#0B3C5D",
          light: "#165a8a",
          dark: "#051f33"
        },
        secondary: "#F5F7FA",
        success: "#2E7D32",
        danger: "#C62828",
        // Adicionando neutros comuns para o SILA System
        surface: "#FFFFFF",
        border: "#E2E8F0"
      },
      // Útil para layouts de dashboard (sidebar/topbar)
      spacing: {
        'sidebar': '260px',
        'topbar': '64px'
      }
    }
  },
  plugins: [],
}