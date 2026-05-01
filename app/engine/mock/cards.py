import random
from uuid import uuid4

from app.engine.state.card import CardState
from app.enums.card import CardAbilities, CardNature


def _card(owner_id, name, attack, health, ability, nature):
    return CardState(
        id=uuid4(),
        card_id=uuid4(),
        owner_id=owner_id,
        name=name,
        attack=attack,
        health=health,
        max_health=health,
        ability=ability,
        nature=nature,
    )


def soldier(owner_id):
    return _card(owner_id, "Soldier", 5, 10, CardAbilities.ATTACK, CardNature.HUMAN)


def medic(owner_id):
    return _card(owner_id, "Medic", 3, 8, CardAbilities.HEAL, CardNature.ROBOT)


def void_beast(owner_id):
    return _card(
        owner_id, "Void Beast", 6, 12, CardAbilities.ATTACK, CardNature.CREATURE
    )


def raider(owner_id):
    return _card(owner_id, "Raider", 7, 8, CardAbilities.ATTACK, CardNature.HUMAN)


def vanguard(owner_id):
    return _card(owner_id, "Vanguard", 4, 13, CardAbilities.ATTACK, CardNature.HUMAN)


def tactician(owner_id):
    return _card(owner_id, "Tactician", 2, 9, CardAbilities.BUFF, CardNature.HUMAN)


def field_doc(owner_id):
    return _card(owner_id, "Field Doc", 2, 11, CardAbilities.HEAL, CardNature.HUMAN)


def mech_guard(owner_id):
    return _card(owner_id, "Mech Guard", 4, 14, CardAbilities.ATTACK, CardNature.ROBOT)


def pulse_drone(owner_id):
    return _card(owner_id, "Pulse Drone", 3, 10, CardAbilities.BUFF, CardNature.ROBOT)


def nanite_nurse(owner_id):
    return _card(owner_id, "Nanite Nurse", 3, 9, CardAbilities.HEAL, CardNature.ROBOT)


def cloak_bot(owner_id):
    return _card(owner_id, "Cloak Bot", 2, 8, CardAbilities.HIDE, CardNature.ROBOT)


def ripper_unit(owner_id):
    return _card(owner_id, "Ripper Unit", 8, 7, CardAbilities.ATTACK, CardNature.ROBOT)


def abyss_hunter(owner_id):
    return _card(
        owner_id, "Abyss Hunter", 7, 11, CardAbilities.ATTACK, CardNature.CREATURE
    )


def brood_mender(owner_id):
    return _card(
        owner_id, "Brood Mender", 3, 10, CardAbilities.HEAL, CardNature.CREATURE
    )


def shade_stalker(owner_id):
    return _card(
        owner_id, "Shade Stalker", 4, 9, CardAbilities.HIDE, CardNature.CREATURE
    )


def alpha_howler(owner_id):
    return _card(
        owner_id, "Alpha Howler", 2, 12, CardAbilities.BUFF, CardNature.CREATURE
    )


def chitin_tank(owner_id):
    return _card(
        owner_id, "Chitin Tank", 5, 15, CardAbilities.ATTACK, CardNature.CREATURE
    )


def mimic_warden(owner_id):
    return _card(
        owner_id, "Mimic Warden", 3, 11, CardAbilities.HIDE, CardNature.CREATURE
    )


def overclock_engineer(owner_id):
    return _card(
        owner_id, "Overclock Engineer", 2, 9, CardAbilities.BUFF, CardNature.ROBOT
    )


ALL_MOCK_CARD_FACTORIES = [
    soldier,
    medic,
    void_beast,
    raider,
    vanguard,
    tactician,
    field_doc,
    mech_guard,
    pulse_drone,
    nanite_nurse,
    cloak_bot,
    ripper_unit,
    abyss_hunter,
    brood_mender,
    shade_stalker,
    alpha_howler,
    chitin_tank,
    mimic_warden,
    overclock_engineer,
]


def draft_random_cards(owner_id, count=4):
    factories = random.sample(
        ALL_MOCK_CARD_FACTORIES, k=min(count, len(ALL_MOCK_CARD_FACTORIES))
    )
    return [factory(owner_id) for factory in factories]
