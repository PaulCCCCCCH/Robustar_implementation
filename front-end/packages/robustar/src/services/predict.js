import { getRequest, postRequest } from './common';

export const APIPredict = async (split, image_url) => {
  return getRequest(`/predict/${split}/${image_url}`);
};

export const APIGetInfluenceImages = async (split, imageId) => {
  return getRequest(`/influence/${split}/${imageId}`);
};

export const APICalculateInfluence = async (configs) => {
  return postRequest(configs, '/influence');
};
