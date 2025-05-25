import time

from client.controller import ClientController
from common.types.server_messages import ServerError, ServerAck

client_controller = ClientController()

def handle_registration():
    registered = False
    while not registered:
        username = input("Please enter your username: ")
        request_id = client_controller.register(username=username, address="localhost")
        res = client_controller.get_response(request_id)

        while not res or res == 'Waiting for response':
            time.sleep(5)
            res = client_controller.get_response(request_id)

        if isinstance(res, ServerError):
            print(f"Error occurred: {res.message}, reason: {res.reason}, restarting registration...")

        elif isinstance(res, ServerAck):
            print("Registration completed successfully! Entering chat...")
            registered = True

def enter_chat():
    raise NotImplementedError

def run_client():
    client_controller.start_mq_client()
    print("Welcome to the Client Application!")
    handle_registration()
    enter_chat()