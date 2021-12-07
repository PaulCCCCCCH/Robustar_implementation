import * as common from './common'

// TODO: the path should not be hard-coded
/**
 * @param {function} success success callback function
 * @param {function} fail fail callback function
 */
const APIPredict = (dataset, imageId, success, failed) => {
    common.getRequest(`predict/${dataset}/${imageId}`, success, failed)
}

export { APIPredict }