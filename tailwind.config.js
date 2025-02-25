/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.{html,js}",
    "./authentication/templates/**/*.{html,js}",
  ],
  plugins: [require("daisyui")],
  daisyui: {
    themes: ["bumblebee"],
  },
};
