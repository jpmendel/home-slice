import os
from django.apps import AppConfig
from .services.light_strip import LightStripService


class LightsConfig(AppConfig):
    name = "lights"
    light_strip_service: LightStripService

    def ready(self):
        # pylint: disable=import-outside-toplevel
        if str(os.environ.get("LIGHTS_PROVIDER")) == "hardware":
            from .services.hardware_light_strip import HardwareLightStripService

            self.light_strip_service = HardwareLightStripService(
                led_count=60,
                led_pin=18,
                led_channel=0,
                led_brightness=20,
            )
        else:
            from .services.local_light_strip import LocalLightStripService

            self.light_strip_service = LocalLightStripService(
                led_count=30,
                output_file=os.path.abspath(
                    os.path.join(__file__, "../local/lights.csv")
                ),
            )

        self.light_strip_service.setup()
