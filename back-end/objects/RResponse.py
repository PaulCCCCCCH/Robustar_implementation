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
            'message': self.message
        }


    @staticmethod
    def ok(data, message='Success'):
        return RResponse(data, code=200, message=message)

    @staticmethod
    def fail(message='Error'):
        return RResponse(code=500, message=message)


