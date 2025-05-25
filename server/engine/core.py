from server.controller import ServerController

server_controller = ServerController()

def run_server():
    server_controller.server_service.client.loop_forever()