# Robustar_migration

## Running
Everything is set up in docker. Run `robustar.sh` for details.

## Configuration File
You need to pass a config file (default `./configs.json`) to `robustar.sh`. It is a `JSON` file with the following fields:

- **weight_to_load**: The name of the weight file to be loaded. Robustar will display its predictions and attention weights on the given dataset. If not provided or file is not found, but `pre_trained` is set to true, Robustar will try to download a trained image somewhere else.
- **model_arch**: The architecture of the model. Choose from `["resnet-18", "resnet-18-32x32", "resnet-18", "resnet-34", "resnet-50", "resnet-101", "resnet-152", "mobilenet-v2"]`. Make sure this matches what's stored in `weight_to_load`.
]`
- **device**: e.g. `'cpu'`, `'cuda'`, `'cuda:5'`, etc. Robustar uses this device to do both training and inference.
- **pre_trained**: Do we load pre-trained weights? If set to false, `weight_to_load` will be ignored and Robustar will train a model from scratch. Note that the image predictions and focus will be non-sensical in this case.




## Dev setup 

See [backend doc](./back-end/README.md) and [frontend doc](./front-end/README.md) for more details
