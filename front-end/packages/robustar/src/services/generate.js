import { postRequest } from './common';

/**
 * @param {object} configs the training configuration
 * @param {function} success success callback function
 * @param {function} fail fail callback function
 */
export const APIGeneratePairedDataset = (mirrored_data_path, user_edit_path, success, failed) => {
  postRequest({ mirrored_data_path, user_edit_path }, `/generate`, success, failed);
};
