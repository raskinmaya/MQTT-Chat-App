from paho.mqtt.client import Client, MQTTMessage
from common.logger import get_logger
from common.types.client_messages import RegisterMessage, SendTextMessage, LookupMessage, DisconnectMessage, \
    SendFileMessage
from common.types.topic import Topic
from server.engine.utils import topic, schema
from server.service import ClientService

logger = get_logger("Server:Controller")
client_service = ClientService()

@topic(Topic.REGISTER.value)
@schema(RegisterMessage)
def register(data: RegisterMessage, parts: list[str], msg: MQTTMessage, client: Client) -> None:
    client_service.register(data.username, data.address, client)

@topic(Topic.DISCONNECT.value)
@schema(DisconnectMessage)
def disconnect(data: DisconnectMessage, parts: list[str], msg: MQTTMessage, client: Client) -> None:
    client_service.disconnect(data.username, data.address, client)

@topic(Topic.SEND_FILE.value)
@schema(SendFileMessage)
def handle_send_file(data: SendFileMessage, parts: list[str], msg: MQTTMessage, client: Client) -> None:
    client_service.send_file(data, client)

@topic(Topic.SEND_MSG.value)
@schema(SendTextMessage)
def send_message(data: SendTextMessage, parts: list[str], msg: MQTTMessage, client: Client) -> None:
    client_service.send_message(data.from_user, data.to_user, data.message, client)

@topic(Topic.LOOKUP.value)
@schema(LookupMessage)
def lookup(data: LookupMessage, parts: list[str], msg: MQTTMessage, client: Client) -> None:
    client_service.lookup(data.requester, data.target, client)
