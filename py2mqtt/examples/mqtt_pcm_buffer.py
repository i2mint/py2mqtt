"""Defines the MQTTTopicReader class"""

from py2mqtt.client import add_subscription, init_client, get_client, mqtt_listen, mqtt_stop_listening, mqtt_listening
from py2mqtt.examples.mqtt_reader import MQTTTopicReader
from py2mqtt.examples.mqtt_pcm_buffer_reader import MQTTPCMBufferReader
from stream2py.stream_buffer import StreamBuffer
from stream2py.buffer_reader import BufferReader

DFLT_SR = 44100

class MQTTPCMBuffer(StreamBuffer):
    """Reads messages from an MQTT topic into an internal buffer and exposes a read() interface.
    """
    _sr: int
    _width: int
    _channels: int
    def __init__(self,
        reader: MQTTTopicReader,
        sr=DFLT_SR,
        width=2,
        channels=1,
        maxlen=1000,
    ):
        self._sr = sr
        self._width = width
        self._channels = channels
        StreamBuffer.__init__(self, reader, maxlen=maxlen)
