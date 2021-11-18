from objects.RServer import RServer
import json


def get_dataset_file(dataOriginId):

    dataManager = RServer.getServer().dataManager
    datasetFileBuffer = dataManager.datasetFileBuffer

    trainset = dataManager.trainset
    testset = dataManager.testset

    if(datasetFileBuffer.get(dataOriginId)):
        return datasetFileBuffer[dataOriginId]

    dataId = dataOriginId.split("/")
    if dataId[0] == "train":
        if(len(trainset.samples) <= int(dataId[1])):
            return "none"
        filePath = trainset.samples[int(dataId[1])][0]
        filePath = filePath.replace("\\", "/").split("/")
        datasetFileBuffer[dataOriginId] = filePath[-2]+"/"+filePath[-1]
        return get_dataset_file(dataOriginId)
    if dataId[0] == "test":
        if(len(testset.samples) <= int(dataId[1])):
            return "none"
        filePath = testset.samples[int(dataId[1])][0]
        filePath = filePath.replace("\\", "/").split("/")
        datasetFileBuffer[dataOriginId] = filePath[-2]+"/"+filePath[-1]
        return get_dataset_file(dataOriginId)
    if dataId[0] == "test_correct":
        filePath = get_correct(True, int(dataId[1]))[0]
        filePath = filePath.replace("\\", "/").split("/")
        datasetFileBuffer[dataOriginId] = filePath[-2]+"/"+filePath[-1]
        return get_dataset_file(dataOriginId)
    if dataId[0] == "test_mistake":
        filePath = get_correct(False, int(dataId[1]))[0]
        filePath = filePath.replace("\\", "/").split("/")
        datasetFileBuffer[dataOriginId] = filePath[-2]+"/"+filePath[-1]
        return get_dataset_file(dataOriginId)
    return "none"

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
