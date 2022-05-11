import { getRequest } from './common';

export const APIGetImageList = (split, start, num_per_page, success, failed) => {
  getRequest(`/image/list/${split}/${start}/${num_per_page}`, success, failed);
};

/**
 * @param {string} split
 * @param {function} success success callback function
 * @param {function} fail fail callback function
 */
export const APIGetSplitLength = (split, success, failed) => {
  getRequest(`/image/${split}`, success, failed);
};

/**
 * @param {string} split
 * @param {function} success success callback function
 * @param {function} fail fail callback function
 */
export const APIGetClassNames = (split, success, failed) => {
  getRequest(`/image/class/${split}`, success, failed);
};

/**
 * @param {string} image_id
 * @param {function} success success callback function
 * @param {function} fail fail callback function
 */
export const APIGetAnnotated = (image_id, success, failed) => {
  getRequest(`/image/get-annotated/${image_id}`, success, failed);
};

/**
 * FIXME: Just an example. Not currently used.
 * @param {string} dataset either 'train' or 'test'
 * @param {int} startFrom the id of the first image in the page
 * @param {function} success success callback function
 * @param {function} fail fail callback function
 */
export const APIGetImagesInPage = (dataset, startFrom, success, failed) => {
  getRequest(`/${dataset}/${startFrom}`, success, failed);
};

/**
 * FIXME: Just an example. Not currently used.
 * @param {string} dataset either 'train' or 'test'
 * @param {int} imageId the id of the image to retrieve
 */
export const APIGetImage = (dataset, imageId, success, failed) => {
  getRequest(`/${dataset}/${imageId}`, success, failed);
};
