'''
Author: Chonghan Chen (paulcccccch@gmail.com)
-----
Last Modified: Thursday, 18th November 2021 12:18:39 am
Modified By: Chonghan Chen (paulcccccch@gmail.com)
-----
'''

class RResponse:
    
    def __init__(self, data, code, message):
        self.data = data
        self.code = code
        self.message = message


    def toJSON(self):
        return {
            'data': self.data,
            'code': self.code,
            'msg': self.message
        }


    @staticmethod
    def ok(data, message='Success', code=0):
        return RResponse(data, code, message=message).toJSON()

    @staticmethod
    def fail(message='Error', code=-1):
        return RResponse(code=code, message=message).toJSON()


