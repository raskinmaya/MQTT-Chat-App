from paho.mqtt.client import Client, MQTTMessage
from common.logger import get_logger
from common.types.client_messages import RegisterMessage, SendTextMessage, LookupMessage, DisconnectMessage, \
    SendFileMessage
from common.types.topic import Topic
from server.engine.utils import topic, schema
from server.service import ServerService


class ServerController:
    def __init__(self):
        self.server_service = ServerService()
        self.logger = get_logger("Server:Controller")

    @topic(Topic.REGISTER.value)
    @schema(RegisterMessage)
    def register(self, data: RegisterMessage, parts: list[str], msg: MQTTMessage, client: Client) -> None:
        self.server_service.register(data.username, data.address, client)

    @topic(Topic.DISCONNECT.value)
    @schema(DisconnectMessage)
    def disconnect(self, data: DisconnectMessage, parts: list[str], msg: MQTTMessage, client: Client) -> None:
        self.server_service.disconnect(data.username, data.address, client)

    @topic(Topic.SEND_FILE.value)
    @schema(SendFileMessage)
    def handle_send_file(self, data: SendFileMessage, parts: list[str], msg: MQTTMessage, client: Client) -> None:
        self.server_service.send_file(data, client)

    @topic(Topic.SEND_MSG.value)
    @schema(SendTextMessage)
    def send_message(self, data: SendTextMessage, parts: list[str], msg: MQTTMessage, client: Client) -> None:
        self.server_service.send_message(data.from_user, data.to_user, data.message, client)

    @topic(Topic.LOOKUP.value)
    @schema(LookupMessage)
    def lookup(self, data: LookupMessage, parts: list[str], msg: MQTTMessage, client: Client) -> None:
        self.server_service.lookup(data.requester, data.target, client)

server_controller = ServerController()