import threading
from objects.RServer import RServer
from utils.path_utils import to_unix
from utils.predict import get_image_prediction, convert_predict_to_array
from objects.RImageFolder import REvalImageFolder
from os import path as osp
from objects.RTask import RTask, TaskType

server = RServer.getServer()
dataManager = server.dataManager
predictBuffer = dataManager.predictBuffer
modelWrapper = RServer.getModelWrapper()

class TestThread(threading.Thread):
    def __init__(self, split):
        super(TestThread, self).__init__()
        self.split = split
        self.stop = False

    def run(self):
        self.startTestThread()
    
    def stop(self):
        print("Setting trainer stop flag...")
        self.stop = True

    def startTestThread(self):
        split = self.split
        if split == 'validation':
            dataset: REvalImageFolder = dataManager.validationset
        elif split == 'test':
            dataset: REvalImageFolder = dataManager.testset
        else:
            raise NotImplementedError('Test called with wrong data split')

        samples = dataset.samples
        dataset_length = len(samples)

        correct_buffer = []
        incorrect_buffer = []

        task = RTask(TaskType.Test, dataset_length)

        for img_path, label in samples:

            output = get_image_prediction(modelWrapper, img_path, dataManager.image_size, argmax=False)
            output_array = convert_predict_to_array(output.cpu().detach().numpy())

            # TODO: replace this snippet with numpy argmax function
            max_value = 0
            max_index = -1
            index = 0
            for output_value in output_array:
                if output_value > max_value:
                    max_value = output_value
                    max_index = index
                index += 1

            is_correct = (max_index == label)
            if is_correct:
                correct_buffer.append((img_path, label))
            else:
                incorrect_buffer.append((img_path, label))

            # task update
            task_update_res = task.update()
            if not task_update_res:
                break
        else:
            # exit task if normal end of the test iteration
            task.exit()

        dataset.add_records(correct_buffer, True)
        dataset.add_records(incorrect_buffer, False)
        


def start_test(split):
    try:

        test_thread = TestThread(split)
        test_thread.start()

    except Exception as e:
        e.with_traceback()
        return None

    return test_thread
