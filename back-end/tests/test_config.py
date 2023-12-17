class TestConfig:
    def test_config_success(self, client, reset_db):
        response = client.get("/config")
        rv = response.get_json()
        assert rv["code"] == 0
        for field in [
            "weight_to_load",
            "model_arch",
            "device",
            "pre_trained",
            "batch_size",
            "shuffle",
            "num_workers",
            "image_size",
            "image_padding",
            "num_classes",
        ]:
            assert field in rv["data"]
