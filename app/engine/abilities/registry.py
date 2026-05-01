from app.engine.abilities.attack import AttackAbility
from app.engine.abilities.heal import HealAbility
from app.engine.abilities.buff import BuffAbility
from app.engine.abilities.hide import HideAbility
from app.enums.card import CardAbilities

ABILITY_REGISTRY = {
    CardAbilities.ATTACK: AttackAbility(),
    CardAbilities.HEAL: HealAbility(),
    CardAbilities.BUFF: BuffAbility(),
    CardAbilities.HIDE: HideAbility(),
}
