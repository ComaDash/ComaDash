from costs import cost_config
from window_store import WindowStore


def current_kpis(store: WindowStore) -> list[dict]:
    cfg = cost_config()
    power = max(0.1, store.latest_value("PotenciaMW", cfg["power_nominal_mw"]))
    biomass = store.latest_value("ConsumoBiomasa", 0.0)
    water = _latest_area_value(store, "AguaIndustrial")
    steam = _latest_tag_value(store, "FT_5101-1")
    condensate = _latest_tag_value(store, "FT_3001")
    vibration = store.latest_value("VibracionRMS", 2.1)
    energy_per_ton = power / max(0.1, biomass)
    condensate_ratio = condensate / max(0.1, steam)
    oee = min(1.0, (power / cfg["power_nominal_mw"]) * (1.0 if vibration < 3.2 else 0.88) * 0.98)
    biomass_cost = biomass * cfg["biomass_per_ton"] / power
    water_mwh = water / power
    vapor_mwh = steam / power
    water_vapor_cost = water * cfg["water_per_m3"] + max(0.0, steam - condensate) * cfg["vapor_loss_per_ton"] - condensate * cfg["condensate_benefit_per_ton"]
    downtime = 0.25 if vibration > 4.0 else 0.0

    return [
        kpi("energia_generada_mwh_h", power, "MWh/h"),
        kpi("throughput_biomasa_ton_h", biomass, "ton/h"),
        kpi("energia_por_ton_biomasa", energy_per_ton, "MWh/ton"),
        kpi("oee", oee * 100, "%"),
        kpi("mtbf_horas_demo", 120 if downtime == 0 else 36, "h"),
        kpi("mttr_horas_demo", 2.5 if downtime == 0 else 4.0, "h"),
        kpi("horas_detencion_no_programada", downtime, "h"),
        kpi("costo_biomasa_por_mwh", biomass_cost, "demo_currency/MWh"),
        kpi("agua_por_mwh", water_mwh, "m3/MWh"),
        kpi("vapor_por_mwh", vapor_mwh, "ton/MWh"),
        kpi("condensado_recuperado", condensate_ratio * 100, "%"),
        kpi("costo_agua_vapor_condensado", water_vapor_cost, "demo_currency/h"),
        kpi("costo_operacional_estimado", water_vapor_cost + biomass * cfg["biomass_per_ton"], "demo_currency/h"),
    ]


def kpi(name: str, value: float, unit: str) -> dict:
    return {"name": name, "value": round(float(value), 3), "unit": unit}


def _latest_tag_value(store: WindowStore, tag: str) -> float:
    for points in store.values.values():
        for point in reversed(points):
            if point.get("tag") == tag:
                return float(point.get("value", 0.0))
    return 0.0


def _latest_area_value(store: WindowStore, area: str) -> float:
    for points in store.values.values():
        for point in reversed(points):
            if point.get("area") == area:
                return float(point.get("value", 0.0))
    return 0.0
