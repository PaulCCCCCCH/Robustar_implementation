import { postRequest, getRequest, deleteRequest } from './common';

/**
 * Send the annotated information to the server to be saved
 * @param {string} dataset either 'train' or 'test'
 * @param {string} dataid the id of the image edited
 * @param {string} image_base64 base64 string repr of the image obtained by Fabric.js API canvas.getDataURL()
 */
export const APISendEdit = async ({
  split,
  image_url,
  image_height,
  image_width,
  image_base64,
}) => {
  const data = {
    image: image_base64,
    image_height,
    image_width,
  };
  return postRequest(data, `/edit/${split}/${image_url}`);
};

export const APIGetProposedEdit = async (split, image_url) => {
  return getRequest(`/propose/${split}/${image_url}`);
};

export const APIStartAutoAnnotate = async (split, data) => {
  return postRequest(data, `/auto-annotate/${split}`);
};

export const APIDeleteEdit = async (split, image_url) => {
  return deleteRequest(`/edit/${split}/${image_url}`);
};
