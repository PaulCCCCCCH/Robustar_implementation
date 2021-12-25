from modules.visualize_module.flashtorch_.utils import apply_transforms, load_image
from objects.RModelWrapper import RModelWrapper
import torch
import modules.influence_module as ptif
import threading
from objects.RDataManager import RDataManager
import pickle
from utils.image_utils import imageURLToPath



# Turns prediction results into array
def convert_predict_to_array(output):
    """
    args:
        output: a tensor of shape (1, num_of_classes) 
    """
    result = []
    for prob in output[0]:
        result.append(float(prob))

    print(result)
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


def calculate_influence(modelWrapper:RModelWrapper, dataManager:RDataManager, test_sample_num=1, r_averaging=1):
    """
    Calculate the influence function for the model.

    args:
        model:          The trained model (PyTorch nn.module)
        dataManager:    RDataManager instance

        num:    Number of test samples for which we calculate influence. If set to -1, it calculates
                influence for the entire dataset.
    """

    INFLUENCES_SAVE_PATH = dataManager.influence_file_path
    influences = {}

    trainloader = dataManager.trainloader
    testloader = dataManager.testloader

    config = ptif.get_default_config()
    config['gpu'] = -1 if modelWrapper.device == 'cpu' else 0
    config['test_sample_num'] = test_sample_num
    config['r_averaging'] = r_averaging
    config['recursion_depth'] = int(len(trainloader.dataset) / config['r_averaging'])
    ptif.init_logging('logfile.log')

    # max_influence_dicts is the dictionary containing the four most influential training images for each testing image
    #   e.g.    {
    #               "0": {
    #                       "523": 254.1763153076172,
    #                       "719": 221.39866638183594,
    #                       "667": 216.841064453125,
    #                       "653": 214.35723876953125
    #                      },
    #               "1":{...},
    #               ...
    #           }

    # TODO: change argument from testloader to misclassified test loader
    # as we are only interested in the influence for misclassified samples
    max_influence_dicts = ptif.calc_img_wise(config, modelWrapper.model, trainloader, testloader) 

    for key in max_influence_dicts.keys():
        train_img_paths = []

        testId = "test/" + key
        test_img_path = imageURLToPath(testId)

        max_influence_dict = max_influence_dicts[key]
        trainIds = list(max_influence_dict.keys())

        for j in range(4):
            trainUrl = "train/" + str(trainIds[j])
            train_img_path = imageURLToPath(trainUrl)
            # TODO: Stores both image path and image url. 
            # Adding / removing samples to training set will cause inconsistency
            # Need to check consistency in data manager when loading.
            train_img_paths.append((train_img_path, trainUrl)) 

        influences[test_img_path] = train_img_paths

    with open(INFLUENCES_SAVE_PATH, "wb") as influence_file:
        pickle.dump(influences, influence_file)

    
class CalcInfluenceThread(threading.Thread):
    def __init__(self, modelWrapper:RModelWrapper, dataManager:RDataManager, test_sample_num, r_averaging):
        super(CalcInfluenceThread, self).__init__()
        self.modelWrapper = modelWrapper
        self.dataManager = dataManager
        self.test_sample_num= test_sample_num
        self.r_averaging = r_averaging

    def run(self):
        calculate_influence(self.modelWrapper, self.dataManager, self.test_sample_num, self.r_averaging)
