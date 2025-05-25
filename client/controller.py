from typing import Union, Literal, Optional
from paho.mqtt.client import MQTTMessage, Client
from client.service import ClientService
from common.logger import get_logger
from common.types.server_messages import ServerMessage
from common.types.topic import Topic
from common.types.topic_router import TopicRouter

router = TopicRouter()

class ClientController:
    def __init__(self):
        self.client_service = ClientService()
        self.logger = get_logger("Client:Controller")

    def run(self):
        self.client_service.run()

    def get_response(self, request_id: str) -> Union[ServerMessage, Literal["Waiting for response"], None]:
        return self.client_service.requests_track.get(request_id)

    #region functions to interact from client gui
    def register(self, username: str, address: str) -> str:
        return self.client_service.register(
            username=username,
            address=address
        )

    def disconnect(self, username: str, address: str) -> str:
        return self.client_service.disconnect(
            username=username,
            address=address
        )

    def send_text_message(self, from_user: str, to_user: str, message: str) -> str:
        return self.client_service.send_text_message(
            from_user=from_user,
            to_user=to_user,
            message=message
        )

    def send_file(self, from_user: str, to_user: str, filename: str,
                  content_base64: str, message: Optional[str] = "") -> str:
        return self.client_service.send_file(
            from_user=from_user,
            to_user=to_user,
            filename=filename,
            content_base64=content_base64,
            message=message
        )

    def lookup(self, requester: str, target: str) -> str:
        return self.client_service.lookup(
            requester=requester,
            target=target
        )
    #endregion

    #region functions to handle messages received on mq
    @router.topic(Topic.REGISTER.value)
    def handle_register_response(self, msg: MQTTMessage) -> None:
        raise NotImplementedError

    @router.topic(Topic.DISCONNECT.value)
    def handle_disconnect_response(self, msg: MQTTMessage) -> None:
        raise NotImplementedError

    @router.topic(Topic.SEND_MSG.value)
    def handle_send_txt_msg_response(self, msg: MQTTMessage) -> None:
        raise NotImplementedError

    @router.topic(Topic.SEND_FILE.value)
    def handle_send_file_response(self, msg: MQTTMessage) -> None:
        raise NotImplementedError

    @router.topic(Topic.LOOKUP.value)
    def handle_lookup_response(self, msg: MQTTMessage) -> None:
        raise NotImplementedError

    @router.topic(Topic.MSG.value)
    def handle_message_received(self, msg: MQTTMessage) -> None:
        raise NotImplementedError
    #endregion