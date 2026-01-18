from .screen_client import ScreenClient



class LoLClientService(ScreenClient):
    def __init__(self):
        super().__init__()

    def find_lol_client_window(self) -> int | None:
        """Find the League of Legends client window handle.
        returns the window handle if found, otherwise None.
        """
        return self.find_window_by_title_strict("League of Legends") 
    
    def find_lol_game_window(self) -> int | None:
        """Find the League of Legends game window handle.
        returns the window handle if found, otherwise None.
        """
        return self.find_window_by_title("League of Legends (TM)")