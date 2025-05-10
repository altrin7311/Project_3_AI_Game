import pygame
import time
from config import OFFSET_X, OFFSET_Y
from config import TILE_SIZE, COLOR_PATH_FADED, COLOR_GOAL, COLOR_HUMAN, COLOR_TEXT, GRID_WIDTH, GRID_HEIGHT

FONT = None

def initialize_fonts():
    global FONT
    if FONT is None:
        FONT = pygame.font.SysFont("arial", 20)

def draw_text_center(screen, text, font, color, x, y):
    label = font.render(text, True, color)
    rect = label.get_rect(center=(x, y))
    screen.blit(label, rect)

def draw_circle_tile(screen, pos, color, big=False):
    x, y = pos
    radius = TILE_SIZE // 2 - (6 if big else 10)
    center = (
        x * TILE_SIZE + TILE_SIZE // 2 + OFFSET_X,
        y * TILE_SIZE + TILE_SIZE // 2 + OFFSET_Y
    )
    pygame.draw.circle(screen, color, center, radius)

def draw_small_circle(screen, pos, color):
    x, y = pos
    radius = TILE_SIZE // 2 - 12
    s = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    center = (TILE_SIZE // 2, TILE_SIZE // 2)
    faded_color = color + (100,) if len(color) == 3 else color
    pygame.draw.circle(s, faded_color, center, radius)
    screen.blit(s, (x * TILE_SIZE + OFFSET_X, y * TILE_SIZE + OFFSET_Y))

# ---------- MINI DISPLAY HELPERS ---------- #

def draw_mini_grid(surface, cell_size):
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            pygame.draw.rect(surface, (60, 60, 60), rect, 1)

def draw_mini_obstacles(surface, obstacles, cell_size):
    for (x, y) in obstacles:
        rect = pygame.Rect(x * cell_size + 2, y * cell_size + 2, cell_size - 4, cell_size - 4)
        pygame.draw.rect(surface, (100, 100, 100), rect)

def draw_mini_path(surface, path, cell_size):
    for (x, y) in path:
        center = (x * cell_size + cell_size // 2, y * cell_size + cell_size // 2)
        pygame.draw.circle(surface, COLOR_PATH_FADED[:3], center, cell_size // 2 - 2)

def draw_mini_start_goal(surface, start, goal, cell_size):
    sx, sy = start
    gx, gy = goal
    pygame.draw.circle(
        surface, COLOR_HUMAN,
        (sx * cell_size + cell_size // 2, sy * cell_size + cell_size // 2),
        cell_size // 2 - 2
    )
    pygame.draw.circle(
        surface, COLOR_GOAL,
        (gx * cell_size + cell_size // 2, gy * cell_size + cell_size // 2),
        cell_size // 2 - 2
    )

def draw_algorithm_mini_views(screen, algorithms, start, goal, obstacles):
    from config import WIDTH, HEIGHT, GRID_WIDTH, GRID_HEIGHT

    font = pygame.font.SysFont("arial", 18)
    metrics_font = pygame.font.SysFont("arial", 14)
    screen.fill((0, 0, 0))  # Clear the background

    columns = 7
    rows = 2
    margin_x, margin_y = 40, 40
    spacing_x, spacing_y = 30, 70

    mini_w = (WIDTH - margin_x * 2 - spacing_x * (columns - 1)) // columns
    mini_h = (HEIGHT - margin_y * 2 - spacing_y * (rows - 1) - 80) // rows
    cell_size = min(mini_w // GRID_WIDTH, mini_h // GRID_HEIGHT)

    algo_list = [(label, func) for (key, (label, func)) in algorithms.items()]

    for index, (label, func) in enumerate(algo_list):
        col = index % columns
        row = index // columns
        x_offset = margin_x + col * (mini_w + spacing_x)
        y_offset = margin_y + row * (mini_h + spacing_y)

        mini_surface = pygame.Surface((mini_w, mini_h))
        mini_surface.fill((20, 20, 20))

        draw_mini_grid(mini_surface, cell_size)
        draw_mini_obstacles(mini_surface, obstacles, cell_size)

        path = []
        nodes_visited = 0
        time_taken = 0
        try:
            start_time = time.time()
            result = func(start, goal, obstacles)
            end_time = time.time()
            time_taken = (end_time - start_time) * 1000  # ms

            if isinstance(result, tuple):
                path, visited = result
                nodes_visited = len(visited)
            else:
                path = result
                nodes_visited = len(path)  # fallback

            if path:
                draw_mini_path(mini_surface, path, cell_size)
        except Exception as e:
            print(f"[❌] Error in {label}: {e}")

        draw_mini_start_goal(mini_surface, start, goal, cell_size)
        screen.blit(mini_surface, (x_offset, y_offset))

        # Title above grid
        draw_text_center(screen, label, font, COLOR_TEXT, x_offset + mini_w // 2, y_offset - 20)

        # Metrics below grid
        draw_text_center(screen, f"Path: {len(path)}", metrics_font, COLOR_TEXT, x_offset + mini_w // 2, y_offset + mini_h - 90)
        draw_text_center(screen, f"Visited: {nodes_visited}", metrics_font, COLOR_TEXT, x_offset + mini_w // 2, y_offset + mini_h -75)
        draw_text_center(screen, f"Time: {time_taken:.2f} ms" , metrics_font, COLOR_TEXT, x_offset + mini_w // 2, y_offset + mini_h -60 )

    draw_text_center(screen, "Press R to Play Again or ESC to Quit",
                     pygame.font.SysFont("arial", 22), COLOR_TEXT, WIDTH // 2, HEIGHT - 25)