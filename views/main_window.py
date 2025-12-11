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
    
    def bind_events(self):
        """Привязка событий"""
        self.controller.on_frame_update = self.update_video_frame
        self.controller.on_status_update = self.update_status
        
    def update_video_frame(self, frame):
        """Обновление отображаемого кадра"""
        try:
            if frame is not None:
                # Конвертация numpy массива в ImageTk
                from PIL import Image, ImageTk
                img = Image.fromarray(frame)
                
                # Масштабирование под размер окна
                label_width = self.video_label.winfo_width()
                label_height = self.video_label.winfo_height()
                
                if label_width > 1 and label_height > 1:
                    img = img.resize((label_width, label_height), Image.Resampling.LANCZOS)
                
                photo = ImageTk.PhotoImage(image=img)
                self.video_label.configure(image=photo)
                self.video_label.image = photo
        except Exception as e:
            print(f"Ошибка обновления кадра: {e}")

    def update_status(self, message):
        """Обновление статусной строки"""
        self.status_var.set(message)
        
    def on_window_resize(self, event):
        """Обработчик изменения размера окна"""
        if event.widget == self.root:
            # Обновляем размер видео при изменении размера окна
            if self.controller.is_playing:
                # Можно добавить логику перерисовки
                pass
    
    def open_file_dialog(self):
        """Открытие диалога выбора файла"""
        file_types = [
            ("Видео файлы", "*.mp4 *.avi *.mov *.mkv *.flv *.wmv"),
            ("Все файлы", "*.*")
        ]
        
        file_path = filedialog.askopenfilename(
            title="Выберите видеофайл",
            filetypes=file_types
        )
        
        if file_path:
            self.controller.load_video(file_path)
    
    def show_about(self):
        """Показ информации о программе"""
        messagebox.showinfo(
            "О программе",
            "Видеоплеер v1.0\n\n"
            "Лабораторная работа №3\n"
            "Приложения с графическим интерфейсом\n\n"
            "Возможности:\n"
            "- Воспроизведение видеофайлов\n"
            "- Управление воспроизведением\n"
            "- Регулировка громкости\n"
            "- Изменение размера окна"
        )