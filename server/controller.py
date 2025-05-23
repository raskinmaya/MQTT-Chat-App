import json

from paho.mqtt.client import Client, MQTTMessage
from pydantic import ValidationError

from common.logger import get_logger
from common.types.requests import RegisterMessage, ChatMessage, LookupMessage
from common.types.topic import Topic
from server.engine.utils import topic_handler
from server.service import ClientService

logger = get_logger("Server:Controller")
client_service = ClientService()

@topic_handler(Topic.REGISTER.value)
def handle_register(parts: list[str], msg: MQTTMessage, client: Client) -> None:
    try:
        data = RegisterMessage.model_validate_json(msg.payload)
        client_service.register(data.username, data.address, client)
    except ValidationError as e:
        logger.error(f"Register validation error: {e}")
        client.publish(Topic.REGISTER.value, json.dumps({"error": str(e)}))

@topic_handler(Topic.MESSAGE.value)
def handle_send(parts: list[str], msg: MQTTMessage, client: Client) -> None:
    try:
        data = ChatMessage.model_validate_json(msg.payload)
        client_service.route_message(data.to_user, data.model_dump(), client)
    except ValidationError as e:
        logger.error(f"Send validation error: {e}")
        client.publish(Topic.MESSAGE.value, json.dumps({"error": str(e)}))

@topic_handler(Topic.LOOKUP.value)
def handle_lookup(parts: list[str], msg: MQTTMessage, client: Client) -> None:
    try:
        data = LookupMessage.model_validate_json(msg.payload)
        client_service.handle_lookup(data.requester, data.target, client)
    except ValidationError as e:
        logger.error(f"Lookup validation error: {e}")
        client.publish(Topic.LOOKUP.value, json.dumps({"error": str(e)}))
