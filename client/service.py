import time
from threading import Thread
from typing import Literal, Any, Optional
from paho.mqtt.client import Client, MQTTMessage
from pydantic import ValidationError
from common.config import setup_mq_client
from common.logger import get_logger
from common.types.client_messages import RegisterMessage, DisconnectMessage, SendTextMessage, \
    SendFileMessage, LookupMessage
from common.types.server_messages import ServerMessage
from common.types.topic import ClientMessageTopic, ServerMessageTopic
from common.types.with_validation import expected_response_types_for_topic, validate_message


class ClientService:
    def __init__(self):
        self.logger = get_logger("Client:Service")
        self.client = Client()
        setup_mq_client(self.client, self.on_message, self.on_connect)
        self.requests_track: dict[str, ServerMessage | Literal['Waiting for response']] = {}
        self.start_monitoring_thread()

    def start_mq_client(self) -> None:
        self.client.loop_start()

    def start_monitoring_thread(self):
        monitoring_thread = Thread(target=self.monitor_requests_track, daemon=True)
        monitoring_thread.start()

    def monitor_requests_track(self):
        while True:
            time.sleep(1)
            for request_id, status in list(self.requests_track.items()):
                if status != "Waiting for response":
                    self.logger.info(f"Request {request_id} has been updated: {status}")
                    del self.requests_track[request_id]

    def on_connect(self, client: Client, userdata: Any, flags: dict[str, Any], rc: int) -> None:
        if rc == 0:
            self.logger.info("Connected to MQTT broker with result code %s", str(rc))

        else:
            self.logger.info(f"Bad connection, returned code: {rc}")

    def on_message(self, client: Client, userdata: Any, msg: MQTTMessage) -> None:
        from client.controller import router
        from client.engine.core import client_controller

        topic_parts = msg.topic.split('/')
        try:
            models = expected_response_types_for_topic.get(topic_parts[0])

            if models:
                data = validate_message(msg.payload, *models)
                self.requests_track[data.request_id] = data

                handler = router.get(topic_parts[0])

                if handler:
                    handler(client_controller, msg)

                else:
                    self.logger.warning("Unhandled topic: %s", msg.topic)

        except ValidationError as e:
            self.logger.error("Request validation error for topic '%s': %s", topic_parts[0], str(e))

    def register(self, username: str, address: str) -> str:
        msg = RegisterMessage(
            username=username,
            address=address
        )

        self.requests_track[msg.request_id] = "Waiting for response"
        self.client.subscribe(f"{ServerMessageTopic.REGISTER_RESPONSE.value}/{address}")
        self.client.publish(
            ClientMessageTopic.REGISTER.value,
            msg.model_dump_json()
        )

        return msg.request_id

    def disconnect(self, username: str, address: str) -> str:
        msg = DisconnectMessage(
            username=username,
            address=address
        )

        self.requests_track[msg.request_id] = "Waiting for response"
        self.client.subscribe(f"{ServerMessageTopic.DISCONNECT_RESPONSE.value}/{address}")
        self.client.publish(
            ClientMessageTopic.DISCONNECT.value,
            msg.model_dump_json()
        )

        return msg.request_id

    def send_text_message(self, from_user: str, to_user: str, message: str) -> str:
        msg = SendTextMessage(
            to_user=to_user,
            from_user=from_user,
            message=message
        )

        self.requests_track[msg.request_id] = "Waiting for response"
        self.client.subscribe(f"{ServerMessageTopic.SEND_MSG_RESPONSE.value}/{from_user}")
        self.client.publish(
            ClientMessageTopic.SEND_MSG.value,
            msg.model_dump_json()
        )

        return msg.request_id

    def send_file(self, from_user: str, to_user: str, filename: str,
                  content_base64: str, message: Optional[str] = "") -> str:
        msg = SendFileMessage(
            to_user=to_user,
            from_user=from_user,
            filename=filename,
            content_base64=content_base64,
            message=message
        )

        self.requests_track[msg.request_id] = "Waiting for response"
        self.client.subscribe(f"{ServerMessageTopic.SEND_FILE_RESPONSE.value}/{from_user}")
        self.client.publish(
            ClientMessageTopic.SEND_FILE.value,
            msg.model_dump_json()
        )

        return msg.request_id

    def lookup(self, requester: str, target: str) -> str:
        msg = LookupMessage(
            requester=requester,
            target=target
        )

        self.requests_track[msg.request_id] = "Waiting for response"
        self.client.subscribe(f"{ServerMessageTopic.LOOKUP_RESPONSE.value}/{requester}")
        self.client.publish(
            ClientMessageTopic.LOOKUP.value,
            msg.model_dump_json()
        )

        return msg.request_id