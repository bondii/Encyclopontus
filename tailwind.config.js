/** @type {import('tailwindcss').Config} */

module.exports = {
  mode: 'jit',
  content: ['./**/*.{html,js,ts,py}'],
  theme: {
    extend: {
      colors: {},
      fontFamily: {
        organic: ['"Bad Script"', 'cursive'],
      },
    },
  },
  plugins: [require('@tailwindcss/forms')],
}
