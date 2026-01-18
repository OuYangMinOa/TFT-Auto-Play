from utils.screen.screen_service import LoLClientService
from src.core.game_info import GameInfo

import cv2

def test_find_lol_client_window():
    service = LoLClientService()
    hwnd = service.find_lol_client_window()
    # Since the LoL client may not be running during the test, we only check the type
    assert isinstance(hwnd, int)

    service.bring_window_to_front(hwnd) if hwnd else None
    rect = service.get_window_rect(hwnd) if hwnd else None
    print(rect)
    if hwnd:
        assert rect is not None
        left, top, right, bottom = rect
        assert right > left
        assert bottom > top

    title = service.get_window_title(hwnd) if hwnd else None
    if hwnd:
        assert title is not None
        assert "League of Legends" in title
    else:
        assert title is None

def test_screen_shot():
    service = LoLClientService()
    hwnd = service.find_lol_client_window()
    result = service.bring_window_to_front(hwnd) 
    assert result is True
    screenshot = service.get_screenshot(hwnd)

    if hwnd:
        assert screenshot is not None
    else:
        assert screenshot is None

    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2GRAY)
    cv2.imwrite("images/test_screenshot.png", screenshot_gray)


    for each_title, hwnd in service.get_all_window_titles():
        print(f"Title: {each_title}, Handle: {hwnd}, {each_title == 'League of Legends'}")


def test_coin_screen_region():
    service = LoLClientService()
    hwnd_client = service.find_lol_client_window()
    hwnd = service.find_lol_game_window()
    service.minimize_window(hwnd_client)
    screenshot = service.get_screenshot(hwnd)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2GRAY)
    print(screenshot.shape)
    print(GameInfo.get_coin(screenshot, (800, 765, 850, 785)))    