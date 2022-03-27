import { getRequest, postRequest } from './common';

/**
 * @param {function} success success callback function
 * @param {function} fail fail callback function
 */
export const APIPredict = (split, imageId, success, failed) => {
  getRequest(`/predict/${split}/${imageId}`, success, failed);
};

/**
 * @param {function} success success callback function
 * @param {function} fail fail callback function
 */
export const APIGetInfluenceImages = (split, imageId, success, failed) => {
  getRequest(`/influence/${split}/${imageId}`, success, failed);
};

/**
 * @param {function} success success callback function
 * @param {function} fail fail callback function
 */
export const APICalculateInfluence = (configs, success, failed) => {
  postRequest(configs, '/influence', success, failed);
};
