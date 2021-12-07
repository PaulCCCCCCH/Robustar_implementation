from objects.RServer import RServer
from objects.RResponse import RResponse
from flask import request
from io import BytesIO
import numpy as np
from PIL import Image
import base64

app = RServer.getServer().getFlaskApp()

@app.route('/edit/<phase>/<image_id>', methods=['POST'])
def user_edit(phase, image_id):
    json_data = request.get_json()

    encoded_string = json_data['image'].split(',')[1]
    decoded = base64.b64decode(encoded_string)

    with Image.open(BytesIO(decoded)) as img:
        print("************************")
        print(np.array(img).shape)




    # decoded = base64.decodestring(encoded_string)
    # print(decoded)
   

    return RResponse.ok("Success!")

