import time
from abc import abstractmethod
from concurrent.futures import ThreadPoolExecutor, Future
from threading import Event as ThreadingEvent
from typing import Tuple
from ..models import (
    ColorPattern,
    ColorAnimation,
    SequenceColorAnimation,
    FadeColorAnimation,
    LinearSweepColorAnimation,
    BinarySweepColorAnimation,
    SnakeColorAnimation,
)


class LightStripService:
    task_executor: ThreadPoolExecutor
    animation: Future | None
    cancel_event: ThreadingEvent | None

    def __init__(self):
        self.task_executor = ThreadPoolExecutor(max_workers=1)
        self.animation = None
        self.cancel_event = None

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

    def create_pattern(self, colors: list[ColorPattern]) -> list[Tuple[int, int, int]]:
        leds = []
        color_index = 0
        color_step = 0
        for _ in range(self.led_count()):
            pattern = colors[color_index]
            if color_step == pattern.step - 1:
                color_step = 0
                color_index = (color_index + 1) % len(colors)
            else:
                color_step += 1
            leds.append(pattern.color)
        return leds

    def set_pattern(self, colors: list[ColorPattern]):
        pattern = self.create_pattern(colors)
        for index, (r, g, b) in enumerate(pattern):
            self.set_led(r, g, b, index)
        self.update()

    def set_animation(self, animations: list[ColorAnimation], repeat: int = 0):
        self.cancel_event = ThreadingEvent()
        self.task_executor.submit(self.play_animations, animations, repeat)

    def play_animations(self, animations: list[ColorAnimation], repeat: int = 0):
        for _ in range(repeat + 1):
            if self.cancel_event and self.cancel_event.is_set():
                break
            for anim in animations:
                if isinstance(anim, SequenceColorAnimation):
                    self.play_sequence_animation(
                        anim.colors,
                        anim.duration or 1,
                    )
                elif isinstance(anim, FadeColorAnimation):
                    self.play_fade_animation(
                        anim.colors,
                        anim.duration or 1,
                        anim.start or 0,
                        anim.end or 1,
                    )
                elif isinstance(anim, LinearSweepColorAnimation):
                    self.play_linear_sweep_animation(
                        anim.colors,
                        anim.duration or 1,
                        anim.start or 0,
                        anim.end or self.led_count(),
                    )
                elif isinstance(anim, BinarySweepColorAnimation):
                    self.play_binary_sweep_animation(
                        anim.colors,
                        anim.duration or 1,
                        anim.start or 0,
                        anim.end or self.led_count(),
                    )
                elif isinstance(anim, SnakeColorAnimation):
                    self.play_snake_animation(
                        anim.colors,
                        anim.duration or 1,
                        anim.start or 0,
                        anim.end or self.led_count(),
                        anim.length or 5,
                    )
        self.cancel_event = None

    def play_sequence_animation(self, colors: list[ColorPattern], duration: float):
        self.set_pattern(colors)
        time.sleep(duration)

    def play_fade_animation(
        self,
        colors: list[ColorPattern],
        duration: float,
        start: float,
        end: float,
    ):
        fade_step = (end - start) / 10.0
        step_duration = duration / 10.0
        current_fade = start
        pattern = self.create_pattern(colors)
        if start <= end:
            condition = lambda x: x <= end
        else:
            condition = lambda x: x >= end
        while condition(current_fade):
            fade_amount = current_fade
            if fade_amount < 0.0:
                fade_amount = 0
            elif fade_amount > 1.0:
                fade_amount = 1
            for index, (r, g, b) in enumerate(pattern):
                self.set_led(
                    int(r * fade_amount),
                    int(g * fade_amount),
                    int(b * fade_amount),
                    index,
                )
            self.update()
            current_fade += fade_step
            time.sleep(step_duration)

    def play_linear_sweep_animation(
        self,
        colors: list[ColorPattern],
        duration: float,
        start: int,
        end: int,
    ):
        if start <= end:
            start_idx = max(start, 0)
            end_idx = min(end, self.led_count())
            iter_step = 1
        else:
            start_idx = min(start, self.led_count()) - 1
            end_idx = max(end, 0) - 1
            iter_step = -1
        step_duration = duration / abs(start_idx - end_idx)
        pattern = self.create_pattern(colors)
        for index in range(start_idx, end_idx, iter_step):
            if self.cancel_event and self.cancel_event.is_set():
                break
            r, g, b = pattern[index]
            self.set_led(r, g, b, index)
            self.update()
            time.sleep(step_duration)

    def play_binary_sweep_animation(
        self,
        colors: list[ColorPattern],
        duration: float,
        start: int,
        end: int,
    ):
        if start <= end:
            start_idx = max(start, 0)
            end_idx = min(end, self.led_count())
        else:
            start_idx = max(end, 0)
            end_idx = min(start, self.led_count())
        sweep_range = end_idx - start_idx
        center_pos = start_idx + sweep_range // 2 - 1
        step_duration = duration / (sweep_range / 2)
        pattern = self.create_pattern(colors)
        start_pos = center_pos
        end_pos = center_pos
        while start_pos >= start_idx or end_pos < end_idx:
            if self.cancel_event and self.cancel_event.is_set():
                break
            if start_pos >= start_idx:
                r, g, b = pattern[start_pos]
                self.set_led(r, g, b, start_pos)
                start_pos -= 1
            if end_pos < end_idx:
                r, g, b = pattern[end_pos]
                self.set_led(r, g, b, end_pos)
                end_pos += 1
            self.update()
            time.sleep(step_duration)

    def play_snake_animation(
        self,
        colors: list[ColorPattern],
        duration: float,
        start: int,
        end: int,
        length: int,
    ):
        if start <= end:
            start_idx = max(start, 0)
            end_idx = min(end, self.led_count())
            head_pos = start_idx
            tail_pos = start_idx - length
            iter_step = 1
            condition = lambda x: x <= end_idx
            is_within_bounds = lambda x: start_idx <= x < end_idx
        else:
            start_idx = min(start, self.led_count()) - 1
            end_idx = max(end, 0) - 1
            head_pos = start_idx
            tail_pos = start_idx + length
            iter_step = -1
            condition = lambda x: x >= end_idx
            is_within_bounds = lambda x: end_idx < x <= start_idx
        step_duration = duration / (abs(start_idx - end_idx) + length)
        pattern = self.create_pattern(colors)
        while condition(tail_pos):
            if self.cancel_event and self.cancel_event.is_set():
                break
            if is_within_bounds(head_pos):
                r, g, b = pattern[head_pos]
                self.set_led(r, g, b, head_pos)
            if is_within_bounds(tail_pos):
                self.set_led(0, 0, 0, tail_pos)
            head_pos += iter_step
            tail_pos += iter_step
            self.update()
            time.sleep(step_duration)

    def cancel_animation(self):
        if self.animation is not None and self.cancel_event is not None:
            self.animation.cancel()
            self.cancel_event.set()
            time.sleep(0.1)
