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

# Buildings
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
car_surface = load_sprite(CAR_IMAGE, (CAR_WIDTH, CAR_HEIGHT), BLUE, "car")
OBSTACLE_SURFACES = [
    load_sprite(CAR_OBSTACLE_IMAGE, (40, 60), RED, "car"),
    load_sprite(SMALL_MONEY_IMAGE, (30, 40), GREEN, "money"),
    load_sprite(LARGE_MONEY_IMAGE, (60, 80), GREEN, "money"),
    load_sprite(EQUIPMENT_IMAGE, (40, 40), YELLOW, "equipment"),
]

# Obstacle templates
OBSTACLE_TEMPLATES = [
    {"width": 40, "height": 60, "color": RED, "money": -5, "equipment": 0, "surface": OBSTACLE_SURFACES[0]},
    {"width": 30, "height": 40, "color": GREEN, "money": 1, "equipment": 0, "surface": OBSTACLE_SURFACES[1]},
    {"width": 60, "height": 80, "color": GREEN, "money": 3, "equipment": 0, "surface": OBSTACLE_SURFACES[2]},
    {"width": 40, "height": 40, "color": YELLOW, "money": 0, "equipment": 1, "surface": OBSTACLE_SURFACES[3]},
]

# Relative obstacle spawn frequency
OBSTACLE_WEIGHTS = [5, 3, 2, 1]
CRASH_ANIMATION_FRAMES = 30

def create_obstacle():
    """Create a new obstacle of random type within the road area."""
    template = random.choices(OBSTACLE_TEMPLATES, weights=OBSTACLE_WEIGHTS, k=1)[0]
    info = template.copy()
    x_min = SIDEWALK_WIDTH
    x_max = WIDTH - SIDEWALK_WIDTH - info["width"]
    x = random.randint(x_min, x_max)
    rect = pygame.Rect(x, -info["height"], info["width"], info["height"])
    info["rect"] = rect
    return info

def main() -> None:
    global car_x, car_y, money, equipment, obstacles

    running = True
    spawn_timer = 0
    start_ticks = pygame.time.get_ticks()
    game_state = "playing"
    crash_timer = 0
    crash_obstacle_rect = None
    restart_rect = None

    def reset_game():
        nonlocal spawn_timer, start_ticks, game_state, crash_timer, crash_obstacle_rect, restart_rect
        global car_x, car_y, money, equipment, obstacles
        car_x = SIDEWALK_WIDTH + ROAD_WIDTH // 2 - CAR_WIDTH // 2
        car_y = HEIGHT - CAR_HEIGHT - 10
        money = 0
        equipment = 0
        obstacles.clear()
        spawn_timer = 0
        start_ticks = pygame.time.get_ticks()
        game_state = "playing"
        crash_timer = 0
        crash_obstacle_rect = None
        restart_rect = None

    while running:
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif game_state == "game_over" and event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect and restart_rect.collidepoint(event.pos):
                    reset_game()

        if game_state == "game_over":
            screen.fill(BLACK)
            over_text = font.render("You crashed, and you're broke", True, WHITE)
            text_rect = over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
            screen.blit(over_text, text_rect)
            button_surf = font.render("Restart", True, WHITE)
            restart_rect = button_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
            pygame.draw.rect(screen, BLUE, restart_rect.inflate(20, 10))
            screen.blit(button_surf, restart_rect)
            pygame.display.flip()
            continue

        keys = pygame.key.get_pressed()
        if game_state == "playing":
            if keys[pygame.K_LEFT] and car_x > SIDEWALK_WIDTH:
                car_x -= car_speed
            if keys[pygame.K_RIGHT] and car_x < WIDTH - SIDEWALK_WIDTH - CAR_WIDTH:
                car_x += car_speed
            if keys[pygame.K_UP] and car_y > 0:
                car_y -= car_speed
            if keys[pygame.K_DOWN] and car_y < HEIGHT - CAR_HEIGHT:
                car_y += car_speed

        if game_state == "playing":
            spawn_timer += dt
            if spawn_timer > 1000:
                spawn_timer = 0
                obstacles.append(create_obstacle())

            elapsed_sec = (pygame.time.get_ticks() - start_ticks) / 1000
            obstacle_speed = BASE_OBSTACLE_SPEED + elapsed_sec * 0.1

            for obs in obstacles:
                obs["rect"].y += obstacle_speed
            obstacles[:] = [obs for obs in obstacles if obs["rect"].y < HEIGHT]

        car_offset = int(math.sin(pygame.time.get_ticks() * 0.02) * 2)
        car_rect = pygame.Rect(car_x, car_y + car_offset, CAR_WIDTH, CAR_HEIGHT)

        if game_state == "playing":
            for obs in obstacles[:]:
                if car_rect.colliderect(obs["rect"]):
                    money += obs["money"]
                    equipment += obs["equipment"]
                    obstacles.remove(obs)
                    if money < 0 and obs["color"] == RED:
                        crash_obstacle_rect = obs["rect"].copy()
                        game_state = "crashing"
                        crash_timer = 0

        if game_state == "crashing":
            crash_timer += 1
            if crash_timer > CRASH_ANIMATION_FRAMES:
                game_state = "game_over"

        # Drawing
        screen.fill(BLACK)
        pygame.draw.rect(screen, SIDEWALK_COLOR, (0, 0, SIDEWALK_WIDTH, HEIGHT))
        pygame.draw.rect(screen, SIDEWALK_COLOR, (WIDTH - SIDEWALK_WIDTH, 0, SIDEWALK_WIDTH, HEIGHT))

        for rect in buildings:
            pygame.draw.rect(screen, BUILDING_COLOR, rect)

        pygame.draw.rect(screen, ROAD_COLOR, (SIDEWALK_WIDTH, 0, ROAD_WIDTH, HEIGHT))
        for i in range(1, LANE_COUNT):
            x = SIDEWALK_WIDTH + i * LANE_WIDTH
            pygame.draw.line(screen, WHITE, (x, 0), (x, HEIGHT), 2)

        if game_state == "crashing" and crash_obstacle_rect:
            jitter = random.randint(-3, 3)
            crash_car = car_rect.move(jitter, jitter)
            crash_obs = crash_obstacle_rect.move(-jitter, jitter)
            screen.blit(car_surface, crash_car)
            screen.blit(OBSTACLE_SURFACES[0], crash_obs)
        else:
            screen.blit(car_surface, car_rect)

        for obs in obstacles:
            screen.blit(obs["surface"], obs["rect"])

        elapsed_sec = (pygame.time.get_ticks() - start_ticks) / 1000
        timer_surface = font.render(f"{elapsed_sec:.1f}", True, WHITE)
        screen.blit(timer_surface, (10, 10))

        money_surface = font.render(f"Money: {money}", True, WHITE)
        equipment_surface = font.render(f"Equip: {equipment}", True, WHITE)
        screen.blit(money_surface, (WIDTH - money_surface.get_width() - 10, 10))
        screen.blit(equipment_surface, (WIDTH - equipment_surface.get_width() - 10, 40))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
