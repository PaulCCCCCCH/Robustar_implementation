import { getRequest } from './common';

/**
 * @param {function} success success callback function
 * @param {function} fail fail callback function
 */
export const APIGetConfig = (success, failed) => {
  getRequest(`/config`, success, failed);
};
