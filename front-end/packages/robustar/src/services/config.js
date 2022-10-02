import { getRequest } from './common';

export const APIGetConfig = async () => {
  return getRequest(`/config`);
};
