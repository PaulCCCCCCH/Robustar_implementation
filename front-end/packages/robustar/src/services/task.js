import { getRequest } from './common';

/**
 * @param {object} configs the training configuration
 */
export const APIStopTask = async (tid) => {
  return getRequest(`/task/stop/${tid}`);
};
