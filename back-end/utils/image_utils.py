from os.path import normpath

from objects.RServer import RServer

dataManager = RServer.getServer().dataManager

datasetDir = dataManager.data_root

trainset = dataManager.trainset
testset = dataManager.testset
validationset = dataManager.validationset
pairedset = dataManager.pairedset

datasetFileBuffer = dataManager.datasetFileBuffer

test_correct_root = dataManager.test_correct_root
test_incorrect_root = dataManager.test_incorrect_root
validation_correct_root = dataManager.validation_correct_root
validation_incorrect_root = dataManager.validation_incorrect_root


def imageURLToPath(image_id):
    """
    Get the real path of the image specified by its id.
    args: 
        imageId:    The id of the image consisting of the dataset split (train/dev/test) 
                    and an index.
                    e.g.  train/10, test/300
    returns:
        imagePath:  The real path to the image, e.g. '/Robustar2/dataset/train/cat/1002.jpg'
    """

    split, indexStr = image_id.split('/')
    imageIndex = int(indexStr)

    # If already buffered, just return
    if image_id in datasetFileBuffer:
        return datasetFileBuffer[image_id]
    if split == 'train':
        filePath = trainset.samples[imageIndex][0]
    elif split == 'annotated':
        filePath = get_annotated(imageIndex)[0]
    elif split == 'validation':
        filePath = validationset.samples[imageIndex][0]
    elif split == 'test':
        filePath = testset.samples[imageIndex][0]
    elif split == 'validation_correct':
        filePath = get_validation_correct(True, imageIndex)[0]
    elif split == 'validation_incorrect':
        filePath = get_validation_correct(False, imageIndex)[0]
    elif split == 'test_correct':
        filePath = get_test_correct(True, imageIndex)[0]
    elif split == 'test_incorrect':
        filePath = get_test_correct(False, imageIndex)[0]
    else:
        # data split not supported
        raise NotImplemented('Data split not supported')

    filePath = normpath(filePath).replace('\\', '/')
    datasetFileBuffer[image_id] = filePath

    return filePath


def getClassStart(split):
    if split == 'train' or split == 'annotated':
        dataset_ls = trainset.samples
        dataset_len = len(dataset_ls)
        class_ls = trainset.classes
        class_idx = trainset.class_to_idx
    elif split == 'validation' or split == 'validation_correct' or split == 'validation_incorrect':
        dataset_ls = validationset.samples
        dataset_len = len(dataset_ls)
        class_ls = validationset.classes
        class_idx = validationset.class_to_idx
    elif split == 'test' or split == 'test_correct' or split == 'test_incorrect':
        dataset_ls = testset.samples
        dataset_len = len(dataset_ls)
        class_ls = testset.classes
        class_idx = testset.class_to_idx
    else:
        raise NotImplemented('Data split not supported')
    print(class_idx)

    for i in range(len(class_ls)):
        num = binarySearchLeftBorderTuple(dataset_ls, dataset_len, i)
        class_idx[class_ls[i]] = num

    if split == 'validation_correct':
        buffer = dataManager.correctValidationBuffer
    elif split == 'validation_incorrect':
        buffer = dataManager.incorrectValidationBuffer
    elif split == 'test_correct':
        buffer = dataManager.correctTestBuffer
    elif split == 'test_incorrect':
        buffer = dataManager.incorrectTestBuffer
    else:
        return class_idx

    for i in range(len(class_ls)):
        num = binarySearchLeftBorder(buffer, len(buffer), class_idx[class_ls[i]])
        class_idx[class_ls[i]] = num

    return class_idx


def binarySearchLeftBorderTuple(ls, length, target):
    left = 0
    right = length
    while left < right:
        mid = (left + right) // 2
        if ls[mid][1] >= target:
            right = mid
        else:
            left = mid + 1
    return left


def binarySearchLeftBorder(ls, length, target):
    left = 0
    right = length
    while left < right:
        mid = (left + right) // 2
        if ls[mid] >= target:
            right = mid
        else:
            left = mid + 1
    return left


def getSplitLength(split):
    """
    Get the length of a data split

    args: 
        split:  e.g. 'train', 'validation', 'test_correct'

    returns:
        The length of the data split as an integer
    """

    if split not in dataManager.split_dict:
        raise NotImplemented('Data split not supported')
    if split == 'annotated':
        return len(dataManager.split_dict[split][0])

    return len(dataManager.split_dict[split])


def get_validation_correct(is_correct, image_index):
    correctValidationBuffer = dataManager.correctValidationBuffer
    incorrectValidationBuffer = dataManager.incorrectValidationBuffer

    if is_correct:
        img_num = correctValidationBuffer[image_index]
    else:
        img_num = incorrectValidationBuffer[image_index]

    return validationset.samples[img_num]


def get_test_correct(is_correct, image_index):
    correctTestBuffer = dataManager.correctTestBuffer
    incorrectTestBuffer = dataManager.incorrectTestBuffer

    if is_correct:
        img_num = correctTestBuffer[image_index]
    else:
        img_num = incorrectTestBuffer[image_index]

    return testset.samples[img_num]

def get_annotated_from_train(train_image_index):
    if int(train_image_index) in dataManager.annotatedInvBuffer:
        return dataManager.annotatedInvBuffer[int(train_image_index)]
    return None

def get_train_from_annotated(annotated_image_index):
    return dataManager.annotatedBuffer[int(annotated_image_index)]

def get_annotated(image_index):
    img_num = dataManager.annotatedBuffer[int(image_index)]
    return pairedset.samples[img_num]