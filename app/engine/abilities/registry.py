from app.engine.abilities.attack import AttackAbility
from app.engine.abilities.heal import HealAbility
from app.engine.abilities.buff import BuffAbility
from app.engine.abilities.hide import HideAbility

ABILITY_REGISTRY = {
    "attack": AttackAbility(),
    "heal": HealAbility(),
    "buff": BuffAbility(),
    "hide": HideAbility(),
}
