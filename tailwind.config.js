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
          "50":"#E9F7DF",
          "100":"#C6F0BB",
          "200":"#A7E89B",
          "300":"#6FD882",
          "400":"#4FCF66",
          "500":"#31b44a", // verd logo
          "600":"#4FCF66",
          "700":"#238034",
          "800":"#1f702e",
          "900":"#1A6027",
          "950":"#124019"
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

