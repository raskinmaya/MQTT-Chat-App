from typing import Any
from uuid import uuid4
from paho.mqtt.client import Client, MQTTMessage
from common.config import setup_mq_client
from common.logger import get_logger
from common.types.server_messages import ServerError, ServerAck, LookupResponse, ChatMessage
from common.types.topic import Topic


class ServerService:
    def __init__(self):
        self.logger = get_logger("Server:Service")
        self.client = Client()
        setup_mq_client(self.client, self.on_message, self.on_connect)
        self.clients_online: dict[str, str] = {}

    def start_mq_client(self):
        self.client.loop_forever()

    def on_connect(self, client: Client, userdata: Any, flags: dict[str, Any], rc: int) -> None:
        self.logger.info("Connected to MQTT broker with result code %s", str(rc))

        for t in Topic:
            self.client.subscribe(f"{t.value}/#")

    def on_message(self, client: Client, userdata: Any, msg: MQTTMessage) -> None:
        from server.controller import router
        from server.engine.core import server_controller

        topic_parts = msg.topic.split('/')
        try:
            handler = router.get(topic_parts[0])
            if handler:
                handler(server_controller, msg)
            else:
                self.logger.warning("Unhandled topic: %s", msg.topic)
        except Exception as e:
            self.logger.error("Error processing message on topic %s: %s", msg.topic, str(e))

    def register(self, request_id: str, username: str, address: str) -> None:
        if not username or not address:
            self.client.publish(
                f"{Topic.REGISTER.value}/{address}",
                ServerError(
                    request_id=request_id,
                    topic=f"{Topic.REGISTER.value}/{address}",
                    username=username,
                    address=address,
                    message="Registration could not be completed",
                    reason="Username or address is empty"
                ).model_dump_json()
            )

        elif username in self.clients_online:
            self.client.publish(
                f"{Topic.REGISTER.value}/{address}",
                ServerError(
                    request_id=request_id,
                    topic=f"{Topic.REGISTER.value}/{address}",
                    username=username,
                    address=address,
                    message="Registration could not be completed",
                    reason="Username is taken"
                ).model_dump_json()
            )

        else:
            self.clients_online[username] = address
            self.logger.info("Registered user %s at %s", username, address)
            self.client.publish(f"{Topic.REGISTER.value}/{address}",
                           ServerAck(
                               request_id=request_id,
                               topic=f"{Topic.REGISTER.value}/{address}",
                               username=username,
                               address=address,
                               message=f"Registration completed for user {username}, address {address}"
                           ).model_dump_json()
            )

    def disconnect(self, request_id: str, username: str, address: str) -> None:
        if not username or not address:
            self.client.publish(
                f"{Topic.DISCONNECT.value}/{address}",
                ServerError(
                    request_id=request_id,
                    topic=f"{Topic.DISCONNECT.value}/{address}",
                    username=username,
                    address=address,
                    message="Disconnect failed",
                    reason="Username or address is empty"
                ).model_dump_json()
            )

        elif username in self.clients_online and self.clients_online[username] == address:
            del self.clients_online[username]
            self.logger.info("Disconnected user %s at %s", username, address)

            self.client.publish(
                f"{Topic.DISCONNECT.value}/{address}",
                ServerAck(
                    request_id=request_id,
                    topic=f"{Topic.DISCONNECT.value}/{address}",
                    username=username,
                    address=address,
                    message=f"User {username} disconnected",
                ).model_dump_json()
            )

        else:
            self.logger.info("Could not disconnect user %s", username)

            self.client.publish(
                f"{Topic.DISCONNECT.value}/{address}",
                ServerError(
                    request_id=request_id,
                    topic=f"{Topic.DISCONNECT.value}/{address}",
                    username=username,
                    address=address,
                    message=f"User {username} disconnect failed",
                    reason="No match between username and password"
                ).model_dump_json()
            )

    def send_message(self, request_id: str, from_user: str, to_user: str, message: str) -> None:
        if not from_user or not to_user or not message:
            self.client.publish(f"{Topic.SEND_MSG.value}/{from_user}",
                           ServerError(
                               request_id=request_id,
                               topic=f"{Topic.SEND_MSG.value}/{from_user}",
                               username=from_user,
                               message="Message was not sent",
                               reason="from_user or to_user or message is empty"
                           ).model_dump_json()
            )

        elif to_user not in self.clients_online:
            self.client.publish(f"{Topic.SEND_MSG.value}/{from_user}",
                           ServerError(
                               request_id=request_id,
                               topic=f"{Topic.SEND_MSG.value}/{from_user}",
                               username=from_user,
                               message="Message was not sent",
                               reason=f"User {to_user} not found"
                           ).model_dump_json()
            )

        else:
            self.client.publish(f"{Topic.MSG.value}/{to_user}", ChatMessage(message=message).model_dump_json())
            self.client.publish(f"{Topic.SEND_MSG.value}/{from_user}",
                           ServerAck(
                               request_id=request_id,
                               topic=f"{Topic.SEND_MSG.value}/{from_user}",
                               username=from_user,
                               message=f"Message to user {to_user} was sent successfully",
                           ).model_dump_json()
            )

            self.logger.info("Message from %s to %s sent", from_user, to_user)

    def send_file(self, request_id: str, from_user: str, to_user: str, filename: str, content_base64: str, message: str) -> None:
        if not to_user or not from_user or not content_base64:
            self.client.publish(
                f"{Topic.SEND_FILE.value}/{from_user}",
                ServerError(
                    request_id=request_id,
                    topic=f"{Topic.SEND_FILE.value}/{from_user}",
                    username=from_user,
                    message="Message was not sent",
                    reason="from_user or to_user or content_base64 is empty"
                ).model_dump_json()
            )

        elif to_user not in self.clients_online:
            self.client.publish(f"{Topic.SEND_FILE.value}/{from_user}",
                           ServerError(
                               request_id=request_id,
                               topic=f"{Topic.SEND_FILE.value}/{from_user}",
                               username=from_user,
                               message="Message was not sent",
                               reason=f"User {to_user} not found"
                           ).model_dump_json()
            )

        else:
            self.client.publish(f"{Topic.SEND_FILE.value}/{from_user}",
                           ServerAck(
                               request_id=request_id,
                               topic=f"{Topic.SEND_FILE.value}/{from_user}",
                               username=from_user,
                               message=f"File message to user {to_user} was sent successfully",
                           ).model_dump_json()
            )

            self.client.publish(f"{Topic.MSG.value}/{to_user}",
                           ChatMessage(
                               request_id=str(uuid4()),
                               filename=filename,
                               message=message,
                               content_base64=content_base64
                           ).model_dump_json()
            )

            self.logger.info("Message from %s to %s sent", from_user, to_user)

    def lookup(self, request_id: str, requester: str, target: str) -> None:
        address = self.clients_online.get(target, "")

        if not address:
            self.client.publish(f"{Topic.LOOKUP.value}/{requester}",
                           ServerError(
                               request_id=request_id,
                               topic=f"{Topic.LOOKUP.value}/{requester}",
                               username=requester,
                               message="Lookup failed",
                               reason=f"Address {target} not found"
                           ).model_dump_json()
            )

        else:
            self.client.publish(f"{Topic.LOOKUP.value}/{requester}",
                           LookupResponse(
                               request_id=request_id,
                               target=target,
                               address=address
                           ).model_dump_json()
            )

        self.logger.info("Lookup from %s to %s -> %s", requester, target, address)