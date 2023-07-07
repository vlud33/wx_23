import paho.mqtt.client as mqtt
import numpy as np

class MQTTClient(mqtt.Client):
    def __init__(self, topic_name, *args, **kwargs):
        self.msg_data = None
        super().__init__(*args, **kwargs)
        self.topic_name = topic_name
        
    def on_connect(self, client, userdata, flags, rc):
        self.subscribe(self.topic_name)

    # def on_disconnect(self, client, userdata, rc):
        # pass

    def get_data(self):
        return self.msg_data

    def on_message(self, client, userdata, message):
        client.subscribe(self.topic_name)
        msg_byte = message.payload
        msg_decode = np.frombuffer(msg_byte, dtype=float, count=-1, offset=0)
        self.msg_data = np.reshape(msg_decode, (40, 2200))
        self.loop_stop()

