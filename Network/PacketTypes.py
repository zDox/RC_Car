from dataclasses import dataclass


@dataclass
class Steering:
    angle: float


@dataclass
class Acceleration:
    speed: int
    time: float


@dataclass
class TelemetryData:
    speed: int
    angle: float
