from fft import dominant_score
from recommendations import RECOMMENDATIONS
from window_store import WindowStore


def current_asset_risk(store: WindowStore) -> list[dict]:
    temp = store.latest_value("TemperaturaEscape")
    dp = store.latest_value("PresionDiferencial")
    power = store.latest_value("PotenciaMW", 23.0)
    humidity = store.latest_value("HumedadBiomasa")
    biomass = store.latest_value("ConsumoBiomasa")
    co = store.latest_value("CO")
    o2 = store.latest_value("O2", 6.0)
    vibration = store.latest_value("VibracionRMS")
    fft_score = dominant_score(store.series("VibracionFFT1X"))
    pump_vibration = store.latest_value("VibracionBombaRMS")
    pump_fft = dominant_score(store.series("VibracionBombaFFTAlta"))
    pump_pressure = store.latest_value("PresionDescargaBomba", 58.0)
    steam = _latest_tag_value(store, "FT_5101-1")
    condensate = _latest_tag_value(store, "FT_3001")

    boiler_fouling = _score(
        (temp - 190.0) / 32.0 * 45.0
        + (dp - 18.0) / 10.0 * 40.0
        + max(0.0, 23.0 - power) / 2.0 * 15.0
    )
    biomass_quality = _score((humidity - 39.0) / 13.0 * 70.0 + (biomass - 32.0) / 5.0 * 30.0)
    combustion = _score((co - 60.0) / 55.0 * 70.0 + max(0.0, 5.5 - o2) / 1.5 * 30.0)
    thermal_circuit = _score(max(0.0, steam - condensate - 35.0) / 35.0 * 100.0)
    turbine = _score((vibration - 2.1) / 2.2 * 75.0 + max(0.0, fft_score - 15.0) / 25.0 * 25.0)
    pump = _score((pump_vibration - 1.6) / 1.8 * 65.0 + max(0.0, pump_fft - 12.0) / 28.0 * 20.0 + max(0.0, 56.0 - pump_pressure) / 9.0 * 15.0)

    return sorted(
        [
            _risk("CalderaBiomasa01", "Caldera", boiler_fouling, "fouling_caldera", f"Temp={temp:.1f}C, DP={dp:.1f}mbar, Potencia={power:.1f}MW"),
            _risk("SistemaBiomasa", "Combustible", biomass_quality, "humedad_biomasa_alta", f"Humedad={humidity:.1f}%, Biomasa={biomass:.1f}ton/h"),
            _risk("CombustionCaldera", "Combustion", combustion, "combustion_inestable", f"CO={co:.1f}ppm, O2={o2:.1f}%"),
            _risk("CircuitoAguaVaporCondensado", "Servicios", thermal_circuit, "perdida_vapor_condensado", f"Vapor={steam:.1f}ton/h, Condensado={condensate:.1f}ton/h"),
            _risk("Turbina", "Generacion", turbine, "desbalance_turbina", f"Vibracion={vibration:.2f}mm/s, FFT={fft_score:.1f}"),
            _risk("BombaAguaAlimentacion", "AguaAlimentacion", pump, "cavitacion_bomba", f"VibBomba={pump_vibration:.2f}mm/s, Presion={pump_pressure:.1f}bar"),
        ],
        key=lambda item: item["risk_score"],
        reverse=True,
    )


def _risk(equipment: str, area: str, risk_score: float, kind: str, reason: str) -> dict:
    rec = RECOMMENDATIONS[kind]
    return {
        "equipment": equipment,
        "area": area,
        "risk_score": round(risk_score, 1),
        "status": _status(risk_score),
        "severity": _severity(risk_score),
        "probable_anomaly": kind,
        "dominant_signal": reason,
        "risk_reason": rec["cause"],
        "suggested_action": rec["action"],
        "expected_impact": rec["impact"],
        "due_minutes": rec["due_minutes"],
    }


def _score(value: float) -> float:
    return max(0.0, min(100.0, value))


def _status(score: float) -> str:
    if score >= 85:
        return "critical"
    if score >= 65:
        return "warning"
    if score >= 35:
        return "watch"
    return "normal"


def _severity(score: float) -> str:
    if score >= 85:
        return "critical"
    if score >= 65:
        return "warning"
    return "info"


def _latest_tag_value(store: WindowStore, tag: str) -> float:
    for points in store.values.values():
        for point in reversed(points):
            if point.get("tag") == tag:
                return float(point.get("value", 0.0))
    return 0.0
