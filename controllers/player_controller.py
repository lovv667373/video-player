# controllers/player_controller.py
"""
Контроллер видеоплеера
"""

import threading
import time
from tkinter import messagebox, simpledialog
from tkinter import simpledialog

class PlayerController:
    """Контроллер для управления видеоплеером"""
    
    def __init__(self, model):
        self.model = model
        self.view = None
        self.root = None  # Ссылка на главное окно Tkinter
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
    
    def open_file(self):
        """Открытие файла через диалог"""
        if self.view:
            self.view.open_file_dialog()
    
    def toggle_play(self):
        """Переключение воспроизведения/паузы"""
        if not self.model.cap:
            messagebox.showwarning("Предупреждение", 
                                 "Сначала откройте видеофайл")
            return
            
        self.is_playing = not self.is_playing
        if self.is_playing:
            self.model.play()
            self.update_status("Воспроизведение")
        else:
            self.model.pause()
            self.update_status("Пауза")
    
    def stop(self):
        """Остановка воспроизведения"""
        self.is_playing = False
        self.model.stop()
        self.update_status("Остановлено")
        
    def set_position(self, position):
        """Установка позиции воспроизведения"""
        try:
            self.model.set_position(float(position))
            if self.view and hasattr(self.view, 'update_video_frame'):
                # Показать кадр в новой позиции
                frame = self.model.get_frame(self.model.current_frame_num)
                if frame is not None:
                    self.view.update_video_frame(frame)
        except Exception as e:
            print(f"Ошибка установки позиции: {e}")
    
    def set_volume(self, volume):
        """Установка громкости"""
        self.model.set_volume(volume)
    
    def start_playback(self):
        """Запуск потока воспроизведения"""
        if self.playback_thread and self.playback_thread.is_alive():
            return
            
        self.playback_thread = threading.Thread(target=self.playback_loop)
        self.playback_thread.daemon = True
        self.playback_thread.start()
    
    def playback_loop(self):
        """Основной цикл воспроизведения"""
        frame_delay = 1.0 / self.model.fps if self.model.fps > 0 else 0.033
        
        while True:
            if self.is_playing and self.model.cap and not self.model.is_paused:
                frame = self.model.get_frame()
                if frame is not None:
                    if self.on_frame_update:
                        self.on_frame_update(frame)
                    
                    # Обновление времени
                    if self.model.total_frames > 0:
                        current_time = self.model.current_frame_num / self.model.fps
                        if self.view and hasattr(self.view, 'control_panel'):
                            self.view.control_panel.update_progress(
                                current_time, self.model.duration
                            )
                
                time.sleep(frame_delay)
            else:
                time.sleep(0.1)  # Небольшая задержка при паузе
    
    def show_size_dialog(self):
        """Показ диалога изменения размера окна"""
        if not self.root:
            return
            
        width = simpledialog.askinteger("Размер окна", 
                                       "Ширина окна:", 
                                       minvalue=400, 
                                       maxvalue=1920)
        height = simpledialog.askinteger("Размер окна", 
                                        "Высота окна:", 
                                        minvalue=300, 
                                        maxvalue=1080)
        
        if width and height:
            self.root.geometry(f"{width}x{height}")
    
    def show_about(self):
        """Показ информации о программе"""
        if self.view:
            self.view.show_about()
    
    def show_help(self):
        """Показ справки"""
        help_text = """
        Управление видеоплеером:
        
        Горячие клавиши:
        - Cmd+O: Открыть файл
        - Пробел: Воспроизведение/Пауза
        - S: Остановить
        - Cmd+Q: Выход
        
        Использование:
        1. Нажмите "Открыть" для выбора видеофайла
        2. Используйте кнопки управления для воспроизведения
        3. Регулируйте громкость с помощью ползунка
        4. Перетаскивайте прогресс-бар для перемотки
        """
        
        messagebox.showinfo("Справка", help_text)
    
    def quit_app(self):
        """Выход из приложения"""
        self.model.release()
        if self.root:
            self.root.quit()
    
    def update_status(self, message):
        """Обновление статуса"""
        if self.on_status_update:
            self.on_status_update(message)