import time

from Paladin.utils import MQTTClient

broker = "broker.emqx.io"
port = 1883
topic = "/python/mqtt"
client_id = "mqtt_publish"


def main():
    n = 0
    client = MQTTClient(broker, port, client_id)
    while True:
        client.publish(topic, str(n))
        time.sleep(1)
        n += 1


if __name__ == '__main__':
    main()
