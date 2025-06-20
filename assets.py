"""Image placeholders for CarGame assets.

Edit the paths below to point to image files. When a path is left empty or the
file does not exist, a simple colored rectangle will be used instead.
"""

from __future__ import annotations

import os
import pygame
from typing import Tuple

# Paths to asset images. Fill these in with your own files later.
CAR_IMAGE = ""
CAR_OBSTACLE_IMAGE = ""
SMALL_MONEY_IMAGE = ""
LARGE_MONEY_IMAGE = ""
EQUIPMENT_IMAGE = ""


def load_sprite(path: str, size: Tuple[int, int], color: Tuple[int, int, int]) -> pygame.Surface:
    """Return a sprite surface from ``path`` or a colored rectangle.

    If ``path`` points to an existing image, that image is loaded and scaled to
    ``size``. Otherwise a plain surface filled with ``color`` is returned.
    """
    if path and os.path.exists(path):
        sprite = pygame.image.load(path).convert_alpha()
        sprite = pygame.transform.smoothscale(sprite, size)
    else:
        sprite = pygame.Surface(size)
        sprite.fill(color)
    return sprite
