from enum import StrEnum


class UpgradeRarity(StrEnum):
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"


class UpgradeType(StrEnum):
    IMPLANT = "implant"
    MUTATION = "mutation"
    EQUIPMENT = "equipment"
    MODULE = "module"
