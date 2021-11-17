import os
from time import sleep

import pyaudio


from py2mqtt.examples.mqtt_writer import MQTTTopicWriter
from py2mqtt import sample_data_dir_path
from py2mqtt.examples.mqtt_reader import MQTTTopicReader
from stream2py.stream_buffer import StreamBuffer
from strand import MultiprocessTaskrunner
# from py2mqtt.examples.mqtt_pcm_buffer import MQTTPCMBuffer

TOPIC = 'test_topic'

def run_writer():
    sleep(2)

    # Enter a filename with PCM data (or use this default one)
    # For this demo, should be 16-bit, 2 channels, 44100 Hz
    src_wav_filepath = os.path.join(sample_data_dir_path, 'drumloop.wav')

    topic = 'test_topic'
    chk_size = 2048  # you may modify these values
    n_chunks = 1000
    with open(src_wav_filepath, 'rb') as fp:
        writer = MQTTTopicWriter(topic, fp)
        for i in range(n_chunks):
            writer.push(fp.read(chk_size))

def mqtt_stream_playback_demo(width=2, channels=2, sr=44100):
    device_simulator = MultiprocessTaskrunner(run_writer)
    device_simulator()
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
        storage_reader = buffer.mk_reader()
        for message_payload in playback_reader:
            pcm_bytes = message_payload[8:]
            play_stream.write(pcm_bytes)
            timestamp_bytes = message_payload[:8]
            print(f'received chunk with timestamp {int.from_bytes(timestamp_bytes, "big")}')

if __name__ == '__main__':
    mqtt_stream_playback_demo()
