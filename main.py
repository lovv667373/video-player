#!/usr/bin/env python3
"""
Главный файл приложения Video Player
"""

import tkinter as tk
from views.main_window import MainWindow
from controllers.player_controller import PlayerController
from models.video_player import VideoPlayer

def main():
    """Точка входа в приложение"""
    try:
        # Создаем корневое окно
        root = tk.Tk()
        root.title("Video Player")
        root.geometry("800x600")
           
        # Создаем модель
        player_model = VideoPlayer()
        
        # Создаем контроллер
        controller = PlayerController(player_model)
        
        # Создаем главное окно
        app = MainWindow(root, controller)
        
        # Запускаем главный цикл
        root.mainloop()
        
    except Exception as e:
        print(f"Ошибка при запуске приложения: {e}")
        input("Нажмите Enter для выхода...")

if __name__ == "__main__":
    main()