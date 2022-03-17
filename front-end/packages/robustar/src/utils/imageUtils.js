import { configs } from '@/configs.js';

/**
 * Converts the index of the image within a page to its global id
 * @param {number} page_idx index of the page
 * @param {number} index index of the image within the page
 */
export const imagePageIdx2Id = (page_idx, index) => {
  return page_idx * configs.imagePerPage + index;
};

/**
 * Converts the coordinate of the image to its global id
 * @param {number} row
 * @param {number} col
 */
export const imageCoord2Idx = (row, col) => {
  return row * configs.imageListCol + col;
};

export const getPageNumber = (imageIdx) => {
  return Math.floor(imageIdx / configs.imagePerPage);
};

/**
 * derive id and url for next image according current id and url
 * @param {number} image_id
 * @param {string} image_url
 * @returns
 */
export const getNextImageByIdAndURL = (image_id, image_url) => {
  const newId = Number(image_id) + 1;
  const arr = image_url.split('/');
  const newUrl = arr.slice(0, arr.length - 1).join('/') + `/${newId}`;
  return [newId, newUrl];
};

/*
 * Return image id and split from a full url, e.g. 'http://localhost:8080/route/train/10
 * gives ["10", "train"]
 */
export const getImageUrlFromFullUrl = (full_url) => {
  const arr = full_url.split('/');
  return [arr[arr.length - 1], arr[arr.length - 2]];
};

/*
 * Replace the split and image id in a full url, e.g.
 * Changing 'http://localhost:8080/route/train/10
 * to 'http://localhost:8080/route/annotated/20
 */
export const replaceSplitAndId = (full_url, split, image_id) => {
  const arr = full_url.split('/');
  const newUrl = arr.slice(0, arr.length - 2).join('/') + `/${split}` + `/${image_id}`;
  return newUrl;
};
