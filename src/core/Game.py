from utils.screen.screen_service import LoLClientService

from .status import GameStatus

import numpy as np
import pyautogui
import time
import cv2

class TFTAutoPlayer:
    def __init__(self, config: dict):
        self.screen_service = LoLClientService()
        self.status : GameStatus = GameStatus.UNKNOWN
        self.config = config

        self.accept_button_img = self.read_picture(self.config['accept_pic'])
        self.find_game_img     = self.read_picture(self.config['find_game_pic'])
        self.leave_game_img    = self.read_picture(self.config['leave_game_pic'])
        self.one_more_game_img = self.read_picture(self.config['one_more_pic'])
        self.item_blue_img     = self.read_picture(self.config['item_blue_pic'])
        self.is_gaming_pic     = self.read_picture(self.config['is_gaming_pic'])

    def loop(self):
        """
        持續監控遊戲畫面，並截取當前畫面，想辦法進入遊戲。
        """
        hwnd_client = self.screen_service.find_lol_client_window()
        if hwnd_client is None:
            self.status = GameStatus.UNKNOWN
            raise RuntimeError("Cannot find League of Legends client window.")
        print("找到 LoL，開始自動化流程")
        while True:
            hwnd_client = self.screen_service.find_lol_client_window()
            
            if hwnd_client is None:
                self.status = GameStatus.UNKNOWN
                continue

            left, top, _, _ = self.screen_service.get_window_rect(hwnd_client)
            screenshot = self.screen_service.get_screenshot(hwnd_client)
            screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
            cv2.imwrite("images/current_screenshot.png", screenshot_gray)
            self.click_find_game_button(screenshot_gray, left, top)
            self.click_accept_button(screenshot_gray, left, top)
            self.click_one_more_game_button(screenshot_gray, left, top)
            time.sleep(3)

            if self.status == GameStatus.SELECTING_ACCEPTS:
                print("等待接受遊戲中...")
                time.sleep(5)
                self.status = GameStatus.IN_TFT_GAME
                continue

            self.update_in_game_status(screenshot_gray, left, top)

            if self.status == GameStatus.IN_TFT_GAME:
                pyautogui.click(x=1, y=1)
                screenshot_game = self.screen_service.get_full_screenshot()
                screenshot_game_gray = cv2.cvtColor(screenshot_game, cv2.COLOR_BGR2GRAY)
                cv2.imwrite("images/full_screen_shot.png", screenshot_game_gray)
                self.click_item_blue_button(screenshot_game_gray, 0, 0)
                self.click_leave_game_button(screenshot_game_gray, left, top)
            else:
                # 有機會截圖到這裡
                self.click_item_blue_button(screenshot_gray, 0, 0)
                self.click_leave_game_button(screenshot_gray, left, top)

    def click_accept_button(self, screenshot: np.ndarray, left: int, top: int):
        """
        點擊接受遊戲按鈕。
        """
        threshold = self.config['thresholds']['accept_button']
        _match, max_loc = self.__check_if_compare(screenshot, self.accept_button_img, threshold)
        if _match:
            self.status = GameStatus.FINDING_MATCH
            print("找到接受按鈕，準備點擊")
            button_x = left + max_loc[0] + self.accept_button_img.shape[1] // 2
            button_y = top + max_loc[1] + self.accept_button_img.shape[0] // 2
            self.screen_service.bring_window_to_front(self.screen_service.find_lol_client_window())
            cv2.waitKey(100) 
            pyautogui.click(x=button_x, y=button_y)
            self.status = GameStatus.SELECTING_ACCEPTS

    def click_find_game_button(self, screenshot: np.ndarray, left: int, top: int):
        """
        點擊尋找遊戲按鈕。
        """
        threshold = self.config['thresholds']['find_game_button']
        _match, max_loc = self.__check_if_compare(screenshot, self.find_game_img, threshold)
        if _match:
            self.status = GameStatus.IN_LOBBY
            print("開始尋找遊戲")
            button_x = left + max_loc[0] + self.find_game_img.shape[1] // 2
            button_y = top + max_loc[1] + self.find_game_img.shape[0] // 2
            self.screen_service.bring_window_to_front(self.screen_service.find_lol_client_window())
            cv2.waitKey(100) 
            pyautogui.click(x=button_x, y=button_y)
            self.status = GameStatus.FINDING_MATCH

    def click_leave_game_button(self, screenshot: np.ndarray, left: int, top: int):
        """
        點擊離開遊戲按鈕。
        """
        threshold = self.config['thresholds']['leave_game_button']
        _match, max_loc = self.__check_if_compare(screenshot, self.leave_game_img, threshold)
        if _match:
            self.status = GameStatus.IN_TFT_GAME
            print("找到離開遊戲按鈕，準備點擊")
            button_x = left + max_loc[0] + self.leave_game_img.shape[1] // 2
            button_y = top + max_loc[1] + self.leave_game_img.shape[0] // 2
            cv2.waitKey(100) 
            pyautogui.moveTo(x=button_x, y=button_y)
            pyautogui.mouseDown(x=button_x, y=button_y)
            time.sleep(0.1)
            pyautogui.mouseUp(x=button_x, y=button_y)
            self.status = GameStatus.POST_GAME_SCREEN

    def update_in_game_status(self, screenshot: np.ndarray, left: int, top: int) -> bool:
        """
        檢查是否在遊戲中。
        """
        threshold = self.config['thresholds']['is_gaming']
        _match, _ = self.__check_if_compare(screenshot, self.is_gaming_pic, threshold)
        if _match:
            print("確認在遊戲中")
            self.status = GameStatus.IN_TFT_GAME
            return True

    def click_one_more_game_button(self, screenshot: np.ndarray, left: int, top: int):
        """
        點擊再來一局按鈕。
        """
        threshold = self.config['thresholds']['one_more_button']
        _match, max_loc = self.__check_if_compare(screenshot, self.one_more_game_img, threshold)
        if _match:
            self.status = GameStatus.POST_GAME_SCREEN
            print("找到再來一局按鈕，準備點擊")
            button_x = left + max_loc[0] + self.one_more_game_img.shape[1] // 2
            button_y = top + max_loc[1] + self.one_more_game_img.shape[0] // 2
            cv2.waitKey(100) 
            pyautogui.click(x=button_x, y=button_y)
            self.status = GameStatus.IN_LOBBY

    def click_item_blue_button(self, screenshot: np.ndarray, left: int, top: int):
        """
        點擊藍色物品按鈕。
        """
        threshold = self.config['thresholds']['item_blue']
        _match, max_loc = self.__check_if_compare(screenshot, self.item_blue_img, threshold)
        if _match:
            self.status = GameStatus.IN_TFT_GAME
            print("找到藍色物品按鈕，準備點擊")
            button_x = left + max_loc[0] + self.item_blue_img.shape[1] // 2
            button_y = top + max_loc[1] + self.item_blue_img.shape[0] // 2
            cv2.waitKey(100) 
            pyautogui.click(x=button_x, y=button_y)


    def __check_if_compare(self, screenshot: np.ndarray, template: np.ndarray, threshold: float) -> bool:
        """
        比較截圖與範本圖片是否相似，若相似度高於閾值則回傳True。
        """
        shot_height, shot_width = screenshot.shape
        res_ratio = (shot_width / self.config['pic_client_resolution']['width'], shot_height / self.config['pic_client_resolution']['height'])
        # 調整接受按鈕圖片大小以符合當前解析度
        template_resized = cv2.resize(template, (int(template.shape[1] * res_ratio[0]), int(template.shape[0] * res_ratio[1])))
        cv2.imwrite("images/resized.png", template_resized)
        result = cv2.matchTemplate(screenshot, template_resized, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        print(f"Template matching max value: {max_val}, threshold: {threshold}, ratio: {res_ratio}")
        return max_val >= threshold, max_loc

    def read_picture(self, path: str) -> np.ndarray:
        """
        讀取圖片檔案，並轉換為灰階影像。
        """
        img = cv2.imread(path)
        if img is None:
            raise FileNotFoundError(f"Cannot read image from path: {path}")
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return gray_img