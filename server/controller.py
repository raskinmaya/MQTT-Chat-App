from paho.mqtt.client import Client, MQTTMessage
from common.messages import RegisterMessage, ChatMessage, LookupMessage
from server.engine.utils import topic_handler
from server.service import ClientService

client_service = ClientService()

@topic_handler("register")
def handle_register(parts: list[str], msg: MQTTMessage, client: Client) -> None:
    data = RegisterMessage.model_validate_json(msg.payload)
    client_service.register(data.username, data.address, client)

@topic_handler("send")
def handle_send(parts: list[str], msg: MQTTMessage, client: Client) -> None:
    message = ChatMessage.model_validate_json(msg.payload)
    client_service.route_message(message.to_user, message.model_dump(), client)

@topic_handler("lookup")
def handle_lookup(parts: list[str], msg: MQTTMessage, client: Client) -> None:
    data = LookupMessage.model_validate_json(msg.payload)
    client_service.handle_lookup(data.requester, data.target, client)
