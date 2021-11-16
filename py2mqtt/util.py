"""Utils"""


try:
    import importlib.resources

    _files = importlib.resources.files  # only valid in 3.9+
except AttributeError:
    import importlib_resources  # needs pip install

    _files = importlib_resources.files

files = _files('py2mqtt')
sample_data_dir = files / 'sample_data'
sample_data_dir_path = str(sample_data_dir)