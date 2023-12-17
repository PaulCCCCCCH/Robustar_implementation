import json

"""
    Helper Functions
"""


def build_dummy_model_metadata(nickname):
    metadata = {
        "class_name": "resnet-18",
        "nickname": nickname,
        "description": "test description",
        "tags": ["tag1", "tag2"],
        "pretrained": "0",
        "predefined": "1",
        "num_classes": "1000",
    }

    return metadata


"""
    Dummy APIs
"""


def dummy_api_upload_dummy_model(client, name: str):
    metadata = build_dummy_model_metadata(name)
    response = client.post(
        f"/model",
        data={"metadata": json.dumps(metadata)},
        content_type="multipart/form-data",
    )
    return response


def dummy_api_set_current_model(client, name: str):
    response = client.post(f"/model/current/{name}")
    return response


def dummy_api_get_current_model(client):
    response = client.get("/model/current")
    return response


def dummy_api_list_models(client):
    response = client.get("/model/list")
    return response


def dummy_api_delete_model(client, name: str):
    response = client.delete(f"/model/{name}")
    return response


"""
    Test Cases
"""


class TestModel:
    class TestModelUpload:
        def test_model_upload(self, client):
            # TODO:
            response = dummy_api_upload_dummy_model(client, "test-resnet-18")
            assert response.status_code == 200

    class TestModelSwitch:
        def test_set_nonexist(self, client):
            model_name = "model-non-exist"
            response = client.post(f"/model/current/{model_name}")
            assert response.status_code != 200

        def test_get_set(self, client):
            # Upload two models
            resp = dummy_api_upload_dummy_model(client, "model-1")
            assert (
                resp.status_code == 200
            ), f"Fail to upload dummy model. {resp.get_json().get('detail')}"
            resp = dummy_api_upload_dummy_model(client, "model-2")
            assert (
                resp.status_code == 200
            ), f"Fail to upload dummy model. {resp.get_json().get('detail')}"

            # Fail when no current model is set
            resp = dummy_api_get_current_model(client)
            assert resp.status_code == 400

            # Set current model to the first one
            resp = dummy_api_set_current_model(client, "model-1")
            assert (
                resp.status_code == 200
            ), f"Fail to set model-1 as current model. {resp.get_json().get('detail')}"

            resp = dummy_api_get_current_model(client)
            assert resp.status_code == 200
            assert (
                resp.get_json()["data"].get("nickname") == "model-1"
            ), f"current model nickname does match expected value"

            # Set current model to the second one
            resp = dummy_api_set_current_model(client, "model-2")
            assert (
                resp.status_code == 200
            ), f"Fail to set model-2 as current model. {resp.get_json().get('detail')}"

            resp = dummy_api_get_current_model(client)
            assert resp.status_code == 200
            assert (
                resp.get_json()["data"].get("nickname") == "model-2"
            ), f"current model nickname does match expected value"

    class TestCRUDModel:
        def test_list(self, client):
            # Upload dummy models
            for model_name in ["model-3", "model-4"]:
                dummy_api_upload_dummy_model(client, model_name)

            # List models
            resp = dummy_api_list_models(client)
            assert resp.status_code == 200
            models = resp.get_json()["data"]
            assert len(models) == 2, "Unexpected number of models in the list"

            model_names = [model["nickname"] for model in models]
            assert "model-3" in model_names
            assert "model-4" in model_names

        def test_delete(self, client):
            # Upload dummy models
            for model_name in ["model-5", "model-6"]:
                dummy_api_upload_dummy_model(client, model_name)

            # Delete model
            resp = dummy_api_delete_model(client, "model-5")
            assert resp.status_code == 200
            assert (
                resp.get_json()["data"].get("nickname") == "model-5"
            ), "Deleted model metadata is wrong"

            # Expect only 1 model left in the list
            resp = dummy_api_list_models(client)
            models = resp.get_json()["data"]
            assert len(models) == 1, "Unexpected number of models in the list"
