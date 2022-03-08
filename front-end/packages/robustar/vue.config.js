// close eslint checking in Vue CLI
module.exports = {
  devServer: {
    // disableHostCheck: true,
    // host: '0.0.0.0',
    overlay: {
      warnings: false,
      errors: false,
    },
  },
  lintOnSave: false,
};
