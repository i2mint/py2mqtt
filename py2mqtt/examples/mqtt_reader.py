"""Defines the MQTTTopicReader class"""

from py2mqtt.client import add_subscription, init_client, get_client, mqtt_listen, mqtt_stop_listening, mqtt_listening
from stream2py.source_reader import SourceReader

class MQTTTopicReader(SourceReader):
    """Reads messages from an MQTT topic into an internal buffer and exposes a read() interface.
    """
    _read_buffer = []
    _mqtt_config = {}
    _keepalive = False
    _get_key = None
    def __init__(self, topic, mqtt_config=None, keepalive=False):
        if mqtt_config:
            self._mqtt_config = mqtt_config
        self._keepalive = keepalive
        add_subscription(topic, self.receive)

    def info(self):
        return {'topic': self._topic}

    def key(self, data):
        """Base sorted case: assume first 64 bits of payload are a timestamp."""
        return int.from_bytes(data[:8])

    def receive(self, payload):
        self._read_buffer.append(payload)

    def read(self, n=None):
        data = self._read_buffer[:n]
        if n is not None:
            self._read_buffer = self._read_buffer[n:]
        else:
            self._read_buffer = []
        if not data:
            return None
        return data

    def open(self):
        if not get_client():
            init_client(**self._mqtt_config)
        if not mqtt_listening():
            mqtt_listen()

    def close(self):
        if not self._keepalive:
            mqtt_stop_listening()

