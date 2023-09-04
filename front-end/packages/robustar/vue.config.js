module.exports = {
  transpileDependencies: ['vuetify'],
  devServer: {
    // disableHostCheck: true,
    host: 'localhost',
    port: process.env.VUE_APP_DEV_PORT,
    open: true,
    proxy: {
      '/api': {
        target: `${process.env.VUE_APP_BASE_URL}:${process.env.VUE_APP_SERVER_PORT}`,
        ws: true,
        changeOrigin: true,
        pathRewrite: {
          '^/api/': '/',
        },
      },
      '/socket.io': {
        target: `${process.env.VUE_APP_BASE_URL}:${process.env.VUE_APP_SERVER_PORT}`,
        ws: true,
        changeOrigin: true,
      },
      '/tensorboard': {
        target: `${process.env.VUE_APP_BASE_URL}:${process.env.VUE_APP_TENSORBOARD_PORT}`,
        ws: true,
        changeOrigin: true,
        pathRewrite: {
          '^/tensorboard': '/',
        },
      },
    },
  },
  // close eslint checking in Vue CLI
  lintOnSave: false,
};
