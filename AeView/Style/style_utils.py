from PySide6.QtWidgets import QGraphicsDropShadowEffect
from PySide6.QtGui import QColor

# aplica el brillo exterior si esta activo o lo quita por completo
def gestionar_estilo_neon(ventana, activo=False, color_hex="#00beff"):
    if activo:
        if not color_hex: color_hex = "#00beff"

        color = QColor(color_hex)
        color.setAlpha(200)

        #comprobamos si la ventana ya tiene un efecto de sombra puesto
        efecto_actual = ventana.ui.outer_frame.graphicsEffect()

        if isinstance(efecto_actual, QGraphicsDropShadowEffect):
            # si ya existe solo le cambiamos el color en el momento
            efecto_actual.setColor(color)
        else:
            # si no existe lo creamos de cero
            brillo = QGraphicsDropShadowEffect(ventana)
            brillo.setOffset(0, 0)
            brillo.setBlurRadius(30)
            brillo.setColor(color)
            ventana.ui.outer_frame.setGraphicsEffect(brillo)

        ventana.margin = 15
    else:
        #apaga el neon completamente
        ventana.ui.outer_frame.setGraphicsEffect(None)
        ventana.margin = 0


class ThemeManager:
    # hojas de estilo
    @staticmethod
    def get_theme(name="defecto"):
        css_defecto = """
            QWidget { color: #cdd6f4; font-family: "Segoe UI", sans-serif; font-size: 13px; background-color: transparent; }
            [objectName^="outer_frame"] { background-color: #11111b; border: 2px solid #89b4fa; border-radius: 15px; }
            [objectName^="main_container"] { background-color: #1e1e2e; border-radius: 12px; border: 1px solid #313244; }
            QPushButton { background-color: #313244; border: 1px solid #45475a; border-radius: 10px; color: #ffffff; padding: 6px 18px; min-height: 28px; }
            QPushButton:hover { background-color: #45475a; border: 1px solid #89b4fa; color: #89b4fa; }
            QPushButton:pressed { background-color: #1e1e2e; border: 1px solid #74c7ec; padding-left: 10px; padding-top: 10px; }
            QPushButton[objectName^="exit_buttom"], QPushButton[objectName^="back_button"] { background-color: transparent; border: 1px solid #45475a; border-radius: 10px; color: #a6adc8; }
            QPushButton[objectName^="exit_buttom"]:hover, QPushButton[objectName^="back_button"]:hover { background-color: #f38ba8; color: #11111b; border: 1px solid #f38ba8; }
            QComboBox { background-color: #181825; border: 2px solid #313244; border-radius: 8px; padding: 5px 12px; color: #cdd6f4; }
            QComboBox:hover { border: 2px solid #89b4fa; }
            QComboBox QAbstractItemView { background-color: #181825; border: 1px solid #45475a; border-radius: 8px; selection-background-color: #313244; selection-color: #89b4fa; outline: none; padding: 4px; }
            QListView { background-color: #11111b; border: 1px solid #313244; border-radius: 12px; padding: 8px; color: #a6adc8; }
            QPlainTextEdit { background-color: #11111b; border: 1px solid #313244; border-radius: 12px; padding: 8px; color: #a6adc8; font-family: 'Consolas', 'Monaco', monospace; font-size: 11px; }
            QProgressBar { border: none; background-color: #313244; height: 12px; text-align: center; color: transparent; border-radius: 6px; }
            QProgressBar::chunk { background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #cba6f7, stop:1 #89b4fa); border-radius: 6px; }
            QLabel { color: #cdd6f4; }
            QLineEdit { background-color: #11111b; border: 1px solid #313244; border-radius: 8px; padding: 5px; color: #cdd6f4; }
        """

        css_retro = """
            QWidget { color: #94e2d5; font-family: "Segoe UI Semibold", sans-serif; font-size: 13px; background-color: transparent; }
            [objectName^="outer_frame"] { background-color: #11111b; border: 2px solid #94e2d5; border-radius: 15px; }
            [objectName^="main_container"] { background-color: #181825; border-radius: 12px; border: 1px solid #313244; }
            QPushButton { background-color: #313244; border: 1px solid #94e2d5; border-radius: 8px; color: #94e2d5; padding: 6px 18px; }
            QPushButton:hover { background-color: #94e2d5; color: #11111b; }
            QComboBox, QListView, QPlainTextEdit, QLineEdit { background-color: #11111b; border: 1px solid #313244; color: #cdd6f4; border-radius: 8px; }
            QProgressBar { background-color: #313244; height: 8px; border-radius: 4px; }
            QProgressBar::chunk { background-color: #94e2d5; }
        """

        css_moderno = """
            QWidget { color: #89b4fa; font-family: "Verdana", sans-serif; font-size: 13px; background-color: transparent; }
            [objectName^="outer_frame"] { background-color: #0b0e14; border: 2px solid #60a5fa; border-radius: 15px; }
            [objectName^="main_container"] { background-color: #111827; border-radius: 12px; border: 1px solid #1f2937; }
            QPushButton { background-color: #1f2937; border: 1px solid #3b82f6; border-radius: 5px; color: #f3f4f6; padding: 6px 18px; }
            QPushButton:hover { background-color: #3b82f6; color: white; }
            QComboBox, QListView, QPlainTextEdit, QLineEdit { background-color: #030712; border: 1px solid #1f2937; color: #9ca3af; border-radius: 5px; }
            QProgressBar { background-color: #1f2937; height: 10px; border-radius: 2px; }
            QProgressBar::chunk { background-color: #60a5fa; }
        """

        temas = {"defecto": css_defecto, "retro": css_retro, "moderno": css_moderno}
        return temas.get(name, css_defecto)

    @staticmethod
    def apply_theme(widget, theme_name):
        estilo = ThemeManager.get_theme(theme_name)
        widget.setStyleSheet(estilo)