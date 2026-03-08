import random
from uuid import uuid4
from app.engine.state.event import EventState


def blood_rain():
    return EventState(
        id=uuid4(),
        name="Blood Rain",
        description="A blood rain event occurs, which causes all human cards to gain insanity.",
        rarity="common",
        status="active",
        source="random",
        effect="blood_rain",
        duration=random.randint(1, 3),
    )


def plague():
    return EventState(
        id=uuid4(),
        name="Plague",
        description="A plague event occurs, which causes all robot cards to gain insanity.",
        rarity="common",
        status="active",
        source="random",
        effect="plague",
        duration=random.randint(1, 3),
    )


def solar_flare():
    return EventState(
        id=uuid4(),
        name="Solar Flare",
        description="A solar flare event occurs, which causes all void cards to gain insanity.",
        rarity="common",
        status="active",
        source="random",
        effect="solar_flare",
        duration=random.randint(1, 3),
    )
