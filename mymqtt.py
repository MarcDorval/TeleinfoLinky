#!/usr/bin/python3

from paho.mqtt import client as mqtt_client

class myMqtt():
    """
        contains basic MQTT resources
    """
    client_id = ""
    broker = ""
    port = 1883

    def __init__(self, client_id):
        self.client_id = client_id
        self.client = mqtt_client.Client(client_id)
        print(self.client)

    def on_connect(self, mqtt_client_id, userdata, flags, rc):
        if rc == 0:
            print(f"Connected to MQTT Broker {self.broker}!")
        else:
            print(f"Failed to connect to MQTT Broker {self.broker}, return code %d\n", rc)

    def on_socket_open(self):
        print(f"socket open")

    def on_socket_close(self):
        print(f"socket close")

    def connect_to(self, broker, port=1883):
        self.client.connect(broker, port, keepalive=60)

    def disconnect(self):
        self.client.disconnect()

    def on_message(self, c, userdata, msg):
        print(userdata)
        print(msg)
        print(f"< {msg.topic}: {msg.payload.decode()}")

    def on_log(self, userdata, level, buf):
        print("log: ", buf)

    def subscribe(self, topics, qos=1):
        self.client.subscribe(topics, qos)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_socket_open = self.on_socket_open
        self.client.on_socket_close = self.on_socket_close
        self.client.onlog = self.on_log

    def publish(self, topic, msg, qos=1, retain=True):
        result = self.client.publish(topic, msg, retain)
        status = result[0]
        if status == 0:
            print(f"{self.client_id} > {topic}: {msg}")
        else:
            print(f"Failed to send message to topic {topic}")

    def listen(self):
        self.client.loop_forever(timeout=1.0)

    def deaf(self):
        self.client.loop_stop()

