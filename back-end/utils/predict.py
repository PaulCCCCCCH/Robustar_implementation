from modules.visualize_module.flashtorch_.utils import load_image
from objects.RModelManager import RModelManager
from objects.RServer import RServer
import torch
import modules.influence_module as ptif
import threading
from objects.RDataManager import RDataManager
import pickle


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


def get_image_prediction(
    model_manager: RModelManager, imgpath: str, imgsize: int, argmax=False
):
    """
    Get the probability for each class predicted by the model on the given image.
    If `argmax` is set to true, return the index of the most probable class.

    args:
        model:      The model to make the predictions
        imgpath:    Path to the image to be predicted
        imgsize:    Resize (scale) the input image to imgsize*imgsize.
    """
    data_manager = RServer.get_data_manager()
    try:
        image = load_image(imgpath)

        image = data_manager.transforms(image)
        image = image.unsqueeze(0)  # The model requires a batch dimension
        image = image.to(model_manager.device)

        model = model_manager.model

        out_score = model(
            image
        )  # size: (1, num_classes). For imageNet, shape is (1, 10)

        if argmax:
            _, predict = torch.max(out_score, 1)
            return int(predict)

        out_probs = torch.nn.functional.softmax(out_score, 1)
        return out_probs
    except Exception:
        raise


def calculate_influence(
    model_manager: RModelManager,
    data_manager: RDataManager,
    in_config
):
    """
    Calculate the influence function for the model.

    args:
        model:          The trained model (PyTorch nn.module)
        dataManager:    RDataManager instance

        num:    Number of test samples for which we calculate influence. If set to -1, it calculates
                influence for the entire dataset.
    """

    config = ptif.get_default_config()
    config.update(in_config)

    batch_size = config['batch_size']
    num_workers = config['num_workers']
    testloader = torch.utils.data.DataLoader(data_manager.testset, batch_size=batch_size, shuffle=False, num_workers=num_workers)
    trainloader = torch.utils.data.DataLoader(data_manager.trainset, batch_size=batch_size, shuffle=False, num_workers=num_workers)

    end_idx = config["test_end_index"]
    if end_idx == -1:
        end_idx = len(testloader.dataset)
    else:
        end_idx = min(len(testloader.dataset), end_idx)

    config["gpu"] = -1 if model_manager.device == "cpu" else 0
    config["test_sample_num"] = end_idx - config["test_start_index"]
    config["outdir"] = data_manager.influence_log_path

    print(f"Starting influence calculation with the following configuration: \n {config}")

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


    # TODO: Now max_influence_dicts will be empty if user stops the influence calculation
    # (i.e., all previous results are thrown away because we only return the full result when
    # influence is calculated for all specified images). Maybe we should instead return influence
    # for each image one by one to build the dictionary slowly, so that when calculation stops,
    # we can save what has been calculated.

    influences = {}
    max_influence_dicts = {}
    try:
        max_influence_dicts = ptif.calc_img_wise(
            config, model_manager.model, trainloader, testloader
        )
    except StopIteration:
        print("Influence calculation stopped!")

    for key in max_influence_dicts.keys():
        train_img_paths = []

        test_id = int(key)
        test_img_path = data_manager.testset.get_image_list(test_id, test_id + 1)[0]

        max_influence_dict = max_influence_dicts[key]
        train_ids = list(max_influence_dict.keys())

        for j in range(4):
            train_id = int(train_ids[j])
            train_img_path = data_manager.trainset.get_image_list(train_id, train_id + 1)[0]
            train_img_paths.append(train_img_path)

        influences[test_img_path] = train_img_paths
    

    data_manager.get_influence_dict().update(influences)
    if influences:
        with open(data_manager.influence_file_path, "wb") as influence_file:
            pickle.dump(data_manager.get_influence_dict(), influence_file)
            print("Influence calculation done.")

def get_calc_influence_thread(configs):
    # Parse the following fields from string to integer
    for key in ["test_start_index", "test_end_index", "recursion_depth", "r_averaging", "scale"]:
        configs[key] = int(configs[key]) 

    return CalcInfluenceThread(
        RServer.get_model_manager(),
        RServer.get_data_manager(),
        configs
    )

class CalcInfluenceThread(threading.Thread):
    def __init__(
        self,
        model_manager: RModelManager,
        data_manager: RDataManager,
        config,
    ):
        super(CalcInfluenceThread, self).__init__()
        self.model_manager = model_manager
        self.dataManager = data_manager
        self.config = config

    def run(self):
        try:
            calculate_influence(
                self.model_manager,
                self.dataManager,
                self.config,
            )
        except Exception as e:
            raise e
        finally:
            RServer.get_model_manager().release_model()

