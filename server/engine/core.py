from typing import Any, Callable
from paho.mqtt.client import Client, MQTTMessage
from common.logger import get_logger
from common.config import MQTT_BROKER, MQTT_PORT
from common.types.topic import Topic

logger = get_logger("Server:Core")
handlers: dict[str, Callable[[list[str], MQTTMessage, Client], None]] = {}

def on_connect(client: Client, userdata: Any, flags: dict[str, Any], rc: int) -> None:
    logger.info("Connected to MQTT broker with result code %s", str(rc))

    for t in Topic:
        client.subscribe(f"{t.value}/#")

def on_message(client: Client, userdata: Any, msg: MQTTMessage) -> None:
    topic_parts = msg.topic.split('/')
    try:
        if topic_parts[0] in handlers:
            handlers[topic_parts[0]](topic_parts, msg, client)
        else:
            logger.warning("Unhandled topic: %s", msg.topic)
    except Exception as e:
        logger.error("Error processing message on topic %s: %s", msg.topic, str(e))

def run_server():
    client: Client = Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT)
    logger.info("Server connected to broker %s:%s", MQTT_BROKER, MQTT_PORT)
    client.loop_forever()