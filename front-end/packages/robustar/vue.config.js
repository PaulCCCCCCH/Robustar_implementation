module.exports = {
  devServer: {
    // disableHostCheck: true,
    host: 'localhost',
    port: 8080,
    open: true,
    hotOnly: true,
    overlay: {
      warnings: false,
      errors: false,
    },
    proxy: {
      '/api': {
        target: process.env.VUE_APP_BASE_URL,
        ws: true,
        changeOrigin: true,
        pathRewrite: {
          '^/api': '',
        },
      },
    },
  },
  // close eslint checking in Vue CLI
  lintOnSave: false,
};
