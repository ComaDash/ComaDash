import numpy as np


def dominant_score(values: list[float]) -> float:
    if len(values) < 8:
        return 0.0
    centered = np.array(values, dtype=float) - float(np.mean(values))
    spectrum = np.abs(np.fft.rfft(centered))
    if len(spectrum) < 2:
        return 0.0
    return round(float(np.max(spectrum[1:]) / max(0.001, np.mean(np.abs(centered)) + 0.001)), 3)
