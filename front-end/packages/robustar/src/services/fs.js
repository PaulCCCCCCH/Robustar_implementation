import { postRequest, getRequest } from './common';

export const APILS = (path, success, failed) => {
    getRequest(`/fs/ls/${path}`, success, failed);
};

export const APIDirLen = (path, success, failed) => {
    getRequest(`/fs/dirlen/${path}`, success, failed);
};

export const APIExist = (path, success, failed) => {
    getRequest(`/fs/exist/${path}`, success, failed);
};

export const APIRmDir = (path, success, failed) => {
    getRequest(`/fs/rm/${path}`, success, failed);
};

export const APIMkDir = (path, success, failed) => {
    getRequest(`/fs/mkdir/${path}`, success, failed);
};

export const APIMkDirs = (path, success, failed) => {
    getRequest(`/fs/mkdirs/${path}`, success, failed);
};

export const APICopyDir = (src_path, dst_path, success, failed) => {
    const data = {
        src_path,
        dst_path,
    };
    postRequest(data, `/fs/cp`, success, failed);
};

export const APIRead = (path, length, success, failed)=> {
    getRequest(`/fs/read/${path}/${length}`, success, failed);
};

export const APIWrite = (data, success, failed) => {
    postRequest(data,`/fs/write/${path}`, success, failed);
};