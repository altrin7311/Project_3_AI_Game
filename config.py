# config.py

# === Grid Settings ===
TILE_SIZE = 48
GRID_WIDTH = 12     # Columns
GRID_HEIGHT = 12    # Rows

# === Screen Size ===
WIDTH = 1400
HEIGHT = 900
FPS = 10

# === Color Definitions (RGB / RGBA) ===
COLOR_BG = (30, 30, 30)
COLOR_GRID = (60, 60, 60)

COLOR_OBSTACLE = (100, 100, 100)
COLOR_GOAL = (0, 128, 0)               # Green
COLOR_HUMAN = (255, 44, 44)            # Red
COLOR_AI = (2, 6, 111)                 # Blue

COLOR_AI_TRAIL = (2, 6, 111, 80)       # Blue faded trail
COLOR_HUMAN_TRAIL = (255, 44, 44, 80)  # Red faded trail
COLOR_PATH_FADED = (0, 100, 255, 100)  # Faded comparison trail

COLOR_TEXT = (255, 255, 255)

OFFSET_X = (WIDTH - GRID_WIDTH * TILE_SIZE) // 2
OFFSET_Y = (HEIGHT - GRID_HEIGHT * TILE_SIZE) // 2