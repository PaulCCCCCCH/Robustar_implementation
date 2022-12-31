from os.path import normpath
import os.path as osp
from objects.RServer import RServer
from utils.path_utils import to_unix
import base64
import mimetypes


def getImagePath(split, start=None, end=None):
    """
    Get the real paths of the images in the range start-end
    args:
        split: 'train', 'annotated', 'validation', 'proposed', 'test', 'validation_correct', 'validation_incorrect'
        'test_correct', 'test_incorrect'
    returns:
        imagePath:  The real path to the image, e.g. '/Robustar2/dataset/train/cat/1002.jpg'
    """
    dataManager = RServer.getDataManager()
    if split == "validation_correct":
        return dataManager.validationset.get_record(correct=True, start=start, end=end)
    if split == "validation_incorrect":
        return dataManager.validationset.get_record(correct=False, start=start, end=end)
    if split == "test_correct":
        return dataManager.testset.get_record(correct=True, start=start, end=end)
    if split == "test_incorrect":
        return dataManager.testset.get_record(correct=False, start=start, end=end)
    if split in dataManager.split_dict:
        return dataManager.split_dict[split].get_image_list(start, end)
    raise NotImplementedError("Invalid data split")


def get_annotated(split: str, path: str):

    dataManager = RServer.getDataManager()
    if split == "annotated":
        paired_path = path
    elif split == "train":
        paired_path = dataManager.pairedset.get_paired_by_train(path)
    else:
        return ""

    if paired_path is None:
        return ""
    return ""


def getNextImagePath(split, path):
    dataManager = RServer.getDataManager()
    allowed_splits = ["train", "annotated", "proposed"]
    if split not in allowed_splits:
        raise NotImplementedError("Split {} not supported".format(split))

    return dataManager.split_dict[split].get_next_image(path)


def getClassStart(split):
    dataManager = RServer.getDataManager()
    trainset = dataManager.trainset
    testset = dataManager.testset
    validationset = dataManager.validationset

    if split == "train" or split == "annotated":
        dataset = trainset
    elif (
        split == "validation"
        or split == "validation_correct"
        or split == "validation_incorrect"
    ):
        dataset = validationset
    elif split == "test" or split == "test_correct" or split == "test_incorrect":
        dataset = testset
    else:
        raise NotImplementedError("Data split not supported")

    class_ls = dataset.classes
    class_starts = dict()

    if split in ["train", "annotated", "validation", "test"]:
        buffer = dataset.samples
    elif split == "validation_correct":
        buffer = dataManager.validationset.buffer_correct
    elif split == "validation_incorrect":
        buffer = dataManager.validationset.buffer_incorrect
    elif split == "test_correct":
        buffer = dataManager.testset.buffer_correct
    elif split == "test_incorrect":
        buffer = dataManager.testset.buffer_incorrect
    else:
        raise NotImplementedError("Data split not supported")

    for i in range(len(class_ls)):
        num = binarySearchLeftBorder(buffer, i)
        class_starts[class_ls[i]] = num

    return class_starts


def getImgData(dataset_img_path):
    dataset_file_buffer = RServer.getDataManager().dataset_file_buffer
    normal_path = to_unix(dataset_img_path)

    if osp.exists(normal_path):
        if normal_path not in dataset_file_buffer:
            refreshImgData(normal_path)
        image_data = dataset_file_buffer[normal_path]
        return image_data
    else:
        raise Exception


def imageToBase64String(path: str) -> str:
    """
    Convert an image to it's base64 string
    args:
        path: path to the image to be converted
    returns:
        base64 string of the image
    """
    normal_path = to_unix(path)
    with open(normal_path, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode()
    image_mime = mimetypes.guess_type(normal_path)[0]

    image_data = "data:" + image_mime + ";base64," + image_base64
    return image_data


def refreshImgData(path: str):
    dataManager = RServer.getDataManager()
    dataset_file_queue = dataManager.dataset_file_queue
    dataset_file_buffer = dataManager.dataset_file_buffer
    dataset_file_queue_len = dataManager.dataset_file_queue_len

    normal_path = to_unix(path)
    image_data = imageToBase64String(normal_path)
    dataset_file_queue.append(normal_path)
    if len(dataset_file_queue) > dataset_file_queue_len:
        temp_path = dataset_file_queue.popleft()
        del dataset_file_buffer[temp_path]
    dataset_file_buffer[normal_path] = image_data


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
