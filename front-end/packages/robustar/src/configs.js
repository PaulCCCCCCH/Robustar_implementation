export const configs = {
  imageSize: 'small', // 'extra small', 'small', 'medium', 'large', 'extra large'
  serverUrl: `${process.env.VUE_APP_BASE_URL}`,
  imageServerUrl: `${process.env.VUE_APP_BASE_URL}/image`,
  imagePathServerUrl: `${process.env.VUE_APP_BASE_URL}/dataset`,
  dataBaseDir: '/Robustar2',
  imagePathParamName: 'image_url',
};
