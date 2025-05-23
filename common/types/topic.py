from enum import Enum

class Topic(Enum):
    REGISTER = "register"
    MESSAGE = "msg"
    FILE = "msg/file"
    LOOKUP = "lookup"