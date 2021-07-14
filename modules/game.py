from typing import Optional

from modules.logger import log
from scenes.entity import Entity, SubtractableDict


class GameException(Exception):
    """Base class for exceptions in this module."""

    pass


class Player(Entity):
    def __init__(self, position: tuple[int, int], sprite: Optional[str] = None):
        super().__init__(position, sprite or ["@"])


class Obstacle(Entity):
    pass


class Message(Entity):
    def __init__(self, message: str, *args):
        super().__init__(*args)
        self.message = message


# This will load from somewhere.
Messages = [
    """I am sorry to let you know that you are stuck here.
Mmhh...
That's no entirely true, you might be able to get away. But can you ?!""",
    "You have the secret Message0: Look around who knows you might find a clue.",
    "Can you print I can escape(whatever)",
]


class Game:
    """Game class that will handle the game screen and render the necessary scene"""

    def __init__(self) -> None:
        self.obstacles: set[tuple[int, int]] = set()
        self.message_pos = set()
        self.message_ = None
        self.entities: set[Optional[Entity]] = set()
        self.player = Player((2, 2))
        self.entities.add(self.player)
        self.load_map()

    @staticmethod
    def get_neighbours(i, j) -> set[tuple[int, int]]:
        """Helper function to return the coordinates surrounding (i, j)."""
        pos = set()
        for i in range(i - 1, i + 2):
            for j in range(j - 1, j + 2):
                # Specify max width and max height
                if i != j and (0 < j < 21 and 0 < i < 21):
                    pos.add((i, j))
        return pos

    def load_map(self, level=0) -> None:
        """
        Load map from the directory according to the specified level.

        Note: Assuming level is safe and has the type integer.
        """
        with open(f"assets/maps/{level}.txt", encoding="utf-8") as map_fd:
            map_data = map_fd.read().splitlines()

        if len(map_data) == 0:
            raise GameException("map loading")

        self.obstacles = set()
        for i, line in enumerate(map_data):
            for j, char in enumerate(line):
                if char == " ":
                    continue
                elif char in "MAX":
                    self.message_pos.update(self.get_neighbours(i, j))
                self.entities.add(Obstacle((i, j), [char]))
                self.obstacles.add((i, j))

    def move_player(self, mov: str) -> None:
        """Move player."""
        # Make a copy of the position of the player.
        pos_y, pos_x = self.player.position

        # Update the position.
        if mov == "j" or mov == "KEY_DOWN":
            pos_y += 1
        if mov == "k" or mov == "KEY_UP":
            pos_y -= 1
        if mov == "h" or mov == "KEY_LEFT":
            pos_x -= 1
        if mov == "l" or mov == "KEY_RIGHT":
            pos_x += 1

        # Check the orientation what is x and y ?
        if (pos_y, pos_x) in self.message_pos:
            log(repr(self.entities))
        if (pos_y, pos_x) not in self.obstacles:
            self.player.position = pos_y, pos_x

    def get_to_be_rendered(self) -> SubtractableDict:
        """
        Get the coordinates where entities are to be rendered, and the characters at those coordinates.

        :return: dict subclass in the form of {(i, j): character}, where (i, j) is the coordinate.
        """
        to_be_rendered = SubtractableDict()
        for entity in self.entities:
            to_be_rendered |= entity.get_to_be_rendered()
        return to_be_rendered
