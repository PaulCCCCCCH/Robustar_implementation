import * as common from './common';

/**
 * @param {object} configs the training configuration
 * @param {function} success success callback function
 * @param {function} fail fail callback function
 */
const APIGeneratePairedDataset = (mirrored_data_path, user_edit_path, success, failed) => {
  common.postRequest({ mirrored_data_path, user_edit_path }, `/generate`, success, failed);
};

export { APIGeneratePairedDataset };
