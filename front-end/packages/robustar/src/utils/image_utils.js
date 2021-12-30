// Not implemented
function getNextImageURLByURL(image_url) {
  return;
}

function getNextImageByIdAndURL(image_id, image_url) {
  const newId = Number(image_id) + 1;
  const arr = image_url.split('/');
  const newUrl = arr.slice(0, arr.length - 1).join('/') + `/${newId}`;
  return [newId, newUrl];
}

/*
 * Return image id and split from a full url, e.g. 'http://localhost:8080/route/train/10
 * gives ["10", "train"]
 */
function getImageUrlFromFullUrl(full_url) {
  const arr = full_url.split('/');
  return [arr[arr.length - 1], arr[arr.length - 2]];
}

export { getNextImageByIdAndURL, getImageUrlFromFullUrl };
