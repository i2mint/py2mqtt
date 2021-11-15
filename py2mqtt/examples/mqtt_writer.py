"""Defines the MQTTTopicWriter class"""

from collections.abc import Iterator
import time
from typing import Iterable

from py2mqtt.client import init_client

class MQTTTopicWriter():
    """Publishes items from a buffer reader to an MQTT topic. Meant to simulate a smart sensor
    or IoT edge device.

    Does not handle any MQTT connectivity details, must be passed an MQTT client instance.
    """
    _topic = ''
    _client = None
    _buffer_reader = iter([])
    def __init__(self, topic: str, buffer_reader: Iterable, client=None):
        """Instantiate an MQTT writer

        :param topic: str - The topic to publish to
        :param buffer_reader: Any iterable (will be wrap
        :param client: An MQTT client instance or any object with a publish(topic, payload) method
        """
        self._topic = topic
        if not client:
            client = init_client(listen=True)
        self._client = client
        if not isinstance(buffer_reader, Iterator):
            buffer_reader = iter(buffer_reader)
        self._buffer_reader = buffer_reader

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
    topic = 'test_topic'
    buffer = iter(range(1e3))
    writer = MQTTTopicWriter(topic, buffer)
    for i in range(10000):
        writer.next()
