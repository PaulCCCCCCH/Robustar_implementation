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
    if (res.data.code == -1) {
      console.log(res.data.msg)
    } else{
      success(res);
    }
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
  axios.post(`/api${baseUrl}${route}`, data).then(
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
  let requestUrl = `/api${route}${pageNo ? `?pageNo=${pageNo}` : ''}`;
  axios.get(requestUrl).then(
    (res) => handleResult(res, success, failed),
    (res) => failed(res)
  );
};

/**
 * make DELETE request
 * @param {string} route
 * @param {function} success callback for success
 * @param {function} failed callback for failure
 * @param {number} pageNo optional
 */
export const deleteRequest = (route, success, failed) => {
  if (!failed) {
    failed = (res) => console.log(res);
  }
  let requestUrl = `/api${route}`;
  axios.delete(requestUrl).then(
    (res) => handleResult(res, success, failed),
    (res) => failed(res)
  );
};
