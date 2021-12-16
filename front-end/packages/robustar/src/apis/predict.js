import * as common from './common';

// TODO: the path should not be hard-coded
/**
 * @param {function} success success callback function
 * @param {function} fail fail callback function
 */
const APIPredict = (split, imageId, success, failed) => {
  common.getRequest(`/predict/${split}/${imageId}`, success, failed);
};

export { APIPredict };
