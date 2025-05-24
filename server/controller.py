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
    # @schema(RegisterMessage)
    def register(self, msg: MQTTMessage, client: Client) -> None:
        data = RegisterMessage.model_validate_json(msg.payload)

        self.server_service.register(
            request_id=data.request_id,
            username=data.username,
            address=data.address,
            client=client
        )

    @router.topic(Topic.DISCONNECT.value)
    # @schema(DisconnectMessage)
    def disconnect(self, msg: MQTTMessage, client: Client) -> None:
        data = DisconnectMessage.model_validate_json(msg.payload)

        self.server_service.disconnect(
            request_id=data.request_id,
            username=data.username,
            address=data.address,
            client=client
        )

    @router.topic(Topic.SEND_FILE.value)
    # @schema(SendFileMessage)
    def handle_send_file(self, msg: MQTTMessage, client: Client) -> None:
        data = SendFileMessage.model_validate_json(msg.payload)

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
    # @schema(SendTextMessage)
    def send_message(self, msg: MQTTMessage, client: Client) -> None:
        data = SendTextMessage.model_validate_json(msg.payload)

        self.server_service.send_message(
            request_id=data.request_id,
            from_user=data.from_user,
            to_user=data.to_user,
            message=data.message,
            client=client
        )

    @router.topic(Topic.LOOKUP.value)
    # @schema(LookupMessage)
    def lookup(self, msg: MQTTMessage, client: Client) -> None:
        data = LookupMessage.model_validate_json(msg.payload)

        self.server_service.lookup(
            request_id=data.request_id,
            requester=data.requester,
            target=data.target,
            client=client
        )