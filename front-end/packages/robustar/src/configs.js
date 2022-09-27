const host = `http://${location.host}`; // e.g., http://localhost:8080
const apiHost = `${host}/api`;
const socketHost = `${host}/soc`;

export const configs = {
  imageSize: 'small', // 'extra small', 'small', 'medium', 'large', 'extra large'
  serverUrl: apiHost,
  socketUrl: socketHost,
  imageServerUrl: `${apiHost}/image`,
  imagePathServerUrl: `${apiHost}/dataset`,
  dataBaseDir: '/Robustar2',
  imagePathParamName: 'image_url',
};
