import axios from 'axios';
import { configs } from '@/configs.js';

const baseUrl = configs.serverUrl;

const successCode = [200, 201];

/**
 * invoke callback according to status code
 * @param {object} res result
 * @param {function} success callback for success
 * @param {function} failed callback for failure
 */
const handleResult = (res, success, failed) => {
  if (successCode.includes(res.status)) {
    success(res);
  } else {
    failed(res);
  }
};

/**
 * make POST request
 * @param {object} data
 * @param {string} route
 * @param {function} success callback for success
 * @param {function} failed callback for failure
 */
export const postRequest = (data, route, success, failed) => {
  if (!failed) {
    failed = (res) => console.log(res);
  }
  axios.post(`${baseUrl}${route}`, data).then(
    (res) => handleResult(res, success, failed),
    (res) => failed(res)
  );
};

/**
 * make GET request
 * @param {string} route
 * @param {function} success callback for success
 * @param {function} failed callback for failure
 * @param {number} pageNo optional
 */
export const getRequest = (route, success, failed, pageNo) => {
  if (!failed) {
    failed = (res) => console.log(res);
  }
  let requestUrl = `${baseUrl}${route}${pageNo ? `?pageNo=${pageNo}` : ''}`;
  axios.get(requestUrl).then(
    (res) => handleResult(res, success, failed),
    (res) => failed(res)
  );
};
