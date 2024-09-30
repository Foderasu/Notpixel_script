import pygetwindow as gw
import pyautogui


class WindowManager:
    def __init__(self, window_title):
        self.window = self.get_window_by_title(window_title)
        self.activate_window()

    def get_window_by_title(self, window_title):
        windows = gw.getWindowsWithTitle(window_title)
        if windows:
            return windows[0]
        else:
            raise Exception(f"Window with title '{window_title}' not found")

    def get_window_geometry(self):
        return {
            "left": self.window.left,
            "top": self.window.top,
            "width": self.window.width,
            "height": self.window.height,
        }

    def activate_window(self):
        self.window.activate()

    def find_button_coordinates(self, button_image_path, confidence=0.8):
        # Захватываем геометрию окна
        window_geometry = self.get_window_geometry()
        # Делаем скриншот окна
        screenshot = pyautogui.screenshot(region=(window_geometry['left'],
                                                  window_geometry['top'],
                                                  window_geometry['width'],
                                                  window_geometry['height']))
        # Ищем кнопку на скриншоте
        button_location = pyautogui.locate(button_image_path, screenshot, confidence=confidence)

        if button_location:
            # Определяем центр кнопки
            button_center = pyautogui.center(button_location)
            # Возвращаем координаты кнопки относительно всего экрана
            return {
                "x": button_center.x + window_geometry['left'],
                "y": button_center.y + window_geometry['top']
            }
        else:
            return None

