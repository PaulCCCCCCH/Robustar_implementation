// close eslint checking in Vue CLI
module.exports = {
  devServer: {
    overlay: {
      warnings: false,
      errors: false,
    },
  },
  lintOnSave: false,
};
