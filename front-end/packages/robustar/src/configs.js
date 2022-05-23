export const configs = {
  imagePerPage: 18, // suggested values: multiple of 12/imageRowSpan
  imageColSpan: 2, // how many columns (12 in total) an image should occupy in a row
  MAX_IMAGE_PER_PAGE: 30,
  MIN_IMAGE_PER_PAGE: 1,
  MAX_IMAGE_COL_SPAN: 12,
  MIN_IMAGE_COL_SPAN: 1,
  serverUrl: `${process.env.VUE_APP_BASE_URL}`,
  imageServerUrl: `${process.env.VUE_APP_BASE_URL}/image`,
  imagePathServerUrl: `${process.env.VUE_APP_BASE_URL}/dataset`,
};
