/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/templates/**/*.html',
    './node_modules/flowbite/**/*.js'
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          "50":"#effbf1",
          "100":"#dff6e3",
          "200":"#bfedc7",
          "300":"#9fe5ac",
          "400":"#3fca58",
          "500":"#31b44a",
          "600":"#2ca041",
          "700":"#27903b",
          "800":"#1f702e",
          "900":"#12401a",
          "950":"#0d3014"
        },
        accent: {
          "100": "#fdd360"
        }
      }
    },
    fontFamily: {
      'body': ['Montserrat', 'sans-serif'],
      'sans': ['Montserrat', 'sans-serif']
    }
  },
  plugins: [
    require('flowbite/plugin')
  ]
}

