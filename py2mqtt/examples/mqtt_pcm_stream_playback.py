import pyaudio

from py2mqtt.examples.mqtt_reader import MQTTTopicReader
from stream2py.stream_buffer import StreamBuffer
# from py2mqtt.examples.mqtt_pcm_buffer import MQTTPCMBuffer

TOPIC = 'test_topic'

def mqtt_stream_playback_demo(width=2, channels=1, sr=44100):
    audio = pyaudio.PyAudio()
    play_stream = audio.open(
        format=audio.get_format_from_width(width),
        channels=channels,
        rate=sr,
        output=True,
    )
    stream_reader = MQTTTopicReader(TOPIC)
    with StreamBuffer(stream_reader, maxlen=1000) as buffer:
        playback_reader = buffer.mk_reader()
        for message_payload in playback_reader:
            pcm_bytes = message_payload[8:]
            play_stream.write(pcm_bytes)
            timestamp_bytes = message_payload[:8]
            print(f'received timestamp_bytes: {message_payload[:8]}, {type(message_payload)}')
            print(f'received chunk with timestamp {int.from_bytes(timestamp_bytes, "big")}')
