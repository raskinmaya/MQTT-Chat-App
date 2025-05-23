import json

from paho.mqtt.client import Client, MQTTMessage
from common.logger import get_logger
from common.types.client_messages import RegisterMessage, ChatMessage, LookupMessage
from common.types.exceptions import UsernameTaken, UserNotFound
from common.types.topic import Topic
from server.engine.utils import topic_handler, with_validation
from server.service import ClientService

logger = get_logger("Server:Controller")
client_service = ClientService()

@topic_handler(Topic.REGISTER.value)
@with_validation(RegisterMessage)
def handle_register(data: RegisterMessage, parts: list[str], msg: MQTTMessage, client: Client) -> None:
    client_service.register(data.username, data.address, client)

@topic_handler(Topic.SEND_MSG.value)
@with_validation(ChatMessage)
def handle_send(data: ChatMessage, parts: list[str], msg: MQTTMessage, client: Client) -> None:
    client_service.route_message(data.from_user, data.to_user, data.model_dump(), client)

@topic_handler(Topic.LOOKUP.value)
@with_validation(LookupMessage)
def handle_lookup(data: LookupMessage, parts: list[str], msg: MQTTMessage, client: Client) -> None:
    client_service.handle_lookup(data.requester, data.target, client)
