import { getRequest } from './common';

export const APIGetImageList = async (split, start, num_per_page) => {
  return getRequest(`/image/list/${split}/${start}/${num_per_page}`);
};

/**
 * @param {string} split
 */
export const APIGetSplitLength = async (split) => {
  return getRequest(`/image/${split}`);
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
  return getRequest(`/image/annotated/${split}/${image_url}`);
};

/**
 * @param {string} split
 * @param {string} image_url
 */
export const APIGetNextImage = async (split, image_url) => {
  return getRequest(`/image/next/${split}/${image_url}`);
};
