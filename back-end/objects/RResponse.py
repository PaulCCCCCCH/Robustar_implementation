from flask import abort, jsonify


def abort_with_error_message(status_code: int, err_message: str, err_code=-1):
    """
    abort with a status code, an error code and a message
    Parameters:
      - status_code: HTTP status code
      - detail: error message
      - err_code: an error code to give more detailed information. Default is -1. An
      example usage is: return xxxxx as err_code when a username is taken. This allows
      the client to gracefully handle the exception.
    """
    response = jsonify({"error_code": err_code, "detail": err_message})
    response.status_code = status_code
    abort(response)


class RResponse:
    def __init__(self, data, code, message):
        self.data = data
        self.code = code
        self.message = message

    def toJSON(self):
        return {"data": self.data, "code": self.code, "msg": self.message}

    @staticmethod
    def ok(data, message="Success", code=0):
        return RResponse(data, code, message=message).toJSON()

    # Deprecated. This will wrap a failure inside a 200 response, which is
    # confusing. Always use abort() instead.
    @staticmethod
    def fail(message="Error", code=-1):
        return RResponse(data="", code=code, message=message).toJSON()

    @staticmethod
    def abort(status_code=500, message="Error", err_code=-1):
        abort_with_error_message(status_code, message, err_code)
