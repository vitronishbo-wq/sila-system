/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                secondary: "#f3f4f6",
            },
            animation: {
                wave: "wave 8s ease-in-out infinite",
            },
        },
    },
    plugins: [],
}
