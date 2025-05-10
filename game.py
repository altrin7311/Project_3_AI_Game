import pygame
import random
from config import *
from player import Player
from ai_algorithms import *
from ui_utils import (
    draw_text_center, draw_circle_tile, draw_small_circle,
    draw_algorithm_mini_views, initialize_fonts
)
from ai_algorithms import ALL_ALGORITHMS


class Game:
    def __init__(self):
        pygame.init()
        initialize_fonts()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("AI Hide & Seek")
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.goal = self.random_tile()
        self.start = self.random_tile_far_from_goal()

        self.obstacles = self.generate_obstacles(exclude=[self.goal, self.start])
        self.human = Player("Human", COLOR_HUMAN, self.start)
        self.ai = Player("AI", COLOR_AI, self.start)

        self.ai_visited = []

        self.algorithm_map = ALL_ALGORITHMS
        self.selected_algorithm = self.select_algorithm_ui()
        self.selected_algo_name, self.selected_algo_func = self.algorithm_map[self.selected_algorithm]
        self.ai_path, self.ai_visited = self.selected_algo_func(self.start, self.goal, self.obstacles)

        self.ai_step = 0
        self.ai_revealed_path = []
        self.human_trail = []
        self.ai_trail = []
        self.player_turn = True
        self.show_all_paths = False
        self.play_again_prompt = False

    def random_tile(self, exclude=[]):
        while True:
            tile = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if tile not in exclude:
                return tile

    def random_tile_far_from_goal(self):
        while True:
            tile = self.random_tile(exclude=[self.goal])
            if abs(tile[0] - self.goal[0]) + abs(tile[1] - self.goal[1]) >= (GRID_WIDTH + GRID_HEIGHT) // 3:
                return tile

    def generate_obstacles(self, exclude=[], count=30):
        attempts = 0
        while True:
            obstacles = set()
            while len(obstacles) < count:
                tile = self.random_tile(exclude=exclude + list(obstacles))
                obstacles.add(tile)
            if astar(self.start, self.goal, list(obstacles)):
                return list(obstacles)
            attempts += 1
            if attempts > 100:
                count -= 5  # Reduce if too hard to solve

    def select_algorithm_ui(self):
        font = pygame.font.SysFont(None, 36)
        selected = 0
        while True:
            self.screen.fill((0, 0, 0))
            draw_text_center(self.screen, "Select AI Algorithm (Enter to Confirm)", font, COLOR_TEXT, WIDTH // 2, 40)
            for i, (key, (name, _)) in enumerate(self.algorithm_map.items()):
                color = (0, 255, 0) if i == selected else COLOR_TEXT
                draw_text_center(self.screen, f"{name}", font, color, WIDTH // 2, 100 + i * 30)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected = (selected - 1) % len(self.algorithm_map)
                    elif event.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(self.algorithm_map)
                    elif event.key == pygame.K_RETURN:
                        return list(self.algorithm_map.keys())[selected]

    def draw_grid(self):
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                rect = pygame.Rect(
                    OFFSET_X + x * TILE_SIZE,
                    OFFSET_Y + y * TILE_SIZE,
                    TILE_SIZE,
                    TILE_SIZE
                )
                pygame.draw.rect(self.screen, COLOR_GRID, rect, 1)

    def draw_elements(self):
        for obs in self.obstacles:
            rect = pygame.Rect(
                OFFSET_X + obs[0] * TILE_SIZE,
                OFFSET_Y + obs[1] * TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE
            )
            pygame.draw.rect(self.screen, COLOR_OBSTACLE, rect)

        draw_circle_tile(self.screen, self.goal, COLOR_GOAL)
        for pos in self.human_trail:
            draw_small_circle(self.screen, pos, COLOR_HUMAN)
        for pos in self.ai_trail:
            draw_small_circle(self.screen, pos, COLOR_AI)
        for pos in self.ai_revealed_path:
            draw_small_circle(self.screen, pos, COLOR_AI)

        draw_circle_tile(self.screen, self.human.pos, COLOR_HUMAN, big=True)
        draw_circle_tile(self.screen, self.ai.pos, COLOR_AI, big=True)

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            self.screen.fill(COLOR_BG)
            self.draw_grid()

            if not self.show_all_paths:
                self.draw_elements()
                font = pygame.font.SysFont(None, 28)
                draw_text_center(self.screen, f"You vs {self.selected_algo_name}", font, COLOR_TEXT, WIDTH // 2, 20)
            else:
                all_other_algos = {
                    k: v for k, v in self.algorithm_map.items() if k != self.selected_algorithm
                }
                draw_algorithm_mini_views(self.screen, all_other_algos, self.start, self.goal, self.obstacles)
                if self.play_again_prompt:
                    font = pygame.font.SysFont(None, 28)
                    draw_text_center(self.screen, "Press R to Play Again or ESC to Quit", font, COLOR_TEXT, WIDTH // 2, HEIGHT - 30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if self.show_all_paths:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False
                        if event.key == pygame.K_r:
                            self.reset()
                            continue

            keys = pygame.key.get_pressed()
            moved = False

            if self.player_turn and not self.show_all_paths:
                if keys[pygame.K_UP]: moved = self.human.move('UP', self.obstacles)
                elif keys[pygame.K_DOWN]: moved = self.human.move('DOWN', self.obstacles)
                elif keys[pygame.K_LEFT]: moved = self.human.move('LEFT', self.obstacles)
                elif keys[pygame.K_RIGHT]: moved = self.human.move('RIGHT', self.obstacles)

                if moved:
                    self.human_trail.append(self.human.pos)
                    self.player_turn = False

            elif not self.player_turn and not self.show_all_paths:
                if self.ai_step < len(self.ai_path):
                    step_pos = self.ai_path[self.ai_step]
                    self.ai.move_to(step_pos)
                    self.ai_revealed_path.append(step_pos)
                    self.ai_trail.append(step_pos)
                    self.ai_step += 1
                self.player_turn = True

            if not self.show_all_paths:
                if self.human.pos == self.goal and self.ai.pos == self.goal:
                    print("It's a Tie!")
                    self.show_all_paths = True
                    self.play_again_prompt = True
                elif self.human.pos == self.goal:
                    print("Human wins! 🎉")
                    self.show_all_paths = True
                    self.play_again_prompt = True
                elif self.ai.pos == self.goal:
                    print("AI wins! 🤖")
                    self.show_all_paths = True
                    self.play_again_prompt = True

            pygame.display.flip()

        pygame.quit()