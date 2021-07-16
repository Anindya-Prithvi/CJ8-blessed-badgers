import json

# import os
# from datetime import datetime

ASSETS_PATH = "assets"
LANGUAGE_PATH = f"{ASSETS_PATH}/lang/"
GAMEDATA_PATH = f"{ASSETS_PATH}/gamedata.json"
GAMESAVE_NEW = f"{ASSETS_PATH}/saves/gamedata_new.json"
GAMESAVE_SAVE = f"{ASSETS_PATH}/saves/gamedata_save.json"


# class GameException(Exception):
#     """Base class for exceptions in this module."""

#     pass


class GameData:
    """Game parent class for managing the game datas"""

    def __init__(self):
        try:
            with open(GAMEDATA_PATH, "r") as file:
                self.data = json.load(file)
        except FileNotFoundError:
            pass

    def update_file_game_data_decorator(function):
        """Decorator used to save the game_data into a file when it's updated"""

        def inner(self, *args):
            function(self, *args)
            with open(GAMEDATA_PATH, "w") as file:
                json.dump(self.data, file, indent=4)

        return inner

    def get_str_in_language(self, *args) -> str:
        """
        Read the args from the language file

        It allow the translation of the game
        """
        selections = [*args]

        try:
            with open(LANGUAGE_PATH + f"lang_{self.get_language()}.json", "r", encoding="utf-8") as lang:
                lang_dict = json.load(lang)
        except FileNotFoundError:
            with open(LANGUAGE_PATH + "lang_en.json", "r", encoding="utf-8") as lang:
                lang_dict = json.load(lang)

        for key in selections:
            try:
                lang_dict = lang_dict[key]
            except KeyError:
                lang_dict = key
            except TypeError:
                lang_dict = key

        return lang_dict

    @update_file_game_data_decorator
    def save_game(self) -> None:
        with open(GAMESAVE_SAVE, "w") as file:
            json.dump(self.data, file, indent=4)

    @update_file_game_data_decorator
    def load_game(self, game_type: str = "new") -> None:
        if game_type == "new":
            path = GAMESAVE_NEW
        elif game_type == "saved":
            path = GAMESAVE_SAVE

        with open(path, "r") as file:
            data_tmp = json.load(file)
            data_tmp["game"] = self.data["game"]
            self.data = data_tmp

    # Game already played
    def is_game_already_played(self) -> bool:
        return self.data["game"]["is_game_already_played"]

    @update_file_game_data_decorator
    def set_game_already_played(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError("Incorrect value type")

        self.data["game"]["is_game_already_played"] = value

    # Game_level
    def get_game_level(self) -> str:
        return self.data["game"]["level"]

    @update_file_game_data_decorator
    def set_game_level(self, game_level) -> None:
        self.data["game"]["level"] = game_level

    def get_language(self) -> str:
        return self.data["game"]["language"]

    @update_file_game_data_decorator
    def set_language(self, language) -> None:
        self.data["game"]["language"] = language

    def get_inventory_item_by_key(self, key) -> dict:
        return self.data["player"]["inventory"][key]

    @update_file_game_data_decorator
    def set_inventory_item_by_key(self, key, value) -> None:
        self.data["player"]["inventory"][key] = value

    @update_file_game_data_decorator
    def inc_inventory_item_by_key(self, key) -> None:
        inventory = self.data["player"]["inventory"]
        if isinstance(inventory[key], int):
            inventory[key] += 1

    @update_file_game_data_decorator
    def dec_inventory_item_by_key(self, key) -> None:
        inventory = self.data["player"]["inventory"]
        if isinstance(inventory[key], int):
            inventory[key] -= 1
        if inventory[key] < 0:
            inventory[key] = 0

    # def get_inventory_items(self) -> list:
    #     return list(self.data["player"]["inventory"].keys())
