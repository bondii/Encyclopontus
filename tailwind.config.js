/** @type {import('tailwindcss').Config} */

module.exports = {
  mode: 'jit',
  content: ['./**/*.{html,js,ts,py}'],
  theme: {
    extend: {
      colors: {},
    },
  },
  plugins: [require('@tailwindcss/forms')],
}
