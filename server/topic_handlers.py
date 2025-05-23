from paho.mqtt.client import Client, MQTTMessage

from server.store import clients_online, offline_messages
from server.utils import topic_handler
from json import loads as json_loads
from json import dumps as json_dumps
from server.core import logger

@topic_handler("register")
def handle_register(parts: list[str], msg: MQTTMessage, client: Client) -> None:
    username = parts[1]
    address = msg.payload.decode()
    clients_online[username] = address
    logger.info("Registered user %s at %s", username, address)
    if username in offline_messages:
        for message in offline_messages[username]:
            client.publish(f"msg/{username}", json_dumps(message))
        del offline_messages[username]

@topic_handler("send")
def handle_send(parts: list[str], msg: MQTTMessage, client: Client) -> None:
    to_user = parts[1]
    message = json_loads(msg.payload.decode())
    if to_user in clients_online:
        client.publish(f"msg/{to_user}", json_dumps(message))
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
