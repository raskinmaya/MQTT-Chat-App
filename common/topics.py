from enum import Enum


class Topics(Enum):
    REGISTER = "register"
    SEND_MESSAGE = "send_message"
    SEND_FILE = "send_file"
    LOOKUP = "lookup"