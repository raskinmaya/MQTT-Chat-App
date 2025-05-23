from paho.mqtt.client import Client
from client.controller import ClientController
from common.config import MQTT_BROKER, MQTT_PORT
from common.logger import get_logger
from typing import Any

from common.types.topic import Topic

logger = get_logger("ChatClient")

class ChatClient:
    def __init__(self, username: str, address: str):
        self.username = username
        self.address = address
        self.client = Client(client_id=username)
        self.controller = ClientController(self.client, username, address)

        self.client.on_connect = self.on_connect
        self.client.on_message = self.controller.handle_incoming_message

    def on_connect(self, client: Client, userdata: Any, flags: dict, rc: int) -> None:
        logger.info(f"Connected to MQTT broker with result code {rc}")
        client.subscribe(f"{Topic.MSG.value}/{self.username}")
        client.subscribe(f"{Topic.LOOKUP.value}/{self.username}")
        self.controller.register()

    def connect(self) -> None:
        logger.info(f"Connecting client {self.username} to broker {MQTT_BROKER}:{MQTT_PORT}")
        self.client.connect(MQTT_BROKER, MQTT_PORT)
        self.client.loop_start()

    def disconnect(self) -> None:
        self.client.loop_stop()
        self.client.disconnect()
        logger.info(f"Disconnected client {self.username}")

    # Helper methods to interact with controller
    def send_message(self, to_user: str, message: str, timestamp: str) -> None:
        self.controller.send_message(to_user, message, timestamp)

    def lookup_user(self, target_user: str) -> None:
        self.controller.lookup_user(target_user)