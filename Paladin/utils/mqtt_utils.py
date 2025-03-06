"""
mqtt utils

Test:
    test for https://broker.emqx.io
    broker = "broker.emqx.io"
    port = 1883
    topic = "/python/mqtt"
    client_id = "your client id(unique)"
"""

import random
from typing import Any, Optional

from paho.mqtt import client as mqtt


class MQTTClient(object):

    def __init__(
        self,
        broker: str,
        port: int,
        client_id: str = f"python-mqtt-{random.randint(0, 1000)}",
        username: Optional[str] = None,
        password: Optional[str] = None,
    ):
        super().__init__()
        self.broker = broker
        self.port = port
        self.client_id = client_id
        self.username = username
        self.password = password
        self.client = self.connect_mqtt()
        self.client.on_message = self.on_message

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
                print(f"Failed to connect, return code {mqtt.error_string(reason_code)}")

        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, self.client_id)
        if self.username and self.password:
            client.username_pw_set(self.username, self.password)
        client.on_connect = on_connect
        client.reconnect_delay_set()  # 设置重新连接
        client.connect_async(self.broker, self.port)
        return client

    def publish(self, topic: str, msg: str):
        """发布消息"""
        result = self.client.publish(topic, msg)
        if result.rc == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}, reason code: {mqtt.error_string(result.rc)}")

    def subscribe(self, topic: str):
        """订阅消息"""
        self.client.subscribe(topic)

    def on_message(self, client: mqtt.Client, userdata: Any, msg: mqtt.MQTTMessage):
        # TODO: process message
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
