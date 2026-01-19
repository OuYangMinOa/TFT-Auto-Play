from src.core import TFTAutoPlayer

import time

if __name__ == "__main__":
    import yaml

    with open("config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    game = TFTAutoPlayer(config)
    game.loop()