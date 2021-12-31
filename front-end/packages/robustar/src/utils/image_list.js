import { configs } from '@/configs.js';

/**
 * Converts the index of the image within a page to its global id
 * @param {*} page_idx index of the page
 * @param {*} index index of the image within the page
 */
const imagePageIdx2Id = (page_idx, index) => {
  return page_idx * configs.imagePerPage + index;
};

const imageCoord2Idx = (row, col) => {
  return row * configs.imageListCol + col;
};

const getPageNumber = (imageIdx) => {
  return Math.floor(imageIdx / configs.imagePerPage)
}

export { imagePageIdx2Id, imageCoord2Idx, getPageNumber };
