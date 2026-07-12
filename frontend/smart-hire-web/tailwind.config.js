/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.njk", "./src/**/*.html"],
  theme: {
    extend: {
      colors: {
        bg: "#faf8f5",
        card: "#ffffff",
        card2: "#f7f3ee",
        ink: { DEFAULT: "#1c1714", 2: "#43392f" },
        muted: "#7c736c",
        faint: "#a89f97",
        line: { DEFAULT: "#ece7e1", 2: "#e0d9d1" },
        brand: { DEFAULT: "#ea580c", d: "#c2410c" },
        tint: { DEFAULT: "#fdebdf", 2: "#fdf3ec" },
        ok: { DEFAULT: "#0e7a4a", tint: "#dcf3e7" },
        warn: { DEFAULT: "#b45309", tint: "#fdeccf" },
        danger: { DEFAULT: "#c2362b", tint: "#fbe3df" },
        info: { DEFAULT: "#0e7490", tint: "#d9f0f4" },
        teal: "#0e7490",
        violet: "#7c3aed",
        rose: "#be185d",
      },
      fontFamily: {
        display: ["Space Grotesk", "system-ui", "sans-serif"],
        body: ["Hanken Grotesk", "system-ui", "sans-serif"],
        mono: ["Space Mono", "ui-monospace", "monospace"],
      },
      borderRadius: {
        DEFAULT: "14px",
        sm: "10px",
        lg: "18px",
        pill: "999px",
      },
      boxShadow: {
        sm: "0 1px 2px rgba(28,23,20,.06)",
        DEFAULT: "0 1px 2px rgba(28,23,20,.06),0 10px 24px -16px rgba(28,23,20,.22)",
        lg: "0 2px 4px rgba(28,23,20,.05),0 24px 48px -24px rgba(28,23,20,.30)",
      },
    },
  },
  corePlugins: {
    preflight: true,
  },
  plugins: [],
};
