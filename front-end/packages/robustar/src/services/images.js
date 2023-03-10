import { getRequest } from './common';
import { configs } from '../configs';

export const APIGetImageList = async (split, start, num_per_page) => {
  return getRequest(`/image/list/${split}/${start}/${num_per_page}`);
};

/**
 * @param {string} split
 */
export const APIGetSplitLength = async (split) => {
  return getRequest(`/image/${split}`);
};

export const APIGetClassifiedSplitLength = async (split) => {
  return getRequest(`/image/classified/${split}`);
};

/**
 * @param {string} split
 */
export const APIGetClassNames = async (split) => {
  return getRequest(`/image/class/${split}`);
};

/**
 * @param {string} split
 * @param {string} image_url
 */
export const APIGetAnnotated = async (split, image_url) => {
  return getRequest(`/image/annotated/${split}?${configs.imagePathParamName}=${image_url}`);
};

/**
 * @param {string} split
 * @param {string} image_url
 */
export const APIGetNextImage = async (split, image_url) => {
  return getRequest(`/image/next/${split}?${configs.imagePathParamName}=${image_url}`);
};
