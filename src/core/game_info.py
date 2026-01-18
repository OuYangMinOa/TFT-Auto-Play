# 使用 ocr 拿到金幣數量
import cv2
import numpy as np
import pytesseract


class GameInfo:

    @classmethod
    def get_coin(cls, screenshot: np.ndarray, roi: tuple[int, int, int, int]) -> int:
        """
        從截圖中擷取金幣數量。
        Args:
            screenshot (np.ndarray): 遊戲截圖。
            roi (tuple[int, int, int, int]): 金幣區域的 (left, top, right, bottom)。
        """
        left, top, right, bottom = roi
        coin_region = screenshot[top:bottom, left:right]
        gray = cv2.cvtColor(coin_region, cv2.COLOR_BGR2GRAY)
        cv2.imwrite("images/coin_region.png", gray)
        text = pytesseract.image_to_string(gray, config='--psm 6 outputbase digits')
        try:
            return int(text)
        except ValueError:
            return 0
