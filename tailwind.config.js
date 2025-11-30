/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html", //Template at the project level
    "./**/templates/**/*.html" // Templates inside apps level
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

