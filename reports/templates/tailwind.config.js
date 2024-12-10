/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./reports/**/*.html", // Include all HTML templates in the reports directory
    "./reports/**/*.js",   // Include any JavaScript files
  ],
  theme: {
    extend: {
      height: {
        'a4': '297mm',
      },
      width: {
        'a4': '210mm',
      },
      colors: {
        primary: {
          light: "#93c5fd",
          DEFAULT: "#3b82f6",
          dark: "#1d4ed8",
        },
        secondary: {
          light: "#fda4af",
          DEFAULT: "#f43f5e",
          dark: "#9f1239",
        },
        success: "#10b981", // For success indicators (e.g., closed ports)
        danger: "#ef4444",  // For danger indicators (e.g., open ports)
      },
    },
    fontFamily: {
      sans: ["Inter", "sans-serif"],
      mono: ["Courier New", "monospace"],
    },
    container: {
      center: true,
      padding: "2rem",
    },
  },
  plugins: [],
};
