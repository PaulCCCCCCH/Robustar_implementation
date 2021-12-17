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

export { getNextImageByIdAndURL };
