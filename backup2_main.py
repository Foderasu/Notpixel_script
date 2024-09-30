import pyautogui
import pyautogui as pag
import random
import time
import keyboard
from app_manager import AppManager
from test import click_on_image  # Импорт функции

# Пути к изображениям кнопок
NO_ENERGY_BUTTON_PATH = r"D:\Blum script\Not Pixel\buttons\No_energy.png"
DEBUG_IMAGE_PATH = r"D:\Blum script\Not Pixel\buttons\Debug_image.png"
NOTPIXEL_SCORE_BUTTON_PATH = r"D:\Blum script\Not Pixel\buttons\Notpixel_score.png"
NOTPIXEL_CLAIM_BUTTON_PATH = r"D:\Blum script\Not Pixel\buttons\Notpixel_claim.png"
NOTPIXEL_ONEMINUTE_PATH = r"D:\Blum script\Not Pixel\buttons\Notpixel_oneminute.png"
NOTPIXEL_CLOSEBANNER_PATH = r"D:\Blum script\Not Pixel\buttons\Notpixel_closebanner.png"
PAINT_BUTTON_PATH = r"D:\Blum script\Not Pixel\buttons\Paint.png"
ZOOM_TAP_PAINT_PATH = r"D:\Blum script\Not Pixel\buttons\Zoom_tap_paint.png"  # Путь к изображению Zoom Tap Paint
OKAY_PROMISE_PATH = r"D:\Blum script\Not Pixel\buttons\Okay_promise.png"
LOADING_PATH = r"D:\Blum script\Not Pixel\buttons\Loading.png"
MENU_PATH = r"D:\Blum script\Not Pixel\buttons\Menu.png"
LETS_GO_PATH = r"D:\Blum script\Not Pixel\buttons\Lets_go.png"
BLACK_SCREEN_PATH = r"D:\Blum script\Not Pixel\buttons\Black_screen.png"
BOOSTS_PATH = r"D:\Blum script\Not Pixel\buttons\Boosts.png"
PAINT_REWARD_BOOST_PATH = r"D:\Blum script\Not Pixel\buttons\Pain_reward_boost.png"
BUY_FOR_PATH = r"D:\Blum script\Not Pixel\buttons\Buy_for.png"
BACK_PATH = r"D:\Blum script\Not Pixel\buttons\Back.png"
OKAY_PATH = r"D:\Blum script\Not Pixel\buttons\Okay.png"
# Глобальная переменная для управления паузой
paused = False

def toggle_pause():
    """Функция для переключения состояния паузы."""
    global paused
    paused = not paused
    if paused:
        print("[INFO] Скрипт приостановлен. Нажмите F1 для продолжения...")
    else:
        print("[INFO] Скрипт возобновлен.")

def click_at_coordinates(x, y, offset_x=0, offset_y=0):
    """Функция кликает на заданные координаты с учетом смещения окна."""
    target_x = x + offset_x
    target_y = y + offset_y
    pag.moveTo(target_x, target_y, duration=0.01)  # Очень быстрое перемещение
    pag.click()
    print(f"[ACTION] Клик по координатам: ({target_x}, {target_y})")

def get_random_coordinates(min_x, max_x, min_y, max_y, previous_coords):
    """Генерирует случайные координаты в заданной области, исключая повторные клики."""
    while True:
        x = random.randint(min_x, max_x)
        y = random.randint(min_y, max_y)
        if (x, y) != previous_coords:
            return x, y

def find_and_click_button(image_path, confidence=0.8):
    """Пытается найти и кликнуть по кнопке. Возвращает True, если клик был выполнен успешно."""
    print(f"[INFO] Поиск кнопки по пути '{image_path}' на экране...")
    try:
        location = pag.locateCenterOnScreen(image_path, confidence=confidence)
        if location:
            pag.moveTo(location, duration=0.01)  # Очень быстрое перемещение
            pag.click()
            print(f"[SUCCESS] Кнопка найдена и нажата на координатах: ({location.x}, {location.y})")
            return True
    except Exception as e:
        print(f"[ERROR] Ошибка поиска кнопки: {e}")
    return False


def scroll_back(amount=1):
    """Прокручивает окно назад."""
    print(f"[INFO] Прокрутка назад на {amount} шагов...")
    pag.scroll(amount * -500)  # Прокручивает на указанное количество единиц
    time.sleep(0.2)  # Немного подождем, чтобы прокрутка была заметна

