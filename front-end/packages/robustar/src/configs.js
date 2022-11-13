const host = `http://${window.location.host}`; // e.g., http://localhost:8080
const apiHost = `${host}/api`;

export const configs = {
  imageSize: 'small', // 'extra small', 'small', 'medium', 'large', 'extra large'
  hostUrl: host,
  serverUrl: apiHost,
  socketUrl: host,
  tensorboardUrl: `${host}/tensorboard`,
  imageServerUrl: `${apiHost}/image`,
  imagePathServerUrl: `${apiHost}/dataset`,
  dataBaseDir: '/Robustar2',
  imagePathParamName: 'image_url',
};
