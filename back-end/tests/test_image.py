from test_app import app, client, PARAM_NAME_IMAGE_PATH


class TestImage:
    class TestGetImageList:
        def test_get_image_list_fail_invalid_split(self, client):
            response = client.get("/image/list/non-exist/1/1")
            assert response.status_code == 500
            rv = response.get_json()
            assert rv['error_code'] == -1
            assert rv['detail'] == 'Error retrieving image paths - Invalid data split'

        # def test_get_image_list_fail_num_per_page_0(self, client):
        #     response = client.get("/image/list/train/1/0")
        #     assert response.status_code == 500
        #     rv = response.get_json()
        #     assert rv['error_code'] == -1
        #     assert rv['detail'] == 'Error retrieving image paths - empty image list [0, 0)'

        # def test_get_image_list_fail_index_out_of_bound(self, client):
        #     response = client.get("/image/list/train/9/10")  # image index 90-99
        #     assert response.status_code == 500
        #     rv = response.get_json()
        #     assert rv['error_code'] == -1
        #     assert rv['detail'] == 'Error retrieving image paths - empty image list [90, 100)'

        def test_get_image_list_success(self, client):
            # image index 0 - 3
            response = client.get("/image/list/train/0/4")
            assert response.status_code == 200
            rv = response.get_json()
            assert rv['data'][0][0] == '/Robustar2/dataset/train/bird/0.JPEG'
            assert rv['data'][1][0] == '/Robustar2/dataset/train/bird/1.JPEG'
            assert rv['data'][2][0] == '/Robustar2/dataset/train/bird/2.JPEG'
            assert rv['data'][3][0] == '/Robustar2/dataset/train/bird/3.JPEG'
            assert rv['code'] == 0
            assert rv['msg'] == 'Success'
            # image index 30 - 35
            response = client.get("/image/list/train/5/6")
            assert response.status_code == 200
            rv = response.get_json()
            assert rv['data'][0][0] == '/Robustar2/dataset/train/dog/0.JPEG'
            assert rv['data'][1][0] == '/Robustar2/dataset/train/dog/1.JPEG'
            assert rv['data'][2][0] == '/Robustar2/dataset/train/dog/2.JPEG'
            assert rv['data'][3][0] == '/Robustar2/dataset/train/dog/3.JPEG'
            assert rv['data'][4][0] == '/Robustar2/dataset/train/dog/4.JPEG'
            assert rv['data'][5][0] == '/Robustar2/dataset/train/dog/5.JPEG'
            assert rv['code'] == 0
            assert rv['msg'] == 'Success'
            # image index 80 - 89 (last 10)
            response = client.get("/image/list/train/8/10")
            assert response.status_code == 200
            rv = response.get_json()
            assert rv['data'][0][0] == '/Robustar2/dataset/train/turtle/0.JPEG'
            assert rv['data'][1][0] == '/Robustar2/dataset/train/turtle/1.JPEG'
            assert rv['data'][2][0] == '/Robustar2/dataset/train/turtle/2.JPEG'
            assert rv['data'][3][0] == '/Robustar2/dataset/train/turtle/3.JPEG'
            assert rv['data'][4][0] == '/Robustar2/dataset/train/turtle/4.JPEG'
            assert rv['data'][5][0] == '/Robustar2/dataset/train/turtle/5.JPEG'
            assert rv['data'][6][0] == '/Robustar2/dataset/train/turtle/6.JPEG'
            assert rv['data'][7][0] == '/Robustar2/dataset/train/turtle/7.JPEG'
            assert rv['data'][8][0] == '/Robustar2/dataset/train/turtle/8.JPEG'
            assert rv['data'][9][0] == '/Robustar2/dataset/train/turtle/9.JPEG'
            assert rv['code'] == 0
            assert rv['msg'] == 'Success'
            # image index 84 - (89) - 90 (1 of 7 out of upper-bound)
            response = client.get("/image/list/train/12/7")
            assert response.status_code == 200
            rv = response.get_json()
            assert rv['data'][0][0] == '/Robustar2/dataset/train/turtle/4.JPEG'
            assert rv['data'][1][0] == '/Robustar2/dataset/train/turtle/5.JPEG'
            assert rv['data'][2][0] == '/Robustar2/dataset/train/turtle/6.JPEG'
            assert rv['data'][3][0] == '/Robustar2/dataset/train/turtle/7.JPEG'
            assert rv['data'][4][0] == '/Robustar2/dataset/train/turtle/8.JPEG'
            assert rv['data'][5][0] == '/Robustar2/dataset/train/turtle/9.JPEG'
            assert rv['code'] == 0
            assert rv['msg'] == 'Success'
            # TODO: [test] other splits - needs other test methods

    class TestGetNextImage:
        def test_get_next_image_fail_invalid_split(self, client):
            response = client.get("/image/next/non-exist?" + PARAM_NAME_IMAGE_PATH + "=/0")
            assert response.status_code == 400
            rv = response.get_json()
            assert rv['error_code'] == -1
            assert rv['detail'] == 'Split non-exist not supported'
            response = client.get("/image/next/test?" + PARAM_NAME_IMAGE_PATH + "=/0")
            assert response.status_code == 400
            rv = response.get_json()
            assert rv['error_code'] == -1
            assert rv['detail'] == 'Split test not supported'

        def test_get_next_image_fail_invalid_path(self, client):
            response = client.get("/image/next/train?" + PARAM_NAME_IMAGE_PATH +
                                  "=/Robustar2/dataset/train/bird/10000.JPEG")
            assert response.status_code == 400
            rv = response.get_json()
            assert rv['error_code'] == -1
            assert rv['detail'] == 'Invalid image path /Robustar2/dataset/train/bird/10000.JPEG'
            response = client.get("/image/next/train?" + PARAM_NAME_IMAGE_PATH +
                                  "=/Robustar2/dataset/train/panda/0.JPEG")
            assert response.status_code == 400
            rv = response.get_json()
            assert rv['error_code'] == -1
            assert rv['detail'] == 'Invalid image path /Robustar2/dataset/train/panda/0.JPEG'
            response = client.get("/image/next/train?" + PARAM_NAME_IMAGE_PATH +
                                  "=/Robustar2/dataset/proposed/bird/0.JPEG")
            assert response.status_code == 400
            rv = response.get_json()
            assert rv['error_code'] == -1
            assert rv['detail'] == 'Invalid image path /Robustar2/dataset/proposed/bird/0.JPEG'
            # TODO: [test] annotated and proposed - needs other test methods
            # rv = client.get("/image/next/annotated/100000").get_json()
            # assert rv['code'] == -1
            # assert rv['msg'] == 'Image with given id not exist'
            # rv = client.get("/image/next/proposed/100000").get_json()
            # assert rv['code'] == -1
            # assert rv['msg'] == 'Image with given id not exist'

        def test_get_next_image_success(self, client):
            response = client.get("/image/next/train?" + PARAM_NAME_IMAGE_PATH +
                            "=/Robustar2/dataset/train/bird/1.JPEG")
            assert response.status_code == 200
            rv = response.get_json()
            assert rv['data'] == '/Robustar2/dataset/train/bird/2.JPEG'
            assert rv['code'] == 0
            assert rv['msg'] == 'Success'
            # TODO: [test] annotated and proposed - needs other test methods

    # class TestGetAnnotated: # TODO [test]

    class TestGetClassPage:
        def test_get_class_page_fail_invalid_split(self, client):
            response = client.get("/image/class/non-exist")
            assert response.status_code == 400
            rv = response.get_json()
            assert rv['error_code'] == -1
            assert rv['detail'] == 'Split not supported'

        def test_get_class_page_success(self, client):
            response = client.get("/image/class/train")
            assert response.status_code == 200
            rv = response.get_json()
            assert rv['code'] == 0
            assert rv['data'] == {'bird': 0, 'cat': 10, 'crab': 20, 'dog': 30, 'fish': 40,
                                  'frog': 50, 'insect': 60, 'primate': 70, 'turtle': 80}
            # TODO: [test] other splits

    class TestGetSplitLength:
        def test_split_length_fail_invalid_split(self, client):
            response = client.get("/image/non-exist")
            assert response.status_code == 400
            rv = response.get_json()
            assert rv['error_code'] == -1
            assert rv['detail'] == 'Split not supported'

        def test_split_length_success(self, client):
            response = client.get("/image/train")
            assert response.status_code == 200
            rv = response.get_json()
            assert rv['code'] == 0
            assert rv['data'] == 90
            # TODO: [test] other splits
