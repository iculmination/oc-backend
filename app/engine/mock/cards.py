from uuid import uuid4
from app.enums.card import CardNature
from app.engine.state.card import CardState


def soldier(owner_id):
    return CardState(
        id=uuid4(),
        card_id=uuid4(),
        owner_id=owner_id,
        name="Soldier",
        attack=5,
        health=10,
        max_health=10,
        ability="attack",
        nature=CardNature.HUMAN,
    )


def medic(owner_id):
    return CardState(
        id=uuid4(),
        card_id=uuid4(),
        owner_id=owner_id,
        name="Medic",
        attack=3,
        health=8,
        max_health=8,
        ability="heal",
        nature=CardNature.ROBOT,
    )


def void_beast(owner_id):
    return CardState(
        id=uuid4(),
        card_id=uuid4(),
        owner_id=owner_id,
        name="Void Beast",
        attack=6,
        health=12,
        max_health=12,
        ability="attack",
        nature=CardNature.CREATURE,
    )