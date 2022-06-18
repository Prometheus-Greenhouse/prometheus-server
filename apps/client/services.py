from paho.mqtt.client import Client, MQTTMessage

from database.base import get_session
from database.models import SensorRecord
from database.repositories.sensor_record import SensorRecordRepos


class ClientService(Client):
    def __init__(self):
        super().__init__()
        self.repos = SensorRecordRepos(session=get_session().__next__())

    def on_temperature(self, msg: MQTTMessage):
        record = SensorRecord(
            farm_id=1,
            green_house_id=1,
            sensor_id=1,
            sensor_data=str(float(msg.payload))
        )
        self.repos.insert(record)
        self.repos.session.commit()

    @staticmethod
    def run():
        client = ClientService()
        client.connect("localhost", 1883, 60)
        client.subscribe("Room/humidity")
        client.subscribe("Room/temperature")

        @client.connect_callback()
        def on_connect(client, userdata, flags, rc):
            print("Connection returned " + str(rc))

        @client.message_callback()
        def on_message(userdata, msg, args):
            print(f"Received `{msg.payload}` from `{msg.topic}` topic")

            if msg.topic == "Room/temperature":
                client.on_temperature(msg)

        client.loop_forever()
