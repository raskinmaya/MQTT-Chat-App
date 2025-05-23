from paho.mqtt.client import Client, MQTTMessage
from common.logger import get_logger
from common.types.client_messages import RegisterMessage, ChatMessage, LookupMessage
from common.types.topic import Topic
from server.engine.utils import topic, schema
from server.service import ClientService

logger = get_logger("Server:Controller")
client_service = ClientService()

@topic(Topic.REGISTER.value)
@schema(RegisterMessage)
def register(data: RegisterMessage, parts: list[str], msg: MQTTMessage, client: Client) -> None:
    client_service.register(data.username, data.address, client)

@topic(Topic.SEND_MSG.value)
@schema(ChatMessage)
def send_message(data: ChatMessage, parts: list[str], msg: MQTTMessage, client: Client) -> None:
    client_service.send_message(data.from_user, data.to_user, data.message, client)

@topic(Topic.LOOKUP.value)
@schema(LookupMessage)
def lookup(data: LookupMessage, parts: list[str], msg: MQTTMessage, client: Client) -> None:
    client_service.lookup(data.requester, data.target, client)
