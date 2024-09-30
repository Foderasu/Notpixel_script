import os
import subprocess
import time
import psutil
import pygetwindow as gw
import re
import pyautogui as pag

class AppManager:
    def __init__(self, base_path, start_number=1, end_number=91, button_paths=None):
        self.base_path = base_path
        self.start_number = start_number
        self.end_number = end_number
        self.button_paths = button_paths if button_paths is not None else []
        self.current_number = self._detect_current_number()
        self.current_process = None
        if self.current_number is not None:
            self._start_app(self.current_number)
        else:
            print("Не обнаружен ни один экземпляр Telegram, начинаем с первого номера.")
            self.current_number = self.start_number
            self._start_app(self.current_number)

    def _get_app_path(self, number):
        folder_name = f"{number} - "
        for name in os.listdir(self.base_path):
            if name.startswith(folder_name):
                return os.path.join(self.base_path, name, "Telegram.exe")
        return None

    def _detect_current_number(self):
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            if proc.info['name'] == 'Telegram.exe' and proc.info['exe']:
                for folder_name in os.listdir(self.base_path):
                    match = re.match(r"(\d+) - ", folder_name)
                    if match:
                        number = int(match.group(1))
                        app_path = os.path.join(self.base_path, folder_name, "Telegram.exe")
                        if proc.info['exe'] == app_path:
                            return number
        return None

    def _start_app(self, number):
        app_path = self._get_app_path(number)
        if app_path and os.path.isfile(app_path):
            try:
                self.current_process = subprocess.Popen(app_path)
                print(f"Запущено: {app_path}")
                time.sleep(3)  # Даем время на запуск приложения

                # Ожидание появления окна и выполнение начальных кликов
                if self._wait_for_window("Telegram"):
                    self._perform_initial_clicks()  # Выполняем начальные клики после запуска приложения
                else:
                    print("[ERROR] Не удалось найти окно TelegramDesktop.")
                    self._close_current_app()  # Закрываем приложение, если окно не найдено

            except Exception as e:
                print(f"[ERROR] Ошибка при запуске приложения '{app_path}': {e}")
                self._close_current_app()  # Закрываем приложение в случае ошибки
                self._get_next_number()  # Переходим к следующему номеру
                self._start_app(self.current_number)  # Пытаемся запустить следующее приложение
        else:
            print(f"[ERROR] Ошибка: файл не найден {app_path}")
            self._get_next_number()  # Переходим к следующему номеру
            self._start_app(self.current_number)  # Пытаемся запустить следующее приложение
    def _wait_for_window(self, title, timeout=30):
        """Ожидание появления окна с заданным заголовком."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            windows = gw.getWindowsWithTitle(title)
            if windows:
                return True
            time.sleep(1)
        print(f"[ERROR] Окно с заголовком '{title}' не найдено в течение {timeout} секунд.")
        return False

    def _perform_initial_clicks(self):
        """Выполняет начальные клики по указанным изображениям."""
        print("[INFO] Выполняем начальные клики...")
        button_paths = [
            r"D:\Blum script\Not Pixel\buttons\Notpixel.png",
            r"D:\Blum script\Not Pixel\buttons\Notpixel_start.png",
            r"D:\Blum script\Not Pixel\buttons\Not_pixel_ok.png"
        ]
        for button_path in button_paths:
            if not self._find_and_click_button(button_path):
                print(f"[ERROR] Не удалось нажать кнопку по пути {button_path}.")
                return
            time.sleep(1)  # Пауза между кликами

    def _find_and_click_button(self, image_path, max_attempts=20, confidence=0.8):
        """
        Пытается найти и кликнуть по кнопке.
        Возвращает True, если клик был выполнен успешно.
        """
        print(f"[INFO] Поиск кнопки по пути '{image_path}' на экране...")
        for attempt in range(1, max_attempts + 1):
            print(f"[INFO] Попытка {attempt} из {max_attempts}")
            try:
                location = pag.locateCenterOnScreen(image_path, confidence=confidence)
                if location:
                    pag.moveTo(location, duration=0.25)
                    pag.click()
                    print(f"[SUCCESS] Кнопка найдена и нажата на координатах: ({location.x}, {location.y})")
                    return True
            except pag.ImageNotFoundException:
                print("[WARNING] Кнопка не найдена. Повторная попытка через 1 секунду...")
                time.sleep(1)
            except ValueError as e:
                print(f"[ERROR] Ошибка поиска кнопки: {e}")
                time.sleep(1)
        print("[ERROR] Кнопка не была найдена после всех попыток.")
        return False

    def _close_telegram_desktop(self):
        window_title = "TelegramDesktop"
        windows = gw.getWindowsWithTitle(window_title)
        for window in windows:
            window.close()
            print(f"Закрыто окно: {window_title}")

    def _close_current_app(self):
        if self.current_process:
            # Завершаем текущий процесс
            self.current_process.terminate()
            self.current_process.wait(timeout=5)  # Ждем завершения процесса в течение 5 секунд
            self.current_process = None
            print("Закрыто текущее приложение")

        # Проверяем, что процесс Telegram действительно закрыт
        if not self._is_telegram_running():
            print("[INFO] Процесс Telegram успешно завершен.")
        else:
            print("[ERROR] Процесс Telegram всё ещё запущен. Попытка завершить принудительно.")
            self._force_close_telegram()

    def _is_telegram_running(self):
        """Проверяет, запущен ли процесс Telegram.exe."""
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == 'Telegram.exe':
                return True
        return False

    def _force_close_telegram(self):
        """Принудительно завершает процесс Telegram.exe."""
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == 'Telegram.exe':
                try:
                    proc.kill()
                    print(f"[FORCE CLOSE] Процесс Telegram (PID: {proc.pid}) был принудительно завершен.")
                except Exception as e:
                    print(f"[ERROR] Не удалось завершить процесс Telegram (PID: {proc.pid}): {e}")

    def _get_next_number(self):
        if self.current_number is not None:
            if self.current_number < self.end_number:
                self.current_number += 1
            else:
                # Если достигли последнего номера, начинаем сначала с начального номера
                print("Достигнут последний номер. Начинаем сначала.")
                self.current_number = self.start_number

    def handle_key(self, key):
        if key == 'f2':
            self._close_current_app()
            self._get_next_number()
            self._start_app(self.current_number)

    def handle_automatic(self):
        while True:
            self.handle_key('f2')
            time.sleep(1)

    def get_current_window(self):
        return gw.getWindowsWithTitle("TelegramDesktop")



