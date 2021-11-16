"""Defines the MQTTTopicWriter class"""

from collections.abc import Iterator
import time
from typing import Iterable

from py2mqtt.client import init_client

class MQTTTopicWriter():
    """Publishes items from an iterable to an MQTT topic. Meant to simulate a smart sensor
    or IoT edge device.
    """
    _topic = ''
    _client = None
    _data = iter([])
    def __init__(self, topic: str, data: Iterable, client=None):
        """Instantiate an MQTT writer

        :param topic: str - The topic to publish to
        :param data: Any iterable
        :param client: Optional - An MQTT client instance or any object with a publish(topic, payload) method
        """
        self._topic = topic
        if not client:
            client = init_client(listen=True)
        self._client = client
        if not isinstance(data, Iterator):
            data = iter(data)
        self._data = data

    def push(self, raw_payload):
        if self._client:
            timestamp = int.to_bytes(int(time.time() * 1e6), 8, 'big', signed=False)
            print(f'chunk timestamp: {int.from_bytes(timestamp, "big")}')
            payload = timestamp + raw_payload
            self._client.publish(self._topic, payload)
            return payload

    def next(self):
        """Reads the next item from the buffer_reader and publishes it to the given topic."""
        if self._buffer_reader and self._client:
            # raw_payload should be bytes
            raw_payload = bytes(next(self._buffer_reader))
            if raw_payload:
                # get timestamp as unsigned 64-bit integer
                timestamp = int(time.time() * 1000).to_bytes(8, 'big', signed=False)
                print(f'chunk timestamp: {int.from_bytes(timestamp, "big")}')
                payload = timestamp + raw_payload
                self._client.publish(self._topic, payload)
                return payload
        return None


if __name__ == '__main__':
    filename = '~/audio/yourfile.wav'
    topic = 'test_topic'
    chk_size = 2048
    n_chunks = 1000
    with open(filename, 'rb') as fp:
        writer = MQTTTopicWriter(topic, fp)
        for i in range(n_chunks):
            writer.push(fp.read(chk_size))
