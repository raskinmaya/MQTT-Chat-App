from typing import Any
from paho.mqtt.client import Client
from pydantic import ValidationError

from common.logger import get_logger
import json

from common.types.exceptions import UsernameAlreadyTaken, UserNotFound
from common.types.topic import Topic

logger = get_logger("Server:ClientService")

class ClientService:
    def __init__(self):
        self.clients: set[str] = set()
        self.clients_online: dict[str, str] = {}
        self.offline_messages: dict[str, list[dict[str, Any]]] = {}

    def register(self, username: str, address: str, client: Client) -> None:
        # TODO Add error handling
        if username in self.clients:
            raise UsernameAlreadyTaken(username)

        self.clients.add(username)
        self.clients_online[username] = address
        logger.info("Registered user %s at %s", username, address)

        if username in self.offline_messages:
            for message in self.offline_messages[username]:
                client.publish(f"{Topic.MESSAGE.value}/{username}", json.dumps(message))
            del self.offline_messages[username]

    def route_message(self, to_user: str, message: dict[str, Any], client: Client) -> None:
        # TODO Add error handling
        if to_user not in self.clients:
            raise UserNotFound(to_user)

        if to_user in self.clients_online:
            client.publish(f"{Topic.MESSAGE.value}/{to_user}", json.dumps(message))
        else:
            self.offline_messages.setdefault(to_user, []).append(message)
        logger.info("Message from %s to %s routed", message['from_user'], to_user)

    def handle_lookup(self, requester: str, target: str, client: Client) -> None:
        address = self.clients_online.get(target, "")

        if not address:
            client.publish(f"{Topic.LOOKUP.value}/{requester}", "Couldn't find address")
        else:
            client.publish(f"{Topic.LOOKUP.value}/{requester}", address)
        logger.info("Lookup from %s to %s -> %s", requester, target, address)