import math
import pygame
import random

from assets import (
    load_sprite,
    CAR_IMAGE,
    CAR_OBSTACLE_IMAGE,
    SMALL_MONEY_IMAGE,
    LARGE_MONEY_IMAGE,
    EQUIPMENT_IMAGE,
)

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Car Game")

clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 180, 0)
YELLOW = (200, 200, 0)

# Road and scenery colors
ROAD_COLOR = (40, 40, 40)
SIDEWALK_COLOR = (120, 120, 120)
BUILDING_COLOR = (170, 170, 170)

# Road layout
SIDEWALK_WIDTH = 50
ROAD_WIDTH = WIDTH - 2 * SIDEWALK_WIDTH
LANE_COUNT = 4
LANE_WIDTH = ROAD_WIDTH // LANE_COUNT

# Car properties
CAR_WIDTH = 40
CAR_HEIGHT = 60
car_x = SIDEWALK_WIDTH + ROAD_WIDTH // 2 - CAR_WIDTH // 2
car_y = HEIGHT - CAR_HEIGHT - 10
car_speed = 5

# Obstacle properties
BASE_OBSTACLE_SPEED = 5
obstacle_speed = BASE_OBSTACLE_SPEED
obstacles = []

# Scoring
money = 0
equipment = 0

# Pre-generate buildings
buildings = []
for side in (0, WIDTH - SIDEWALK_WIDTH):
    y_pos = 0
    while y_pos < HEIGHT:
        b_height = random.randint(60, 150)
        rect = pygame.Rect(side, y_pos, SIDEWALK_WIDTH, b_height)
        buildings.append(rect)
        y_pos += b_height + 20

# Font
font = pygame.font.SysFont(None, 36)

# Sprites - use placeholders when no images are supplied
car_surface = load_sprite(CAR_IMAGE, (CAR_WIDTH, CAR_HEIGHT), BLUE)
OBSTACLE_SURFACES = [
    load_sprite(CAR_OBSTACLE_IMAGE, (40, 60), RED),
    load_sprite(SMALL_MONEY_IMAGE, (30, 40), GREEN),
    load_sprite(LARGE_MONEY_IMAGE, (60, 80), GREEN),
    load_sprite(EQUIPMENT_IMAGE, (40, 40), YELLOW),
]

# Obstacle templates
OBSTACLE_TEMPLATES = [
    {"width": 40, "height": 60, "color": RED, "money": -5, "equipment": 0, "surface": OBSTACLE_SURFACES[0]},
    {"width": 30, "height": 40, "color": GREEN, "money": 1, "equipment": 0, "surface": OBSTACLE_SURFACES[1]},
    {"width": 60, "height": 80, "color": GREEN, "money": 3, "equipment": 0, "surface": OBSTACLE_SURFACES[2]},
    {"width": 40, "height": 40, "color": YELLOW, "money": 0, "equipment": 1, "surface": OBSTACLE_SURFACES[3]},
]

# Relative likelihood for each obstacle type. The order corresponds to
# OBSTACLE_TEMPLATES above. Cars are most common followed by small and large
# money blocks and finally the yellow equipment crates.
OBSTACLE_WEIGHTS = [5, 3, 2, 1]

def create_obstacle():
    """Create a new obstacle of random type within the road area."""
    # Weighted choice so that cars appear most often followed by small
    # money, large money and equipment.
    template = random.choices(OBSTACLE_TEMPLATES, weights=OBSTACLE_WEIGHTS, k=1)[0]
    info = template.copy()
    x_min = SIDEWALK_WIDTH
    x_max = WIDTH - SIDEWALK_WIDTH - info["width"]
    x = random.randint(x_min, x_max)
    rect = pygame.Rect(x, -info["height"], info["width"], info["height"])
    info["rect"] = rect
    return info

def main() -> None:
    """Run the main game loop."""
    global car_x, car_y, money, equipment

    running = True
    spawn_timer = 0
    start_ticks = pygame.time.get_ticks()

    while running:
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and car_x > SIDEWALK_WIDTH:
            car_x -= car_speed
        if keys[pygame.K_RIGHT] and car_x < WIDTH - SIDEWALK_WIDTH - CAR_WIDTH:
            car_x += car_speed
        if keys[pygame.K_UP] and car_y > 0:
            car_y -= car_speed
        if keys[pygame.K_DOWN] and car_y < HEIGHT - CAR_HEIGHT:
            car_y += car_speed

        # Spawn obstacles
        spawn_timer += dt
        if spawn_timer > 1000:
            spawn_timer = 0
            obstacles.append(create_obstacle())

        # Increase speed over time
        elapsed_sec = (pygame.time.get_ticks() - start_ticks) / 1000
        obstacle_speed = BASE_OBSTACLE_SPEED + elapsed_sec * 0.1

        # Move obstacles
        for obs in obstacles:
            obs["rect"].y += obstacle_speed

        # Remove off-screen obstacles
        obstacles[:] = [obs for obs in obstacles if obs["rect"].y < HEIGHT]

        # Car bounce animation
        car_offset = int(math.sin(pygame.time.get_ticks() * 0.02) * 2)
        car_rect = pygame.Rect(car_x, car_y + car_offset, CAR_WIDTH, CAR_HEIGHT)

        # Collision detection
        for obs in obstacles[:]:
            if car_rect.colliderect(obs["rect"]):
                money += obs["money"]
                equipment += obs["equipment"]
                obstacles.remove(obs)

        # Drawing
        screen.fill(BLACK)

        # Sidewalks
        pygame.draw.rect(screen, SIDEWALK_COLOR, (0, 0, SIDEWALK_WIDTH, HEIGHT))
        pygame.draw.rect(screen, SIDEWALK_COLOR, (WIDTH - SIDEWALK_WIDTH, 0, SIDEWALK_WIDTH, HEIGHT))

        # Buildings
        for rect in buildings:
            pygame.draw.rect(screen, BUILDING_COLOR, rect)

        # Road
        pygame.draw.rect(screen, ROAD_COLOR, (SIDEWALK_WIDTH, 0, ROAD_WIDTH, HEIGHT))

        # Lane lines
        for i in range(1, LANE_COUNT):
            x = SIDEWALK_WIDTH + i * LANE_WIDTH
            pygame.draw.line(screen, WHITE, (x, 0), (x, HEIGHT), 2)

        # Car
        screen.blit(car_surface, car_rect)

        # Obstacles
        for obs in obstacles:
            screen.blit(obs["surface"], obs["rect"])

        # Timer
        timer_surface = font.render(f"{elapsed_sec:.1f}", True, WHITE)
        screen.blit(timer_surface, (10, 10))

        # Scores
        money_surface = font.render(f"Money: {money}", True, WHITE)
        equipment_surface = font.render(f"Equip: {equipment}", True, WHITE)
        screen.blit(money_surface, (WIDTH - money_surface.get_width() - 10, 10))
        screen.blit(equipment_surface, (WIDTH - equipment_surface.get_width() - 10, 40))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
