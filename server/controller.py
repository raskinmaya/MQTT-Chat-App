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

    def start_mq_client(self) -> None:
        self.server_service.start_mq_client()

    @router.topic(Topic.REGISTER.value)
    @schema(RegisterMessage)
    def register(self, data: RegisterMessage) -> None:
        self.server_service.register(
            request_id=data.request_id,
            username=data.username,
            address=data.address,
        )

    @router.topic(Topic.DISCONNECT.value)
    @schema(DisconnectMessage)
    def disconnect(self, data: DisconnectMessage) -> None:
        self.server_service.disconnect(
            request_id=data.request_id,
            username=data.username,
            address=data.address,
        )

    @router.topic(Topic.SEND_FILE.value)
    @schema(SendFileMessage)
    def send_file(self, data: SendFileMessage) -> None:
        self.server_service.send_file(
            request_id=data.request_id,
            from_user=data.from_user,
            to_user=data.to_user,
            filename=data.filename,
            content_base64=data.content_base64,
            message=data.message,
        )

    @router.topic(Topic.SEND_MSG.value)
    @schema(SendTextMessage)
    def send_message(self, data: SendTextMessage) -> None:
        self.server_service.send_message(
            request_id=data.request_id,
            from_user=data.from_user,
            to_user=data.to_user,
            message=data.message,
        )

    @router.topic(Topic.LOOKUP.value)
    @schema(LookupMessage)
    def lookup(self, data: LookupMessage) -> None:
        self.server_service.lookup(
            request_id=data.request_id,
            requester=data.requester,
            target=data.target,
        )