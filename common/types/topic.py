from enum import Enum

class ClientMessageTopic(Enum):
    REGISTER = "register"
    DISCONNECT = "disconnect"
    LOOKUP = "lookup"
    SEND_MSG = "sendMsg"
    SEND_FILE = "sendFile"

class ServerMessageTopic(Enum):
    MSG = "msg"
    REGISTER_RESPONSE = "registerResponse"
    DISCONNECT_RESPONSE = "disconnectResponse"
    LOOKUP_RESPONSE = "lookupResponse"
    SEND_MSG_RESPONSE = "sendMessageResponse"
    SEND_FILE_RESPONSE = "sendFileResponse"