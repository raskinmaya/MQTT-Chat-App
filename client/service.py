from typing import Literal, Any

from paho.mqtt.client import Client, MQTTMessage
from pydantic import ValidationError

from common.config import MQTT_BROKER, MQTT_PORT
from common.logger import get_logger
from common.types.client_messages import RegisterMessage, ClientMessage
from common.types.server_messages import ServerMessage, ServerAck, ServerError, LookupResponse, ChatMessage
from common.types.topic import Topic


class ClientService:
    def __init__(self):
        self.client = Client()
        self.requests_track: dict[str, ServerMessage | Literal['Waiting for response']] = {}
        self.logger = get_logger("Client:Service")
        self.client.on_message = self.on_message
        self.client.connect(MQTT_BROKER, MQTT_PORT)
    def validate_message(self, payload: bytes, *models: type[ServerMessage]) -> ServerMessage:
        """Validate the payload against multiple models, return the first successful match."""
        for model in models:
            try:
                return model.model_validate_json(payload)
            except ValidationError:
                continue
        raise ValidationError("Payload does not match any expected message type.")

    def on_message(self, client: Client, userdata: Any, msg: MQTTMessage) -> None:
        topic_parts = msg.topic.split('/')
        try:
            topic_to_models = {
                Topic.REGISTER.value: (ServerError, ServerAck),
                Topic.DISCONNECT.value: (ServerError, ServerAck),
                Topic.MSG.value: (ChatMessage,),
                Topic.LOOKUP.value: (ServerError, LookupResponse),
                Topic.SEND_MSG.value: (ServerError, ServerAck),
                Topic.SEND_FILE.value: (ServerError, ServerAck),
            }

            models = topic_to_models.get(topic_parts[0])

            if models:
                data = self.validate_message(msg.payload, *models)
                self.requests_track[data.request_id] = data

            else:
                self.logger.warning("Unknown topic: %s", topic_parts[0])

        except ValidationError as e:
            self.logger.error("Request validation error for topic '%s': %s", topic_parts[0], str(e))

    def register(self, username: str, address: str) -> str:
        register_message = RegisterMessage(
            username=username,
            address=address
        )

        self.requests_track[register_message.request_id] = "Waiting for response"

        self.client.subscribe(f"{Topic.REGISTER.value}/{address}")

        self.client.publish(
            f"{Topic.REGISTER.value}/{address}",
            register_message.model_dump_json()
        )

        return register_message.request_id

