import json

def build_dummy_model_metadata(nickname):
    metadata = {
        "class_name": "resnet-18-32x32",
        "nickname": nickname,
        "description": "test description",
        "tags": ["tag1", "tag2"],
        "pretrained": "0",
        "predefined": "1",
    }

    return metadata


"""
    Dummy APIs
"""
def dummy_api_upload_dummy_model(client, name: str, must_succeed=False):
    metadata = build_dummy_model_metadata(name)
    response = client.post(
        f"/model",
        data={"metadata": json.dumps(metadata)},
        content_type="multipart/form-data",
    )
    if must_succeed:
        assert response.status_code == 200

    return response


def dummy_api_set_current_model(client, name: str, must_succeed=False):
    response = client.post(f"/model/current/{name}")
    if must_succeed:
        assert response.status_code == 200

    return response


def dummy_api_get_current_model(client, must_succeed=False):
    response = client.get("/model/current")
    if must_succeed:
        assert response.status_code == 200

    return response


def dummy_api_list_models(client, must_succeed=False):
    response = client.get("/model/list")
    if must_succeed:
        assert response.status_code == 200

    return response


def dummy_api_delete_model(client, name: str, must_succeed=False):
    response = client.delete(f"/model/{name}")
    if must_succeed:
        assert response.status_code == 200

    return response


