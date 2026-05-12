// tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{html,ts}",
  ],
  theme: {
    extend: {
      // Colores institucionales GAMLP
      colors: {
        'gamlp-verde':    '#2E7D32',
        'gamlp-azul':     '#1565C0',
        'ica-bueno':      '#4CAF50',
        'ica-moderado':   '#FFEB3B',
        'ica-malo':       '#FF9800',
        'ica-peligroso':  '#F44336',
      }
    },
  },
  plugins: [],
}