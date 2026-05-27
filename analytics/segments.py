SEGMENT_BY_TAG = {
    "FT_5001": {
        "segment_id": "agua-industrial-captacion",
        "from_node": "Pozo/Captacion",
        "to_node": "Estanque agua industrial",
        "fluid": "Agua Industrial",
        "unit_generator": "UG1",
        "operating_condition": "Media carga",
        "variable": "Flujo",
        "unit": "m3/h",
        "source": "digital-twin+xlsx-reference",
        "source_sheet": "UG_1_MT",
        "stage": "Captacion",
        "impacted_problem": "excessive_water_loss",
    },
    "FT_2101-1": {
        "segment_id": "agua-alimentacion-ecoi-caldera",
        "from_node": "ECOI",
        "to_node": "Caldera",
        "fluid": "Agua Alimentacion",
        "unit_generator": "UG1",
        "operating_condition": "Media carga",
        "variable": "Flujo",
        "unit": "m3/h",
        "source": "digital-twin+xlsx-reference",
        "source_sheet": "UG_1_MT",
        "stage": "Alimentacion caldera",
        "impacted_problem": "well_water_thermal_degradation",
    },
    "FT_5002": {
        "segment_id": "agua-desmineralizada-makeup",
        "from_node": "Osmosis",
        "to_node": "Make-up circuito agua-vapor",
        "fluid": "Agua Desmineralizada",
        "unit_generator": "UG1",
        "operating_condition": "Media carga",
        "variable": "Flujo",
        "unit": "m3/h",
        "source": "digital-twin+xlsx-reference",
        "source_sheet": "UG_1_MT",
        "stage": "Reposicion",
        "impacted_problem": "excessive_water_loss",
    },
    "FT_5101-1": {
        "segment_id": "vapor-sobrecalentado-caldera-turbina",
        "from_node": "Caldera",
        "to_node": "Turbina",
        "fluid": "Vapor Sobrecalentado",
        "unit_generator": "UG1",
        "operating_condition": "Media carga",
        "variable": "Flujo",
        "unit": "ton/h",
        "source": "digital-twin+xlsx-reference",
        "source_sheet": "UG_1_MT",
        "stage": "Generacion vapor",
        "impacted_problem": "excessive_water_loss",
    },
    "TIC_5101-1": {
        "segment_id": "temperatura-vapor-sobrecalentado",
        "from_node": "Sobrecalentador",
        "to_node": "Header vapor",
        "fluid": "Vapor Sobrecalentado",
        "unit_generator": "UG1",
        "operating_condition": "Media carga",
        "variable": "Temperatura",
        "unit": "°C",
        "source": "digital-twin+xlsx-reference",
        "source_sheet": "UG_1_MT",
        "stage": "Calidad termica",
        "impacted_problem": "well_water_thermal_degradation",
    },
    "FT_3001": {
        "segment_id": "condensado-retorno-tanque",
        "from_node": "Proceso/retorno",
        "to_node": "Tanque condensado",
        "fluid": "Condensado",
        "unit_generator": "UG1",
        "operating_condition": "Media carga",
        "variable": "Flujo",
        "unit": "ton/h",
        "source": "digital-twin+xlsx-reference",
        "source_sheet": "UG_1_MT",
        "stage": "Retorno condensado",
        "impacted_problem": "excessive_water_loss",
    },
}


def context_for(point: dict) -> dict:
    tag = point.get("tag", "")
    context = dict(SEGMENT_BY_TAG.get(tag, {}))
    if not context and point.get("area") in {"AguaIndustrial", "AguaAlimentacion", "AguaDesmineralizada", "VaporSobrecalentado", "Condensado"}:
        context = {
            "segment_id": f"{point.get('area', 'unknown')}-{point.get('equipment', 'unknown')}-{point.get('variable', 'unknown')}",
            "from_node": point.get("from_node", "unknown"),
            "to_node": point.get("to_node", point.get("equipment", "unknown")),
            "fluid": point.get("fluid", point.get("area", "unknown")),
            "unit_generator": point.get("unit_generator", "unknown"),
            "operating_condition": point.get("operating_condition", "unknown"),
            "variable": point.get("variable", "unknown"),
            "unit": point.get("unit", ""),
            "source": point.get("source", "unknown"),
            "source_sheet": point.get("source_sheet", ""),
            "stage": point.get("stage", ""),
            "impacted_problem": "data_quality_context",
        }

    for key in ("from_node", "to_node", "fluid", "unit_generator", "operating_condition", "source", "source_sheet", "stage"):
        if point.get(key):
            context[key] = point[key]
    if point.get("unit"):
        context["unit"] = point["unit"]
    if point.get("variable"):
        context["variable"] = point["variable"]

    return context


def quality_for(point: dict, context: dict) -> str:
    if not point:
        return "MISSING"
    quality = str(point.get("quality", "UNKNOWN")).upper()
    if quality != "GOOD":
        return quality
    if not context:
        return "NO_SEGMENT_CONTEXT"
    if point.get("value") is None:
        return "MISSING_VALUE"
    return "GOOD"


def confidence_for(quality: str, context: dict) -> float:
    if quality == "GOOD" and context.get("source_sheet"):
        return 0.95
    if quality == "GOOD":
        return 0.8
    if quality in {"NO_SEGMENT_CONTEXT", "UNKNOWN"}:
        return 0.45
    return 0.25
