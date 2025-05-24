import json
from typing import Callable, Type
from paho.mqtt.client import MQTTMessage, Client
from pydantic import BaseModel, ValidationError

from common.logger import get_logger

def schema(model: Type[BaseModel]):
    def decorator(func: Callable[[BaseModel, list[str], Client], None]):
        def wrapper(parts: list[str], msg: MQTTMessage, client: Client):
            try:
                data = model.model_validate_json(msg.payload)
                func(data, parts, client)
            except ValidationError as e:
                get_logger("SchemaValidation").error("Request validation error: %s", str(e))
                client.publish("error/validation", json.dumps({"error": e.errors()}))
        return wrapper
    return decorator