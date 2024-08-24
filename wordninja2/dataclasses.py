from dataclasses import dataclass


@dataclass
class Segmentation:
    tokens: list[str]
    score: float
