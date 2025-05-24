from typing import Optional

from paho.mqtt.client import Client

from common.logger import get_logger
from common.types.client_messages import LookupMessage, SendTextMessage, RegisterMessage, SendFileMessage, \
    DisconnectMessage
from common.types.topic import Topic


class ClientService:
    def __init__(self, mqtt_client: Client):
        self.client = mqtt_client
        self.logger = get_logger("Client:Service")

    def register(self, username: str, address: str) -> None:
        self.client.publish(
            Topic.REGISTER.value,
            RegisterMessage(username=username, address=address).model_dump_json()
        )

        self.logger.info(f"Attempting register client {username} with address {address}")

    def disconnect(self, username: str, address: str) -> None:
        self.client.publish(
            Topic.DISCONNECT.value,
            DisconnectMessage(username=username, address=address).model_dump_json()
        )

        self.logger.info(f"Attempting disconnect for user {username}")

    def send_message(self, from_user: str, to_user: str, message: str) -> None:
        self.client.publish(
            Topic.SEND_MSG.value,
            SendTextMessage(from_user=from_user, to_user=to_user, message=message).model_dump_json()
        )

        self.logger.info(f"Attempting to send message to user {to_user}")

    def send_file(self, from_user: str, to_user: str, content_base64: str, filename: str, message: Optional[str]) -> None:
        self.client.publish(
            Topic.SEND_FILE.value,
            SendFileMessage(from_user=from_user, to_user=to_user, filename=filename, content_base64=content_base64, message=message).model_dump_json()
        )

        self.logger.info(f"Attempting to send file message to user {to_user}")

    def lookup(self, requester: str, target: str) -> None:
        self.client.publish(
            Topic.LOOKUP.value,
            LookupMessage(requester=requester, target=target).model_dump_json()
        )

        self.logger.info(f"Lookup requested for user {target}")