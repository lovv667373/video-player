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