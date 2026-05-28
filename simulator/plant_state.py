from dataclasses import dataclass


@dataclass
class PlantState:
    scenario: str
    tick: int = 0

    def advance(self) -> int:
        self.tick += 1
        return self.tick
