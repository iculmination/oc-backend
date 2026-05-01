from app.enums.card import CardEffects
from app.engine.effects.insanity import InsanityEffect
from app.engine.effects.hidden import HiddenEffect
from app.engine.effects.bleed import BleedEffect
from app.engine.effects.poison import PoisonEffect

EFFECT_REGISTRY = {
    CardEffects.INSANITY: InsanityEffect(),
    CardEffects.HIDDEN: HiddenEffect(),
    CardEffects.BLEED: BleedEffect(),
    CardEffects.POISON: PoisonEffect(),
}
