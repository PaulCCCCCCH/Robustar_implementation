import json

from test_app import app, client


class TestTest:
    class TestStartTestThread:
        def test_start_test_thread_fail_invalid_split(self, client):
            data = {'split': 'invalid'}
            response = client.post("/test", json=json.loads(json.dumps(data)))
            assert response.status_code == 500
            rv = response.get_json()
            assert rv['error_code'] == -1
            assert rv['detail'] == 'Failed to start testingTest called with wrong data split'

        # def test_start_test_thread_success(self, client):  # TODO: exception in thread?  # TODO: invalid pass
        #     data = {'split': 'validation'}
        #     rv = client.post("/test", json=json.loads(json.dumps(data))).get_json()
        #     assert rv['code'] == 0
        #     data = {'split': 'test'}
        #     rv = client.post("/test", json=json.loads(json.dumps(data))).get_json()
        #     assert rv['code'] == 0

    class TestTestResultCorrect:
        def test_test_result_correct(self, client):  # TODO: test
            assert True
