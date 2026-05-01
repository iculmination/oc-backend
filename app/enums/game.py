from enum import StrEnum


class GameStatus(StrEnum):
    PENDING = "pending"
    ONGOING = "ongoing"
    PAUSED = "paused"
    FINISHED = "finished"
    CANCELLED = "cancelled"
    ABORTED = "aborted"
