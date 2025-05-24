from typing import Any
from paho.mqtt.client import Client, MQTTMessage
from common.logger import get_logger
from common.config import MQTT_BROKER, MQTT_PORT
from common.types.topic import Topic
from server.controller import router, ServerController

logger = get_logger("Server:Core")
server_controller = ServerController()

def on_connect(client: Client, userdata: Any, flags: dict[str, Any], rc: int) -> None:
    logger.info("Connected to MQTT broker with result code %s", str(rc))

    for t in Topic:
        client.subscribe(f"{t.value}/#")

def on_message(client: Client, userdata: Any, msg: MQTTMessage) -> None:
    topic_parts = msg.topic.split('/')
    try:
        handler = router.get(topic_parts[0])
        if handler:
            handler(server_controller, msg, client)
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