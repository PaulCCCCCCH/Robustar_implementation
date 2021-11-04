![Robustar](logo2.png "Robustar")

# To Run Backend
```
cd back-end # If you are not already in this folder
pip install -r requirements.txt
python run server.py
```


# Robustar

https://hub.docker.com/r/cdonglin/robustar

[Google Drive](https://drive.google.com/drive/folders/1QOP1UGJu2c0OZvTEGZ6FvlbaaiV7ROYb?usp=sharing) 


# Notes

- `user-edit`: is a json of `{<dataset_type>/<img_id>: <img_data>}`, where `<dataset_type>` is usually `train`, `<img_id>` is `0` to `len(dataset) - 1` and `<img_data>` is a comma-separated 1D array (in a string) of length `img_width * img_width * 4` (rgba representation of image, flattened). An example key-value paired is `{"train/0": "124, 126, 54, 255, ..."}`

# Dev 

Robustar reads from the following directories (absolute path, i.e. `Robustar2` folder is placed immediatly under `/` of your file system)

- `/Robuster2/checkpoint_images` for pre-trained weights
- `/Robuster2/dataset/train` for training dataset
- `/Robuster2/dataset/test` for test dataset
- `/Robuster2/dataset/paired` for paired dataset
- `/Robuster2/influence_images` for calculated influence 
- `/Robuster2/user-edit.json` for user edit.
