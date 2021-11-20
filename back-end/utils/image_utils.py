from objects.RServer import RServer
import json
from os.path import normpath
from utils.path_utils import split_path

dataManager = RServer.getServer().dataManager
datasetFileBuffer = dataManager.datasetFileBuffer

trainset = dataManager.trainset
testset = dataManager.testset


def imageIdToPath(imageId):
    """
    Get the real path of the image specified by its id.

    args: 
        imageId:    The id of the image consisting of the dataset split (train/dev/test) 
                    and an index.
                    e.g.  train/10, test/300

    returns:
        imagePath:  The real path to the image, e.g. '/Robustar2/dataset/train/cat/1002.jpg
    """

    split, indexStr = imageId.split('/')
    imageIndex = int(indexStr)

    # If already buffered, just return
    if imageId in datasetFileBuffer:
        return datasetFileBuffer[imageId]

    filePath = None
    if split == 'train':
        filePath = trainset.samples[imageIndex][0]
    elif split == 'test':
        filePath = testset.samples[imageIndex][0]
    elif split == 'test_correct':
        filePath = get_correct(True, imageIndex)[0]
    elif split == 'test_mistake':
        filePath = get_correct(False, imageIndex)[0]
    else:
        # data split not supported
        raise NotImplemented

    filePath = normpath(filePath)
    datasetFileBuffer[imageId] = filePath
    return filePath 


def get_correct(isCorrect, id):

    dataManager = RServer.getServer().dataManager
    CorrectBuffer = dataManager.correctBuffer
    MistakeBuffer = dataManager.mistakeBuffer

    testset = dataManager.testset

    if CorrectBuffer is None or MistakeBuffer is None:
        CorrectBuffer, MistakeBuffer = get_classify_list()

    if isCorrect:
        img_num = CorrectBuffer[id]
    else:
        img_num = MistakeBuffer[id]

    return testset.samples[img_num]


# TODO: Not implemented
# 获得正确分类和错误分类的编号
def get_classify_list():
    correct_list, mistake_list = [], []
    # 读取分类结果
    with open('classify.json', 'r') as f:
        results = json.load(f)
    # 处理每一条分类结果
    for i in range(len(results)):
        r = results[i]
        if r[0] == r[1]:
            correct_list.append(i)
        else:
            mistake_list.append(i)
    return correct_list, mistake_list
