import * as common from './common';

/**
 * @param {function} success success callback function
 * @param {function} fail fail callback function
 */
const APIPredict = (split, imageId, success, failed) => {
  common.getRequest(`/predict/${split}/${imageId}`, success, failed);
};

/**
 * @param {function} success success callback function
 * @param {function} fail fail callback function
 */
const APIGetInfluenceImages = (split, imageId, success, failed) => {
  common.getRequest(`/influence/${split}/${imageId}`, success, failed);
};

/**
 * @param {function} success success callback function
 * @param {function} fail fail callback function
 */
const APICalculateInfluence = (configs, success, failed) => {
  common.postRequest(configs, '/influence', success, failed);
};

export { APIPredict, APICalculateInfluence, APIGetInfluenceImages };
