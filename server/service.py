from typing import Any
from paho.mqtt.client import Client
from common.logger import get_logger
import json

from common.types.client_messages import FileTransferMessage
from common.types.server_messages import ServerError, ServerAck, LookupResponse, ChatMessage
from common.types.topic import Topic

logger = get_logger("Server:ClientService")

class ClientService:
    def __init__(self):
        self.clients_online: dict[str, str] = {}

    def register(self, username: str, address: str, client: Client) -> None:
        if username in self.clients_online:
            client.publish(
                f"{Topic.REGISTER.value}/{address}",
                ServerError(
                    topic=f"{Topic.REGISTER.value}/{address}",
                    username=username,
                    address=address,
                    message="Registration could not be completed",
                    reason="Username is taken"
                ).model_dump_json()
            )

        else:
            self.clients_online[username] = address
            logger.info("Registered user %s at %s", username, address)
            client.publish(f"{Topic.REGISTER.value}/{address}",
                           ServerAck(
                               topic=f"{Topic.REGISTER.value}/{address}",
                               username=username,
                               address=address,
                               message=f"Registration completed for user {username}"
                           ).model_dump_json()
            )

    def disconnect(self, username: str, address: str, client: Client) -> None:
        if username in self.clients_online and self.clients_online[username] == address:
            client.publish(
                f"{Topic.DISCONNECT.value}/{address}",
                ServerAck(
                    topic=f"{Topic.DISCONNECT.value}/{address}",
                    username=username,
                    address=address,
                    message=f"User {username} disconnected",
                ).model_dump_json()
            )

        else:
            client.publish(
                f"{Topic.DISCONNECT.value}/{address}",
                ServerError(
                    topic=f"{Topic.DISCONNECT.value}/{address}",
                    username=username,
                    address=address,
                    message=f"User {username} disconnect failed",
                    reason="No match between username and password"
                ).model_dump_json()
            )

    def send_message(self, from_user: str, to_user: str, message: str, client: Client) -> None:
        if to_user not in self.clients_online:
            client.publish(f"{Topic.SEND_MSG.value}/{from_user}",
                           ServerError(
                               topic=f"{Topic.SEND_MSG.value}/{from_user}",
                               username=from_user,
                               message="Message was not sent",
                               reason=f"User {to_user} not found"
                           ).model_dump_json()
            )

        else:
            client.publish(f"{Topic.MESSAGE.value}/{to_user}", ChatMessage(message=message).model_dump_json())
            client.publish(f"{Topic.SEND_MSG.value}/{from_user}",
                           ServerAck(
                               topic=f"{Topic.SEND_MSG.value}/{from_user}",
                               username=from_user,
                               message=f"Message to user {to_user} was sent successfully",
                           ).model_dump_json()
            )

            logger.info("Message from %s to %s sent", from_user, to_user)

    def send_file(self, data: FileTransferMessage, client: Client) -> None:
        if data.to_user not in self.clients_online:
            client.publish(f"{Topic.SEND_FILE.value}/{data.from_user}",
                           ServerError(
                               topic=f"{Topic.SEND_FILE.value}/{data.from_user}",
                               username=data.from_user,
                               message="Message was not sent",
                               reason=f"User {data.to_user} not found"
                           ).model_dump_json()
            )

        else:
            client.publish(f"{Topic.SEND_FILE.value}/{data.from_user}",
                           ServerAck(
                               topic=f"{Topic.SEND_FILE.value}/{data.from_user}",
                               username=data.from_user,
                               message=f"File message to user {data.to_user} was sent successfully",
                           ).model_dump_json()
            )

            client.publish(f"{Topic.MESSAGE.value}/{data.to_user}",
                           ChatMessage(
                               message=data.message,
                               content_base64=data.content_base64
                           ).model_dump_json()
            )

            logger.info("Message from %s to %s sent", data.from_user, data.to_user)

    def lookup(self, requester: str, target: str, client: Client) -> None:
        address = self.clients_online.get(target, "")

        if not address:
            client.publish(f"{Topic.LOOKUP.value}/{requester}",
                           ServerError(
                               topic=f"{Topic.LOOKUP.value}/{requester}",
                               username=requester,
                               message="Lookup failed",
                               reason=f"Address {target} not found"
                           ).model_dump_json()
            )

        else:
            client.publish(f"{Topic.LOOKUP.value}/{requester}",
                           LookupResponse(
                               target=target,
                               address=address
                           ).model_dump_json()
            )

        logger.info("Lookup from %s to %s -> %s", requester, target, address)