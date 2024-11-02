/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/*.html',
    './static/js/**/*.js',
    './static/css/*.css',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#5FACF1'
      },
    },
  },
  plugins: [],
}

