import threading

from objects.RServer import RServer
from utils.image_utils import imageURLToPath
from utils.predict import get_image_prediction, convert_predict_to_array
from os import path as osp

# app = RServer.getServer().getFlaskApp()
server = RServer.getServer()
dataManager = server.dataManager
predictBuffer = dataManager.predictBuffer
modelWrapper = RServer.getModelWrapper()

validationset = dataManager.validationset
testset = dataManager.testset

validation_correct_root = dataManager.validation_correct_root
validation_incorrect_root = dataManager.validation_incorrect_root
test_correct_root = dataManager.test_correct_root
test_incorrect_root = dataManager.test_incorrect_root


def start_test(split):
    try:
        def startTestThread():
            if split == 'validation':
                dataset_length = len(validationset.samples)
                # print(dataset_length)

                correct_file = open(validation_correct_root, mode='w')
                incorrect_file = open(validation_incorrect_root, mode='w')

                attribute = dataManager.validationset.classes
            elif split == 'test':
                dataset_length = len(testset.samples)
                # print(dataset_length)

                correct_file = open(test_correct_root, mode='w')
                incorrect_file = open(test_incorrect_root, mode='w')

                attribute = dataManager.testset.classes
            else:
                raise NotImplemented

            correct_buffer = []
            incorrect_buffer = []

            for img_index in range(dataset_length):
                image_url = split + "/" + str(img_index)

                datasetImgPath = imageURLToPath(image_url)
                imgPath = osp.join(server.baseDir, datasetImgPath).replace('\\', '/')
                # print(imgPath)

                # TODO: 32 should not be hardcoded!
                output = get_image_prediction(modelWrapper, imgPath, dataManager.image_size, argmax=False)
                output_array = convert_predict_to_array(output.cpu().detach().numpy())

                max_value = 0
                max_index = -1
                index = 0
                for output_value in output_array:
                    if output_value > max_value:
                        max_value = output_value
                        max_index = index
                    index += 1

                # print(attribute[max_index])
                # print(imgPath.split('/')[-2])
                is_correct = (attribute[max_index] == imgPath.split('/')[-2])
                # print(is_correct)
                if is_correct:
                    correct_buffer.append(img_index)
                    correct_file.write(str(img_index) + '\n')
                else:
                    incorrect_buffer.append(img_index)
                    incorrect_file.write(str(img_index) + '\n')

            if split == 'validation':
                dataManager.correctValidationBuffer = correct_buffer
                dataManager.incorrectValidationBuffer = incorrect_buffer
            elif split == 'test':
                dataManager.correctTestBuffer = correct_buffer
                dataManager.incorrectTestBuffer = incorrect_buffer
            else:
                raise NotImplemented

            dataManager.split_dict[split + '_correct'] = correct_buffer 
            dataManager.split_dict[split + '_incorrect'] = incorrect_buffer 

            correct_file.close()
            incorrect_file.close()

        test_thread = threading.Thread(target=startTestThread)
        test_thread.start()

    except Exception as e:
        e.with_traceback()
        return None

    return test_thread
