import json
from typing import Any

from paho.mqtt.client import Client, MQTTMessage
from common.logger import get_logger
from common.config import MQTT_BROKER, MQTT_PORT, CA_CERT, CLIENT_CERT, CLIENT_KEY

logger = get_logger("Server:Core")
clients_online: dict[str, str] = {}
offline_messages: dict[str, list[dict[str, Any]]] = {}

def on_connect(client: Client, userdata: Any, flags: dict[str, Any], rc: int) -> None:
    logger.info("Connected to MQTT broker with result code %s", str(rc))
    client.subscribe("register/#")
    client.subscribe("send/#")
    client.subscribe("lookup/#")

def on_message(client: Client, userdata: Any, msg: MQTTMessage) -> None:
    topic_parts: list[str] = msg.topic.split('/')
    try:
        if topic_parts[0] == "register":
            username = topic_parts[1]
            address = msg.payload.decode()
            clients_online[username] = address
            logger.info("Registered user %s at %s", username, address)
            if username in offline_messages:
                for message in offline_messages[username]:
                    client.publish(f"msg/{username}", json.dumps(message))
                del offline_messages[username]

        elif topic_parts[0] == "send":
            to_user = topic_parts[1]
            message = json.loads(msg.payload.decode())
            if to_user in clients_online:
                client.publish(f"msg/{to_user}", json.dumps(message))
            else:
                offline_messages.setdefault(to_user, []).append(message)
            logger.info("Message from %s to %s routed", message['from'], to_user)

        elif topic_parts[0] == "lookup":
            requester = topic_parts[1]
            target = msg.payload.decode()
            address = clients_online.get(target, "")
            client.publish(f"lookup_response/{requester}", address)
            logger.info("Lookup from %s to %s -> %s", requester, target, address)
    except Exception as e:
        logger.error("Error processing message: %s", str(e))


def run_server():
    client: Client = Client()
    client.on_connect = on_connect
    client.on_message = on_message
    # client.tls_set(ca_certs=CA_CERT, certfile=CLIENT_CERT, keyfile=CLIENT_KEY)
    client.connect(MQTT_BROKER, MQTT_PORT)
    logger.info("Server connected to broker %s:%s", MQTT_BROKER, MQTT_PORT)
    client.loop_forever()