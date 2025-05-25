import time

from client.controller import ClientController
from common.types.server_messages import ServerError, ServerAck

client_controller = ClientController()

def run_client():
    client_controller.start_mq_client()
    registered = False
    
    print("Welcome to the Client Application!")
    
    while not registered:
        username = input("Please enter your username: ")
        request_id = client_controller.register(username=username, address="localhost")
        res = client_controller.get_response(request_id)

        while not res or res == 'Waiting for response':
            time.sleep(5)
            res = client_controller.get_response(request_id)

        if isinstance(res, ServerError):
            print("Error occurred: %s, reason: %s", res.message, res.reason)

        elif isinstance(res, ServerAck):
            print("Registration completed successfully!")
            registered = True


    print("Menu will be printed here")