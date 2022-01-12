import * as common from './common';

/**
 * @param {function} success success callback function
 * @param {function} fail fail callback function
 */
const APIGetConfig = (success, failed) => {
  common.getRequest(`/config`, success, failed);
};

export { APIGetConfig };
