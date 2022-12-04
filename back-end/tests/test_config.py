from test_app import app, client


class TestConfig:
    def test_config_success(self, client):
        response = client.get("/config")
        rv = response.get_json()
        assert rv["code"] == 0
        assert rv["data"] == {
            "weight_to_load": "resnet-18.pth",
            "model_arch": "resnet-18-32x32",
            "device": "cpu",
            "pre_trained": False,
            "batch_size": 16,
            "shuffle": True,
            "num_workers": 8,
            "image_size": 32,
            "image_padding": "none",
            "num_classes": 9,
        }
