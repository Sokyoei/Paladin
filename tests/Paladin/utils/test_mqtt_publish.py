import time

from Paladin.utils import MQTTClient
from Paladin.utils.mqtt_utils import ClientMode

BROKER = "broker.emqx.io"
PORT = 1883
TOPIC = "/python/mqtt"
CLIENT_ID = "mqtt_publish"


def main():
    n = 0
    client = MQTTClient(BROKER, PORT, ClientMode.PUBLISH, CLIENT_ID)
    while True:
        client.publish(TOPIC, str(n))
        time.sleep(1)
        n += 1


if __name__ == '__main__':
    main()
