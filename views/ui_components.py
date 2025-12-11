"""
Компоненты пользовательского интерфейса
"""

import tkinter as tk
from tkinter import ttk, Menu

class ControlPanel(ttk.Frame):
    """Панель управления воспроизведением"""
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        """Настройка интерфейса панели управления"""
        # Кнопка открытия файла
        open_btn = ttk.Button(self, text="Открыть", 
                            command=self.controller.open_file)
        open_btn.pack(side=tk.LEFT, padx=2)
        
        # Кнопки управления
        self.play_btn = ttk.Button(self, text="▶", width=3,
                                 command=self.controller.toggle_play)
        self.play_btn.pack(side=tk.LEFT, padx=2)
        
        stop_btn = ttk.Button(self, text="⏹", width=3,
                            command=self.controller.stop)
        stop_btn.pack(side=tk.LEFT, padx=2)
        
        # Прогресс-бар
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Scale(self, from_=0, to=100,
                                    variable=self.progress_var,
                                    orient=tk.HORIZONTAL,
                                    command=self.on_progress_change)
        self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        # Громкость
        ttk.Label(self, text="🔊").pack(side=tk.LEFT, padx=(10, 2))
        
        self.volume_var = tk.IntVar(value=50)
        volume_scale = ttk.Scale(self, from_=0, to=100,
                               variable=self.volume_var,
                               orient=tk.HORIZONTAL,
                               command=self.on_volume_change,
                               length=100)
        volume_scale.pack(side=tk.LEFT, padx=(0, 10))
        
        # Время
        self.time_label = ttk.Label(self, text="00:00 / 00:00")
        self.time_label.pack(side=tk.RIGHT, padx=10)
        
    def on_progress_change(self, value):
        """Обработка изменения прогресса"""
        try:
            self.controller.set_position(float(value))
        except ValueError:
            pass
    
    def on_volume_change(self, value):
        """Обработка изменения громкости"""
        try:
            self.controller.set_volume(int(float(value)))
        except ValueError:
            pass
    
    def update_progress(self, current_time, total_time):
        """Обновление прогресса и времени"""
        self.progress_var.set((current_time / total_time) * 100 if total_time > 0 else 0)
        
        # Форматирование времени
        current_str = self.format_time(current_time)
        total_str = self.format_time(total_time)
        self.time_label.config(text=f"{current_str} / {total_str}")
        
    def format_time(self, seconds):
        """Форматирование времени в MM:SS"""
        if seconds < 0:
            return "00:00"
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"

class MenuBar(Menu):
    """Меню приложения"""
    
    def __init__(self, root, controller):
        super().__init__(root)
        self.controller = controller
        self.setup_menu()

