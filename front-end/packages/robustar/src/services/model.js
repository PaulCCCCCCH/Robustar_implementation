import { getRequest, postRequest, deleteRequest, putRequest } from './common';
import { configs } from '../configs';

/**
 * Fetch the currently active model's metadata.
 */
export const APIGetCurrentModel = async () => {
  return getRequest(`/model/current`);
};

/**
 * Set a specific model as the current active model.
 * @param {string} modelID
 */
export const APISetCurrentModel = async (modelID) => {
  return postRequest(`/model/current/${modelID}`);
};

/**
 * Delete a specific model by its ID.
 * @param {string} modelID
 */
export const APIDeleteModel = async (modelID) => {
  return deleteRequest(`/model/${modelID}`);
};

/**
 * Upload a new model.
 * @param {Object} metadata - Model metadata
 * @param {string|null} code - Model code (for custom models)
 * @param {File|null} weightFile - Weight file (if available)
 */
export const APIUploadModel = async (metadata, code = null, weightFile = null) => {
  const formData = new FormData();
  formData.append('metadata', JSON.stringify(metadata));

  if (code) formData.append('code', code);
  if (weightFile) formData.append('weight_file', weightFile);
  console.log(metadata)
  return postRequest(`/model`, formData);
};

/**
 * Update a model.
 * @param {int} id - Model id
 * @param {Object} metadata - Model metadata
 */
export const APIUpdateModel = async (id, metadata) => {
  const formData = new FormData();
  formData.append('metadata', JSON.stringify(metadata));

  return putRequest(`/model/${id}`, formData);
};

/**
 * Fetch the list of all models.
 */
export const APIGetAllModels = async () => {
  return getRequest(`/model/list`);
};

/**
 * Duplicate a model by its id.
 * @param {string} modelID
 */
export const APIDuplicateModel = async (modelID) => {
  return postRequest(`/model/duplicate/${modelID}`);
};

/**
 * Get predefined model list.
 * @param {string} modelName
 */
export const APIGetPredefinedModels = async () => {
  return getRequest(`/model/predefined`);
};
