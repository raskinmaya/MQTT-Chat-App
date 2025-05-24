from typing import Callable
from paho.mqtt.client import MQTTMessage, Client


class TopicRouter:
    def __init__(self):
        self.handlers: dict[str, Callable[['ServerController', MQTTMessage, Client], None]] = {}

    def topic(self, topic: str):
        """
        Decorator for registering handler functions for specific MQTT topics.

        Args:
            topic (str): The MQTT topic pattern to register the handler for

        Returns:
            callable: The decorator function
        """

        def decorator(func: Callable[['ServerController', MQTTMessage, Client], None]):
            self.handlers[topic] = func
            return func

        return decorator

    def get(self, topic: str):
        return self.handlers.get(topic)

    @property
    def topics(self):
        return list(self.handlers.keys())