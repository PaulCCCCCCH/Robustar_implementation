![Robustar](logo2.png "Robustar")

# To Run Backend
```
cd back-end # If you are not already in this folder
pip install -r requirements.txt
python server.py
```


# Robustar

https://hub.docker.com/r/cdonglin/robustar

[Google Drive](https://drive.google.com/drive/folders/1QOP1UGJu2c0OZvTEGZ6FvlbaaiV7ROYb?usp=sharing) 


# Notes

- `user-edit`: is a json of `{<dataset_type>/<img_id>: <img_data>}`, where `<dataset_type>` is usually `train`, `<img_id>` is `0` to `len(dataset) - 1` and `<img_data>` is a comma-separated 1D array (in a string) of length `img_width * img_width * 4` (rgba representation of image, flattened). An example key-value paired is `{"train/0": "124, 126, 54, 255, ..."}`

# Dev 

Robustar reads from the following directories (absolute path, i.e. `Robustar2` folder is placed immediatly under `/` of your file system. Specifically, for linux and MacOS, put the folder under `/` directory. For Windows, put it directly under the volumn your operating system is installed (usually `C:`).

- `/robustar2/checkpoint_images` for pre-trained weights
- `/robustar2/dataset/train` for training dataset. Each subfolder under this directory should contain images for a class, i.e. it should follow the format of pytorch `ImageFolder`. Check [here](https://developpaper.com/detailed-explanation-of-the-use-of-imagefolder-in-pytorch/) for more details about `ImageFolder`
- `/robustar2/dataset/validation` for validation dataset
- `/robustar2/dataset/test` for test dataset
- `/robustar2/dataset/paired` for paired dataset
- `/robustar2/influence_images` for calculated influence images
- `/robustar2/user-edit.json` for user edit.
- `/robustar2/configs.json` for server configs. You directly may copy `configs.json` in the repository over.

You can download our example dataset [here](https://drive.google.com/file/d/1DTaPnWV91C9VXZ9JOBz7hoDxfyUXBpUv/view?usp=sharing)


