/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Pirate Theme Colors
        'navy': {
          50: '#e7e9ef',
          100: '#c3c8d7',
          200: '#9ca4bc',
          300: '#7580a1',
          400: '#58658c',
          500: '#3b4a78',
          600: '#334170',
          700: '#283565',
          800: '#1e2a5b',
          900: '#0f1a48',
        },
        'teal': {
          50: '#e0f7f6',
          100: '#b3ebe9',
          200: '#80dedb',
          300: '#4dd1cd',
          400: '#26c7c2',
          500: '#00bdb7',
          600: '#00ada8',
          700: '#009996',
          800: '#008684',
          900: '#006562',
        },
        'gold': {
          50: '#fff8e1',
          100: '#ffecb3',
          200: '#ffe082',
          300: '#ffd54f',
          400: '#ffca28',
          500: '#ffc107',
          600: '#ffb300',
          700: '#ffa000',
          800: '#ff8f00',
          900: '#ff6f00',
        },
        'treasure': '#d4af37',
        'ocean': '#006994',
        'storm': '#2c3e50',
      },
      fontFamily: {
        'pirate': ['Cinzel', 'serif'],
        'body': ['Inter', 'sans-serif'],
      },
      backgroundImage: {
        'ocean-gradient': 'linear-gradient(135deg, #0f1a48 0%, #1e2a5b 50%, #006994 100%)',
      }
    },
  },
  plugins: [],
  darkMode: 'class',
}
