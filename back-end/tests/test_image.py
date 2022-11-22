from test_app import app, client, PARAM_NAME_IMAGE_PATH
from objects.RServer import RServer


class TestImage:
    class TestGetImageList:
        def test_get_image_list_fail_invalid_split(self, client):
            response = client.get("/image/list/non-exist/1/1")
            assert response.status_code == 400
            rv = response.get_json()
            assert rv['error_code'] == -1
            assert rv['detail'] == 'Invalid data split'

        def test_get_image_list_fail_num_per_page_0(self, client):
            response = client.get("/image/list/train/1/0")
            assert response.status_code == 400
            rv = response.get_json()
            assert rv['error_code'] == -1
            assert rv['detail'] == 'Invalid non-positive num_per_page'

        def test_get_image_list_fail_index_out_of_bound(self, client):
            # train, image index 90-99
            response = client.get("/image/list/train/9/10")
            assert response.status_code == 400
            rv = response.get_json()
            assert rv['error_code'] == -1
            assert rv['detail'] == 'Out of upper-bound'
            # test, image index 90-99
            response = client.get("/image/list/test/9/10")
            assert response.status_code == 400
            rv = response.get_json()
            assert rv['error_code'] == -1
            assert rv['detail'] == 'Out of upper-bound'
            # validation, image index 90-99
            response = client.get("/image/list/validation/9/10")
            assert response.status_code == 400
            rv = response.get_json()
            assert rv['error_code'] == -1
            assert rv['detail'] == 'Out of upper-bound'
            # TODO: split `validation_(in)correct`, `annotated` (&`_(in)correct`) and `proposed`

        def test_get_image_list_success(self, client):
            # train, image index 0 - 3
            response = client.get("/image/list/train/0/4")
            assert response.status_code == 200
            rv = response.get_json()
            assert rv['data'][0][0] == RServer.getServer().baseDir + '/dataset/train/bird/0.JPEG'
            assert rv['data'][1][0] == RServer.getServer().baseDir + '/dataset/train/bird/1.JPEG'
            assert rv['data'][2][0] == RServer.getServer().baseDir + '/dataset/train/bird/2.JPEG'
            assert rv['data'][3][0] == RServer.getServer().baseDir + '/dataset/train/bird/3.JPEG'
            assert rv['code'] == 0
            assert rv['msg'] == 'Success'
            # train, image index 80 - 89 (last 10)
            response = client.get("/image/list/train/8/10")
            assert response.status_code == 200
            rv = response.get_json()
            assert rv['data'][0][0] == RServer.getServer().baseDir + '/dataset/train/turtle/0.JPEG'
            assert rv['data'][1][0] == RServer.getServer().baseDir + '/dataset/train/turtle/1.JPEG'
            assert rv['data'][2][0] == RServer.getServer().baseDir + '/dataset/train/turtle/2.JPEG'
            assert rv['data'][3][0] == RServer.getServer().baseDir + '/dataset/train/turtle/3.JPEG'
            assert rv['data'][4][0] == RServer.getServer().baseDir + '/dataset/train/turtle/4.JPEG'
            assert rv['data'][5][0] == RServer.getServer().baseDir + '/dataset/train/turtle/5.JPEG'
            assert rv['data'][6][0] == RServer.getServer().baseDir + '/dataset/train/turtle/6.JPEG'
            assert rv['data'][7][0] == RServer.getServer().baseDir + '/dataset/train/turtle/7.JPEG'
            assert rv['data'][8][0] == RServer.getServer().baseDir + '/dataset/train/turtle/8.JPEG'
            assert rv['data'][9][0] == RServer.getServer().baseDir + '/dataset/train/turtle/9.JPEG'
            assert rv['code'] == 0
            assert rv['msg'] == 'Success'
            # train, image index 84 - (89) - 90 (1 of 7 out of upper-bound)
            response = client.get("/image/list/train/12/7")
            assert response.status_code == 200
            rv = response.get_json()
            assert rv['data'][0][0] == RServer.getServer().baseDir + '/dataset/train/turtle/4.JPEG'
            assert rv['data'][1][0] == RServer.getServer().baseDir + '/dataset/train/turtle/5.JPEG'
            assert rv['data'][2][0] == RServer.getServer().baseDir + '/dataset/train/turtle/6.JPEG'
            assert rv['data'][3][0] == RServer.getServer().baseDir + '/dataset/train/turtle/7.JPEG'
            assert rv['data'][4][0] == RServer.getServer().baseDir + '/dataset/train/turtle/8.JPEG'
            assert rv['data'][5][0] == RServer.getServer().baseDir + '/dataset/train/turtle/9.JPEG'
            assert rv['code'] == 0
            assert rv['msg'] == 'Success'
            # test, image index 84 - (89) - 90 (1 of 7 out of upper-bound)
            response = client.get("/image/list/test/12/7")
            assert response.status_code == 200
            rv = response.get_json()
            assert rv['data'][0][0] == RServer.getServer().baseDir + '/dataset/test/turtle/4.JPEG'
            assert rv['data'][1][0] == RServer.getServer().baseDir + '/dataset/test/turtle/5.JPEG'
            assert rv['data'][2][0] == RServer.getServer().baseDir + '/dataset/test/turtle/6.JPEG'
            assert rv['data'][3][0] == RServer.getServer().baseDir + '/dataset/test/turtle/7.JPEG'
            assert rv['data'][4][0] == RServer.getServer().baseDir + '/dataset/test/turtle/8.JPEG'
            assert rv['data'][5][0] == RServer.getServer().baseDir + '/dataset/test/turtle/9.JPEG'
            assert rv['code'] == 0
            assert rv['msg'] == 'Success'
            # validation, image index 84 - (89) - 90 (1 of 7 out of upper-bound)
            response = client.get("/image/list/validation/12/7")
            assert response.status_code == 200
            rv = response.get_json()
            assert rv['data'][0][0] == RServer.getServer().baseDir + '/dataset/test/turtle/4.JPEG'
            assert rv['data'][1][0] == RServer.getServer().baseDir + '/dataset/test/turtle/5.JPEG'
            assert rv['data'][2][0] == RServer.getServer().baseDir + '/dataset/test/turtle/6.JPEG'
            assert rv['data'][3][0] == RServer.getServer().baseDir + '/dataset/test/turtle/7.JPEG'
            assert rv['data'][4][0] == RServer.getServer().baseDir + '/dataset/test/turtle/8.JPEG'
            assert rv['data'][5][0] == RServer.getServer().baseDir + '/dataset/test/turtle/9.JPEG'
            assert rv['code'] == 0
            assert rv['msg'] == 'Success'
            # TODO: split `validation_(in)correct`, `annotated`, `test_(in)correct` and `proposed`

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
                                  "=" + RServer.getServer().baseDir + "/dataset/train/bird/10000.JPEG")
            assert response.status_code == 400
            rv = response.get_json()
            assert rv['error_code'] == -1
            assert rv['detail'] == 'Invalid image path ' + RServer.getServer().baseDir + '/dataset/train/bird/10000.JPEG'
            response = client.get("/image/next/train?" + PARAM_NAME_IMAGE_PATH +
                                  "=" + RServer.getServer().baseDir + "/dataset/train/panda/0.JPEG")
            assert response.status_code == 400
            rv = response.get_json()
            assert rv['error_code'] == -1
            assert rv['detail'] == 'Invalid image path ' + RServer.getServer().baseDir + '/dataset/train/panda/0.JPEG'
            response = client.get("/image/next/train?" + PARAM_NAME_IMAGE_PATH +
                                  "=" + RServer.getServer().baseDir + "/dataset/proposed/bird/0.JPEG")
            assert response.status_code == 400
            rv = response.get_json()
            assert rv['error_code'] == -1
            assert rv['detail'] == 'Invalid image path ' + RServer.getServer().baseDir + '/dataset/proposed/bird/0.JPEG'
            # TODO: split `annotated` and `proposed`

        def test_get_next_image_success(self, client):
            response = client.get("/image/next/train?" + PARAM_NAME_IMAGE_PATH +
                                  "=" + RServer.getServer().baseDir + "/dataset/train/bird/1.JPEG")
            assert response.status_code == 200
            rv = response.get_json()
            assert rv['data'] == RServer.getServer().baseDir + '/dataset/train/bird/2.JPEG'
            assert rv['code'] == 0
            assert rv['msg'] == 'Success'
            # TODO: split `annotated` and `proposed`

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
            response = client.get("/image/class/annotated")
            assert response.status_code == 200
            rv = response.get_json()
            assert rv['code'] == 0
            assert rv['data'] == {'bird': 0, 'cat': 10, 'crab': 20, 'dog': 30, 'fish': 40,
                                  'frog': 50, 'insect': 60, 'primate': 70, 'turtle': 80}
            response = client.get("/image/class/validation")
            assert response.status_code == 200
            rv = response.get_json()
            assert rv['code'] == 0
            assert rv['data'] == {'bird': 0, 'cat': 10, 'crab': 20, 'dog': 30, 'fish': 40,
                                  'frog': 50, 'insect': 60, 'primate': 70, 'turtle': 80}
            # response = client.get("/image/class/validation_correct")
            # assert response.status_code == 200
            # rv = response.get_json()
            # assert rv['code'] == 0
            # assert rv['data'] == {'bird': 0, 'cat': 10, 'crab': 20, 'dog': 30, 'fish': 40,
            #                       'frog': 50, 'insect': 60, 'primate': 70, 'turtle': 80}
            # response = client.get("/image/class/validation_incorrect")
            # assert response.status_code == 200
            # rv = response.get_json()
            # assert rv['code'] == 0
            assert rv['data'] == {'bird': 0, 'cat': 10, 'crab': 20, 'dog': 30, 'fish': 40,
                                  'frog': 50, 'insect': 60, 'primate': 70, 'turtle': 80}
            response = client.get("/image/class/test")
            assert response.status_code == 200
            rv = response.get_json()
            assert rv['code'] == 0
            assert rv['data'] == {'bird': 0, 'cat': 10, 'crab': 20, 'dog': 30, 'fish': 40,
                                  'frog': 50, 'insect': 60, 'primate': 70, 'turtle': 80}
            # response = client.get("/image/class/test_correct")
            # assert response.status_code == 200
            # rv = response.get_json()
            # assert rv['code'] == 0
            # assert rv['data'] == {'bird': 0, 'cat': 10, 'crab': 20, 'dog': 30, 'fish': 40,
            #                       'frog': 50, 'insect': 60, 'primate': 70, 'turtle': 80}
            # response = client.get("/image/class/test_incorrect")
            # assert response.status_code == 200
            # rv = response.get_json()
            # assert rv['code'] == 0
            # assert rv['data'] == {'bird': 0, 'cat': 10, 'crab': 20, 'dog': 30, 'fish': 40,
            #                       'frog': 50, 'insect': 60, 'primate': 70, 'turtle': 80}
            # TODO: split `validation_(in)correct`, `test_(in)correct`) and `proposed`

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
