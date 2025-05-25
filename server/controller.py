from typing import Callable

from paho.mqtt.client import Client, MQTTMessage
from common.logger import get_logger
from common.types.client_messages import RegisterMessage, SendTextMessage, LookupMessage, DisconnectMessage, \
    SendFileMessage
from common.types.topic import Topic
from common.types.topic_router import TopicRouter
from common.types.with_validation import schema
from server.service import ServerService

router = TopicRouter()

class ServerController:
    def __init__(self):
        self.server_service = ServerService()
        self.logger = get_logger("Server:Controller")

    @router.topic(Topic.REGISTER.value)
    @schema(RegisterMessage)
    def register(self, data: RegisterMessage, client: Client) -> None:
        self.server_service.register(
            request_id=data.request_id,
            username=data.username,
            address=data.address,
            client=client
        )

    @router.topic(Topic.DISCONNECT.value)
    @schema(DisconnectMessage)
    def disconnect(self, data: DisconnectMessage, client: Client) -> None:
        self.server_service.disconnect(
            request_id=data.request_id,
            username=data.username,
            address=data.address,
            client=client
        )

    @router.topic(Topic.SEND_FILE.value)
    @schema(SendFileMessage)
    def send_file(self, data: SendFileMessage, client: Client) -> None:
        self.server_service.send_file(
            request_id=data.request_id,
            from_user=data.from_user,
            to_user=data.to_user,
            filename=data.filename,
            content_base64=data.content_base64,
            message=data.message,
            client=client
        )

    @router.topic(Topic.SEND_MSG.value)
    @schema(SendTextMessage)
    def send_message(self, data: SendTextMessage, client: Client) -> None:
        self.server_service.send_message(
            request_id=data.request_id,
            from_user=data.from_user,
            to_user=data.to_user,
            message=data.message,
            client=client
        )

    @router.topic(Topic.LOOKUP.value)
    @schema(LookupMessage)
    def lookup(self, data: LookupMessage, client: Client) -> None:
        self.server_service.lookup(
            request_id=data.request_id,
            requester=data.requester,
            target=data.target,
            client=client
        )