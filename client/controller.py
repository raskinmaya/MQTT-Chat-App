from typing import Optional

from paho.mqtt.client import MQTTMessage, Client

from client.service import ClientService
from common.logger import get_logger
from common.types.server_messages import ServerError, ServerAck
from common.types.topic import Topic
from common.types.topic_router import TopicRouter

router = TopicRouter()
class ClientController:
    def __init__(self):
        self.client_service = ClientService()
        self.logger = get_logger("Client:Controller")

    def register(self, username: str, address: str) -> None:
        self.client_service.register(username, address)

    @router.topic(Topic.REGISTER.value)
    def on_register_response(self, data: ServerAck | ServerError, parts: list[str], msg: MQTTMessage, client: Client) -> None:
        self.client_service.on_register_response(data)

    def disconnect(self, username: str, address: str) -> None:
        self.client_service.disconnect(username, address)

    def send_message(self, from_user: str, to_user: str, message: str) -> None:
        self.client_service.send_message(from_user, to_user, message)

    def send_file(self, from_user: str, to_user: str, filename: str, content_base64: str, message: Optional[str]) -> None:
        self.client_service.send_file(from_user, to_user, content_base64, filename, message)

    def lookup(self, requester: str, target_user: str) -> None:
        self.client_service.lookup(requester, target_user)