from contextlib import suppress
from itertools import cycle
from typing import Any, ClassVar

from blessed import Terminal
from fpstimer import FPSTimer

from screensaver.screens import Rain, Screen


class Screensaver:
    FPS: ClassVar[int] = 60
    SCREENS: ClassVar[list[type[Screen[Any]]]] = [Rain]

    def __init__(self, term: Terminal) -> None:
        self._term = term
        self._screen_iterator = cycle(self.SCREENS)
        self._current_screen = next(self._screen_iterator)(self._term)

    def run(self) -> None:
        timer = FPSTimer()
        dt = 1 / self.FPS

        with self._term.cbreak(), self._term.fullscreen(), self._term.hidden_cursor():
            while True:
                key = self._term.inkey(timeout=0)
                if key == " ":
                    self._current_screen = next(self._screen_iterator)(self._term)

                self._current_screen.update(dt)

                print(self._current_screen.render(), end="", flush=True)

                dt = timer.sleep()


def main() -> None:
    term = Terminal()

    screensaver = Screensaver(term)

    with suppress(KeyboardInterrupt):
        screensaver.run()


if __name__ == "__main__":
    main()
