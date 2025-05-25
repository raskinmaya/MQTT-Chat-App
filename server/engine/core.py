from common.logger import get_logger
from server.controller import ServerController

server_controller = ServerController()
logger = get_logger("Server:Core")

def run_server():
    server_controller.logger.info("Server is starting...")
    server_controller.start_mq_client()