from typing import Optional, Callable

from paho.mqtt.client import Client, MQTTMessage
from client.service import ClientService
from common.logger import get_logger


class ClientController:
    def __init__(self, mqtt_client: Client):
        self.client_service = ClientService(mqtt_client)
        self.logger = get_logger("Client:Controller")

    def register(self, username: str, address: str) -> None:
        self.client_service.register(username, address)

    def disconnect(self, username: str, address: str) -> None:
        self.client_service.disconnect(username, address)

    def send_message(self, from_user: str, to_user: str, message: str) -> None:
        self.client_service.send_message(from_user, to_user, message)

    def send_file(self, from_user: str, to_user: str, filename: str, content_base64: str, message: Optional[str]) -> None:
        self.client_service.send_file(from_user, to_user, content_base64, filename, message)

    def lookup(self, requester: str, target_user: str) -> None:
        self.client_service.lookup(requester, target_user)