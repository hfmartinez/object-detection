/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        vietnam: ['"Be Vietnam Pro"', "sans=serif"],
      },

      colors: {
        "dark-blue": "#142C43",
        "bright-red": "hsl(12, 88%, 59%)",
        "dark-grayish-blue": "hsl(227, 12%, 61%)",
        "very-dark-blue": "hsl(233, 12%, 13%)",
        "very-pale-red": "hsl(13, 100%, 96%)",
        "vary-light-gray": "hsl(0, 0%, 98%)",
      },
    },
  },
  plugins: [],
};
