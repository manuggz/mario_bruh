from  src.GameEngine.game_manager import GameManager
from src.GameEngine.color_interface import ColorInterface
from src.GameArena.mario_level import MarioLevel

if __name__ == "__main__":
    gm = GameManager("Mario Bruh")
    gm.push_interface(MarioLevel())
    gm.run()
