import sys

import blessed

from modules.logger import log
from scenes import AboutScene, GameScene, StartScene


def main() -> None:
    """Main function"""
    log("The game start")
    term = blessed.Terminal()
    # Start the menu
    keypressed = StartScene().render(term)
    log(keypressed, "keypressed")
    # Get the result of the menu to start or the tutorial or game
    while keypressed != "q":
        if keypressed == "n":  # New game
            log("New game", "menu")
            GameScene().render(term)
            pass
        elif keypressed == "t":  # Run the tutorial
            log("New tutorial", "menu")
            GameScene("tuto").render(term)
            pass
        elif keypressed == "c":  # Load last game
            log("Load last game", "menu")
            # Load the saved game data
            pass
        elif keypressed == "a":  # About the team, jam, why this
            log("About the game", "menu")
            AboutScene().render(term)
            keypressed = StartScene().render(term)

    log("The game end")
    print(term.clear)
    sys.exit(0)


if __name__ == "__main__":
    main()