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
 * @param {string} split
 * @param {string} image_url
 * @param {function} success success callback function
 * @param {function} fail fail callback function
 */
export const APIGetAnnotated = (split, image_url, success, failed) => {
  getRequest(`/image/annotated/${split}/${image_url}`, success, failed);
};


/**
 * @param {string} split 
 * @param {string} image_url 
 * @param {function} success 
 * @param {function} failed 
 */
export const APIGetNextImage = (split, image_url, success, failed) => {
  getRequest(`/image/next/${split}/${image_url}`, success, failed)
}