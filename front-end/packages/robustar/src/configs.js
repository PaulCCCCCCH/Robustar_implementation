const host = `http://${window?.location?.host ?? ''}`;
console.log(process.env.NODE_ENV);

export const configs = {
  imageSize: 'small', // 'extra small', 'small', 'medium', 'large', 'extra large'
  serverUrl: `${host}/api`,
  socketUrl: host,
  tensorboardUrl:
    process.env.NODE_ENV === 'development' || process.env.NODE_ENV === 'test'
      ? `${process.env.VUE_APP_BASE_URL}:${process.env.VUE_APP_TENSORBOARD_PORT}`
      : `${host}/tensorboard`,
  imageServerUrl: `${host}/api/image`,
  imagePathServerUrl: `${host}/api/dataset`,
  dataBaseDir: '/Robustar2',
  imagePathParamName: 'image_url',
};
