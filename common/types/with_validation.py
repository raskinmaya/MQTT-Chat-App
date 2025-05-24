from functools import wraps
from paho.mqtt.client import MQTTMessage
from typing import Type, Callable

from pydantic import BaseModel


def schema(message_cls: Type[BaseModel]):
    """
    Decorator to transform 'msg.payload' into a validated model instance (data)
    and pass it as an argument to the original function.
    """

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(self, msg: MQTTMessage, client, *args, **kwargs):
            # Validate and parse the MQTTMessage payload using the provided schema
            try:
                data = message_cls.model_validate_json(msg.payload)
            except Exception as e:  # Handle validation errors gracefully
                raise ValueError(f"Invalid payload for {message_cls.__name__}: {str(e)}")

            # Call the original function with the transformed arguments
            return func(self, data, client, *args, **kwargs)

        return wrapper

    return decorator
