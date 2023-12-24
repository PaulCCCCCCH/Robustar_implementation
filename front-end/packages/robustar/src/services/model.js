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
 * @param {string} modelName
 */
export const APISetCurrentModel = async (modelName) => {
    return postRequest(`/model/current/${modelName}`);
};

/**
 * Delete a specific model by its name.
 * @param {string} modelName
 */
export const APIDeleteModel = async (modelName) => {
    return deleteRequest(`/model/${modelName}`);
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

    return postRequest(`/model`, formData);
};

/**
 * Update a model.
 * @param {string} name - Model name
 * @param {Object} metadata - Model metadata
 */
export const APIUpdateModel = async (name, metadata) => {
  const formData = new FormData();
  formData.append('metadata', JSON.stringify(metadata));

  return putRequest(`/model/${name}`, formData);
};

/**
 * Fetch the list of all models.
 */
export const APIGetAllModels = async () => {
    return getRequest(`/model/list`);
};

/**
 * Duplicate a model by its name.
 * @param {string} modelName
 */
export const APIDuplicateModel = async (modelName) => {
  return postRequest(`/model/duplicate/${modelName}`);
};

/**
 * Get predefined model list.
 * @param {string} modelName
 */
export const APIGetPredefinedModels = async () => {
  return getRequest(`/model/predefined`);
};