import math
import pygame
import random

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

# Pre-generate simple buildings along the sidewalks
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

# Predefined obstacle templates
OBSTACLE_TEMPLATES = [
    {
        "width": 40,
        "height": 60,
        "color": RED,
        "money": -5,
        "equipment": 0,
    },
    {
        "width": 60,
        "height": 80,
        "color": GREEN,
        "money": 3,
        "equipment": 0,
    },
    {
        "width": 30,
        "height": 40,
        "color": GREEN,
        "money": 1,
        "equipment": 0,
    },
    {
        "width": 40,
        "height": 40,
        "color": YELLOW,
        "money": 0,
        "equipment": 1,
    },
]


def create_obstacle():
    """Create a new obstacle of random type within the road area."""
    template = random.choice(OBSTACLE_TEMPLATES)
    info = template.copy()
    x_min = SIDEWALK_WIDTH
    x_max = WIDTH - SIDEWALK_WIDTH - info["width"]
    x = random.randint(x_min, x_max)
    rect = pygame.Rect(x, -info["height"], info["width"], info["height"])
    info["rect"] = rect
    return info


def main() -> None:
    """Run the main game loop."""
    global car_x, money, equipment

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

        # Spawn obstacles
        spawn_timer += dt
        if spawn_timer > 1000:  # Spawn every second
            spawn_timer = 0
            obstacles.append(create_obstacle())

        # Speed up obstacles over time
        elapsed_sec = (pygame.time.get_ticks() - start_ticks) / 1000
        obstacle_speed = BASE_OBSTACLE_SPEED + elapsed_sec * 0.1

        # Move obstacles
        for obs in obstacles:
            obs["rect"].y += obstacle_speed

        # Remove off-screen obstacles
        obstacles[:] = [obs for obs in obstacles if obs["rect"].y < HEIGHT]

        # Car bounces slightly to simulate movement
        car_offset = int(math.sin(pygame.time.get_ticks() * 0.02) * 2)
        car_rect = pygame.Rect(
            car_x,
            car_y + car_offset,
            CAR_WIDTH,
            CAR_HEIGHT,
        )
        for obs in obstacles[:]:
            if car_rect.colliderect(obs["rect"]):
                money += obs["money"]
                equipment += obs["equipment"]
                obstacles.remove(obs)

        # Drawing
        screen.fill(BLACK)

        # Draw sidewalks
        pygame.draw.rect(
            screen,
            SIDEWALK_COLOR,
            (0, 0, SIDEWALK_WIDTH, HEIGHT),
        )
        right_side = (WIDTH - SIDEWALK_WIDTH, 0, SIDEWALK_WIDTH, HEIGHT)
        pygame.draw.rect(screen, SIDEWALK_COLOR, right_side)

        # Draw buildings
        for rect in buildings:
            pygame.draw.rect(screen, BUILDING_COLOR, rect)

        # Draw road
        road_rect = (SIDEWALK_WIDTH, 0, ROAD_WIDTH, HEIGHT)
        pygame.draw.rect(screen, ROAD_COLOR, road_rect)

        # Draw lane lines
        for i in range(1, LANE_COUNT):
            x = SIDEWALK_WIDTH + i * LANE_WIDTH
            pygame.draw.line(screen, WHITE, (x, 0), (x, HEIGHT), 2)

        # Draw car
        pygame.draw.rect(screen, BLUE, car_rect)

        # Draw obstacles
        for obs in obstacles:
            pygame.draw.rect(screen, obs["color"], obs["rect"])

        # Draw timer
        elapsed_sec = (pygame.time.get_ticks() - start_ticks) / 1000
        timer_surface = font.render(f"{elapsed_sec:.1f}", True, WHITE)
        screen.blit(timer_surface, (10, 10))

        # Draw scores
        money_surface = font.render(f"Money: {money}", True, WHITE)
        equipment_surface = font.render(f"Equip: {equipment}", True, WHITE)
        screen.blit(
            money_surface,
            (WIDTH - money_surface.get_width() - 10, 10),
        )
        screen.blit(
            equipment_surface,
            (WIDTH - equipment_surface.get_width() - 10, 40),
        )

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
