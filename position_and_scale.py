from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QApplication
from detecting_roblox import get_roblox_window, get_window_rect

def update_position(window):
    # Only set position if the window hasn't been dragged and isn't matching Roblox chat
    if not hasattr(window, "has_been_dragged") or not window.has_been_dragged:
        hwnd = get_roblox_window()
        if hwnd and window.config["matchrobloxchat"]:
            rect = get_window_rect(hwnd)
            if rect:
                chat_width = min(300, rect[2] - rect[0])
                chat_height = min(200, (rect[3] - rect[1]) // 3)
                window.setGeometry(rect[0], rect[3] - chat_height, chat_width, chat_height)
                window.show()
        else:
            screen = QApplication.primaryScreen().geometry()
            width, height = window.width(), window.height()  # Use current size
            if window.config["cursorplacement"]:
                cursor = QCursor.pos()
                x, y = cursor.x(), cursor.y()
                x = max(0, min(x, screen.width() - width))
                y = max(0, min(y, screen.height() - height))
            elif window.config["fixedplacement"]:
                positions = {
                    "upleft": (0, 0),
                    "upright": (screen.width() - width, 0),
                    "downleft": (0, screen.height() - height),
                    "downright": (screen.width() - width, screen.height() - height),
                    "center": ((screen.width() - width) // 2, (screen.height() - height) // 2),
                    "top": ((screen.width() - width) // 2, 0),
                    "bottom": ((screen.width() - width) // 2, screen.height() - height),
                    "centerleft": (0, (screen.height() - height) // 2),
                    "centerright": (screen.width() - width, (screen.height() - height) // 2)
                }
                x, y = positions.get(window.config["fixedplacement"], (0, 0))
            else:
                x, y = screen.width() - width, screen.height() - height
            window.setGeometry(x, y, width, height)
            window.show()