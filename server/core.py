import json
from typing import Any, Callable
from paho.mqtt.client import Client, MQTTMessage
from common.logger import get_logger
from common.config import MQTT_BROKER, MQTT_PORT, CA_CERT, CLIENT_CERT, CLIENT_KEY
from server.utils import topic_handler

logger = get_logger("Server:Core")
handlers: dict[str, Callable[[list[str], MQTTMessage, Client], None]] = {}

clients_online: dict[str, str] = {}
offline_messages: dict[str, list[dict[str, Any]]] = {}

@topic_handler("register")
def handle_register(parts: list[str], msg: MQTTMessage, client: Client) -> None:
    username = parts[1]
    address = msg.payload.decode()
    clients_online[username] = address
    logger.info("Registered user %s at %s", username, address)
    if username in offline_messages:
        for message in offline_messages[username]:
            client.publish(f"msg/{username}", json.dumps(message))
        del offline_messages[username]

@topic_handler("send")
def handle_send(parts: list[str], msg: MQTTMessage, client: Client) -> None:
    to_user = parts[1]
    message = json.loads(msg.payload.decode())
    if to_user in clients_online:
        client.publish(f"msg/{to_user}", json.dumps(message))
    else:
        offline_messages.setdefault(to_user, []).append(message)
    logger.info("Message from %s to %s routed", message['from'], to_user)

@topic_handler("lookup")
def handle_lookup(parts: list[str], msg: MQTTMessage, client: Client) -> None:
    requester = parts[1]
    target = msg.payload.decode()
    address = clients_online.get(target, "")
    client.publish(f"lookup_response/{requester}", address)
    logger.info("Lookup from %s to %s -> %s", requester, target, address)

def on_connect(client: Client, userdata: Any, flags: dict[str, Any], rc: int) -> None:
    logger.info("Connected to MQTT broker with result code %s", str(rc))
    client.subscribe("register/#")
    client.subscribe("send/#")
    client.subscribe("lookup/#")

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
    # client.tls_set(ca_certs=CA_CERT, certfile=CLIENT_CERT, keyfile=CLIENT_KEY)
    client.connect(MQTT_BROKER, MQTT_PORT)
    logger.info("Server connected to broker %s:%s", MQTT_BROKER, MQTT_PORT)
    client.loop_forever()