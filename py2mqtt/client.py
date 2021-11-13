"""Defines functions to instantiate and access an MQTT client."""

from typing import Callable

import paho.mqtt.client as mqtt

client_dict = {}
subscriptions = {}

def add_subscription(topic: str, handler: Callable):
    subscriptions[topic] = handler

def on_connect(client, userdata, flags, rc):
    print(f'Connected with result code {str(rc)}')
    for topic in subscriptions:
        client.subscribe(topic)

def on_message(client, userdata, msg):
    handler = subscriptions.get(msg.topic)
    if handler:
        handler(msg.payload)

def init_client(hostname='localhost', port=1883, timeout=60, blocking=False, listen=True):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    if blocking:
        client.connect(hostname, port, timeout)
    else:
        client.connect_async(hostname, port, timeout)
    client_dict['client'] = client
    client_dict['blocking'] = blocking
    if listen:
        mqtt_listen()
    return client

def get_client():
    return client_dict.get('client')

def mqtt_listening():
    return client_dict.get('listening')

def get_subscriptions():
    return subscriptions.keys()

def mqtt_listen():
    client = client_dict.get('client')
    if client:
        client_dict['listening'] = True
        if client_dict.get('blocking'):
            print('Listening for MQTT messages until process terminates...')
            client.loop_forever()
        else:
            print('Listening for MQTT messages in a separate thread.')
            client.loop_start()
            return client
    return None

def mqtt_stop_listening():
    client = client_dict.get('client')
    if client:
        client_dict['listening'] = False
        client.loop_stop()
    return None

def publish(topic, payload):
    client = client_dict.get('client')
    client.publish(topic, payload)
