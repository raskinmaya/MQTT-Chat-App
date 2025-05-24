from typing import Optional, Any
from paho.mqtt.client import Client
from client.engine.core import on_message, on_connect
from common.config import MQTT_BROKER, MQTT_PORT
from common.logger import get_logger
from common.types.client_messages import LookupMessage, SendTextMessage, RegisterMessage, SendFileMessage, \
    DisconnectMessage
from common.types.server_messages import ServerError, ServerAck
from common.types.topic import Topic


class ClientService:
    def __init__(self):
        self.client = Client()
        self.username = ""
        self.address = ""

        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.logger = get_logger("Client:Service")

    def register(self, username: str, address: str) -> None:
        self.username = username
        self.address = address

        self.client.publish(
            Topic.REGISTER.value,
            RegisterMessage(username=username, address=address).model_dump_json()
        )

        self.logger.info(f"Attempting register client {username} with address {address}")

    def on_register_response(self, data: ServerAck | ServerError) -> None:
        if isinstance(data, ServerError):
            self.on_registration_failed(data.username, data.reason)

        else:
            self.on_registration_complete(data.username)

    def on_registration_failed(self, username: str, reason: str) -> None:
        self.logger.info(f"Registration failed for user {username}, reason: {reason}")
        print(f"Registration failed for user {username}, reason: {reason}")

    def on_registration_complete(self, username: str) -> None:
        self.logger.info(f"Connecting client {username} to broker {MQTT_BROKER}:{MQTT_PORT}")
        self.client.connect(MQTT_BROKER, MQTT_PORT)
        self.client.loop_start()

    def disconnect(self, username: str, address: str) -> None:
        self.client.publish(
            Topic.DISCONNECT.value,
            DisconnectMessage(username=username, address=address).model_dump_json()
        )

        self.logger.info(f"Attempting disconnect for user {username}")

    def on_disconnect_complete(self, username: str):
        self.client.loop_stop()
        self.client.disconnect()
        self.logger.info(f"Disconnected user {username}")

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