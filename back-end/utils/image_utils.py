from os.path import normpath
from objects.RServer import RServer
from utils.edit_utils import get_train_and_paired_path

dataManager = RServer.getDataManager()

datasetDir = dataManager.data_root

trainset = dataManager.trainset
testset = dataManager.testset
validationset = dataManager.validationset
pairedset = dataManager.pairedset
proposedset = dataManager.proposedset

datasetFileBuffer = dataManager.datasetFileBuffer


def getImagePath(split, start=None, end=None):
    """
    Get the real paths of the images in the range start-end
    args: 
        split: 'train', 'annotated', 'validation', 'proposed', 'test', 'validation_correct', 'validation_incorrect'
        'test_correct', 'test_incorrect'
    returns:
        imagePath:  The real path to the image, e.g. '/Robustar2/dataset/train/cat/1002.jpg'
    """

    # # If already buffered, just return
    # if image_url in datasetFileBuffer:
    #     return datasetFileBuffer[image_url]
    if split == 'validation_correct':
        return dataManager.validationset.get_record(correct=True, start=start, end=end)
    if split == 'validation_incorrect':
        return dataManager.validationset.get_record(correct=False, start=start, end=end)
    if split == 'test_correct':
        return dataManager.testset.get_record(correct=True, start=start, end=end)
    if split == 'test_incorrect':
        return dataManager.testset.get_record(correct=False, start=start, end=end)
    else:
        if split not in dataManager.split_dict:
            raise NotImplementedError('Invalid data split!')
        return dataManager.split_dict[split].get_image_list(start, end)
    
def getNextImagePath(split, path):
    allowed_splits = ['train', 'annotated', 'proposed']
    if split not in allowed_splits:
        raise NotImplementedError('Next image only supported for {}'.format(allowed_splits))

    return dataManager.split_dict[split].get_next_image(path)


def getClassStart(split):
    if split == 'train' or split == 'annotated':
        dataset = trainset
    elif split == 'validation' or split == 'validation_correct' or split == 'validation_incorrect':
        dataset = validationset
    elif split == 'test' or split == 'test_correct' or split == 'test_incorrect':
        dataset = testset
    else:
        raise NotImplementedError('Data split not supported')

    class_ls = dataset.classes
    class_starts = dict()

    if split in ['train', 'annotated', 'validation', 'test']:
        buffer = dataset.samples
    elif split == 'validation_correct':
        buffer = dataManager.validationset.buffer_correct
    elif split == 'validation_incorrect':
        buffer = dataManager.validationset.buffer_incorrect
    elif split == 'test_correct':
        buffer = dataManager.testset.buffer_correct
    elif split == 'test_incorrect':
        buffer = dataManager.testset.buffer_incorrect
    else:
        raise NotImplementedError('Data split not supported')

    for i in range(len(class_ls)):
        num = binarySearchLeftBorder(buffer, i)
        class_starts[class_ls[i]] = num

    return class_starts


def binarySearchLeftBorder(ls, target: int):
    """
    Args
        ls: Image.samples, a list of (image_path, class_index) pairs
        target: target class index 
    """
    left = 0
    right = len(ls)
    while left < right:
        mid = (left + right) // 2
        if ls[mid][1] >= target:
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

    return len(getImagePath(split, None, None))
