from typing import Callable, Union
from paho.mqtt.client import MQTTMessage, Client


class TopicRouter:
    def __init__(self):
        self.handlers: dict[str, Callable[[Union['ServerController','ClientController'], MQTTMessage, Client], None]] = {}

    def topic(self, topic: str):
        def decorator(func: Callable[[Union['ServerController','ClientController'], MQTTMessage, Client], None]):
            self.handlers[topic] = func
            return func

        return decorator

    def get(self, topic: str):
        return self.handlers.get(topic)

    @property
    def topics(self):
        return list(self.handlers.keys())