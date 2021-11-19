from modules.visualize_module.flashtorch_.utils import apply_transforms, load_image
from objects.RModelWrapper import RModelWrapper
import torch

# 将预测结果转换为字符串
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