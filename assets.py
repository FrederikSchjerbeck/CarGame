"""Image placeholders for CarGame assets.

Edit the paths below to point to image files. When a path is left empty or the
file does not exist, a simple colored placeholder will be drawn instead.
Each placeholder has a transparent background and approximates the shape of the
object so the game still looks reasonable without custom graphics.
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


def load_sprite(
    path: str,
    size: Tuple[int, int],
    color: Tuple[int, int, int],
    shape: str = "rect",
) -> pygame.Surface:
    """Return a sprite surface from `path` or a colored placeholder.

    If `path` points to an existing image, that image is loaded and scaled to
    `size`. Otherwise an alpha surface is created and `shape` is drawn on it
    using `color`.
    """
    if path and os.path.exists(path):
        sprite = pygame.image.load(path).convert_alpha()
        sprite = pygame.transform.smoothscale(sprite, size)
        return sprite

    # Draw placeholder graphic with transparent background
    sprite = pygame.Surface(size, pygame.SRCALPHA)

    if shape == "car":
        body_rect = pygame.Rect(0, size[1] * 0.3, size[0], size[1] * 0.55)
        pygame.draw.rect(sprite, color, body_rect, border_radius=size[0] // 8)
        roof_rect = pygame.Rect(size[0] * 0.2, size[1] * 0.05, size[0] * 0.6, size[1] * 0.35)
        pygame.draw.rect(sprite, color, roof_rect, border_radius=size[0] // 10)
        wheel_radius = max(2, size[0] // 8)
        pygame.draw.circle(sprite, (0, 0, 0), (int(size[0] * 0.25), int(size[1] * 0.9)), wheel_radius)
        pygame.draw.circle(sprite, (0, 0, 0), (int(size[0] * 0.75), int(size[1] * 0.9)), wheel_radius)
    elif shape == "money":
        pygame.draw.rect(sprite, color, sprite.get_rect(), border_radius=4)
        pygame.draw.rect(sprite, (0, 0, 0), sprite.get_rect(), 2, border_radius=4)
    elif shape == "equipment":
        pygame.draw.rect(sprite, color, sprite.get_rect(), border_radius=3)
        width, height = size
        pygame.draw.line(sprite, (0, 0, 0), (0, 0), (width, height), 2)
        pygame.draw.line(sprite, (0, 0, 0), (width, 0), (0, height), 2)
    else:
        pygame.draw.rect(sprite, color, sprite.get_rect())

    return sprite
