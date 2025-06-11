// tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  theme: {
    extend: {
      colors: {
        'f1-red': 'var(--f1-red)',
        'f1-black': 'var(--f1-black)',
        'f1-offwhite': 'var(--f1-offwhite)',
        'f1-white': 'var(--f1-white)',
        'f1-gray-30': 'var(--f1-gray-30)',
        'f1-gray-50': 'var(--f1-gray-50)',
        'f1-gray-70': 'var(--f1-gray-70)',
        'f1-gray-90': 'var(--f1-gray-90)',

        'team-mercedes': 'var(--team-mercedes)',
        'team-redbull': 'var(--team-redbull)',
        'team-ferrari': 'var(--team-ferrari)',
        'team-mclaren': 'var(--team-mclaren)',
        'team-astonmartin': 'var(--team-astonmartin)',
        'team-alpine': 'var(--team-alpine)',
        'team-williams': 'var(--team-williams)',
        'team-alfa': 'var(--team-alfa)',
        'team-haas': 'var(--team-haas)',
      },
      fontFamily: {
        formula1wide: ['Formula1Wide', 'fantasy'],
        formula1regular: ['Formula1Regular', 'sans-serif'],
        formula1bold: ['Formula1Bold', 'sans-serif'],
      },
    },
  },
  // optional: content, plugins, etc.
};
