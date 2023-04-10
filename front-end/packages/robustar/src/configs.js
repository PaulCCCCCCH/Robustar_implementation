const baseUrl = process.env.VUE_APP_BASE_URL;
const clientPort = process.env.VUE_APP_CLIENT_PORT;

export const configs = {
  imageSize: 'small', // 'extra small', 'small', 'medium', 'large', 'extra large'
  serverUrl: `${baseUrl}:${clientPort}/api`,
  socketUrl: `${baseUrl}:${clientPort}`,
  tensorboardUrl: `${baseUrl}:${clientPort}/tensorboard`,
  imageServerUrl: `${baseUrl}:${clientPort}/api/image`,
  imagePathServerUrl: `${baseUrl}:${clientPort}/api/dataset`,
  dataBaseDir: '/Robustar2',
  imagePathParamName: 'image_url',
};
