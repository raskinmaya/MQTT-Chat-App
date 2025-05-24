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
        self.controller = ClientController(self.client)

    def on_connect(self, client: Client, userdata: Any, flags: dict, rc: int) -> None:
        self.controller.register(self.username, self.address)

    def on_registration_complete(self) -> None:
        logger.info(f"Connecting client {self.username} to broker {MQTT_BROKER}:{MQTT_PORT}")
        self.client.connect(MQTT_BROKER, MQTT_PORT)
        self.client.loop_start()

    def disconnect(self) -> None:
        self.controller.disconnect(username=self.username, address=self.address)

    def send_message(self, to_user: str, message: str) -> None:
        self.controller.send_message(from_user=self.username, to_user=to_user, message=message)

    def lookup(self, target_user: str) -> None:
        self.controller.lookup(requester=self.username, target_user=target_user)