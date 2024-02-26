import json
"""
    Helper functions
"""
def build_dummy_model_metadata():
    metadata = {
        "class_name": "resnet-18-32x32",
        "nickname": "dummy-model",
        "description": "test description",
        "tags": ["tag1", "tag2"],
        "pretrained": "0",
        "predefined": "1",
    }

    return metadata

def must_succeed(api_call):
    resp = api_call()
    assert resp.status_code == 200
    return resp


"""
    Dummy APIs
"""
def dummy_api_upload_dummy_model(client):
    metadata = build_dummy_model_metadata()
    response = client.post(
        f"/model",
        data={"metadata": json.dumps(metadata)},
        content_type="multipart/form-data",
    )
    return response


def dummy_api_set_current_model(client, model_id: int):
    response = client.post(f"/model/current/{model_id}")
    return response


def dummy_api_get_current_model(client):
    response = client.get("/model/current")
    return response


def dummy_api_list_models(client):
    response = client.get("/model/list")
    return response


def dummy_api_delete_model(client, model_id: int):
    response = client.delete(f"/model/{model_id}")
    return response
