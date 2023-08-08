import os
import importlib
from objects.RServer import RServer


def init_model(code_path, arch):
    """ Initialize the model by importing the class named arch in the file specified by code_path
    """
    try:
        spec = importlib.util.spec_from_file_location("model_def", code_path)
        model_def = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(model_def)
        model = getattr(model_def, arch)()
        return model
    except Exception as e:
        print("Failed to initialize the model.")
        print(e)
        raise e


def clear_model_temp_files(model_id):
    """ Clear the temporary files associated with the model
    """
    code_path = os.path.join(RServer.get_server().base_dir, f'{model_id}.py')
    weight_path = os.path.join(RServer.get_server().base_dir, f'{model_id}.pth')
    try:
        if os.path.exists(code_path):
            os.remove(code_path)
        if os.path.exists(weight_path):
            os.remove(weight_path)
    except Exception as e:
        print("Failed to clear the temporary files associated with the model.")
        print(e)
        raise e


def val_model(model):
    """ Validate the model by running the model against a small portion of the validation dataset
    """
    pass


def save_model(metadata):
    pass
