module.exports = {
  purge: [],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      spacing: { //왼쪽은 class로 사용 h-25vh 이런식, 오른쪽은 css
        "25vh": "25vh",
        "50vh": "50vh",
        "75vh": "75vh",
      },
      borderRadius: {
        xl: "1.5rem",
      }
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
