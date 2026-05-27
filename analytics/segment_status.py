from recommendations import RECOMMENDATIONS
from segments import SEGMENT_BY_TAG, confidence_for, context_for, quality_for
from window_store import WindowStore


WATER_TAGS = {"FT_5001", "FT_2101-1", "FT_5002", "FT_5101-1", "FT_3001", "TIC_5101-1"}


def current_segment_status(store: WindowStore) -> list[dict]:
    points = [_latest_tag_point(store, tag) for tag in WATER_TAGS]
    points = [point for point in points if point]
    if not points:
        return []

    by_tag = {point.get("tag", ""): point for point in points}
    steam = _value(by_tag.get("FT_5101-1"))
    condensate = _value(by_tag.get("FT_3001"))
    feedwater = _value(by_tag.get("FT_2101-1"))
    makeup = _value(by_tag.get("FT_5002"))
    intake = _value(by_tag.get("FT_5001"))
    steam_temp = _value(by_tag.get("TIC_5101-1"))

    recovery_gap = max(0.0, steam - condensate)
    recovery_ratio = condensate / max(0.1, steam)
    water_excess = max(0.0, intake + makeup - feedwater)
    thermal_gap = max(0.0, 505.0 - steam_temp)

    statuses = []
    for point in points:
        tag = point.get("tag", "")
        context = context_for(point)
        quality = quality_for(point, context)
        risk_score, reason, problem, cost = _score_tag(tag, point, recovery_gap, recovery_ratio, water_excess, thermal_gap)
        rec = RECOMMENDATIONS["perdida_vapor_condensado"]
        if problem == "well_water_thermal_degradation":
            cause = "Posible degradacion termica; confirmar temperatura/caudal contra fuente real antes de actuar"
            action = "Revisar intercambio termico, calidad de agua y tendencia de temperatura del vapor"
        else:
            cause = rec["cause"]
            action = rec["action"]
        if quality != "GOOD":
            risk_score = max(risk_score, 35.0)
            reason = f"{reason}; calidad={quality}"

        statuses.append(
            {
                **context,
                "tag": tag,
                "quality": quality,
                "status": _status(risk_score),
                "risk_score": round(risk_score, 1),
                "reason": reason,
                "impacted_problem": problem or context.get("impacted_problem", "excessive_water_loss"),
                "recommendation_cause": cause,
                "recommendation_link": action,
                "cost_efficiency_impact": cost,
                "value": _value(point),
                "confidence": confidence_for(quality, context),
            }
        )

    return sorted(statuses, key=lambda item: item["risk_score"], reverse=True)


def _score_tag(tag: str, point: dict, recovery_gap: float, recovery_ratio: float, water_excess: float, thermal_gap: float) -> tuple[float, str, str, str]:
    if tag == "FT_3001":
        score = _clamp(max(0.0, 0.72 - recovery_ratio) / 0.32 * 100.0)
        return (
            score,
            f"Retorno de condensado bajo: recuperacion {recovery_ratio * 100:.1f}% y brecha vapor-condensado {recovery_gap:.1f} ton/h",
            "excessive_water_loss",
            f"Sobrecosto termico estimado por reposicion/condensado: {recovery_gap:.1f} ton/h de brecha",
        )
    if tag == "FT_5101-1":
        score = _clamp(max(0.0, recovery_gap - 25.0) / 35.0 * 85.0)
        return (score, f"Vapor generado excede retorno de condensado por {recovery_gap:.1f} ton/h", "excessive_water_loss", "Mayor vapor por MWh y menor recuperacion de calor")
    if tag in {"FT_5001", "FT_5002", "FT_2101-1"}:
        score = _clamp(max(0.0, water_excess - 45.0) / 55.0 * 75.0)
        return (score, f"Reposicion/captacion por sobre alimentacion efectiva: exceso simplificado {water_excess:.1f} m3/h", "excessive_water_loss", "Mayor agua por MWh; balance simplificado sin conversion completa")
    if tag == "TIC_5101-1":
        score = _clamp(thermal_gap / 25.0 * 70.0)
        return (score, f"Temperatura de vapor bajo referencia demo por {thermal_gap:.1f} °C", "well_water_thermal_degradation", "Menor calidad termica; baja confianza hasta integrar fuente historica")
    return (0.0, "Segmento monitoreado sin desviacion relevante", SEGMENT_BY_TAG.get(tag, {}).get("impacted_problem", "excessive_water_loss"), "Sin impacto estimado")


def _latest_tag_point(store: WindowStore, tag: str) -> dict | None:
    for points in store.values.values():
        for point in reversed(points):
            if point.get("tag") == tag:
                return point
    return None


def _value(point: dict | None) -> float:
    if not point:
        return 0.0
    return float(point.get("value", 0.0))


def _clamp(value: float) -> float:
    return max(0.0, min(100.0, value))


def _status(score: float) -> str:
    if score >= 85:
        return "critical"
    if score >= 65:
        return "warning"
    if score >= 35:
        return "watch"
    return "normal"
