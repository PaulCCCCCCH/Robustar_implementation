from objects.RServer import RServer
import json
from flask import request
import os

app = RServer.getServer().getFlaskApp()

@app.route('/edit', methods=['POST'])
def user_edit():
    if 'src' in request.form and 'content' in request.form:
        src = request.form.get("src")
        content = request.form.get("content")

        data = {}
        file_path = 'user-edit.json'
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                data = json.load(f)
        data[src] = content

        with open(file_path, 'w') as f:
            json.dump(data, f)

        return "success"
    return 'invalid image content'

