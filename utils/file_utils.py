"""
Утилиты для работы с файлами
"""

import os

def get_supported_formats():
    """Получение списка поддерживаемых форматов"""
    return {
        '.mp4': 'MPEG-4',
        '.avi': 'AVI',
        '.mov': 'QuickTime',
        '.mkv': 'Matroska',
        '.flv': 'Flash Video',
        '.wmv': 'Windows Media Video',
    }

def is_video_file(file_path):
    """Проверка, является ли файл видео"""
    _, ext = os.path.splitext(file_path.lower())
    supported = get_supported_formats()
    return ext in supported

def get_file_info(file_path):
    """Получение информации о файле"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл не найден: {file_path}")
    
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    file_ext = os.path.splitext(file_path)[1].lower()
    
    return {
        'name': file_name,
        'size': file_size,
        'extension': file_ext,
        'path': file_path
    }