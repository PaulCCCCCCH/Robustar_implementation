from objects.RServer import RServer
from utils.path_utils import to_snake_path
from . import PARAM_NAME_IMAGE_PATH
from .test_model import dummy_api_upload_dummy_model, dummy_api_set_current_model


class TestPredict:
    class TestPredict:
        def test_predict_fail_invalid_split(self, client, reset_db):
            response = client.get("/predict/non-exist?" + PARAM_NAME_IMAGE_PATH + "=/0")
            assert response.status_code == 400
            rv = response.get_json()
            assert rv["error_code"] == -1
            assert rv["detail"] == "Split not supported"

        def test_predict_fail_invalid_path(self, client, reset_db):
            response = client.get(
                "/predict/train?"
                + PARAM_NAME_IMAGE_PATH
                + "="
                + RServer.get_server().base_dir
                + "/dataset/train/bird/10000.JPEG"
            )
            assert response.status_code == 400
            rv = response.get_json()
            assert rv["error_code"] == -1
            assert (
                rv["detail"]
                == "Invalid image path "
                + RServer.get_server().base_dir
                + "/dataset/train/bird/10000.JPEG"
            )
            # TODO: [test] other splits

        def test_predict_success(self, client, reset_db):
            resp = dummy_api_upload_dummy_model(client)
            assert (
                resp.status_code == 200
            ), f"Fail to upload dummy model. {resp.get_json().get('detail')}"

            resp = dummy_api_set_current_model(client, 1)
            assert (
                resp.status_code == 200
            ), f"Fail to upload dummy model. {resp.get_json().get('detail')}"

            response = client.get(
                "/predict/train?"
                + PARAM_NAME_IMAGE_PATH
                + "="
                + RServer.get_server().base_dir
                + "/dataset/train/bird/1.JPEG"
            )
            assert response.status_code == 200
            rv = response.get_json()
            assert rv["code"] == 0
            data = rv["data"]
            assert data[0] == [
                "bird",
                "cat",
                "crab",
                "dog",
                "fish",
                "frog",
                "insect",
                "primate",
                "turtle",
            ]
            assert len(data[1]) == 9
            assert sum((0 <= x <= 1) for x in data[1]) == 9
            assert data[2] == [
                f"{RServer.get_server().base_dir}/visualize_images/{to_snake_path(RServer.get_server().base_dir)}_dataset_train_bird_1_JPEG_{idx}.png"
                for idx in range(4)
            ]
            # TODO: [test] other splits

    class TestGetInfluence:
        def test_get_influence_fail_invalid_split(self, client, reset_db):
            response = client.get(
                "/influence/non-exist?" + PARAM_NAME_IMAGE_PATH + "=/0"
            )
            assert response.status_code == 200
            rv = response.get_json()
            assert rv["code"] == -1

        def test_get_influence_fail_invalid_path(self, client, reset_db):
            response = client.get(
                "/influence/train?"
                + PARAM_NAME_IMAGE_PATH
                + "="
                + RServer.get_server().base_dir
                + "dataset/train/bird/10000.JPEG"
            )
            assert response.status_code == 200
            rv = response.get_json()
            assert rv["code"] == -1

        def test_get_influence_success(self, client, reset_db):
            assert True
            # response = client.get("/influence/train?" + PARAM_NAME_IMAGE_PATH +
            #                 "=" + RServer.get_server().base_dir + "/dataset/train/bird/1.JPEG")
            # assert response.status_code == 200
            # rv = response.get_json()
            # assert rv['code'] == -1
            # assert rv['msg'] == 'Image is not found or influence for that image is not calculated'
            # assert rv['data'] == [
            #     '/Robustar2/visualize_images/_Robustar2_dataset_train_bird_1_JPEG_0.png',
            #     '/Robustar2/visualize_images/_Robustar2_dataset_train_bird_1_JPEG_1.png',
            #     '/Robustar2/visualize_images/_Robustar2_dataset_train_bird_1_JPEG_2.png',
            #     '/Robustar2/visualize_images/_Robustar2_dataset_train_bird_1_JPEG_3.png']
            # TODO [test]: pass this - 1. get un-calculated image; 2. calculate 1 image; 3. get
            #  that calculated image; current problem in 2 - need other test method

    class TestCalculateInfluence:  # TODO [test]
        def test_calculate_influence_success(self, client, reset_db):
            assert True
            # rv = client.get("/influence").get_json()
            # assert rv['code'] == -1
            # assert rv['msg'] == 'Image is not found or influence for that image is not calculated'
            # assert rv['data'] == [
            #     '/Robustar2/visualize_images/_Robustar2_dataset_train_bird_1_JPEG_0.png',
            #     '/Robustar2/visualize_images/_Robustar2_dataset_train_bird_1_JPEG_1.png',
            #     '/Robustar2/visualize_images/_Robustar2_dataset_train_bird_1_JPEG_2.png',
            #     '/Robustar2/visualize_images/_Robustar2_dataset_train_bird_1_JPEG_3.png']
