from typing import Any
from paho.mqtt.client import Client
from common.logger import get_logger
import json

logger = get_logger("ClientService")

class ClientService:
    def __init__(self):
        self.clients_online: dict[str, str] = {}
        self.offline_messages: dict[str, list[dict[str, Any]]] = {}

    def register(self, username: str, address: str, client: Client) -> None:
        self.clients_online[username] = address
        logger.info("Registered user %s at %s", username, address)
        if username in self.offline_messages:
            for message in self.offline_messages[username]:
                client.publish(f"msg/{username}", json.dumps(message))
            del self.offline_messages[username]

    def route_message(self, to_user: str, message: dict[str, Any], client: Client) -> None:
        if to_user in self.clients_online:
            client.publish(f"msg/{to_user}", json.dumps(message))
        else:
            self.offline_messages.setdefault(to_user, []).append(message)
        logger.info("Message from %s to %s routed", message['from_user'], to_user)

    def handle_lookup(self, requester: str, target: str, client: Client) -> None:
        address = self.clients_online.get(target, "")
        client.publish(f"lookup_response/{requester}", address)
        logger.info("Lookup from %s to %s -> %s", requester, target, address)