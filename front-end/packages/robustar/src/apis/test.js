import * as common from './common';

/**
 * @param {function} split the test split ('validation' or 'test')
 * @param {function} success success callback function
 * @param {function} fail fail callback function
 */
const APIStartTest = (split, success, failed) => {
  common.postRequest(split, `/test`, success, failed);
};

export { APIStartTest };
