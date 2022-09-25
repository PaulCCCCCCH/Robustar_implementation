from test_app import app, client


class TestTask:
    class TestStopTask:
        def test_stop_task_fail_invalid_task_id(self, client):
            rv = client.get("/task/stop/1").get_json()
            assert rv['code'] == -1
            assert rv['msg'] == 'Task(1) not in list'

        def test_stop_task_success(self, client): # TODO: test
            pass