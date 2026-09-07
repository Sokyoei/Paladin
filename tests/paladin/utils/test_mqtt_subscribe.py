from paladin.utils import MQTTClient
from paladin.utils.mqtt_utils import ClientMode

BROKER = "broker.emqx.io"
PORT = 1883
TOPIC = "/python/mqtt"
CLIENT_ID = "mqtt_subscribe"


def main():
    client = MQTTClient(BROKER, PORT, ClientMode.SUBSCRIBE, CLIENT_ID)
    client.subscribe(TOPIC)
    client.client.loop_forever(retry_first_connection=True)


if __name__ == '__main__':
    main()
