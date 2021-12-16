import * as common from './common';

/**
 * Send the annotated information to the server to be saved
 * @param {string} dataset either 'train' or 'test'
 * @param {string} dataid the id of the image edited
 * @param {string} image_base64 base64 string repr of the image obtained by Fabric.js API canvas.getDataURL()
 * @param {function} success success callback function
 * @param {function} fail fail callback function
 */
const APISendEdit = (split, image_id, image_height, image_width, image_base64, success, failed) => {
  const data = {
    image: image_base64,
    image_height,
    image_width,
  };
  common.postRequest(data, `/edit/${split}/${image_id}`, success, failed);
};

export { APISendEdit };
