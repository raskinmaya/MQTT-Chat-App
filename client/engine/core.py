from typing import Any
from paho.mqtt.client import Client, MQTTMessage

from client.controller import router
from common.logger import get_logger

logger = get_logger("Server:Core")

def on_connect(client: Client, userdata: Any, flags: dict[str, Any], rc: int) -> None:
    logger.info("Connected to MQTT broker with result code %s", str(rc))

def on_message(client: Client, userdata: Any, msg: MQTTMessage) -> None:
    topic_parts = msg.topic.split('/')
    try:
        if topic_parts[0] in router.handlers:
            router.handlers[topic_parts[0]](topic_parts, msg, client)
        else:
            logger.warning("Unhandled topic: %s", msg.topic)
    except Exception as e:
        logger.error("Error processing message on topic %s: %s", msg.topic, str(e))