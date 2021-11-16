/* eslint-disable */
module.exports = () => ({
  mode: 'development',
  devServer: {
    compress: true,
    open: true,
    hot: true,
    host: '127.0.0.1',
    static: './examples',
    allowedHosts: 'all',
  },
  devtool: 'eval-source-map',
});
