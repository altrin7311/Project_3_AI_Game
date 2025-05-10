# player.py

from config import GRID_WIDTH, GRID_HEIGHT

class Player:
    def __init__(self, name, color, pos):
        """
        Initialize a player with a name, color, and starting position.
        """
        self.name = name
        self.color = color  # RGB tuple
        self.pos = pos      # (x, y) grid coordinates

    def move(self, direction, obstacles):
        """
        Move the player in the specified direction if the move is valid
        (i.e., within bounds and not into an obstacle).
        Returns True if move is successful, False otherwise.
        """
        x, y = self.pos

        if direction == 'UP':
            new_pos = (x, y - 1)
        elif direction == 'DOWN':
            new_pos = (x, y + 1)
        elif direction == 'LEFT':
            new_pos = (x - 1, y)
        elif direction == 'RIGHT':
            new_pos = (x + 1, y)
        else:
            return False

        if (
            0 <= new_pos[0] < GRID_WIDTH and
            0 <= new_pos[1] < GRID_HEIGHT and
            new_pos not in obstacles
        ):
            self.pos = new_pos
            return True

        return False

    def move_to(self, position):
        """
        Instantly move the player to a specific position.
        Used by AI during path traversal.
        """
        self.pos = position