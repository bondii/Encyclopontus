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
      boxShadow: {
        'glow-xl': '0 0 25px -5px rgb(0 0 0 / 0.1)',
      },
    },
  },
  plugins: [require('@tailwindcss/forms')],
}
