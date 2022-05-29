import * as common from './common';

/**
 * @param {object} configs the training configuration
 * @param {function} success success callback function
 * @param {function} fail fail callback function
 */
const APIStopTask = (tid, success, failed) => {
  console.log(tid);
  console.log(`/task/stop/${tid}`);
  common.getRequest(`/task/stop/${tid}`, success, failed);
};

export { APIStopTask };
