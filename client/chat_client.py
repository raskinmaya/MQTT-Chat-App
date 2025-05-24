from paho.mqtt.client import Client
from client.controller import ClientController
from common.config import MQTT_BROKER, MQTT_PORT
from common.logger import get_logger
from typing import Any, Optional


class ChatClient:
    def __init__(self, username: str, address: str):
        self.username = username
        self.address = address
        self.client = Client(client_id=username)
        self.controller = ClientController(self.client)
        self.logger = get_logger("Chat:Client")

    def try_register(self, client: Client, userdata: Any, flags: dict, rc: int) -> None:
        self.controller.register(self.username, self.address)

    def try_disconnect(self) -> None:
        self.controller.disconnect(username=self.username, address=self.address)

    def try_send_message(self, to_user: str, message: str) -> None:
        self.controller.send_message(from_user=self.username, to_user=to_user, message=message)

    def try_send_file(self, to_user: str, filename: str, content_base64: str, message: Optional[str]) -> None:
        self.controller.send_file(from_user=self.username, to_user=to_user, filename=filename, content_base64=content_base64, message=message)

    def try_lookup(self, target_user: str) -> None:
        self.controller.lookup(requester=self.username, target_user=target_user)