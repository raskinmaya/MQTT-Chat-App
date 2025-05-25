import os
from collections.abc import Callable
from typing import Any
from paho.mqtt.client import Client, MQTTMessage
from paho.mqtt.properties import Properties
from paho.mqtt.reasoncodes import ReasonCodes


MQTT_BROKER: str = os.getenv("MQTT_BROKER", "0.0.0.0")
MQTT_PORT: int = int(os.getenv("MQTT_PORT", 1883))

def setup_mq_client(
        client: Client,
        on_message: Callable[[Client, Any, MQTTMessage], object | None],
        on_connect: Callable[[Client, Any, dict[str, int], int], object] |
                    Callable[[Client, Any, dict[str, int], ReasonCodes, Properties | None], object | None],
):
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(MQTT_BROKER, MQTT_PORT)