/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        dark: {
          950: '#080C18',
          900: '#0D1628',
          850: '#111E35',
          800: '#182540',
          700: '#1F3055',
          600: '#2A4070',
        },
        brand: {
          // Primary: Electric Blue (energetic, sporty)
          cyan:    '#00D4FF',
          // Accent: Vibrant Orange (high-energy, action)
          violet:  '#FF6B2B',
          // Secondary: Bright Indigo
          purple:  '#6366F1',
          // Success: Bright Green
          emerald: '#00E676',
          // Danger: Vivid Red
          rose:    '#FF3B6B',
          // Warning: Gold
          amber:   '#FFB800',
        }
      },
      fontFamily: {
        sans: ['Cairo', 'Inter', 'system-ui', 'sans-serif'],
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
        'fade-in': 'fadeIn 0.4s ease-out',
      },
      keyframes: {
        glow: {
          '0%':   { boxShadow: '0 0 10px rgba(0, 212, 255, 0.25)' },
          '100%': { boxShadow: '0 0 30px rgba(0, 212, 255, 0.6)' },
        },
        fadeIn: {
          '0%':   { opacity: '0', transform: 'translateY(8px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        }
      }
    },
  },
  plugins: [],
}
