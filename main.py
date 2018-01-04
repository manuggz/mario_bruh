from src.GameArena.mario_level import MarioLevel
from src.game_engine_ggz.game_manager import GameManager

if __name__ == "__main__":
    gm = GameManager("Mario Bruh")
    gm.push_interface(MarioLevel(gm))
    gm.run()
