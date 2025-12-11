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
