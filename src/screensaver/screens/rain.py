import random
from dataclasses import dataclass
from typing import NamedTuple, override

from screensaver.screens import Screen
from screensaver.screens.base import Particle


@dataclass
class Raindrop(Particle):
    speed: float


class RaindropType(NamedTuple):
    chars: tuple[str, ...]
    colors: tuple[str, ...]
    speed_range: tuple[int, int]


class Rain(Screen[Raindrop]):
    PARTICLE_COUNT = 150

    TYPES: tuple[RaindropType, ...] = (
        RaindropType(
            chars=("┃", "║", "∫", "█", "╽"),
            colors=("#ffffff", "#f0f8ff", "#f5f5f5", "#e0e0e0", "#edf2f4"),
            speed_range=(90, 120),
        ),
        RaindropType(
            chars=("|", "¦", "j", "┋", "{"),
            colors=("#28628f", "#1b3d52", "#3d85a1", "#55a3bc", "#0f2430"),
            speed_range=(60, 90),
        ),
        RaindropType(
            chars=("·", "⸳", ",", ".", "'", "`"),
            colors=("#363945", "#4a4a4a", "#2c2f33", "#5c6370", "#1e2124"),
            speed_range=(20, 60),
        ),
    )
    WEIGHTS: tuple[int, ...] = (5, 25, 70)

    @override
    def _spawn(self) -> Raindrop:
        [variant] = random.choices(self.TYPES, weights=self.WEIGHTS, k=1)
        color = self._term.color_hex(random.choice(variant.colors))
        return Raindrop(
            x=random.randint(0, self._term.width - 1),
            y=random.randint(0, self._term.height - 1),
            char=color + random.choice(variant.chars),
            speed=random.uniform(*variant.speed_range),
        )

    @override
    def _update_particle(self, particle: Raindrop, dt: float) -> None:
        particle.y += particle.speed * dt
