/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        paper: {
          canvas: '#FAF7F2',
          card: '#FFFFFF',
          sumi: '#2B2523',
          butter: '#FFE5A3',
          oatmeal: '#EFEAE1',
        },
        jlpt: {
          n1: { DEFAULT: '#E63956', tint: '#FFEAEF' },
          n2: { DEFAULT: '#FF6B35', tint: '#FFF0E8' },
          n3: { DEFAULT: '#7CB518', tint: '#F2F8E6' },
          n4: { DEFAULT: '#0096C7', tint: '#E2F4FA' },
          n5: { DEFAULT: '#8338EC', tint: '#F2E8FD' },
        },
        level: {
          DEFAULT: 'var(--level)',
          tint: 'var(--level-tint)',
        },
      },
      boxShadow: {
        'retro-sm': '2px 2px 0px #2B2523',
        retro: '3px 3px 0px #2B2523',
        'retro-lg': '5px 5px 0px #2B2523',
      },
      borderWidth: { 3: '3px' },
      fontFamily: {
        body: ['"Zen Kaku Gothic New"', '"Noto Sans TC"', '"Noto Sans JP"', 'sans-serif'],
        display: ['"Zen Maru Gothic"', '"Zen Kaku Gothic New"', 'sans-serif'],
        mono: ['"DM Mono"', '"Courier New"', 'monospace'],
      },
    },
  },
  plugins: [],
};
