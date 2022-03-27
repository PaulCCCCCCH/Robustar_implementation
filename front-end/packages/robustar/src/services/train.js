import { getRequest, postRequest } from './common';

/**
 * @param {object} configs the training configuration
 * @param {function} success success callback function
 * @param {function} fail fail callback function
 */
export const APIStartTrain = (configs, success, failed) => {
  postRequest(configs, `/train`, success, failed);
};

export const APIStopTrain = (success, failed) => {
  getRequest(`/train/stop`, success, failed);
};
