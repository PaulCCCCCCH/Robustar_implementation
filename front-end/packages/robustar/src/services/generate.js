import { postRequest } from './common';

/**
 * @param {object} configs the training configuration
 */
export const APIGeneratePairedDataset = async (mirrored_data_path, user_edit_path) => {
  return postRequest(`/generate`, { mirrored_data_path, user_edit_path });
};
