from app.enums.event import Events
from app.engine.events.blood_rain import BloodRainEvent
from app.engine.events.plague import PlagueEvent
from app.engine.events.solar_flare import SolarFlareEvent

EVENTS_REGISTRY = {
    Events.BLOOD_RAIN: BloodRainEvent(),
    Events.PLAGUE: PlagueEvent(),
    Events.SOLAR_FLARE: SolarFlareEvent(),
}
