import os
import pickle as pkl
import json
from PIL import Image

import json
import numpy as np

image_extensions = ['jpg', 'jpeg', 'png']

def get_image_data(image_data, target_width):
    assert image_data is not None

    # An rgba value of (255, 255, 255, 255) means the user has marked the area.
    # We assign a 1 for this pixel.
    source = []
    temp = image_data.split(',')
    for i in range(0, len(temp), 4):
        if temp[i+0] == temp[i+1] == temp[i+2] == temp[i+3] == '255':
            source.append(1)
        else:
            source.append(0)

    current_width = int(len(source) ** 0.5)
    ratio = 1.0 * current_width / target_width
    result = []

    """
    Fixme: the following code is for scaling. E.g. An image was 32*32, but it
    was scaled (up sampling) to 224*224 on the drawing board for easier editing.
    The user-edit array would then be 224*224, and we would need to scale it back
    to 32*32, or something else.

    Do we still need to keep this?
    """
    y = ratio / 2
    for _ in range(target_width):
        x = 0
        for _ in range(target_width):
            p = int(y) * int(current_width) + int(x)
            if p >= len(source):
                continue
            result.append(source[p])
            x += ratio
        y += ratio

    return np.array(result).reshape(target_width, target_width)



def generate_paired_data(mirroredDataPath, userEditFile):
    mirroredDataPath = os.path.normpath(mirroredDataPath)
    newDataPath = os.sep.join(mirroredDataPath.split(os.sep)[:-1] + ['paired'])
    if not os.path.exists(newDataPath):
        os.mkdir(newDataPath)

    # Read user edit information
    with open(userEditFile) as f:
        userEditDict = json.load(f)
    userEditDict = {os.path.normpath(k): userEditDict[k] for k in userEditDict.keys()}

    # Get the image size of the original data set
    d = os.listdir(mirroredDataPath)[0]
    classFolderMirrored = '{}/{}'.format(mirroredDataPath, d)
    img = '{}/{}'.format(classFolderMirrored, os.listdir(classFolderMirrored)[0])
    with open(img, 'rb') as f:
        img = Image.open(f)
        targetSize = img.size[0]

    # Each image has an index, from 0 to len(dataset) - 1
    image_idx = 0
    # iterate through each class folder (e.g. d = ./bird, ./cat, etc.)
    for d in os.listdir(mirroredDataPath):
        classFolderMirrored = '{}/{}'.format(mirroredDataPath, d)
        classFolderNew = '{}/{}'.format(newDataPath, d)
        if not os.path.exists(classFolderNew):
            os.mkdir(classFolderNew)

        # Filter out files with extensions not in the 'image_extensions' variable
        imgNames = list(filter(lambda n: any(n.lower().endswith(ext) for ext in image_extensions), os.listdir(classFolderMirrored)))
        for imgName in imgNames:
            imgNew = os.path.normpath('{}/{}'.format(classFolderNew, imgName))

            # search_key is '/train/0', '/train/1', etc.
            searchKey = os.path.normpath('/{}/{}'.format(mirroredDataPath.split(os.sep)[-1], image_idx))
            if dictLooseContains(userEditDict, searchKey):  # User edited the image. Creating paired image for this image
                                                            # If a paired image already exists for this image, it will be replaced
                print("Found edit!")
                imageData = dictLooseGetKey(userEditDict, searchKey)
                userEditArr = get_image_data(imageData, targetSize) # useEditArr is a numpy array
                with open(imgNew, 'wb') as f:
                    pkl.dump(userEditArr, f)
            else:  # User has not edited the image. If paired image already exists, do nothing. Otherwise generate a placeholder.
                if not os.path.exists(imgNew):
                    with open(imgNew, 'wb') as f:
                        pkl.dump(None, f)
                    # np.save(imgNew, userEditArr) # This gives wrong extension

            image_idx += 1  # increment image index


# Check if the normalized key is in the dictionary
def dictLooseContains(_dict, key):
    return os.path.normpath(key) in _dict


# 模糊读取json的key
def dictLooseGetKey(_dict, key):
    looseKey = os.path.normpath(key)
    if looseKey in _dict:
        return _dict[key]
    return None

if __name__ == "__main__":
    with open('user-edit.json') as f:
        obj = json.load(f)
    data = get_image_data(obj['/train/1'], 224)
    print(data)
    print(data.shape)
    generate_paired_data('./dataset/ten/train', 'user-edit.json')
