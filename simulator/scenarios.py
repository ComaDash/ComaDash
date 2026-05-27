import math


SCENARIOS = {
    "normal",
    "fouling_caldera",
    "humedad_biomasa_alta",
    "perdida_vapor_condensado",
    "desbalance_turbina",
    "cavitacion_bomba",
    "combustion_inestable",
}


def ramp(tick: int, max_value: float = 1.0) -> float:
    return min(max_value, tick / 60.0)


def multiplier(scenario: str, variable: str, tick: int) -> float:
    r = ramp(tick)
    if scenario == "fouling_caldera":
        return {
            "TemperaturaEscape": 1 + 0.18 * r,
            "PresionDiferencial": 1 + 0.45 * r,
            "ConsumoBiomasa": 1 + 0.10 * r,
            "PotenciaMW": 1 - 0.07 * r,
            "O2": 1 - 0.08 * r,
            "CO": 1 + 0.55 * r,
        }.get(variable, 1.0)
    if scenario == "humedad_biomasa_alta":
        return {
            "HumedadBiomasa": 1 + 0.32 * r,
            "ConsumoBiomasa": 1 + 0.16 * r,
            "PotenciaMW": 1 - 0.10 * r,
            "TemperaturaEscape": 1 - 0.04 * r,
            "CO": 1 + 0.25 * r,
        }.get(variable, 1.0)
    if scenario == "perdida_vapor_condensado":
        return {
            "Flujo": 1 + 0.20 * r,
            "PotenciaMW": 1 - 0.06 * r,
        }.get(variable, 1.0)
    if scenario == "desbalance_turbina":
        return {
            "VibracionRMS": 1 + 1.4 * r,
            "VibracionFFT1X": 1 + 2.7 * r + 0.15 * math.sin(tick),
            "PotenciaMW": 1 - 0.03 * r,
        }.get(variable, 1.0)
    if scenario == "cavitacion_bomba":
        return {
            "VibracionBombaRMS": 1 + 1.35 * r,
            "VibracionBombaFFTAlta": 1 + 3.8 * r + 0.25 * math.sin(tick * 1.7),
            "PresionDescargaBomba": 1 - 0.18 * r,
            "PotenciaMW": 1 - 0.025 * r,
        }.get(variable, 1.0)
    if scenario == "combustion_inestable":
        return {
            "CO": 1 + 1.35 * r + 0.12 * math.sin(tick * 0.8),
            "O2": 1 - 0.28 * r + 0.06 * math.sin(tick * 0.9),
            "PotenciaMW": 1 - 0.055 * r + 0.015 * math.sin(tick * 0.6),
            "ConsumoBiomasa": 1 + 0.08 * r,
            "TemperaturaEscape": 1 + 0.06 * r,
        }.get(variable, 1.0)
    return 1.0


def offset(scenario: str, area: str, tag: str, variable: str, tick: int) -> float:
    r = ramp(tick)
    if scenario == "perdida_vapor_condensado" and area == "Condensado" and variable == "Flujo":
        return -34.0 * r
    if scenario == "perdida_vapor_condensado" and area in {"AguaIndustrial", "AguaAlimentacion", "AguaDesmineralizada"}:
        return 12.0 * r
    if scenario == "cavitacion_bomba" and area == "AguaAlimentacion" and tag == "FT_2101-1":
        return -14.0 * r
    return 0.0
