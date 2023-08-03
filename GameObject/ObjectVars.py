from dataclasses import dataclass


@dataclass()
class MoveDirections:
    up = 0
    down = 1
    left = 2
    right = 3