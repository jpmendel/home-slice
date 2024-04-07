import os
from abc import abstractmethod
from typing import List, Tuple

if str(os.environ.get("LIGHTS_PROVIDER")) == "hardware":
    # pylint: disable-all
    from rpi_ws281x import PixelStrip, Color  # type: ignore
else:

    class PixelStrip:
        pass

    class Color:
        pass


class LightStripService:
    def __init__(self):
        pass

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def led_count(self) -> int:
        pass

    @abstractmethod
    def set_led(self, red: int, green: int, blue: int, index: int):
        pass

    @abstractmethod
    def update(self):
        pass

    def set_solid_color(self, red: int, green: int, blue: int):
        for index in range(self.led_count()):
            self.set_led(red, green, blue, index)
        self.update()

    def clear_color(self):
        self.set_solid_color(0, 0, 0)


class HardwareLightStripService(LightStripService):
    pixel_strip: PixelStrip

    def __init__(
        self,
        led_count: int,
        led_pin: int,
        led_channel: int,
        led_frequency: int = 800000,
        led_dma: int = 10,
        led_brightness: int = 255,
        led_invert: bool = False,
    ):
        super(HardwareLightStripService, self).__init__()
        self.pixel_strip = PixelStrip(
            led_count,
            led_pin,
            led_frequency,
            led_dma,
            led_invert,
            led_brightness,
            led_channel,
        )  # type: ignore

    def setup(self):
        self.pixel_strip.begin()  # type: ignore

    def led_count(self) -> int:
        return self.pixel_strip.numPixels()  # type: ignore

    def set_led(self, red: int, green: int, blue: int, index: int):
        color = Color(int(red), int(green), int(blue))  # type: ignore
        self.pixel_strip.setPixelColor(index, color)  # type: ignore

    def update(self):
        self.pixel_strip.show()  # type: ignore


class LocalLightStripService(LightStripService):
    leds: List[Tuple[int, int, int]]
    output_file: str | None
    is_started: bool

    def __init__(self, led_count: int, output_file: str | None = None):
        super(LocalLightStripService, self).__init__()
        self.leds = [(0, 0, 0)] * led_count
        self.output_file = output_file
        self.is_started = False

    def setup(self):
        if self.output_file is not None:
            with open(self.output_file, "w", encoding="utf-8") as output_file:
                led_color_strings = ["(0, 0, 0)\n"] * self.led_count()
                output_file.writelines(led_color_strings)
        self.is_started = True

    def led_count(self) -> int:
        return len(self.leds)

    def set_led(self, red: int, green: int, blue: int, index: int):
        if not self.is_started:
            return
        if 0 <= index < self.led_count():
            self.leds[index] = (red, green, blue)

    def update(self):
        if not self.is_started or self.output_file is None:
            return
        with open(self.output_file, "w", encoding="utf-8") as output_file:
            led_color_strings = [f"({r}, {g}, {b})\n" for (r, g, b) in self.leds]
            output_file.writelines(led_color_strings)
