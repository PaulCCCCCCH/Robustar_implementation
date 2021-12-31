import * as common from './common';

/**
 * FIXME: Just an example. Not currently used.
 * @param {string} dataset either 'train' or 'test'
 * @param {int} startFrom the id of the first image in the page
 * @param {function} success success callback function
 * @param {function} fail fail callback function
 */
const APIGetSplitLength = (split, success, failed) => {
  common.getRequest(`/image/${split}`, success, failed);
};


/**
 * FIXME: Just an example. Not currently used.
 * @param {string} dataset either 'train' or 'test'
 * @param {int} startFrom the id of the first image in the page
 * @param {function} success success callback function
 * @param {function} fail fail callback function
 */
const APIGetImagesInPage = (dataset, startFrom, success, failed) => {
  common.getRequest(`/${dataset}/${startFrom}`, success, failed);
};

/**
 * FIXME: Just an example. Not currently used.
 * @param {string} dataset either 'train' or 'test'
 * @param {int} imageId the id of the image to retrieve
 */
const APIGetImage = (dataset, imageId, success, failed) => {
  common.getRequest(`/${dataset}/${imageId}`, success, failed);
};

export { APIGetImagesInPage, APIGetImage, APIGetSplitLength };
