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
 */
export const postRequest = async (route, data) => {
  return axios.post(`/api${route}`, data, { validateStatus: validateStatus });
};

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
  return axios.delete(requestUrl, { validateStatus: validateStatus });
};

/**
 * make PUT request
 * @param {object} data
 * @param {string} route
 */
export const putRequest = async (route, data) => {
  return axios.put(`/api${route}`, data, { validateStatus: validateStatus });
};
