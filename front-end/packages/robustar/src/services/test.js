import { postRequest } from './common';

/**
 * @param {function} split the test split ('validation' or 'test')
 * @param {function} success success callback function
 * @param {function} fail fail callback function
 */
export const APIStartTest = (split, success, failed) => {
  postRequest(split, `/test`, success, failed);
};
