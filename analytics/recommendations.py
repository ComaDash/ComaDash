from datetime import datetime, timedelta, timezone
from uuid import uuid4


RECOMMENDATIONS = {
    "fouling_caldera": {
        "equipment": "CalderaBiomasa01",
        "cause": "Ensuciamiento progresivo por ceniza o escoria en superficies de intercambio",
        "action": "Programar limpieza de caldera y revisar calidad/combustión de biomasa antes del siguiente turno",
        "impact": "Reduce biomasa por MWh y evita caída de potencia",
        "due_minutes": 480,
    },
    "humedad_biomasa_alta": {
        "equipment": "SistemaBiomasa",
        "cause": "Humedad alta de biomasa reduce poder calorífico y estabilidad de combustión",
        "action": "Separar lote húmedo, ajustar mezcla y revisar condiciones de acopio",
        "impact": "Recupera energía específica y reduce consumo de biomasa",
        "due_minutes": 180,
    },
    "perdida_vapor_condensado": {
        "equipment": "CircuitoAguaVaporCondensado",
        "cause": "Pérdida de vapor/condensado o trampa/válvula defectuosa",
        "action": "Inspeccionar retorno de condensado, trampas de vapor y líneas críticas con TAGs FT_5101-1/FT_3001",
        "impact": "Reduce reposición de agua, vapor por MWh y sobrecosto térmico",
        "due_minutes": 240,
    },
    "desbalance_turbina": {
        "equipment": "Turbina",
        "cause": "Desbalance o desalineación mecánica con componente 1X elevada",
        "action": "Programar inspección vibracional, balanceo y revisión de rodamientos",
        "impact": "Evita detención no programada y protege disponibilidad/OEE",
        "due_minutes": 120,
    },
    "cavitacion_bomba": {
        "equipment": "BombaAguaAlimentacion",
        "cause": "Posible cavitación o restricción hidráulica en bomba de agua de alimentación",
        "action": "Revisar NPSH, succión, filtro, válvulas y presión de descarga de la bomba",
        "impact": "Evita daño mecánico, pérdida de caudal y detención del circuito agua-vapor",
        "due_minutes": 90,
    },
    "combustion_inestable": {
        "equipment": "CombustionCaldera",
        "cause": "Relación aire/combustible inestable con CO elevado u O2 fuera de banda",
        "action": "Ajustar aire de combustión, revisar alimentación de biomasa y verificar analizadores O2/CO",
        "impact": "Mejora eficiencia térmica y reduce emisiones por combustión incompleta",
        "due_minutes": 60,
    },
}


def build(anomaly: dict) -> dict:
    cfg = RECOMMENDATIONS[anomaly["type"]]
    due = datetime.now(timezone.utc) + timedelta(minutes=cfg["due_minutes"])
    return {
        "recommendation_id": f"REC-{uuid4().hex[:8]}",
        "anomaly_id": anomaly["anomaly_id"],
        "equipment": cfg["equipment"],
        "severity": anomaly["severity"],
        "probable_cause": cfg["cause"],
        "suggested_action": cfg["action"],
        "due_before": due.isoformat(timespec="minutes").replace("+00:00", "Z"),
        "due_minutes": cfg["due_minutes"],
        "expected_impact": cfg["impact"],
        "impacted_kpis": anomaly.get("impacted_kpis", ""),
        "ack_status": "open",
    }
