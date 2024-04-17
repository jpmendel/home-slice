# pylint: disable=import-error
from rpi_ws281x import PixelStrip, Color  # type: ignore

from .light_strip import LightStripService


# We kind of need to ignore all code in this class and just trust that it works.
# The code from the ws281x library can only install properly on the ARM
# processor of a Rasbperry Pi, so it will cause a ton of errors when using
# another architecture for development.
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
        super().__init__()
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

    def get_leds(self) -> list[tuple[int, int, int]]:
        return [(0, 0, 0) for _ in range(0, self.led_count())]

    def set_led(self, red: int, green: int, blue: int, index: int):
        color = Color(int(red), int(green), int(blue))  # type: ignore
        self.pixel_strip.setPixelColor(index, color)  # type: ignore

    def update(self):
        self.pixel_strip.show()  # type: ignore
