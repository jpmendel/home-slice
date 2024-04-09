from typing import Tuple
from django.db import models


class ColorPattern:
    color: Tuple[int, int, int]
    step: int

    def __init__(self, color: Tuple[int, int, int], step: int):
        self.color = color
        self.step = step


class ColorAnimation:
    colors: list[ColorPattern]
    duration: float | None

    def __init__(self, colors: list[ColorPattern], duration: float):
        self.colors = colors
        self.duration = duration


class SequenceColorAnimation(ColorAnimation):
    pass


class FadeColorAnimation(ColorAnimation):
    start: float | None
    end: float | None

    def __init__(
        self,
        colors: list[ColorPattern],
        duration: float,
        start: float,
        end: float,
    ):
        super().__init__(colors, duration)
        self.start = start
        self.end = end


class LinearSweepColorAnimation(ColorAnimation):
    start: int | None
    end: int | None

    def __init__(
        self,
        colors: list[ColorPattern],
        duration: float,
        start: int,
        end: int,
    ):
        super().__init__(colors, duration)
        self.start = start
        self.end = end


class BinarySweepColorAnimation(ColorAnimation):
    start: int | None
    end: int | None

    def __init__(
        self,
        colors: list[ColorPattern],
        duration: float,
        start: int,
        end: int,
    ):
        super().__init__(colors, duration)
        self.start = start
        self.end = end


class SnakeColorAnimation(ColorAnimation):
    start: int | None
    end: int | None
    length: int | None

    def __init__(
        self,
        colors: list[ColorPattern],
        duration: float,
        start: int,
        end: int,
        length: int,
    ):
        super().__init__(colors, duration)
        self.start = start
        self.end = end
        self.length = length
