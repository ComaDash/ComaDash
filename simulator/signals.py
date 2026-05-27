import random
from datetime import datetime, timezone

from catalog import Signal
from scenarios import multiplier, offset


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def value_for(signal: Signal, scenario: str, tick: int) -> float:
    noise = random.gauss(0, signal.noise)
    value = signal.baseline * multiplier(scenario, signal.variable, tick)
    value += offset(scenario, signal.area, signal.tag, signal.variable, tick)
    return round(max(0.0, value + noise), 3)


def payload(signal: Signal, scenario: str, tick: int) -> dict:
    data = {
        "timestamp": utc_now(),
        "site": "Lautaro",
        "plant": "Planta1",
        "area": signal.area,
        "equipment": signal.equipment,
        "tag": signal.tag,
        "variable": signal.variable,
        "value": value_for(signal, scenario, tick),
        "unit": signal.unit,
        "quality": "GOOD",
        "source": signal.source,
        "scenario": scenario,
    }

    for field in (
        "from_node",
        "to_node",
        "fluid",
        "unit_generator",
        "operating_condition",
        "source_sheet",
        "stage",
    ):
        value = getattr(signal, field)
        if value:
            data[field] = value

    return data
