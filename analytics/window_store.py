from collections import defaultdict, deque
from dataclasses import dataclass, field


@dataclass
class WindowStore:
    maxlen: int = 120
    values: dict[str, deque[dict]] = field(default_factory=lambda: defaultdict(deque))

    def add(self, point: dict) -> None:
        key = point.get("variable", "unknown")
        bucket = self.values[key]
        bucket.append(point)
        while len(bucket) > self.maxlen:
            bucket.popleft()

    def latest(self, variable: str) -> dict | None:
        bucket = self.values.get(variable)
        return bucket[-1] if bucket else None

    def latest_value(self, variable: str, default: float = 0.0) -> float:
        point = self.latest(variable)
        if not point:
            return default
        return float(point.get("value", default))

    def series(self, variable: str) -> list[float]:
        return [float(p.get("value", 0.0)) for p in self.values.get(variable, [])]
