from os.path import normpath

from objects.RServer import RServer

dataManager = RServer.getServer().dataManager

datasetDir = dataManager.data_root

trainset = dataManager.trainset
testset = dataManager.testset
validationset = dataManager.validationset

datasetFileBuffer = dataManager.datasetFileBuffer

correctTestBuffer = dataManager.correctTestBuffer
incorrectTestBuffer = dataManager.incorrectTestBuffer
correctValidationBuffer = dataManager.correctValidationBuffer
incorrectValidationBuffer = dataManager.incorrectValidationBuffer

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
        imagePath:  The real path to the image, e.g. '/Robustar2/dataset/train/cat/1002.jpg
    """

    split, indexStr = image_id.split('/')
    imageIndex = int(indexStr)

    # If already buffered, just return
    if image_id in datasetFileBuffer:
        return datasetFileBuffer[image_id]

    if split == 'train':
        filePath = trainset.samples[imageIndex][0]
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
        raise NotImplemented

    filePath = normpath(filePath).replace('\\', '/')
    datasetFileBuffer[image_id] = filePath

    return filePath


def get_test_correct(is_correct, image_index):
    if correctTestBuffer == [] or incorrectTestBuffer == []:
        get_classify_test_list(correctTestBuffer, incorrectTestBuffer)

    if is_correct:
        img_num = correctTestBuffer[image_index]
    else:
        img_num = incorrectTestBuffer[image_index]

    return testset.samples[img_num]


def get_validation_correct(is_correct, image_index):
    if correctValidationBuffer == [] or incorrectValidationBuffer == []:
        get_classify_validation_list(correctValidationBuffer, incorrectValidationBuffer)

    if is_correct:
        img_num = correctValidationBuffer[image_index]
    else:
        img_num = incorrectValidationBuffer[image_index]

    return validationset.samples[img_num]


def get_classify_test_list(correct_test_buffer, incorrect_test_buffer):
    with open(test_correct_root, 'r') as f:
        for line in f:
            correct_test_buffer.append(int(line))

    with open(test_incorrect_root, 'r') as f:
        for line in f:
            incorrect_test_buffer.append(int(line))


def get_classify_validation_list(correct_validation_buffer, incorrect_validation_buffer):
    with open(validation_correct_root, 'r') as f:
        for line in f:
            correct_validation_buffer.append(int(line))

    with open(validation_incorrect_root, 'r') as f:
        for line in f:
            incorrect_validation_buffer.append(int(line))
