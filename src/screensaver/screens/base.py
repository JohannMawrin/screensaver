from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar

from blessed import Terminal


@dataclass
class Particle:
    x: float
    y: float
    char: str


class Screen[T: Particle](ABC):
    PARTICLE_COUNT: ClassVar[int] = 100

    def __init__(self, term: Terminal) -> None:
        self._term = term
        self._particles = [self._spawn() for _ in range(self.PARTICLE_COUNT)]

    @abstractmethod
    def _spawn(self) -> T:
        pass

    @abstractmethod
    def _update_particle(self, particle: T, dt: float) -> None:
        pass

    def update(self, dt: float) -> None:
        for i, particle in enumerate(self._particles):
            self._update_particle(particle, dt)

            if (
                not (0 <= particle.x < self._term.width)
                or particle.y >= self._term.height
            ):
                new_particle = self._spawn()
                new_particle.y = 0
                self._particles[i] = new_particle

    def render(self) -> str:
        output = [str(self._term.clear)]
        output.extend([
            str(self._term.move_xy(int(p.x), int(p.y)) + p.char)
            for p in self._particles
        ])
        return "".join(output)
