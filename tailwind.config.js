/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./ezqna/**/*.{html,js,py}"],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: ["light"],
  },
};
