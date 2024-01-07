import json

from . import PARAM_NAME_IMAGE_PATH
from objects.RServer import RServer


class TestEdit:
    class TestUserEdit:  # TODO: split `annotated` and `proposed`
        def test_user_edit_fail_invalid_split(self, client, reset_db):
            response = client.post("/edit/non-exist?image_url=0")
            assert response.status_code == 400
            rv = response.get_json()
            assert rv["error_code"] == -1
            assert rv["detail"] == "Split non-exist not supported"
            response = client.post("/edit/test?image_url=0")
            assert response.status_code == 400
            rv = response.get_json()
            assert rv["error_code"] == -1
            assert rv["detail"] == "Split test not supported"

        def test_user_edit_fail_invalid_path(self, client, reset_db):
            data = {
                "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAMSURBVBhXY/j//z8ABf4C/qc1gYQAAAAASUVORK5CYII=",
                "image_height": "224",
                "image_width": "224",
            }  # a png image of 1*1 pixel in white
            response = client.post(
                "/edit/train?"
                + PARAM_NAME_IMAGE_PATH
                + "="
                + RServer.get_server().base_dir
                + "/dataset/train/bird/10000.JPEG",
                json=json.loads(json.dumps(data)),
            )
            assert response.status_code == 400
            rv = response.get_json()
            assert rv["error_code"] == -1
            assert rv["detail"] == "invalid image path"

        def test_user_edit_fail_broken_image_data(self, client, reset_db):
            data = {
                "image": "data:image/png;base64,iVBORw0KGgoAAAANS",
                "image_height": "224",
                "image_width": "224",
            }
            response = client.post(
                "/edit/train?"
                + PARAM_NAME_IMAGE_PATH
                + "="
                + RServer.get_server().base_dir
                + "/dataset/train/bird/1.JPEG",
                json=json.loads(json.dumps(data)),
            )
            assert response.status_code == 400
            rv = response.get_json()
            assert rv["error_code"] == -1
            assert rv["detail"] == "Broken image, fail to decode"

    def test_user_edit_success(self, client, reset_db):
        data = {
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAMSURBVBhXY/j//z8ABf4C/qc1gYQAAAAASUVORK5CYII=",
            "image_height": "224",
            "image_width": "224",
        }  # a png image of 1*1 pixel in white
        response = client.post(
            "/edit/train?"
            + PARAM_NAME_IMAGE_PATH
            + "="
            + RServer.get_server().base_dir
            + "/dataset/train/bird/0.JPEG",
            json=json.loads(json.dumps(data)),
        )
        assert response.status_code == 200
        rv = response.get_json()
        assert rv["code"] == 0
        assert "Success" in rv["msg"]


# class TestDeleteEdit:  # TODO [test]

# class TestProposeEdit:  # TODO [test]


class TestAutoAnnotate:  # TODO [test]
    def test_auto_annotate_success(self, client, reset_db):
        assert True


# def test_image_success(self, client):  # for refrences only
#     response = client.get("/image/train/2", follow_redirects=True)
#     assert len(response.history) == 1  # Check that there was one redirect response
#     assert response.request.path == "/dataset/Robustar2/dataset/train/bird/10.JPEG"
#     response = client.get("/image/test/2", follow_redirects=True)
#     assert len(response.history) == 1
#     assert response.request.path == "/dataset/Robustar2/dataset/test/bird/10.JPEG"