def handle_window_activation_error(window, min_x, max_x, min_y, max_y, previous_coords):
    """Обрабатывает ошибку активации окна, возвращая курсор в нужную область и кликая по координатам."""
    print("[ERROR] Ошибка активации окна. Попытка вернуть курсор в нужную область.")
    random_x, random_y = get_random_coordinates(min_x, max_x, min_y, max_y, previous_coords)
    click_at_coordinates(random_x, random_y, window.left, window.top)
    previous_coords = (random_x, random_y)
    time.sleep(0.5)  # Подождем немного перед повторной попыткой

def main():
    global paused, paint_flag
    paint_flag = False
    score_clicked = False

    # Инициализация AppManager
    base_path = r"D:\Telegram ферма"  # Замените на ваш путь
    app_manager = AppManager(base_path)

    print("[INFO] Запуск скрипта...")
    print("[INFO] Для паузы/возобновления скрипта нажмите F1. Для выхода нажмите ESC.")

    # Задаем диапазон координат для кликов
    min_x, max_x = 100, 200  #min_x, max_x = 130, 160 min_y, max_y = 300, 330
    min_y, max_y = 300, 400
    previous_coords = (0, 0)

    # Назначаем клавишу F1 для паузы и ESC для выхода
    keyboard.add_hotkey('F1', toggle_pause)
    keyboard.add_hotkey('ESC', lambda: exit("[INFO] Скрипт остановлен пользователем."))

    try:
        while True:
            if paused:
                time.sleep(0.5)
                continue

            windows = app_manager.get_current_window()
            if not windows:
                print("[ERROR] Окно с заголовком 'TelegramDesktop' не найдено.")
                app_manager._perform_initial_clicks()
                time.sleep(1)  # Подождите немного и попробуйте снова
                continue

            for window in windows:
                # Попытка активировать окно
                try:
                    window.activate()
                    time.sleep(0.1)
                except Exception as e:
                    print(f"[ERROR] Ошибка активации окна '{window.title}': {e}")
                    handle_window_activation_error(window, min_x, max_x, min_y, max_y, previous_coords)
                    continue

                offset_x, offset_y = window.left, window.top
                print(f"[INFO] Активировано окно '{window.title}' с смещением ({offset_x}, {offset_y}).")

                # Проверяем наличие изображения Zoom Tap Paint
                #if find_and_click_button(PAINT_BUTTON_PATH):
                    #print("[INFO] Обнаружено изображение Zoom Tap Paint. Выполняем скролл.")
                    #scroll_back()

                # Основной цикл кликов по случайным координатам
                for _ in range(5):  # Количество кликов, можно настроить
                    random_x, random_y = get_random_coordinates(min_x, max_x, min_y, max_y, previous_coords)

                    # Проверяем, была ли нажата кнопка score
                    if score_clicked:
                        break  # Прерываем цикл кликов, если кнопка нажата

                    click_at_coordinates(random_x, random_y, offset_x, offset_y)
                    scroll_back()
                    previous_coords = (random_x, random_y)
                    time.sleep(0.01)  # Очень короткая пауза между кликами

                    # Клик по изображению Paint после каждого клика
                    if find_and_click_button(PAINT_BUTTON_PATH):
                        print("[SUCCESS] Кнопка Paint нажата.")
                        paint_flag = True

                # Поиск и нажатие кнопок после появления No_energy
                if find_and_click_button(NO_ENERGY_BUTTON_PATH) and paint_flag == True:
                    time.sleep(2)
                    print("[INFO] Обнаружена кнопка No_energy. Переходим к действиям.")

                    if find_and_click_button(NOTPIXEL_SCORE_BUTTON_PATH):
                        print("[INFO] Обнаружена кнопка Notpixel_score. Переходим к следующему шагу.")
                        score_clicked = True
                        time.sleep(3)
                        if find_and_click_button(NOTPIXEL_CLAIM_BUTTON_PATH) or find_and_click_button(NOTPIXEL_ONEMINUTE_PATH):
                            print("[INFO] Обнаружена кнопка Notpixel_claim или Notpixel_oneminute. Закрываем приложение.")
                            time.sleep(1)
                            app_manager._close_telegram_desktop()
                            app_manager._close_current_app()  # Закрываем текущее приложение
                            app_manager._get_next_number()  # Переходим к следующему номеру
                            app_manager._start_app(app_manager.current_number)  # Запускаем следующее приложение
                            paint_flag = False
                            score_clicked = False
                        if find_and_click_button(LOADING_PATH):
                             print("[INFO] Обнаружена кнопка Loading. Ожидаем.")
                             time.sleep(3)
                        if find_and_click_button(BOOSTS_PATH):
                            print("[INFO] Обнаружена кнопка BOOSTS. Переходим к действиям.")
                            time.sleep(1)
                        if find_and_click_button(PAINT_REWARD_BOOST_PATH):
                            time.sleep(1)
                            print("[INFO] Обнаружена кнопка PAINT_REWARD. Переходим к действиям.")
                        if find_and_click_button(BUY_FOR_PATH):
                            time.sleep(2)
                            print("[INFO] Обнаружена кнопка BUY_FOR. Переходим к действиям.")
                            app_manager._close_telegram_desktop()
                            app_manager._close_current_app()  # Закрываем текущее приложение
                            app_manager._get_next_number()  # Переходим к следующему номеру
                            app_manager._start_app(app_manager.current_number)  # Запускаем следующее приложение
                            score_clicked = False
                else:
                    # Если No_energy не найден, ищем Notpixel_closebanner и другие кнопки
                    if find_and_click_button(NOTPIXEL_CLOSEBANNER_PATH):
                        print("[INFO] Обнаружена кнопка Notpixel_closebanner. Переходим к действиям.")
                        find_and_click_button(BACK_PATH)
                    if find_and_click_button(OKAY_PATH):
                        print("[INFO] Обнаружена кнопка Notpixel_closebanner. Переходим к действиям.")
                        #click_on_image((1586 - 25, 108 - 25, 50, 50))  # Используем координаты и размеры для клика
                    #elif find_and_click_button(BLACK_SCREEN_PATH):
                        #print("[INFO] Обнаружена кнопка Black_screen. Переходим к действиям")
                        #app_manager._close_telegram_desktop()
                    elif find_and_click_button(OKAY_PROMISE_PATH):
                        print("[INFO] Обнаружена кнопка Okay_promise. Переходим к действиям.")
                    elif find_and_click_button(LETS_GO_PATH):
                        print("[INFO] Обнаружена кнопка Lets_go. Переходим к действиям.")
                    elif find_and_click_button(MENU_PATH):
                        print("[INFO] Обнаружена кнопка Menu. Переходим к действиям.")
                        app_manager._close_telegram_desktop()
                    if find_and_click_button(LOADING_PATH):# Добавлена проверка на кнопки Notpixel_claim и Notpixel_oneminute
                        time.sleep(3)
                    if find_and_click_button(NOTPIXEL_CLAIM_BUTTON_PATH) or find_and_click_button(NOTPIXEL_ONEMINUTE_PATH):
                        print("[INFO] Обнаружена кнопка Notpixel_claim или Notpixel_oneminute в блоке else. Закрываем приложение.")
                        time.sleep(1)
                        app_manager._close_telegram_desktop()
                        app_manager._close_current_app()  # Закрываем текущее приложение
                        app_manager._get_next_number()  # Переходим к следующему номеру
                        app_manager._start_app(app_manager.current_number)  # Запускаем следующее приложение
                        paint_flag = False
                        score_clicked = False
                    if find_and_click_button(BOOSTS_PATH):
                        print("[INFO] Обнаружена кнопка BOOSTS. Переходим к действиям.")
                    if find_and_click_button(PAINT_REWARD_BOOST_PATH):
                        print("[INFO] Обнаружена кнопка PAINT_REWARD. Переходим к действиям.")
                    if find_and_click_button(BUY_FOR_PATH):
                        time.sleep(2)
                        print("[INFO] Обнаружена кнопка BUY_FOR. Переходим к действиям.")
                        app_manager._close_telegram_desktop()
                        app_manager._close_current_app()  # Закрываем текущее приложение
                        app_manager._get_next_number()  # Переходим к следующему номеру
                        app_manager._start_app(app_manager.current_number)  # Запускаем следующее приложение
            time.sleep(0.1)

    except Exception as e:
        print(f"[ERROR] Произошла ошибка во время выполнения скрипта: {e}")

if __name__ == "__main__":
    main()