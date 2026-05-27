from dataclasses import dataclass


@dataclass(frozen=True)
class Signal:
    area: str
    equipment: str
    variable: str
    unit: str
    baseline: float
    noise: float
    tag: str = ""
    from_node: str = ""
    to_node: str = ""
    fluid: str = ""
    unit_generator: str = ""
    operating_condition: str = ""
    source: str = "digital-twin"
    source_sheet: str = ""
    stage: str = ""


SIGNALS: list[Signal] = [
    Signal("Caldera", "Gases", "TemperaturaEscape", "°C", 184.0, 1.8),
    Signal("Caldera", "Gases", "PresionDiferencial", "mbar", 18.0, 0.4),
    Signal("Caldera", "Combustion", "HumedadBiomasa", "%", 39.0, 0.8),
    Signal("Caldera", "Combustion", "ConsumoBiomasa", "ton/h", 32.0, 0.5),
    Signal("Caldera", "Combustion", "O2", "%", 6.0, 0.2),
    Signal("Caldera", "Combustion", "CO", "ppm", 55.0, 4.0),
    Signal("Generacion", "Generador", "PotenciaMW", "MW", 23.0, 0.25),
    Signal("Generacion", "Turbina", "VibracionRMS", "mm/s", 2.1, 0.08),
    Signal("Generacion", "Turbina", "VibracionFFT1X", "mm/s", 0.7, 0.04),
    Signal("AguaIndustrial", "Captacion", "Flujo", "m3/h", 125.0, 2.5, "FT_5001", "Pozo/Captacion", "Estanque agua industrial", "Agua Industrial", "UG1", "Media carga", "digital-twin+xlsx-reference", "UG_1_MT", "Captacion"),
    Signal("AguaAlimentacion", "ECOI", "Flujo", "m3/h", 91.0, 1.5, "FT_2101-1", "ECOI", "Caldera", "Agua Alimentacion", "UG1", "Media carga", "digital-twin+xlsx-reference", "UG_1_MT", "Alimentacion caldera"),
    Signal("AguaAlimentacion", "BombaAlimentacion", "VibracionBombaRMS", "mm/s", 1.6, 0.08, "PMP_AF_01", "Succion bomba AF", "Descarga bomba AF", "Agua Alimentacion", "UG1", "Media carga", "digital-twin", "", "Bombeo"),
    Signal("AguaAlimentacion", "BombaAlimentacion", "VibracionBombaFFTAlta", "mm/s", 0.45, 0.03, "PMP_AF_01", "Succion bomba AF", "Descarga bomba AF", "Agua Alimentacion", "UG1", "Media carga", "digital-twin", "", "Bombeo"),
    Signal("AguaAlimentacion", "BombaAlimentacion", "PresionDescargaBomba", "bar", 58.0, 0.6, "PT_AF_01", "Bomba alimentacion", "Colector descarga", "Agua Alimentacion", "UG1", "Media carga", "digital-twin", "", "Bombeo"),
    Signal("AguaDesmineralizada", "Osmosis", "Flujo", "m3/h", 47.0, 1.0, "FT_5002", "Osmosis", "Make-up circuito agua-vapor", "Agua Desmineralizada", "UG1", "Media carga", "digital-twin+xlsx-reference", "UG_1_MT", "Reposicion"),
    Signal("VaporSobrecalentado", "Caldera", "Flujo", "ton/h", 104.0, 1.6, "FT_5101-1", "Caldera", "Turbina", "Vapor Sobrecalentado", "UG1", "Media carga", "digital-twin+xlsx-reference", "UG_1_MT", "Generacion vapor"),
    Signal("VaporSobrecalentado", "Caldera", "Temperatura", "°C", 512.0, 2.0, "TIC_5101-1", "Sobrecalentador", "Header vapor", "Vapor Sobrecalentado", "UG1", "Media carga", "digital-twin+xlsx-reference", "UG_1_MT", "Calidad termica"),
    Signal("Condensado", "Retorno", "Flujo", "ton/h", 71.0, 1.2, "FT_3001", "Proceso/retorno", "Tanque condensado", "Condensado", "UG1", "Media carga", "digital-twin+xlsx-reference", "UG_1_MT", "Retorno condensado"),
]


def topic(prefix: str, signal: Signal) -> str:
    parts = [prefix, signal.area, signal.equipment]
    if signal.tag:
        parts.append(signal.tag)
    parts.append(signal.variable)
    return "/".join(parts)
