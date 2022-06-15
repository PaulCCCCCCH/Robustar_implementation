# Robustar launcher

## Windows Setup
```
conda install -c conda-forge pyside2
pip install docker
```


## Linux / MacOS Setup
```
conda install -c conda-forge pyside2

TODO...
```


## Running
First, make sure your docker service is running. Then, run the python script.
```
python launcher.py
```

## FAQ
### Error: `pywintypes.error: (2, 'CreateFile', 'The system cannot find the file specified while installing Sitecore Docker images)`
Make sure your docker service is running.

### Error `NameError: name 'NpipeHTTPAdapter' is not defined`
If you see this error, we recommend you to start a new `conda` environment with `python3.7`, and go through the setup again.