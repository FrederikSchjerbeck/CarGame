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
OBSTACLE_WIDTH = 40
OBSTACLE_HEIGHT = 60
obstacle_speed = 5
obstacles = []

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

def create_obstacle():
    """Create a new obstacle within the road area."""
    x_min = SIDEWALK_WIDTH
    x_max = WIDTH - SIDEWALK_WIDTH - OBSTACLE_WIDTH
    x = random.randint(x_min, x_max)
    rect = pygame.Rect(x, -OBSTACLE_HEIGHT, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
    return rect

# Game loop
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

    # Move obstacles
    for obs in obstacles:
        obs.y += obstacle_speed

    # Remove off-screen obstacles
    obstacles = [obs for obs in obstacles if obs.y < HEIGHT]

    # Check collisions
    car_rect = pygame.Rect(car_x, car_y, CAR_WIDTH, CAR_HEIGHT)
    for obs in obstacles:
        if car_rect.colliderect(obs):
            running = False

    # Drawing
    screen.fill(BLACK)

    # Draw sidewalks
    pygame.draw.rect(screen, SIDEWALK_COLOR, (0, 0, SIDEWALK_WIDTH, HEIGHT))
    pygame.draw.rect(screen, SIDEWALK_COLOR, (WIDTH - SIDEWALK_WIDTH, 0, SIDEWALK_WIDTH, HEIGHT))

    # Draw buildings
    for rect in buildings:
        pygame.draw.rect(screen, BUILDING_COLOR, rect)

    # Draw road
    pygame.draw.rect(screen, ROAD_COLOR, (SIDEWALK_WIDTH, 0, ROAD_WIDTH, HEIGHT))

    # Draw lane lines
    for i in range(1, LANE_COUNT):
        x = SIDEWALK_WIDTH + i * LANE_WIDTH
        pygame.draw.line(screen, WHITE, (x, 0), (x, HEIGHT), 2)

    # Draw car
    pygame.draw.rect(screen, BLUE, car_rect)

    # Draw obstacles
    for obs in obstacles:
        pygame.draw.rect(screen, RED, obs)

    # Draw timer
    elapsed_sec = (pygame.time.get_ticks() - start_ticks) / 1000
    timer_surface = font.render(f"{elapsed_sec:.1f}", True, WHITE)
    screen.blit(timer_surface, (10, 10))

    pygame.display.flip()

pygame.quit()
