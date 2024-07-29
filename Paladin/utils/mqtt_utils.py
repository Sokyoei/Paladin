"""
mqtt utils

Test:
    test for https://broker.emqx.io
    broker = "broker.emqx.io"
    port = 1883
    topic = "/python/mqtt"
    client_id = "your client id(unique)"
"""

import enum
import random
import threading
import time
from typing import Any

from paho.mqtt import client as mqtt


class MQTTType(enum.IntEnum):
    PUBLISH = 1
    SUBSCRIBE = 2


class MQTTManager(threading.Thread):

    def __init__(
        self,
        mqtt_type: MQTTType,
        broker: str,
        port: int,
        topic: str,
        client_id: str = f"python-mqtt-{random.randint(0, 1000)}",
    ):
        super().__init__()
        self.mqtt_type = mqtt_type
        self.broker = broker
        self.port = port
        self.topic = topic
        self.client_id = client_id
        self.client = self.connect_mqtt()

    def run(self):
        if self.mqtt_type == MQTTType.PUBLISH:
            self.client.loop_start()
            self.publish()
        elif self.mqtt_type == MQTTType.SUBSCRIBE:
            self.subscribe()
            self.client.loop_forever()

    def connect_mqtt(self) -> mqtt.Client:
        """链接 mqtt 服务器"""

        def on_connect(
            client: mqtt.Client,
            userdata: Any,
            flags: mqtt.ConnectFlags,
            reason_code: mqtt.ReasonCode,
            properties: mqtt.Properties,
        ):
            if reason_code == 0:
                print("Connected to MQTT Broker!")
            else:
                print(f"Failed to connect, return code {reason_code}")

        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, self.client_id)
        # client.username_pw_set(username=username, password=password)
        client.on_connect = on_connect
        client.connect(self.broker, self.port)
        return client

    def publish(self):
        """发布消息"""
        msg_count = 0
        while True:
            time.sleep(1)
            msg = f"messages: {msg_count}"
            result = self.client.publish(self.topic, msg)
            if result.rc == 0:
                print(f"Send `{msg}` to topic `{self.topic}`")
            else:
                print(f"Failed to send message to topic {self.topic}, reason code: {result.rc}")
            msg_count += 1

    def subscribe(self):
        """订阅消息"""

        def on_message(client: mqtt.Client, userdata: Any, msg: mqtt.MQTTMessage):
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

        self.client.subscribe(self.topic)
        self.client.on_message = on_message
