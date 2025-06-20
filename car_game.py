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

# Car properties
CAR_WIDTH = 40
CAR_HEIGHT = 60
car_x = WIDTH // 2 - CAR_WIDTH // 2
car_y = HEIGHT - CAR_HEIGHT - 10
car_speed = 5

# Obstacle properties
OBSTACLE_WIDTH = 40
OBSTACLE_HEIGHT = 60
obstacle_speed = 5
obstacles = []

# Font
font = pygame.font.SysFont(None, 36)

def create_obstacle():
    x = random.randint(0, WIDTH - OBSTACLE_WIDTH)
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
    if keys[pygame.K_LEFT] and car_x > 0:
        car_x -= car_speed
    if keys[pygame.K_RIGHT] and car_x < WIDTH - CAR_WIDTH:
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

    # Collision detection
    car_rect = pygame.Rect(car_x, car_y, CAR_WIDTH, CAR_HEIGHT)
    for obs in obstacles:
        if car_rect.colliderect(obs):
            running = False

    # Drawing
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, car_rect)
    for obs in obstacles:
        pygame.draw.rect(screen, RED, obs)

    # Draw survival time
    seconds = (pygame.time.get_ticks() - start_ticks) // 1000
    text = font.render(f"Time: {seconds}s", True, BLACK)
    screen.blit(text, (10, 10))

    pygame.display.flip()

pygame.quit()
