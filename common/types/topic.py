from enum import Enum

class Topic(Enum):
    REGISTER = "register"
    MESSAGE = "msg"
    FILE = "msg/file"
    LOOKUP = "lookup"
    SEND_MSG = "send/msg"
    SEND_FILE = "send/file"