import socket
import time
from client.chat_client import ChatClient
from datetime import datetime
import paho.mqtt.client as mqtt
import json
import threading
import time

from client.controller import ClientController
from common.types.topic import Topic

BROKER = "localhost"
PORT = 1883

username = None
client = mqtt.Client()
registered = False
client_controller = ClientController(client)

def on_connect(client, userdata, flags, rc):
    print(f"[SYSTEM] Connected to MQTT broker (code {rc})")

def get_local_ip():
    try:
        # Works for most networks
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def on_message(client, userdata, msg):
    global registered
    topic_parts = msg.topic.split('/')
    payload = msg.payload.decode()

    if topic_parts[0] == "register" and topic_parts[-1] == "response":
        data = json.loads(payload)
        if data.get("success"):
            print(f"[SYSTEM] Username '{username}' registered successfully.")
            registered = True
            client.subscribe(f"msg/+/+")
            client.subscribe(f"lookup/{username}/response")
        else:
            print(f"[SYSTEM] Username '{username}' rejected: {data.get('reason')}")
    elif topic_parts[0] == "msg":
        sender = topic_parts[1]
        print(f"[{sender}] {payload}")
    elif topic_parts[0] == "lookup":
        print(f"[LOOKUP RESPONSE] {payload}")
    else:
        print(f"[UNKNOWN MESSAGE] {msg.topic}: {payload}")


def try_register():
    global username
    while True:
        username = input("Choose your username: ").strip()
        default_address = f"{get_local_ip()}:9000"
        address = input(f"Enter your address (default: {default_address}): ").strip()
        if not address:
            address = default_address

        if not username:
            continue

        # Subscribe to own registration response
        client.subscribe(f"{Topic.REGISTER.value}/{address}")
        client_controller.register(username, address)


        # Wait for response
        for _ in range(20):  # wait max 2 seconds
            if registered:
                return
            time.sleep(0.1)

        print("[SYSTEM] No response or registration failed. Try another username.")
        client.unsubscribe(f"{Topic.REGISTER.value}/{address}")


def send_message(receiver, message):
    topic = f"send/msg/{username}/{receiver}"
    payload = json.dumps({"text": message})
    client.publish(topic, payload)


def lookup_user(target):
    payload = json.dumps({"target": target})
    client.publish(f"lookup/{username}", payload)


def disconnect():
    client.publish(f"disconnect/{username}", "")
    print("[SYSTEM] Disconnected.")


def cli_loop():
    while True:
        try:
            command = input("> ").strip()
            if command.startswith("send "):
                _, receiver, *msg = command.split()
                send_message(receiver, ' '.join(msg))
            elif command.startswith("lookup "):
                _, user = command.split()
                lookup_user(user)
            elif command == "exit":
                disconnect()
                break
            else:
                print("Commands: send <user> <message>, lookup <user>, exit")
        except KeyboardInterrupt:
            disconnect()
            break


def run():
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT, 60)

    threading.Thread(target=client.loop_forever, daemon=True).start()

    try_register()
    cli_loop()


if __name__ == "__main__":
    run()