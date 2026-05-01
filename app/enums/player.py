from enum import StrEnum


class PlayerStatus(StrEnum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    LEFT = "left"


class PlayerRole(StrEnum):
    HOST = "host"
    GUEST = "guest"
