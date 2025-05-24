from typing import Union, Literal

from paho.mqtt.client import MQTTMessage, Client

from client.service import ClientService
from common.logger import get_logger
from common.types.client_messages import RegisterMessage
from common.types.server_messages import ServerMessage
from common.types.topic import Topic
from common.types.topic_router import TopicRouter
from common.types.with_validation import schema

router = TopicRouter()

class ClientController:
    def __init__(self):
        self.client_service = ClientService()
        self.logger = get_logger("Client:Controller")

    def get_response(self, request_id: str) -> Union[ServerMessage, Literal["Waiting for response"], None]:
        return self.client_service.requests_track.get(request_id)

    def register(self, username: str, address: str) -> str:
        return self.client_service.register(
            username=username,
            address=address,
        )

    # @router.topic(Topic.DISCONNECT.value)
    # @schema(DisconnectMessage)
    # def disconnect(self, data: DisconnectMessage, parts: list[str], msg: MQTTMessage, client: Client) -> None:
    #     self.server_service.disconnect(
    #         request_id=data.request_id,
    #         username=data.username,
    #         address=data.address,
    #         client=client
    #     )
    #
    # @router.topic(Topic.SEND_FILE.value)
    # @schema(SendFileMessage)
    # def handle_send_file(self, data: SendFileMessage, parts: list[str], msg: MQTTMessage, client: Client) -> None:
    #     self.server_service.send_file(
    #         request_id=data.request_id,
    #         from_user=data.from_user,
    #         to_user=data.to_user,
    #         filename=data.filename,
    #         content_base64=data.content_base64,
    #         message=data.message,
    #         client=client
    #     )
    #
    # @router.topic(Topic.SEND_MSG.value)
    # @schema(SendTextMessage)
    # def send_message(self, data: SendTextMessage, parts: list[str], msg: MQTTMessage, client: Client) -> None:
    #     self.server_service.send_message(
    #         request_id=data.request_id,
    #         from_user=data.from_user,
    #         to_user=data.to_user,
    #         message=data.message,
    #         client=client
    #     )
    #
    # @router.topic(Topic.LOOKUP.value)
    # @schema(LookupMessage)
    # def lookup(self, data: LookupMessage, parts: list[str], msg: MQTTMessage, client: Client) -> None:
    #     self.server_service.lookup(
    #         request_id=data.request_id,
    #         requester=data.requester,
    #         target=data.target,
    #         client=client
    #     )