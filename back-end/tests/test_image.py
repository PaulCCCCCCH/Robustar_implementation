from test_app import app, client, PARAM_NAME_IMAGE_PATH


class TestImage:
    class TestGetImageList:
        def test_get_image_list_fail_invalid_split(self, client):
            rv = client.get("/image/list/non-exist/1/1").get_json()
            assert rv['code'] == -1
            assert rv['msg'] == 'Error retrieving image paths - Invalid data split'

        def test_get_image_list_fail_num_per_page_0(self, client):
            rv = client.get("/image/list/train/1/0").get_json()
            assert rv['code'] == -1
            assert rv['msg'] == 'Error retrieving image paths - cannot get image idx [0, 0)'

        def test_get_image_list_fail_index_out_of_bound(self, client):
            rv = client.get("/image/list/train/900/10").get_json()  # image index 9000-9009
            assert rv['code'] == -1
            assert rv['msg'] == 'Error retrieving image paths - cannot get image idx [9000, 9010)'

        def test_get_image_list_success(self, client):
            # image index 0 - 3
            rv = client.get("/image/list/train/0/4").get_json()
            assert rv['data'][0][0] == '/Robustar2/dataset/train/bird/0.JPEG'
            assert rv['data'][1][0] == '/Robustar2/dataset/train/bird/1.JPEG'
            assert rv['data'][2][0] == '/Robustar2/dataset/train/bird/10.JPEG'
            assert rv['data'][3][0] == '/Robustar2/dataset/train/bird/100.JPEG'
            assert rv['code'] == 0
            assert rv['msg'] == 'Success'
            # image index 3000 - 3005
            rv = client.get("/image/list/train/500/6").get_json()
            assert rv['data'][0][0] == '/Robustar2/dataset/train/dog/0.JPEG'
            assert rv['data'][1][0] == '/Robustar2/dataset/train/dog/1.JPEG'
            assert rv['data'][2][0] == '/Robustar2/dataset/train/dog/10.JPEG'
            assert rv['data'][3][0] == '/Robustar2/dataset/train/dog/100.JPEG'
            assert rv['data'][4][0] == '/Robustar2/dataset/train/dog/101.JPEG'
            assert rv['data'][5][0] == '/Robustar2/dataset/train/dog/102.JPEG'
            assert rv['code'] == 0
            assert rv['msg'] == 'Success'
            # image index 8990 - 8999 (last 10)
            rv = client.get("/image/list/train/899/10").get_json()
            assert rv['data'][0][0] == '/Robustar2/dataset/train/turtle/990.JPEG'
            assert rv['data'][1][0] == '/Robustar2/dataset/train/turtle/991.JPEG'
            assert rv['data'][2][0] == '/Robustar2/dataset/train/turtle/992.JPEG'
            assert rv['data'][3][0] == '/Robustar2/dataset/train/turtle/993.JPEG'
            assert rv['data'][4][0] == '/Robustar2/dataset/train/turtle/994.JPEG'
            assert rv['data'][5][0] == '/Robustar2/dataset/train/turtle/995.JPEG'
            assert rv['data'][6][0] == '/Robustar2/dataset/train/turtle/996.JPEG'
            assert rv['data'][7][0] == '/Robustar2/dataset/train/turtle/997.JPEG'
            assert rv['data'][8][0] == '/Robustar2/dataset/train/turtle/998.JPEG'
            assert rv['data'][9][0] == '/Robustar2/dataset/train/turtle/999.JPEG'
            assert rv['code'] == 0
            assert rv['msg'] == 'Success'
            # image index 8995 - (8999) - 9001 (2 of 7 out of upper-bound)
            rv = client.get("/image/list/train/1285/7").get_json()
            assert rv['data'][0][0] == '/Robustar2/dataset/train/turtle/995.JPEG'
            assert rv['data'][1][0] == '/Robustar2/dataset/train/turtle/996.JPEG'
            assert rv['data'][2][0] == '/Robustar2/dataset/train/turtle/997.JPEG'
            assert rv['data'][3][0] == '/Robustar2/dataset/train/turtle/998.JPEG'
            assert rv['data'][4][0] == '/Robustar2/dataset/train/turtle/999.JPEG'
            assert rv['code'] == 0
            assert rv['msg'] == 'Success'
            # TODO: [test] other splits - needs other test methods

    class TestGetNextImage:
        def test_get_next_image_fail_invalid_split(self, client):
            rv = client.get("/image/next/non-exist?" + PARAM_NAME_IMAGE_PATH + "=/0").get_json()
            assert rv['code'] == -1
            assert rv['msg'] == 'Split non-exist not supported'
            rv = client.get("/image/next/test?" + PARAM_NAME_IMAGE_PATH + "=/0").get_json()
            assert rv['code'] == -1
            assert rv['msg'] == 'Split test not supported'

        def test_get_next_image_fail_invalid_path(self, client):
            rv = client.get("/image/next/train?" + PARAM_NAME_IMAGE_PATH +
                            "=/Robustar2/dataset/train/bird/10000.JPEG").get_json()
            assert rv['code'] == -1
            assert rv['msg'] == 'Invalid image path /Robustar2/dataset/train/bird/10000.JPEG'
            rv = client.get("/image/next/train?" + PARAM_NAME_IMAGE_PATH +
                            "=/Robustar2/dataset/train/panda/0.JPEG").get_json()
            assert rv['code'] == -1
            assert rv['msg'] == 'Invalid image path /Robustar2/dataset/train/panda/0.JPEG'
            rv = client.get("/image/next/train?" + PARAM_NAME_IMAGE_PATH +
                            "=/Robustar2/dataset/proposed/bird/0.JPEG").get_json()
            assert rv['code'] == -1
            assert rv['msg'] == 'Invalid image path /Robustar2/dataset/proposed/bird/0.JPEG'
            # TODO: [test] annotated and proposed - needs other test methods
            # rv = client.get("/image/next/annotated/100000").get_json()
            # assert rv['code'] == -1
            # assert rv['msg'] == 'Image with given id not exist'
            # rv = client.get("/image/next/proposed/100000").get_json()
            # assert rv['code'] == -1
            # assert rv['msg'] == 'Image with given id not exist'

        def test_get_next_image_success(self, client):
            rv = client.get("/image/next/train?" + PARAM_NAME_IMAGE_PATH +
                            "=/Robustar2/dataset/train/bird/1.JPEG").get_json()
            assert rv['data'] == '/Robustar2/dataset/train/bird/10.JPEG'
            assert rv['code'] == 0
            assert rv['msg'] == 'Success'
            # TODO: [test] annotated and proposed - needs other test methods

    # class TestGetAnnotated: # TODO [test]

    class TestGetClassPage:
        def test_get_class_page_fail_invalid_split(self, client):
            rv = client.get("/image/class/non-exist").get_json()
            assert rv['code'] == -1
            assert rv['msg'] == 'Split not supported'

        def test_get_class_page_success(self, client):
            rv = client.get("/image/class/train").get_json()
            assert rv['code'] == 0
            assert rv['data'] == {'bird': 0, 'cat': 1000, 'crab': 2000, 'dog': 3000, 'fish': 4000,
                                  'frog': 5000, 'insect': 6000, 'primate': 7000, 'turtle': 8000}
            # TODO: [test] other splits

    class TestGetSplitLength:
        def test_split_length_fail_invalid_split(self, client):
            rv = client.get("/image/non-exist").get_json()
            assert rv['code'] == -1
            assert rv['msg'] == 'Split not supported'

        def test_split_length_success(self, client):
            rv = client.get("/image/train").get_json()
            assert rv['code'] == 0
            assert rv['data'] == 9000
            # TODO: [test] other splits
