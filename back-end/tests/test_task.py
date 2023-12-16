from test_app import client


class TestTask:
    class TestStopTask:
        def test_stop_task_fail_invalid_task_id(self, client):
            response = client.get("/task/stop/1")
            assert response.status_code == 400
            rv = response.get_json()
            assert rv['error_code'] == -1
            assert rv['detail'] == 'Task(1) not in list'

        def test_stop_task_success(self, client): # TODO: test
            assert True