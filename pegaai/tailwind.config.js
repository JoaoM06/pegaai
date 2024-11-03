/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/templates/*.html',
    './static/css/*.css'
  ],
  theme: {
    extend: {
      colors: {
        primary: '#5FACF1',
        facebook: '#0866FF',
      },
    },
  },
  plugins: [],
}

