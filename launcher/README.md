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

## Packaging
To package the launcher, it is recommended to create a new python environment. You can use Conda or Virtualenv to do so. The following instructions use Conda.
First, create a new environment with necessary packages
```
conda create -n <name-of-env> python=3.9
conda activate <name-of-env>
pip install PySide2
pip install docker
pip install pyinstaller
```
Then, in `\launcher` folder, run
```
pyinstaller app.spec
```
After that you shall see a new folder `\launcher\dist`, inside it is the newly packaged launcher. 

## FAQ
### Error: `pywintypes.error: (2, 'CreateFile', 'The system cannot find the file specified while installing Sitecore Docker images)`
Make sure your docker service is running.

### Error `NameError: name 'NpipeHTTPAdapter' is not defined`
If you see this error, we recommend you to start a new `conda` environment with `python3.7`, and go through the setup again.