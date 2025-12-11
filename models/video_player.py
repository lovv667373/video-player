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