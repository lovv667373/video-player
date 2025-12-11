"""
Контроллер видеоплеера
"""

import threading
import time
from tkinter import messagebox, simpledialog

class PlayerController:
    """Контроллер для управления видеоплеером"""

    def __init__(self, model):
        self.model = model
        self.view = None
        self.is_playing = False
        self.playback_thread = None
        self.on_frame_update = None
        self.on_status_update = None
        
    def set_view(self, view):
        """Установка представления"""
        self.view = view
        
    def load_video(self, file_path):
        """Загрузка видеофайла"""
        try:
            if self.model.load_video(file_path):
                self.update_status(f"Загружено: {file_path}")
                # Запускаем поток воспроизведения
                self.start_playback()
                return True
            else:
                messagebox.showerror("Ошибка", 
                                   "Не удалось загрузить видеофайл")
                return False
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки: {str(e)}")
            return False