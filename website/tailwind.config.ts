/** @type {import('tailwindcss').Config} */
export default {
  // Add ".md" to the content array
  content: ["./src/**/*.{html,js,svelte,ts,md}"],
  theme: {
    extend: {      fontFamily: {
        // Use the exact name from your @font-face
        'ebgaramond': ['EB Garamond', 'serif'],
        'alegreya': ['Alegreya', 'serif'],
        'crimson': ['Crimson Pro', 'serif'],
      },},
  },
  plugins: [require("@tailwindcss/typography"), require("daisyui")],
};
