import os.path

from PIL import Image
from objects.RServer import RServer
from io import BytesIO
from utils.image_utils import cache_image
import threading
from objects.RTask import RTask, TaskType
import time


def get_train_and_paired_path(split, image_path):
    dataManager = RServer.get_data_manager()
    if split == "train":
        train_img_path = image_path
        paired_img_path = dataManager.pairedset.convert_train_path_to_paired(
            train_img_path
        )
    elif split == "annotated":
        paired_img_path = image_path
        train_img_path = dataManager.pairedset.convert_paired_path_to_train(
            paired_img_path
        )
    elif split == "proposed":
        train_img_path = dataManager.proposedset.convert_paired_path_to_train(
            image_path
        )
        paired_img_path = dataManager.pairedset.convert_train_path_to_paired(
            train_img_path
        )
    else:
        raise NotImplementedError(
            "Getting train-paired pair only works for `train`, `annotated` and `proposed` splits"
        )

    return train_img_path, paired_img_path


def remove_edit(path: str):
    RServer.get_data_manager().pairedset.remove_image(path)


def clear_edit():
    RServer.get_data_manager().pairedset.clear_images()


def save_edit(split, image_path, image_data, image_height, image_width):
    """
    Save edited image as png in paired data folder.
    If 'split' is 'train', image_path should point to the training image.
    If 'split' is 'annotated', image_path should point to the annotated image.
    If 'split' is 'proposed', image_path should point to the proposed image.
    """

    train_img_path, paired_img_path = get_train_and_paired_path(split, image_path)
    data_manager = RServer.get_data_manager()

    if not os.path.exists(train_img_path):
        raise ValueError("invalid image path")

    with Image.open(BytesIO(image_data)) as img:

        to_save = img.resize((image_width, image_height))
        # to_save = to_save.convert('RGB') # image comming from canvas is RGBA

        to_save.save(paired_img_path, format="png")

        data_manager.pairedset.save_annotated_image(
            train_img_path, data_manager.trainset, image_data, image_height, image_width
        )
        cache_image(paired_img_path)


def propose_edit(split, image_path, return_image=False):
    """
    Propose an annotation for an training image specified by image_path and return the path to the proposed image
    """

    dataManager = RServer.get_data_manager()
    if split == "train":
        train_img_path = image_path
        proposed_path = dataManager.proposedset.convert_train_path_to_paired(
            train_img_path
        )
    elif split == "annotated":
        proposed_path = image_path
        train_img_path = dataManager.proposedset.convert_paired_path_to_train(
            proposed_path
        )
    else:
        raise NotImplementedError(
            "We can only propose an edit for 'train' or `annotated` split"
        )

    if not dataManager.proposedset.is_annotated(train_img_path):
        pil_image = RServer.get_auto_annotator().annotate_single(
            train_img_path, dataManager.image_size
        )
        dataManager.proposedset.save_annotated_image(
            train_img_path, dataManager.trainset, pil_image
        )
    else:
        if return_image:
            pil_image = Image.open(proposed_path)
        else:
            pil_image = None

    return proposed_path, pil_image


def start_auto_annotate(split, start: int, end: int):
    if split != "train":
        raise NotImplementedError("Auto annotation only supported for train split")

    data_manager = RServer.get_data_manager()
    # -1 means annotate till the end
    if end == -1:
        end = len(data_manager.trainset)
    end = min(end, len(data_manager.trainset))
    if start == end:
        return

    def auto_annotate_thread(split, start, end):
        task = RTask(TaskType.AutoAnnotate, end - start)
        starttime = time.time()

        for train_path in data_manager.trainset.get_image_list(start, end):
            # Propose edit for this image
            proposed_image_path, pil_image = propose_edit(split, train_path, True)

            # Save the image to paired data folder
            data_manager.pairedset.save_annotated_image(
                train_path, data_manager.trainset, pil_image
            )

            task_update_res = task.update()
            if not task_update_res:
                endtime = time.time()
                print("Time consumption:", endtime - starttime)
                print("Auto annotate stopped!")
                return
        # task.exit()

    auto_annotate_thread = threading.Thread(
        target=auto_annotate_thread, args=(split, start, end)
    )
    auto_annotate_thread.start()
