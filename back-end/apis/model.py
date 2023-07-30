import string
from flask import request
from flask import Blueprint

model_api = Blueprint("model_api", __name__)

@model_api.route("/model/current", methods=["GET"])
def GetCurrModel():
    """ Get the model that is currently active """
    """ return data
    {
        id: string,
        name: string,
        details: string,
    }
    """
    pass


@model_api.route("/model/current/<model_id>", methods=["POST"])
def SetCurrModel(model_id: string):
    """ return 200 on success """
    pass


@model_api.route("/model/<id>", methods=["DELETE"])
def DeleteModel():
    """ return data
    {
        id: string,
        name: string,
        details: string,
    }
    """
    pass


@model_api.route("/model", methods=["POST"])
def UploadModel():
    """ Should also accept (optionally) a model weight file as argument """
    """ After training a model, should do the same"""
    """ return data
        {
            id: string,
            name: string,
            details: string,
        }

    """
    pass


@model_api.route("/model/list", methods=["GET"])
def GetAllModels():
    """ return data
    [
        {
            id: string,
            name: string,
            details: string,
        },
        ...
    ]
    """
    pass

