"""
Модель видеоплеера
"""

import cv2
import numpy as np
from PIL import Image, ImageTk
import threading
import time

class VideoPlayer:
    """Класс для работы с видеофайлами"""
    
    def __init__(self):
        self.cap = None
        self.current_frame = None
        self.is_playing = False
        self.is_paused = False
        self.total_frames = 0
        self.current_frame_num = 0
        self.fps = 0
        self.duration = 0
        self.volume = 50  # Громкость от 0 до 100
        self.playback_thread = None

    def load_video(self, file_path):
        """Загрузка видеофайла"""
        try:
            if self.cap is not None:
                self.cap.release()
                
            self.cap = cv2.VideoCapture(file_path)
            if not self.cap.isOpened():
                raise ValueError("Не удалось открыть видеофайл")
                
            self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.fps = self.cap.get(cv2.CAP_PROP_FPS)
            self.duration = self.total_frames / self.fps if self.fps > 0 else 0
            self.current_frame_num = 0
            
            return True
        except Exception as e:
            print(f"Ошибка загрузки видео: {e}")
            return False
    
    def get_frame(self, frame_num=None):
        """Получение кадра из видео"""
        try:
            if self.cap is None:
                return None
                
            if frame_num is not None:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
                self.current_frame_num = frame_num
                
            ret, frame = self.cap.read()
            if ret:
                self.current_frame_num += 1
                # Конвертация BGR (OpenCV) в RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                return frame
            return None
        except Exception as e:
            print(f"Ошибка получения кадра: {e}")
            return None
        
    def play(self):
        """Начало воспроизведения"""
        if self.cap is None:
            return
            
        self.is_playing = True
        self.is_paused = False
        
    def pause(self):
        """Пауза воспроизведения"""
        self.is_paused = True
        
    def stop(self):
        """Остановка воспроизведения"""
        self.is_playing = False
        self.is_paused = False
        self.current_frame_num = 0
        if self.cap is not None:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    def set_position(self, position):
        """Установка позиции воспроизведения (0-100%)"""
        if self.cap is None:
            return
            
        frame_num = int((position / 100) * self.total_frames)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        self.current_frame_num = frame_num
    
    def set_volume(self, volume):
        """Установка громкости"""
        self.volume = max(0, min(100, volume))
    
    def release(self):
        """Освобождение ресурсов"""
        if self.cap is not None:
            self.cap.release()
            self.cap = None