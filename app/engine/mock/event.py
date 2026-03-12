import random
from uuid import uuid4
from app.engine.state.event import EventState
from app.enums.card import CardNature, CardEffects
from app.enums.event import EventStatus, EventSource, EventRarity


def blood_rain():
    return EventState(
        id=uuid4(),
        name="Blood Rain",
        description="A blood rain event occurs, which causes all human cards to gain insanity.",
        rarity=EventRarity.COMMON,
        status=EventStatus.ONGOING,
        source=EventSource.RANDOM,
        effect="blood_rain",
        applies_effect=CardEffects.INSANITY,
        affects_nature=CardNature.HUMAN,
        duration=random.randint(1, 3),
    )


def plague():
    return EventState(
        id=uuid4(),
        name="Plague",
        description="A plague event occurs, which causes all robot cards to gain insanity.",
        rarity=EventRarity.COMMON,
        status=EventStatus.ONGOING,
        source=EventSource.RANDOM,
        effect="plague",
        applies_effect=CardEffects.INSANITY,
        affects_nature=CardNature.ROBOT,
        duration=random.randint(1, 3),
    )


def solar_flare():
    return EventState(
        id=uuid4(),
        name="Solar Flare",
        description="A solar flare event occurs, which causes all creature cards to gain insanity.",
        rarity=EventRarity.COMMON,
        status=EventStatus.ONGOING,
        source=EventSource.RANDOM,
        effect="solar_flare",
        applies_effect=CardEffects.INSANITY,
        affects_nature=CardNature.CREATURE,
        duration=random.randint(1, 3),
    )
