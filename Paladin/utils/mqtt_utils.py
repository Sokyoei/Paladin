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
from typing import Any, Optional

from loguru import logger
from paho.mqtt import client as mqtt

TOPIC = "/python/mqtt"


class ClientMode(enum.IntEnum):
    PUBLISH = 0
    SUBSCRIBE = 1


class MQTTClient(object):

    def __init__(
        self,
        broker: str,
        port: int,
        client_mode: ClientMode,
        client_id: str = f"python-mqtt-{random.randint(0, 1000)}",
        username: Optional[str] = None,
        password: Optional[str] = None,
    ):
        super().__init__()
        self.broker = broker
        self.port = port
        self.client_mode = client_mode
        self.client_id = client_id
        self.username = username
        self.password = password
        self.client = self.connect_mqtt()
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        self.client.enable_logger()

    def connect_mqtt(self) -> mqtt.Client:
        """链接 mqtt 服务器"""

        def on_connect(
            client: mqtt.Client,
            userdata: Any,
            flags: mqtt.ConnectFlags,
            reason_code: mqtt.ReasonCode,
            properties: mqtt.Properties,
        ):
            if reason_code == mqtt.MQTT_ERR_SUCCESS:
                logger.info("Connected to MQTT Broker!")
                if self.client_mode == ClientMode.SUBSCRIBE:
                    self.client.subscribe(TOPIC)  # 每次重新连接时都订阅 TOPIC
            else:
                logger.error(f"Failed to connect, reason is: {mqtt.error_string(reason_code)}")

        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, self.client_id)
        if self.username and self.password:
            client.username_pw_set(self.username, self.password)
        client.on_connect = on_connect
        if self.client_mode == ClientMode.SUBSCRIBE:
            client.reconnect_delay_set(max_delay=20)  # 设置重新连接
            client.connect_async(self.broker, self.port)
        elif self.client_mode == ClientMode.PUBLISH:
            client.connect(self.broker, self.port)
        else:
            raise NotImplementedError(f"{self.client_mode} is not implemented.")
        return client

    def publish(self, topic: str, msg: str):
        """发布消息"""
        result = self.client.publish(topic, msg)
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            logger.debug(f"Send `{msg}` to topic `{topic}`")
        else:
            logger.error(f"Failed to send message to topic {topic}, reason is: {mqtt.error_string(result.rc)}")

    def subscribe(self, topic: str):
        """订阅消息"""
        self.client.subscribe(topic)

    def on_message(self, client: mqtt.Client, userdata: Any, msg: mqtt.MQTTMessage):
        # TODO: process message
        logger.info(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    def unsubscribe(self, topic: str):
        rc = self.client.unsubscribe(topic)
        if rc == mqtt.MQTT_ERR_SUCCESS:
            logger.info(f"Unsubscribe {topic}")
        else:
            logger.error(f"Unsubscribe {topic} fail, reason is: {mqtt.error_string(rc)}")

    def on_disconnect(
        self,
        client: mqtt.Client,
        userdata: Any,
        flags: mqtt.ConnectFlags,
        reason_code: mqtt.ReasonCode,
        properties: mqtt.Properties,
    ):
        if reason_code == mqtt.MQTT_ERR_SUCCESS:
            logger.info("Disconnected to MQTT Broker!")
        else:
            logger.error(f"Failed to disconnect, reason is: {mqtt.error_string(reason_code)}")
