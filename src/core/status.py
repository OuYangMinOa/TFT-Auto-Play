from enum import Enum, auto



class GameStatus(Enum):
    UNKNOWN             = auto()
    IN_LOBBY            = auto()
    FINDING_MATCH       = auto()
    SELECTING_ACCEPTS   = auto()
    WAITING_FOR_PLAYERS = auto()
    IN_TFT_GAME         = auto()
    POST_GAME_SCREEN    = auto()