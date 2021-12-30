import * as common from './common';

/**
 * @param {object} configs the training configuration
 * @param {function} success success callback function
 * @param {function} fail fail callback function
 */
const APIStartTrain = (configs, success, failed) => {
  common.postRequest(configs, `/train`, success, failed);
};

const APIStopTrain = (success, failed) => {
  common.getRequest(`/train/stop`, success, failed);
};

export { APIStartTrain, APIStopTrain };
