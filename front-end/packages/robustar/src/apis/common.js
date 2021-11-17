import axios from 'axios';
import { configs } from '@/configs.js';

const baseUrl = configs.serverUrl;

const successCode = [200, 201];

const handleResult = (res, success, failed) => {
  // console.log(res)
  if (successCode.includes(res.status)) {
    success(res);
  } else {
    failed(res);
  }
};

const patchRequest = (data, route, success, failed) => {
  if (!failed) {
    failed = (res) => console.log(res);
  }
  axios.patch(`${baseUrl}${route}`, data).then(
    (res) => handleResult(res, success, failed),
    (res) => failed(res)
  );
};

const postRequest = (data, route, success, failed) => {
  if (!failed) {
    failed = (res) => console.log(res);
  }
  axios.post(`${baseUrl}${route}`, data).then(
    (res) => handleResult(res, success, failed),
    (res) => failed(res)
  );
};

/**
 *
 * @param {*} pageNo This is an optional argument
 */
const getRequest = (route, success, failed, pageNo) => {
  if (!failed) {
    failed = (res) => console.log(res);
  }
  let requestUrl = `${baseUrl}${route}`;
  if (pageNo) {
    requestUrl += `?pageNo=${pageNo}`;
  }
  axios.get(requestUrl).then(
    (res) => handleResult(res, success, failed),
    (res) => failed(res)
  );
};

const deleteRequest = (data, route, success, failed) => {
  if (!failed) {
    failed = (res) => console.log(res);
  }
  axios
    .delete(`${baseUrl}${route}`, {
      data,
    })
    .then(
      (res) => handleResult(res, success, failed),
      (res) => failed(res)
    );
};

export { baseUrl, getRequest, patchRequest, postRequest, deleteRequest };
