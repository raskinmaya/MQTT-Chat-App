from functools import wraps
from paho.mqtt.client import MQTTMessage
from typing import Type, Callable
from pydantic import BaseModel, ValidationError
from common.types.client_messages import ClientMessage
from common.types.server_messages import ServerMessage, ServerError, ServerAck, ChatMessage, LookupResponse
from common.types.topic import ClientMessageTopic, ServerMessageTopic


def schema(message_cls: Type[BaseModel]):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(self, msg: MQTTMessage, *args, **kwargs):
            # Validate and parse the MQTTMessage payload using the provided schema
            try:
                data = message_cls.model_validate_json(msg.payload)
            except Exception as e:  # Handle validation errors gracefully
                raise ValueError(f"Invalid payload for {message_cls.__name__}: {str(e)}")

            # Call the original function with the transformed arguments
            return func(self, data, *args, **kwargs)

        return wrapper

    return decorator

expected_response_types_for_topic = {
                ServerMessageTopic.REGISTER_RESPONSE.value: (ServerError, ServerAck),
                ServerMessageTopic.DISCONNECT_RESPONSE.value: (ServerError, ServerAck),
                ServerMessageTopic.MSG.value: (ChatMessage,),
                ServerMessageTopic.LOOKUP_RESPONSE.value: (ServerError, LookupResponse),
                ServerMessageTopic.SEND_MSG_RESPONSE.value: (ServerError, ServerAck),
                ServerMessageTopic.SEND_FILE_RESPONSE.value: (ServerError, ServerAck),
}

def validate_message(
        payload: bytes,
        *models: type[ServerMessage | ClientMessage]
) -> ServerMessage:
    """Validate the payload against multiple models, return the first successful match."""
    for model in models:
        try:
            return model.model_validate_json(payload)
        except ValidationError:
            continue
    raise ValidationError("Payload does not match any expected message type.")