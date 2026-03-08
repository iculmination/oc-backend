from enum import StrEnum


class EventRarity(StrEnum):
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"


class EventStatus(StrEnum):
    PENDING = "pending"
    ONGOING = "ongoing"
    PAUSED = "paused"
    FINISHED = "finished"
    CANCELLED = "cancelled"
    ABORTED = "aborted"


class EventSource(StrEnum):
    RANDOM = "random"
    CALLED = "called"
    TRIGGERED = "triggered"
    IMMEDIATE = "immediate"
    DELAYED = "delayed"
