from typing import Tuple
from django.db import models


class ColorPattern:
    color: Tuple[int, int, int]
    step: int
