"""
Interfaces for Python to transmit, receive, and act on data over an MQTT connection.
"""

from py2mqtt.util import files, sample_data_dir_path, sample_data_dir

from importlib_resources import files

sample_data_dir_path = files('py2mqtt.sample_data')
