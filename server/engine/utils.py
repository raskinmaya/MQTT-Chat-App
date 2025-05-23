from typing import Callable
from paho.mqtt.client import MQTTMessage, Client
from server.engine.core import handlers

def topic_handler(topic: str) -> Callable:
    def decorator(func: Callable[[list[str], MQTTMessage, Client], None]) -> Callable:
        handlers[topic] = func
        return func

    return decorator