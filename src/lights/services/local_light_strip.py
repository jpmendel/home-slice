from typing import Optional
from .light_strip import LightStripService


# Use this version of the class if you are running on something other than
# a Raspberry Pi connected to a physical light strip.
class LocalLightStripService(LightStripService):
    leds: list[tuple[int, int, int]]
    output_file: Optional[str]
    is_started: bool

    def __init__(self, led_count: int, output_file: Optional[str] = None):
        super().__init__()
        self.leds = [(0, 0, 0)] * led_count
        self.output_file = output_file
        self.is_started = False

    def setup(self):
        if self.output_file is not None:
            with open(self.output_file, "w", encoding="utf-8") as output_file:
                led_color_strings = ["0,0,0\n"] * self.led_count()
                output_file.writelines(led_color_strings)
        self.is_started = True

    def led_count(self) -> int:
        return len(self.leds)

    def get_leds(self) -> list[tuple[int, int, int]]:
        leds = []
        if self.output_file is not None:
            with open(self.output_file, "r", encoding="utf-8") as output_file:
                lines = [line.rstrip().split(",") for line in output_file]
                leds = [(int(line[0]), int(line[1]), int(line[2])) for line in lines]
        return leds

    def set_led(self, red: int, green: int, blue: int, index: int):
        if not self.is_started:
            return
        if 0 <= index < self.led_count():
            self.leds[index] = (red, green, blue)

    def update(self):
        if not self.is_started or self.output_file is None:
            return
        with open(self.output_file, "w", encoding="utf-8") as output_file:
            led_color_strings = [f"{r},{g},{b}\n" for (r, g, b) in self.leds]
            output_file.writelines(led_color_strings)
