"""
Subscribe to a topic on an mqtt broker

Will run a loop
"""

import threading
import random

from paho.mqtt import client as mqtt_client


#broker = 'broker.emqx.io'
broker = '192.168.1.31'  # raspberry Pi at home running mosquito
port = 1883
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = ''
password = ''


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    #client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client, topic : str):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message

    print('subscribe:', topic)

def run():
    client = connect_mqtt()

    topic = "classroom/pythonscript"
    subscribe(client, topic)

    topic = "classroom/pushbutton1"
    subscribe(client, topic)

    #
    client.loop_forever()
    #client.loop_start()


if __name__ == '__main__':
    #run()
    sub=threading.Thread(target=run)
    sub.start()