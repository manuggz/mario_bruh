from  src.GameEngine.game_manager import GameManager
from src.GameEngine.color_interface import ColorInterface

if __name__ == "__main__":
    gm = GameManager()
    gm.push_interface(ColorInterface('blue'))
    gm.run()
