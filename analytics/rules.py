from datetime import datetime, timezone
from uuid import uuid4

from fft import dominant_score
from recommendations import RECOMMENDATIONS
from window_store import WindowStore


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def anomaly(kind: str, severity: str, score: float, evidence: str, impacted_kpis: str) -> dict:
    rec = RECOMMENDATIONS[kind]
    return {
        "anomaly_id": f"ANOM-{uuid4().hex[:8]}",
        "timestamp": now(),
        "type": kind,
        "severity": severity,
        "equipment": rec["equipment"],
        "score": round(score, 3),
        "message": evidence,
        "probable_cause": rec["cause"],
        "impacted_kpis": impacted_kpis,
        "detector": "threshold_trend_fft",
    }


def evaluate(store: WindowStore) -> list[dict]:
    temp = store.latest_value("TemperaturaEscape")
    dp = store.latest_value("PresionDiferencial")
    power = store.latest_value("PotenciaMW")
    humidity = store.latest_value("HumedadBiomasa")
    biomass = store.latest_value("ConsumoBiomasa")
    co = store.latest_value("CO")
    o2 = store.latest_value("O2", 6.0)
    steam = _latest_tag_value(store, "FT_5101-1")
    condensate = _latest_tag_value(store, "FT_3001")
    vibration = store.latest_value("VibracionRMS")
    fft_score = dominant_score(store.series("VibracionFFT1X"))
    pump_vibration = store.latest_value("VibracionBombaRMS")
    pump_pressure = store.latest_value("PresionDescargaBomba", 58.0)
    pump_fft_score = dominant_score(store.series("VibracionBombaFFTAlta"))

    found: list[dict] = []
    if temp > 206 and dp > 24 and power < 22.4:
        found.append(anomaly(
            "fouling_caldera",
            "warning" if temp < 220 else "critical",
            min(1.0, (temp - 190) / 40 + (dp - 18) / 40),
            f"TemperaturaEscape={temp:.1f}°C, PresionDiferencial={dp:.1f}mbar y PotenciaMW={power:.1f}",
            "energia_especifica,costo_biomasa_mwh,oee",
        ))
    if humidity > 48 and biomass > 35 and power < 22:
        found.append(anomaly(
            "humedad_biomasa_alta",
            "warning",
            min(1.0, (humidity - 39) / 16),
            f"HumedadBiomasa={humidity:.1f}% aumenta consumo {biomass:.1f} ton/h y baja potencia {power:.1f} MW",
            "throughput_biomasa,energia_ton,costo_biomasa_mwh",
        ))
    if steam > 112 and condensate and condensate < 58:
        found.append(anomaly(
            "perdida_vapor_condensado",
            "critical" if condensate < 52 else "warning",
            min(1.0, (steam - condensate) / 80),
            f"Vapor={steam:.1f} ton/h con condensado FT_3001={condensate:.1f} ton/h",
            "vapor_mwh,condensado_recuperado,costo_operacional",
        ))
    if vibration > 3.4 or (vibration > 3.0 and fft_score > 30):
        found.append(anomaly(
            "desbalance_turbina",
            "critical" if vibration > 4.3 else "warning",
            min(1.0, vibration / 5.0),
            f"VibracionRMS={vibration:.2f} mm/s y score FFT={fft_score:.2f}",
            "mtbf,mttr,oee,horas_detencion_no_programada",
        ))
    if pump_vibration > 2.6 and (pump_pressure < 52 or pump_fft_score > 28):
        found.append(anomaly(
            "cavitacion_bomba",
            "critical" if pump_vibration > 3.4 or pump_pressure < 48 else "warning",
            min(1.0, pump_vibration / 4.0 + max(0.0, 55 - pump_pressure) / 30),
            f"VibracionBombaRMS={pump_vibration:.2f} mm/s, PresionDescargaBomba={pump_pressure:.1f} bar y score FFT={pump_fft_score:.2f}",
            "mtbf,mttr,oee,horas_detencion_no_programada,agua_por_mwh",
        ))
    if co > 92 and o2 < 5.2:
        found.append(anomaly(
            "combustion_inestable",
            "critical" if co > 120 or o2 < 4.6 else "warning",
            min(1.0, (co - 60) / 80 + max(0.0, 5.8 - o2) / 6),
            f"CO={co:.1f} ppm con O2={o2:.1f}% indica combustion incompleta",
            "energia_por_ton_biomasa,costo_biomasa_mwh,oee",
        ))
    return found


def _latest_tag_value(store: WindowStore, tag: str) -> float:
    for points in store.values.values():
        for point in reversed(points):
            if point.get("tag") == tag:
                return float(point.get("value", 0.0))
    return 0.0
