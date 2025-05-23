from enum import Enum

class Topic(Enum):
    REGISTER = "register"
    DISCONNECT = "disconnect"
    MESSAGE = "msg"
    LOOKUP = "lookup"
    SEND_MSG = "send/msg"
    SEND_FILE = "send/file"