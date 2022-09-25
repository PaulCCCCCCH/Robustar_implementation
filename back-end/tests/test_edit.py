import json

from test_app import app, client


class TestEdit:
    class TestUserEdit:
        def test_user_edit_fail_invalid_split(self, client):
            rv = client.post("/edit/non-exist/0").get_json()
            assert rv['code'] == -1
            assert rv['msg'] == 'Split non-exist not supported'
            rv = client.post("/edit/test/0").get_json()
            assert rv['code'] == -1
            assert rv['msg'] == 'Split test not supported'

        # def test_user_edit_fail_invalid_path(self, client):  # TODO: [test] get one correct data
        #     data = {'image': 'imageName,placeholder',
        #             "image_height": -1,
        #             "image_width": -1
        #             }
        #     rv = client.post("/edit/train/Robustar2/dataset/train/bird/10000.JPEG",
        #                      json=json.loads(json.dumps(data))).get_json()
        #     assert rv['code'] == -1
        #     # assert rv['msg'] == ''

        # def test_user_edit_success(self, client):  # TODO: [test] get one correct data
        #     data = {'image': 'imageName,placeholder',
        #             "image_height": -1,
        #             "image_width": -1
        #             }
        #     rv = client.post("/edit/train/9", json=json.loads(json.dumps(data))).get_json()
        #     assert rv['code'] == 0
        #     # TODO: [test] test `bird/106.JPEG annotated, first row of /Robustar2/annotated.txt is 10`
        #     # TODO: [test] more test cases ...

    # class TestDeleteEdit:  # TODO [test]

    # class TestProposeEdit:  # TODO [test]

    class TestAutoAnnotate:  # TODO [test] do this later - front end changes
        def test_auto_annotate_success(self, client):
            assert True

# def test_image_success(self, client):  # for refrences only
#     response = client.get("/image/train/2", follow_redirects=True)
#     assert len(response.history) == 1  # Check that there was one redirect response
#     assert response.request.path == "/dataset/Robustar2/dataset/train/bird/10.JPEG"
#     response = client.get("/image/test/2", follow_redirects=True)
#     assert len(response.history) == 1
#     assert response.request.path == "/dataset/Robustar2/dataset/test/bird/10.JPEG"
