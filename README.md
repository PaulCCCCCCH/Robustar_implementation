# Robustar

![Logo](doc/logo_long.png "logo")

This repository contains the source code for [Robustar, an interactive toolbox for robust vision classification](https://github.com/HaohanWang/Robustar).

## To Run Docker

First, run `robustar.sh -m setup -a <version_name>` to pull robustar image. 

Then, run `robustar.sh -m run <options> `. For a list of `<options>`, please run `robustar.sh` with no arguments. Make sure you set up the mounting directories and port forwarding correctly.

If at any point you wish to change the setting, please remove the docker container and setup a new one. You can run `docker container ls -a` to see a list of containers, and use `docker container rm <name>` to remove.

Please make sure port 6848 and 6006 on your machine are available. 

## Configuration File
You need to pass a config file (default `./configs.json`) to `robustar.sh`. It is a `JSON` file with the following fields:

- **weight_to_load**: The name of the weight file to be loaded. Robustar will display its predictions and attention weights on the given dataset. If not provided or file is not found, but `pre_trained` is set to true, Robustar will try to download a trained image somewhere else.
- **model_arch**: The architecture of the model. Choose from `["resnet-18", "resnet-18-32x32", "resnet-18", "resnet-34", "resnet-50", "resnet-101", "resnet-152", "mobilenet-v2"]`. Make sure this matches what's stored in `weight_to_load`.
]`
- **device**: e.g. `'cpu'`, `'cuda'`, `'cuda:5'`, etc. Robustar uses this device to do both training and inference.
- **pre_trained**: Do we load pre-trained weights? If set to false, `weight_to_load` will be ignored and Robustar will train a model from scratch. Note that the image predictions and focus will be non-sensical in this case.



## Build Docker Image
In front-end directory, run ` lerna run build `.   

Then, return back to root directory and run
```
docker build --build-arg VCUDA=<cuda version> .
```
where `<cuda version>` is chosen from `cpu`, `9.2`, `10.2`, `11.1` and `11.3`.

Adjust the tag of the docker image with
```
docker tag <image_id> <user_id>/<repo>:<version>
```

Finally, push onto DockerHub with:
```
docker push <user_id>/<repo>:<version>
```

## Dev setup 

See [backend doc](./back-end/README.md) and [frontend doc](./front-end/README.md) for more details

