"""Defines the MQTTPCMBufferReader class"""

import pyaudio

from py2mqtt.client import add_subscription, init_client, get_client, mqtt_listen, mqtt_stop_listening, mqtt_listening
from py2mqtt.examples.mqtt_reader import MQTTTopicReader
from stream2py.stream_buffer import BufferReader

DFLT_SR = 44100

class MQTTPCMBufferReader(BufferReader):
    """Reads data from a buffer of PCM chunks and plays back.
    """
    _sr: int
    _width: int
    _channels: int
    _audio: pyaudio.PyAudio
    _play_stream = None
    def __init__(self,
        sr=DFLT_SR,
        width=2,
        channels=1,
        **kwargs,
    ):
        self._sr = sr
        self._width = width
        self._channels = channels
        self._audio = pyaudio.PyAudio()
        self._play_stream = self._audio.open(
            format=self._audio.get_format_from_width(width),
            channels=channels,
            rate=sr,
            output=True,
        )
        BufferReader.__init__(self, **kwargs)

    def next(self, *args, **kwargs) -> BufferReader:
        payload = BufferReader.next(self, *args, **kwargs)
        pcm_bytes = payload[8:]
        self._play_stream.write(pcm_bytes)
        return payload
