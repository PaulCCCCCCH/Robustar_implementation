import { getRequest, postRequest } from './common';
import { configs } from '../configs';

/**
 * @param {function} success success callback function
 * @param {function} fail fail callback function
 */
export const APIPredict = (split, image_url, success, failed) => {
  getRequest(`/predict/${split}?${configs.imagePathParamName}=${image_url}`, success, failed);
};

/**
 * @param {function} success success callback function
 * @param {function} fail fail callback function
 */
export const APIGetInfluenceImages = (split, image_url, success, failed) => {
  getRequest(`/influence/${split}?${configs.imagePathParamName}=${image_url}`, success, failed);
};

/**
 * @param {function} success success callback function
 * @param {function} fail fail callback function
 */
export const APICalculateInfluence = (configs, success, failed) => {
  postRequest(configs, '/influence', success, failed);
};
