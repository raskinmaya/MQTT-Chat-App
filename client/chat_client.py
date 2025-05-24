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

    def send_message(self, to_user: str, message: str, timestamp: str) -> None:
        self.controller.send_message(to_user, message, timestamp)

    def lookup(self, target_user: str) -> None:
        self.controller.lookup(target_user)