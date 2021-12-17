import * as common from './common';

/**
 * @param {function} success success callback function
 * @param {function} fail fail callback function
 */
const APIStartTest = (success, failed) => {
  common.postRequest(null, `/test`, success, failed);
};

export { APIStartTest };
