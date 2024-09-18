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
          "500":"#31a836", // verd base
          "600":"#2ca041",
          "700":"#27903b",
          "800":"#1f702e",
          "900":"#12401a",
          "950":"#0d3014"
        },
        groc: {
          "500": "#fed116", // groc base
          "700": "#e2bd5a",
          "900": "#a9882e"
        },
        blau: {
          "300": "#028db4",
          "500": "#028db4", // blau base
          "700": "#164066"
        },
        gris: {
          "500": "#929e9e"  // gris base
          
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

