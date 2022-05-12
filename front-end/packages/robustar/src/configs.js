export const configs = {
  imagePerPage: 18, // suggested values: 12 or 18 (multiple of 6)
  serverUrl: process.env.VUE_APP_BASE_URL,
  imageServerUrl: `${process.env.VUE_APP_BASE_URL}/image`,
  imagePathServerUrl: `${process.env.VUE_APP_BASE_URL}/dataset`,
};
