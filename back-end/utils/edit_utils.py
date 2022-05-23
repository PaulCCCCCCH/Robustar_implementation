from PIL import Image
from sklearn import datasets
from objects.RServer import RServer
from io import BytesIO
from utils.path_utils import get_paired_path
import shutil
import threading
from objects.RTask import RTask, TaskType
import time

server = RServer.getServer()
dataManager = server.getDataManager()


def get_train_and_paired_path(split, image_path):
    if split == 'train':
        train_img_path = image_path
        paired_img_path = dataManager.pairedset.convert_train_path_to_paired(train_img_path)
    elif split == 'annotated':
        paired_img_path = image_path
        train_img_path = dataManager.pairedset.convert_paired_path_to_train(paired_img_path)
    elif split == 'proposed':
        train_img_path = dataManager.proposedset.convert_paired_path_to_train(image_path)
        paired_img_path = dataManager.pairedset.convert_train_path_to_paired(train_img_path)
    else:
        raise NotImplementedError('Getting train-paired pair only works for `train`, `annotated` and `proposed` splits')

    return train_img_path, paired_img_path


def save_edit(split, image_path, image_data, image_height, image_width):
    """
    Save edited image as png in paired data folder.
    If 'split' is 'train', image_path should point to the training image.
    If 'split' is 'annotated', image_path should point to the annotated image.
    If 'split' is 'proposed', image_path should point to the proposed image.
    The file name will still end with `JPEG` extension.
    """

    train_img_path, paired_img_path = get_train_and_paired_path(split, image_path)

    with Image.open(BytesIO(image_data)) as img:

        to_save = img.resize((image_width, image_height))
        # to_save = to_save.convert('RGB') # image comming from canvas is RGBA

        to_save.save(paired_img_path, format='png')

        dataManager.pairedset.save_annotated_image(train_img_path, image_data, image_height, image_width)
        dataManager.trainset.update_paired_data([train_img_path], [paired_img_path])


def propose_edit(split, image_path, return_image=False):
    """
    Propose an annotation for an training image specified by image_path and return the path to the proposed image
    """

    if split == 'train':
        train_img_path = image_path
        proposed_path = dataManager.proposedset.convert_train_path_to_paired(train_img_path)
    elif split == 'annotated':
        proposed_path = image_path
        train_img_path = dataManager.proposedset.convert_paired_path_to_train(proposed_path)
    else:
        raise NotImplementedError("We can only propose an edit for 'train' or `annotated` split")

    if not dataManager.proposedset.is_annotated(train_img_path):
        pil_image = server.getAutoAnnotator().annotate_single(train_img_path, dataManager.image_size)
        dataManager.proposedset.save_annotated_image(train_img_path, pil_image)
    else:
        if return_image:
            pil_image = Image.open(proposed_path)
        else:
            pil_image = None

    return proposed_path, pil_image
        

def start_auto_annotate(split, num_to_gen):
    if split != 'train': raise NotImplementedError('Auto annotation only supported for train split')
    num_to_gen = min(num_to_gen, len(dataManager.trainset))

    def auto_annotate_thread(split, num_to_gen):
        task = RTask(TaskType.AutoAnnotate, num_to_gen)
        starttime = time.time()

        for train_path in dataManager.trainset.get_image_list(None, num_to_gen):
            # Propose edit for this image
            proposed_image_path, pil_image = propose_edit(split, train_path, True)

            # Save the image to paired data folder
            dataManager.pairedset.save_annotated_image(train_path, pil_image)

            task_update_res = task.update()
            if not task_update_res:
                endtime = time.time()
                print("Time consumption:", endtime-starttime)
                print("Auto annotate stopped!")
                return 
        task.exit()


    test_thread = threading.Thread(target=auto_annotate_thread, args=(split, num_to_gen))
    test_thread.start()

