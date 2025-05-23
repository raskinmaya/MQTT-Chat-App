import json
from typing import Callable, Type
from paho.mqtt.client import MQTTMessage, Client
from pydantic import BaseModel, ValidationError
from server.controller import logger
from server.engine.core import handlers

def topic_handler(topic: str) -> Callable:
    def decorator(func: Callable[[list[str], MQTTMessage, Client], None]) -> Callable:
        handlers[topic] = func
        return func

    return decorator

def with_validation(model: Type[BaseModel]):
    def decorator(func: Callable[[BaseModel, list[str], Client], None]):
        def wrapper(parts: list[str], msg: MQTTMessage, client: Client):
            try:
                data = model.model_validate_json(msg.payload)
                func(data, parts, client)
            except ValidationError as e:
                logger.error("Request validation error: %s", str(e))
                client.publish("error/validation", json.dumps({"error": e.errors()}))
        return wrapper
    return decorator