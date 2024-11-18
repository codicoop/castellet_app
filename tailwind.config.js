/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/templates/**/*.html',
    './node_modules/flowbite/**/*.js'
  ],
  plugins: [
    require('flowbite/plugin'),
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          "50":"#E9F7DF",
          "100":"#C6F0BB",
          "200":"#A7E89B",
          "300":"#6FD972",
          "400":"#4FCF66",
          "500":"#31b44a", // verd logo
          "600":"#2CA041",
          "700":"#238034",
          "800":"#1A6027",
          "900":"#124019",
          "950":"#124019"
        },
        blau: {
          "300":"#02AFDE",
          "400":"#029EC9",
          "500":"#028db4", // blau app
          "600":"#0C678D",
          "700":"#164066",
        },
        groc: {
          "100": "#FEEEAE",
          "300": "#FEE271",
          "500": "#fed116", // groc base
          "700": "#e2bd5a",
          "900": "#a9882e"
        },
        gris: {
          "500": "#929e9e"  // gris base
        }
      },
      boxShadow: {
        'video': '0 1.6px 7.2px 0 rgba(0, 0, 0, 0.21)',
        'card': '0 4px 18px 0 rgba(0, 0, 0, 0.21)'
      }
    },
    fontFamily: {
      'title': ['Montserrat', 'sans-serif'],
      'body': ['Source Sans Pro', 'sans-serif']
    },
  },
}

