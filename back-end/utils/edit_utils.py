from PIL import Image
from objects.RServer import RServer
from io import BytesIO
from utils.image_utils import imageURLToPath, imageSplitIdToPath
from utils.path_utils import get_paired_path
import shutil
import threading
from objects.RTask import RTask, TaskType
import time

server = RServer.getServer()
app = server.getFlaskApp()
dataManager = server.getDataManager()

def update_annotated_list(image_id):
    if int(image_id) in dataManager.annotatedInvBuffer:
        save_idx = dataManager.annotatedInvBuffer[int(image_id)]
    else:
        save_idx = len(dataManager.annotatedBuffer)
        dataManager.annotatedInvBuffer[int(image_id)] = save_idx
    dataManager.annotatedBuffer[save_idx] = int(image_id)

    dataManager.dump_annotated_list() # TODO: Change this to SQLite



def save_edit(split, image_id, image_data, image_height, image_width):

    with Image.open(BytesIO(image_data)) as img:
    
        img_path = imageURLToPath('{}/{}'.format(split, image_id))

        paired_img_path = get_paired_path(img_path, dataManager.train_root, dataManager.paired_root)

        to_save = img.resize((image_width, image_height))
        to_save = to_save.convert('RGB') # image comming from canvas is RGBA

        to_save.save(paired_img_path)

        update_annotated_list(image_id)



def propose_edit(split, image_id):
    """
    propose an annotation for image with split and image_id 
    split can only be 'train' and '
    """

    image_url = '{}/{}'.format(split, image_id)
    proposedAnnotationBuffer = dataManager.proposedAnnotationBuffer

    if int(image_id) not in proposedAnnotationBuffer:
        image_path = imageURLToPath(image_url)
        pil_image = server.getAutoAnnotator().annotate_single(image_path, dataManager.image_size)
        # image_name = image_url.replace('.', '_').replace('/', '_').replace('\\', '_')
        proposed_image_path = get_paired_path(image_path, dataManager.train_root, dataManager.proposed_annotation_root)
        # proposed_image_path = osp.join(dataManager.proposed_annotation_root, image_name) + '.jpg'
        pil_image.save(proposed_image_path)
        proposedAnnotationBuffer.add(int(image_id))

    proposed_image_id = int(image_id)
    return proposed_image_id
        

def start_auto_annotate(split, num_to_gen):
    def auto_annotate_thread(split, num_to_gen):
        task = RTask(TaskType.AutoAnnotate, num_to_gen)
        starttime = time.time()

        for image_id in range(num_to_gen):
            proposed_image_id = propose_edit(split, image_id)
            proposed_image_path = imageSplitIdToPath('proposed', proposed_image_id)
            paired_img_path = get_paired_path(proposed_image_path, dataManager.proposed_annotation_root, dataManager.paired_root)
            print("Copying from {} to {}".format(proposed_image_path, paired_img_path))
            shutil.copy(proposed_image_path, paired_img_path)
            update_annotated_list(image_id)
            task_update_res = task.update()
            if not task_update_res:
                endtime = time.time()
                print("Time consumption:", endtime-starttime)
                print("Trainning stopped!")
                return 


    test_thread = threading.Thread(target=auto_annotate_thread, args=(split, num_to_gen))
    test_thread.start()

