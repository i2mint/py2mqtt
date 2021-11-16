# py2mqtt
Interfaces for Python to transmit, receive, and act on data over an MQTT connection.

To install:	```pip install py2mqtt```.
If running from source, you must install `paho-mqtt` and `stream2py`.

You must also have access to an MQTT broker (usually on localhost).

## Installing an MQTT broker on OS X

https://formulae.brew.sh/formula/mosquitto

```bash
$ brew install mosquitto

$ brew services start mosquitto
```

## Audio playback demo

1. Ensure you have `pyaudio` installed. If not: `pip install pyaudio` + some system installs (http://people.csail.mit.edu/hubert/pyaudio/). 
2. Run the file `py2mqtt/examples/mqtt_pcm_stream_playback.py`.
3. Run the data producer code in a separate process:

```python
from py2mqtt.examples.mqtt_writer import MQTTTopicWriter

# Enter a filename with PCM data (or use this default one)
# For this demo, should be 16-bit, 1 channel, 44100 Hz
import importlib_resources, py2mqtt
src_wav_filepath = str(importlib_resources.files(py2mqtt) / 'sample_data' / 'drumloop.wav')

topic = 'test_topic'
chk_size = 2048  # you may modify these values
n_chunks = 1000
with open(src_wav_filepath, 'rb') as fp:
    writer = MQTTTopicWriter(topic, fp)
    for i in range(n_chunks):
        writer.push(fp.read(chk_size))
```

You should hear the WAV file played back after being chunked, passed through the MQTT broker as a series of messages, and reassembled by the reader.
