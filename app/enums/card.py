from enum import StrEnum


class Rarity(StrEnum):
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"


class CardNature(StrEnum):
    HUMAN = "human"
    ANIMAL = "animal"
    CREATURE = "creature"
    PLANT = "plant"
    RESOURCE = "resource"
    ROBOT = "robot"


class CardSpecialty(StrEnum):
    SOLDIER = "soldier"
    ENGINEER = "engineer"
    SCIENTIST = "scientist"
    TRADER = "trader"
    LEADER = "leader"
    HERO = "hero"
    VILLAIN = "villain"
    NEUTRAL = "neutral"


class CardFaction(StrEnum):
    EMPIRE = "empire"
    PIRATES = "pirates"
    RITUALISTS = "ritualists"
    MECHANOIDS = "mechanoids"
    ABYSSAL = "abyssal"
    COLONY = "colony"
    TRADERS = "traders"
