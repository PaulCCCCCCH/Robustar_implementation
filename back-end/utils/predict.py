from modules.visualize_module.flashtorch_.utils import apply_transforms, load_image
from objects.RModelWrapper import RModelWrapper
import torch
import modules.influence_module as ptif
import threading
import time
from objects.RDataManager import RDataManager
from objects.RTask import RTask, TaskType
import pickle
from utils.path_utils import to_unix


# Turns prediction results into array
def convert_predict_to_array(output):
    """
    args:
        output: a tensor of shape (1, num_of_classes) 
    """
    result = []
    for prob in output[0]:
        result.append(float(prob))

    # print(result)
    return result


def get_image_prediction(modelWrapper: RModelWrapper, imgpath: str, imgsize: int, argmax=False):
    """
    Get the probability for each class predicted by the model on the given image.
    If `argmax` is set to true, return the index of the most probable class.
    
    args:
        model:      The model to make the predictions
        imgpath:    Path to the image to be predicted
        imgsize:    Resize (scale) the input image to imgsize*imgsize.
    """
    try:
        image = load_image(imgpath)
        image = apply_transforms(image,imgsize)
        image = image.to(modelWrapper.device)

        model = modelWrapper.model

        out_score = model(image) # size: (1, num_classes). For imageNet, shape is (1, 10)

        if argmax:
            _, predict = torch.max(out_score, 1)
            return int(predict)

        out_probs = torch.nn.functional.softmax(out_score, 1)
        return out_probs
    except Exception:
        raise


def calculate_influence(modelWrapper:RModelWrapper, dataManager:RDataManager, start_idx, end_idx, r_averaging=1):
    """
    Calculate the influence function for the model.

    args:
        model:          The trained model (PyTorch nn.module)
        dataManager:    RDataManager instance

        num:    Number of test samples for which we calculate influence. If set to -1, it calculates
                influence for the entire dataset.
    """

    task = RTask(TaskType.AutoAnnotate, end_idx - start_idx)
    starttime = time.time()
    influence_buffer = dataManager.get_influence_buffer()

    # Force num_workers to be 0 to prevent error
    testloader = torch.utils.data.DataLoader(
        dataManager.testset, batch_size=dataManager.batch_size, shuffle=False, num_workers=0)
    trainloader = torch.utils.data.DataLoader(
        dataManager.trainset, batch_size=dataManager.batch_size, shuffle=False, num_workers=0)

    # trainloader = dataManager.trainloader
    # testloader = dataManager.testloader

    if end_idx == -1:
        end_idx = len(testloader.dataset)
    else:
        end_idx = min(len(testloader.dataset), end_idx)

    gpu = -1 if modelWrapper.device == 'cpu' else 0

    recursion_depth = int(len(trainloader.dataset) / r_averaging)
    ptif.init_logging('logfile.log')

    # max_influence_dict is the dictionary containing the four most influential training images for a testing image
    #   e.g.    
    #               {
    #                       "523": 254.1763153076172,
    #                       "719": 221.39866638183594,
    #                       "667": 216.841064453125,
    #                       "653": 214.35723876953125
    #               }

    # TODO: change argument from testloader to misclassified test loader
    # as we are only interested in the influence for misclassified samples
    for idx in range(start_idx, end_idx):
        test_path = to_unix(testloader.dataset.samples[idx][0])
        if not influence_buffer.contains(test_path):
            max_influence_dict = ptif.calc_img_wise(idx, modelWrapper.model, trainloader, testloader, gpu, recursion_depth, r_averaging) 
            lst = sorted(list(max_influence_dict.items()), key=lambda p: p[1]) # sort according to influence value
            lst = [p[0] for p in lst] 
            influence_buffer.set(test_path, [to_unix(trainloader.dataset.samples[int(train_idx)][0]) for train_idx in lst])

        task_update_res = task.update()
        if not task_update_res:
            endtime = time.time()
            print("Time consumption:", endtime-starttime)
            print("Influence calculation stopped")
            return 
