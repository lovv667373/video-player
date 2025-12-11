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