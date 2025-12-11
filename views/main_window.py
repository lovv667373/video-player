"""
Главное окно приложения
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from views.ui_components import ControlPanel, MenuBar
import threading

class MainWindow:
    """Класс главного окна приложения"""
    
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.video_label = None
        self.control_panel = None
        self.setup_ui()
        self.bind_events()
    
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        # Меню
        self.menu_bar = MenuBar(self.root, self.controller)
        self.root.config(menu=self.menu_bar)
        
        # Основная область
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Область для видео
        video_frame = ttk.Frame(main_frame, relief=tk.SUNKEN, borderwidth=2)
        video_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.video_label = ttk.Label(video_frame, text="Откройте видеофайл", 
                                     background='black', foreground='white')
        self.video_label.pack(fill=tk.BOTH, expand=True)
        
        # Панель управления
        self.control_panel = ControlPanel(main_frame, self.controller)
        self.control_panel.pack(fill=tk.X)
        
        # Статус бар
        self.status_var = tk.StringVar(value="Готов")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Настройка изменения размера окна
        self.root.minsize(400, 300)
        self.root.bind('<Configure>', self.on_window_resize)