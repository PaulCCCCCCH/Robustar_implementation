import { postRequest, getRequest, deleteRequest } from './common';

/**
 * Send the annotated information to the server to be saved
 * @param {string} dataset either 'train' or 'test'
 * @param {string} dataid the id of the image edited
 * @param {string} image_base64 base64 string repr of the image obtained by Fabric.js API canvas.getDataURL()
 * @param {function} success success callback function
 * @param {function} fail fail callback function
 */
export const APISendEdit = (
  split,
  image_url,
  image_height,
  image_width,
  image_base64,
  success,
  failed
) => {
  const data = {
    image: image_base64,
    image_height,
    image_width,
  };
  postRequest(data, `/edit/${split}/${image_url}`, success, failed);
};

export const APIGetProposedEdit = (split, image_url, success, failed) => {
  getRequest(`/propose/${split}/${image_url}`, success, failed);
};

export const APIStartAutoAnnotate = (split, data, success, failed) => {
  postRequest(data, `/auto-annotate/${split}`, success, failed);
};

export const APIDeleteEdit = (split, image_url, success, failed) => {
  deleteRequest(`/edit/${split}/${image_url}`, success, failed);
};
