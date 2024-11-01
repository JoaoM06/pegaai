/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',            // Diretório principal de templates
    './apps/**/templates/**/*.html',    // Diretório de templates dentro dos apps
    './static/**/*.js',                 // Inclua JavaScript, se você usa Tailwind com JS
    './**/*.html'
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

