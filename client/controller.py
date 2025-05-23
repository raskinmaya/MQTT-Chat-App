from typing import Callable, Optional
from paho.mqtt.client import Client, MQTTMessage
from common.logger import get_logger
from common.types.requests import ChatMessage, LookupMessage, RegisterMessage
from common.types.topic import Topic

logger = get_logger("ClientController")

class ClientController:
    def __init__(self, mqtt_client: Client, username: str, address: str):
        self.client = mqtt_client
        self.username = username
        self.address = address

    def handle_incoming_message(self, client: Client, userdata, msg: MQTTMessage) -> None:
        topic_parts = msg.topic.split('/')
        try:
            raise NotImplementedError
        except Exception as e:
            logger.error(f"Error handling incoming message on {msg.topic}: {e}")

    def register(self) -> None:
        self.client.publish(
            Topic.REGISTER.value,
            RegisterMessage(username=self.username, address=self.address).model_dump_json()
        )

        logger.info(f"Registered client {self.username} with address {self.address}")

    def send_message(self, to_user: str, message: str, timestamp: str) -> None:
        self.client.publish(
            Topic.MESSAGE.value,
            ChatMessage(from_user=self.username, to_user=to_user, message=message, timestamp=timestamp).model_dump_json()
        )

        logger.info(f"Sent message to {to_user}")

    def lookup_user(self, target_user: str) -> None:
        self.client.publish(
            Topic.LOOKUP.value,
            LookupMessage(requester=self.username, target=target_user).model_dump_json()
        )

        logger.info(f"Lookup requested for user {target_user}")