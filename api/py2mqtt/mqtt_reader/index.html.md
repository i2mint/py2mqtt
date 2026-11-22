# py2mqtt.mqtt_reader

Defines the MQTTTopicReader class

## Classes

| [`MQTTTopicReader`](#py2mqtt.mqtt_reader.MQTTTopicReader)   | Reads messages from an MQTT topic into an internal buffer and exposes a read() interface.   |
|--------------------------------------------------------------------|---------------------------------------------------------------------------------------------|

## Module Contents

### *class* py2mqtt.mqtt_reader.MQTTTopicReader(topic, mqtt_config=None, keepalive=False, max_buffer_len=None)

Bases: `stream2py.source_reader.SourceReader`

Reads messages from an MQTT topic into an internal buffer and exposes a read() interface.

#### info()

A dict with important source info. Default can be init_kwargs and open timestamp.

This info will be available in BufferReader after SourceReader has opened but any changes
made between open and close are not guaranteed to be visible. Any continuous status updates
should be included with read data instead.

* **Returns:**
  dict

#### key(data)

Base sorted case: assume first 64 bits of payload are a timestamp.

#### receive(payload)

Appends an incoming message payload to the read buffer.

If max_buffer_len is set and the read buffer is full, shifts the first value off the buffer.

#### read()

Read the next item, or `None` if nothing is ready.

#### open()

Set up source to be read and set some source info affected by open time like the time of
open. Will be called in StreamBuffer immediately before first read.

#### close()

Close and clean up source reader.
Will be called when StreamBuffer stops or if an exception is raised during read and append
loop.
