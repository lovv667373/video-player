"""
Пользовательские исключения
"""

class VideoError(Exception):
    """Базовое исключение для ошибок видео"""
    pass

class FileNotFoundError(VideoError):
    """Файл не найден"""
    pass

class UnsupportedFormatError(VideoError):
    """Неподдерживаемый формат файла"""
    pass

class PlaybackError(VideoError):
    """Ошибка воспроизведения"""
    pass