import { getRequest } from './common';

/**
 * @param {object} configs the training configuration
 */
export const APIStopTask = async (tid) => {
  console.log(tid);
  console.log(`/task/stop/${tid}`);
  return getRequest(`/task/stop/${tid}`);
};
