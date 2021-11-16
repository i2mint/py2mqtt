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
    _max_buffer_len = None
    def __init__(self, topic, mqtt_config=None, keepalive=False, max_buffer_len=None):
        if mqtt_config:
            self._mqtt_config = mqtt_config
        self._keepalive = keepalive
        self._max_buffer_len = max_buffer_len
        add_subscription(topic, self.receive)

    def info(self):
        return {'topic': self._topic}

    def key(self, data):
        """Base sorted case: assume first 64 bits of payload are a timestamp."""
        return int.from_bytes(data[:8], 'big', signed=False)

    def receive(self, payload):
        """Appends an incoming message payload to the read buffer.

        If max_buffer_len is set and the read buffer is full, shifts the first value off the buffer.
        """
        if self._max_buffer_len and len(self._read_buffer) >= self._max_buffer_len:
            self._read_buffer = self._read_buffer[1:]
        self._read_buffer.append(payload)

    def read(self):
        if not self._read_buffer:
            return None
        data = self._read_buffer[0]
        self._read_buffer = self._read_buffer[1:]
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

