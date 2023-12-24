import { postRequest } from './common';

/**
 * @param {function} split the test split ('validation' or 'test')
 */
export const APIStartTest = async (split) => {
  return postRequest(split, `/test`);
};
