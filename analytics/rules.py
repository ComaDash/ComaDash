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
    steam = _latest_tag_value(store, "FT_5101-1")
    condensate = _latest_tag_value(store, "FT_3001")
    vibration = store.latest_value("VibracionRMS")
    fft_score = dominant_score(store.series("VibracionFFT1X"))

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
    return found


def _latest_tag_value(store: WindowStore, tag: str) -> float:
    for points in store.values.values():
        for point in reversed(points):
            if point.get("tag") == tag:
                return float(point.get("value", 0.0))
    return 0.0
