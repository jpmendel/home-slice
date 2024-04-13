from typing import Optional, Tuple
from django.db import models


class ColorPattern:
    color: Tuple[int, int, int]
    step: int

    def __init__(self, color: Tuple[int, int, int], step: int):
        self.color = color
        self.step = step


class ColorAnimation:
    colors: list[ColorPattern]
    duration: Optional[float]

    def __init__(self, colors: list[ColorPattern], duration: Optional[float]):
        self.colors = colors
        self.duration = duration


class SequenceColorAnimation(ColorAnimation):
    pass


class FadeColorAnimation(ColorAnimation):
    start: Optional[float]
    end: Optional[float]

    def __init__(
        self,
        colors: list[ColorPattern],
        duration: Optional[float],
        start: Optional[float],
        end: Optional[float],
    ):
        super().__init__(colors, duration)
        self.start = start
        self.end = end


class LinearSweepColorAnimation(ColorAnimation):
    start: Optional[int]
    end: Optional[int]

    def __init__(
        self,
        colors: list[ColorPattern],
        duration: Optional[float],
        start: Optional[int],
        end: Optional[int],
    ):
        super().__init__(colors, duration)
        self.start = start
        self.end = end


class BinarySweepColorAnimation(ColorAnimation):
    start: Optional[int]
    end: Optional[int]

    def __init__(
        self,
        colors: list[ColorPattern],
        duration: Optional[float],
        start: Optional[int],
        end: Optional[int],
    ):
        super().__init__(colors, duration)
        self.start = start
        self.end = end


class SnakeColorAnimation(ColorAnimation):
    start: Optional[int]
    end: Optional[int]
    length: Optional[int]

    def __init__(
        self,
        colors: list[ColorPattern],
        duration: Optional[float],
        start: Optional[int],
        end: Optional[int],
        length: Optional[int],
    ):
        super().__init__(colors, duration)
        self.start = start
        self.end = end
        self.length = length
