import { getRequest, postRequest } from './common';
import { configs } from '../configs';

export const APIPredict = async (split, image_url) => {
  return getRequest(`/predict/${split}?${configs.imagePathParamName}=${image_url}`);
};

export const APIGetInfluenceImages = async (split, image_url) => {
  return getRequest(`/influence/${split}?${configs.imagePathParamName}=${image_url}`);
};

export const APICalculateInfluence = async (configs) => {
  return postRequest('/influence', configs);
};
