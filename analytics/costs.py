import os


def env_float(name: str, default: float) -> float:
    try:
        return float(os.getenv(name, str(default)))
    except ValueError:
        return default


def cost_config() -> dict[str, float]:
    return {
        "biomass_per_ton": env_float("COST_BIOMASS_PER_TON", 42.0),
        "water_per_m3": env_float("COST_WATER_PER_M3", 0.9),
        "vapor_loss_per_ton": env_float("COST_VAPOR_LOSS_PER_TON", 8.0),
        "condensate_benefit_per_ton": env_float("CONDENSATE_RECOVERY_BENEFIT_PER_TON", 3.0),
        "power_nominal_mw": env_float("POWER_NOMINAL_MW", 24.0),
    }
