from typing import Optional

from modules.game_data import GameData
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


class Game:
    """Game class that will handle the game screen and render the necessary scene"""

    def __init__(self, game_data: GameData) -> None:
        self.game_data = game_data
        self.story = self.game_data.get_str_in_language("messages", "story", "room_1")

        self.obstacles: set[tuple[int, int]] = set()
        self.message_pos = set()
        self.entities: set[Optional[Entity]] = set()
        self.player = Player((2, 2))
        self.entities.add(self.player)
        self.load_map()

    @staticmethod
    def get_neighbours(x, y) -> set[tuple[int, int]]:
        """Helper function to return the coordinates surrounding (x,y)."""
        neighbours = set()
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                # From Sachin
                # if (i == x and j == y) or not (1 < i < 25 and 1 < j < 57):
                #     continue
                # Specify max width and max height
                if i != j and (0 < j < 21 and 0 < i < 21):
                    neighbours.add((i, j))
        return neighbours

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
            pos_x -= 1  # 2 for more smoothness
        if mov == "l" or mov == "KEY_RIGHT":
            pos_x += 1

        # Check the orientation what is x and y ?
        if (pos_y, pos_x) in self.message_pos:
            # log(repr(self.entities))
            pass
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

    def get_sidebar_content(self) -> str:
        data = {}
        data.update(self.game_data.data["game"])
        data.pop("colors")
        data.pop("last_saved")
        return data
