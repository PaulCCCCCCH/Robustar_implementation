from test_app import app, client


class TestPredict:
    # class TestPredict:
    #     def test_predict_fail_invalid_split(self, client):
    #         rv = client.get("/predict/non-exist/0").get_json()
    #         assert rv['code'] == -1
    #         assert rv['msg'] == 'Split not supported'
    #
    #     def test_predict_fail_invalid_path(self, client):
    #         rv = client.get("/predict/train/Robustar2/dataset/train/bird/10000.JPEG").get_json()
    #         assert rv['code'] == -1
    #         assert rv['msg'] == 'Invalid image path /Robustar2/dataset/train/bird/10000.JPEG'
    #         # TODO: [test] other splits
    #
    #     def test_predict_success(self, client):
    #         rv = client.get("/predict/train/Robustar2/dataset/train/bird/1.JPEG").get_json()
    #         assert rv['code'] == 0
    #         data = rv['data']
    #         assert data[0] == ['bird', 'cat', 'crab', 'dog', 'fish',
    #                            'frog', 'insect', 'primate', 'turtle']
    #         assert len(data[1]) == 9
    #         assert sum((0 <= x <= 1) for x in data[1]) == 9
    #         assert data[2] == [
    #             '/Robustar2/visualize_images/_Robustar2_dataset_train_bird_1_JPEG_0.png',
    #             '/Robustar2/visualize_images/_Robustar2_dataset_train_bird_1_JPEG_1.png',
    #             '/Robustar2/visualize_images/_Robustar2_dataset_train_bird_1_JPEG_2.png',
    #             '/Robustar2/visualize_images/_Robustar2_dataset_train_bird_1_JPEG_3.png']
    #         # TODO: [test] other splits
    #
    # class TestGetInfluence:
    #     def test_get_influence_fail_invalid_split(self, client):
    #         rv = client.get("/influence/non-exist/0").get_json()
    #         assert rv['code'] == -1
    #         assert rv['msg'] == 'Image is not found or influence for that image is not calculated'
    #
    #     def test_get_influence_fail_invalid_path(self, client):
    #         rv = client.get("/influence/train/Robustar2/dataset/train/bird/10000.JPEG").get_json()
    #         assert rv['code'] == -1
    #         assert rv['msg'] == 'Image is not found or influence for that image is not calculated'
    #
    #     def test_get_influence_success(self, client):
    #         rv = client.get("/influence/train/Robustar2/dataset/train/bird/1.JPEG").get_json()
    #         assert rv['code'] == -1
    #         assert rv['msg'] == 'Image is not found or influence for that image is not calculated'
    #         # assert rv['data'] == [
    #         #     '/Robustar2/visualize_images/_Robustar2_dataset_train_bird_1_JPEG_0.png',
    #         #     '/Robustar2/visualize_images/_Robustar2_dataset_train_bird_1_JPEG_1.png',
    #         #     '/Robustar2/visualize_images/_Robustar2_dataset_train_bird_1_JPEG_2.png',
    #         #     '/Robustar2/visualize_images/_Robustar2_dataset_train_bird_1_JPEG_3.png']
    #         # TODO [test]: pass this - 1. get un-calculated image; 2. calculate 1 image; 3. get
    #         #  that calculated image; current problem in 2 - need other test method

    class TestCalculateInfluence:  # TODO [test]
        def test_calculate_influence_success(self, client):
            rv = client.get("/influence").get_json()
            # assert rv['code'] == -1
            # assert rv['msg'] == 'Image is not found or influence for that image is not calculated'
            # assert rv['data'] == [
            #     '/Robustar2/visualize_images/_Robustar2_dataset_train_bird_1_JPEG_0.png',
            #     '/Robustar2/visualize_images/_Robustar2_dataset_train_bird_1_JPEG_1.png',
            #     '/Robustar2/visualize_images/_Robustar2_dataset_train_bird_1_JPEG_2.png',
            #     '/Robustar2/visualize_images/_Robustar2_dataset_train_bird_1_JPEG_3.png']
