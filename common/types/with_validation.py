import json
from functools import wraps
from typing import Callable, Type
from paho.mqtt.client import MQTTMessage, Client
from pydantic import BaseModel, ValidationError

from common.logger import get_logger



from functools import wraps
from pydantic import ValidationError
import json


def schema(model: Type[BaseModel]) -> Callable:
    """
    A decorator to validate `msg.payload` against the given Pydantic model schema and inject parsed data into the function arguments.

    :param model: A Pydantic model class to validate against.
    :return: Decorated function.
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Extract `msg` from args or kwargs
            msg = kwargs.get('msg', None)
            if not msg and len(args) > 0:
                msg = args[-2]  # Assuming `msg` is always the last positional argument.

            if not msg.payload:
                raise ValueError(f"'msg' must have a 'payload' attribute.")

            try:
                # Decode and parse the payload as JSON
                payload_data = json.loads(msg.payload)
                # Validate against the provided Pydantic model
                validated_data = model(**payload_data)
            except (json.JSONDecodeError, ValidationError) as e:
                raise ValueError(f"Validation error occurred: {e}")

            # Add validated data into `kwargs` and also allow `parts` injection if expected
            kwargs['data'] = validated_data

            # Call the wrapped function with updated kwargs
            return func(*args, **kwargs)

        return wrapper

    return decorator
