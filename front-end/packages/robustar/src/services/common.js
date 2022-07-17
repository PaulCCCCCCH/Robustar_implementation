import axios from 'axios';
import { configs } from '@/configs.js';

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
      console.log(res.data.msg);
    } else {
      success(res);
    }
  } else {
    failed(res);
  }
};

const validateStatus = (status) => [200, 201].includes(status);

/**
 * make POST request
 * @param {object} data
 * @param {string} route
 * @param {function} success callback for success
 * @param {function} failed callback for failure
 */
// export const postRequest = (data, route, success, failed) => {
//   if (!failed) {
//     failed = (res) => console.log(res);
//   }
//   axios.post(`/api${configs.serverUrl}${route}`, data).then(
//     (res) => handleResult(res, success, failed),
//     (res) => failed(res)
//   );
// };

/**
 * make POST request
 * @param {object} data
 * @param {string} route
 */
export const postRequest = async (data, route) => {
  return axios.post(`/api${route}`, data, { validateStatus: validateStatus });
};

/**
 * make GET request
 * @param {string} route
 * @param {function} success callback for success
 * @param {function} failed callback for failure
 * @param {number} pageNo optional
 */
// export const getRequest = (route, success, failed, pageNo) => {
//   if (!failed) {
//     failed = (res) => console.log(res);
//   }
//   let requestUrl = `/api${route}${pageNo ? `?pageNo=${pageNo}` : ''}`;
//   axios.get(requestUrl).then(
//     (res) => handleResult(res, success, failed),
//     (res) => failed(res)
//   );
// };

/**
 * make GET request
 * @param {string} route
 * @param {number} pageNo optional
 */
export const getRequest = async (route, pageNo) => {
  let requestUrl = `/api${route}${pageNo ? `?pageNo=${pageNo}` : ''}`;
  return axios.get(requestUrl, { validateStatus: validateStatus });
};

/**
 * make DELETE request
 * @param {string} route
 */
export const deleteRequest = async (route) => {
  let requestUrl = `/api${route}`;
  return axios.delete(requestUrl);
};
