class TestConfig:
    def test_config_success(self, client, reset_db):
        response = client.get("/config")
        rv = response.get_json()
        assert rv["code"] == 0
        for field in [
            "device",
            "image_size",
            "image_padding",
            "num_classes",
        ]:
            assert field in rv["data"]
