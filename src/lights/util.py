from typing import Optional, Tuple
from .models import ColorPatternStep


def color_from_hue(hue: int) -> Tuple[int, int, int]:
    if hue == 0:
        return (0, 0, 0)
    if hue == 255:
        return (255, 255, 255)
    h = hue / 255
    kr = (5 + h * 6) % 6
    kg = (3 + h * 6) % 6
    kb = (1 + h * 6) % 6

    r = round((1 - max(min(kr, 4 - kr, 1), 0)) * 255)
    g = round((1 - max(min(kg, 4 - kg, 1), 0)) * 255)
    b = round((1 - max(min(kb, 4 - kb, 1), 0)) * 255)
    return (r, g, b)


def pattern_from_colors(colors: list[str]) -> list[ColorPatternStep]:
    pattern: list[ColorPatternStep] = []
    current: Optional[int] = None
    step = 0
    for color in colors:
        hue = int(color)
        if hue != current:
            if current is not None:
                rgb = color_from_hue(current)
                pattern.append(ColorPatternStep(rgb, step))
                step = 0
            current = hue
        step += 1
    if current is not None:
        rgb = color_from_hue(current)
        pattern.append(ColorPatternStep(rgb, step))
    return pattern
