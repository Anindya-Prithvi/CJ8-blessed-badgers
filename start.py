import sys

import blessed

from modules.game_data import GameData
from modules.logger import log
from screens import AboutScreen, GameScreen, LanguageScreen, MenuScreen


def main() -> None:
    """Main function"""
    log("The game start", "Title")
    term = blessed.Terminal()
    game_data = GameData()
    keypressed = None

    with term.fullscreen(), term.cbreak():
        while keypressed != "q":
            keypressed = MenuScreen(game_data=game_data).render(term)
            if keypressed == "n":  # New game
                print(term.clear)
                # game_data.set_game_mode("new")
                GameScreen().render(term)
                game_data.load_game("new")
                game_data.update_game_mode("normal")
                # GameScreen(game_data=game_data).render(term)
            elif keypressed == "t":
                game_data.update_game_mode("tutorial")
                # GameScreen(game_data=game_data).render(term)
                pass
            elif keypressed == "c":
                game_data.load_game("saved")
                game_data.update_game_mode("normal")
                # GameScreen(game_data=game_data).render(term)
            elif keypressed == "a":
                AboutScreen(game_data=game_data).render(term)
            elif keypressed == "l":
                lang_selected = LanguageScreen(game_data=game_data).render(term)
                if lang_selected:
                    game_data.update_language(lang_selected)

    print(f"BYE!{term.normal}")
    sys.exit(0)


if __name__ == "__main__":
    main()
