import importlib


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


def val_model(model):
    """ Validate the model by running the model against a small portion of the validation dataset
    """
    pass


# TODO: align the arguments with the actual database design
def save_model(model):
    pass
