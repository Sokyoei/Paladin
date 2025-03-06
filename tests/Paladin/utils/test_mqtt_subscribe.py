from Paladin.utils import MQTTClient

broker = "broker.emqx.io"
port = 1883
topic = "/python/mqtt"
client_id = "mqtt_subscribe"


def main():
    client = MQTTClient(broker, port, client_id)
    client.subscribe(topic)
    client.client.loop_forever(retry_first_connection=True)


if __name__ == '__main__':
    main()
