/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        rw: {
          bg: "#050B14",           
          surface: "#0A1628",     
          "surface-2": "#0E1F38", // cards internas / hover
          border: "#1B3A5C",      // bordes de cards
          primary: "#2E9BFF",     
          "primary-soft": "#1f88ddff",
          cyan: "#35D6FF",         
          text: "#E8F1FA",        
          muted: "#7A93AD",        
          success: "#22C55E",     
          warning: "#FACC15",      
          danger: "#EF4444",       
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
      },
      boxShadow: {
        neon: "0 0 12px rgba(46, 155, 255, 0.25)",
        "neon-strong": "0 0 20px rgba(53, 214, 255, 0.4)",
      },
      borderRadius: {
        card: "1rem",
      },
    },
  },
  plugins: [],
};