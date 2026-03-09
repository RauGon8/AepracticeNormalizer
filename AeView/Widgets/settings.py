from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QColorDialog
from AeView.Ui.ui_settings import Ui_Form
from AeCore.AeUtils.settings_manager import SettingsManager
from AeView.Style.style_utils import gestionar_estilo_neon, ThemeManager

class SettingsWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.main_window = main_window
        self.settings_manager = SettingsManager()

        # si el json falla lee false por defecto
        ajustes = self.settings_manager.cargar_ajustes()
        self.color_actual = ajustes.get("neon_color", "#00beff")
        self.ui.activar_neon.setChecked(ajustes.get("neon_activo", False))

        tema_guardado = ajustes.get("tema", "defecto")
        index = self.ui.tipo_color.findText(tema_guardado)
        if index >= 0:
            self.ui.tipo_color.setCurrentIndex(index)

        #aplicar estilo heredado al abrir
        ThemeManager.apply_theme(self, tema_guardado)
        gestionar_estilo_neon(self, ajustes.get("neon_activo", False), self.color_actual)

        # conexiones
        self.ui.back_button.clicked.connect(self.close)
        self.ui.cambiar_color_neon.clicked.connect(self.elegir_color)
        self.ui.boton_guardar.clicked.connect(self.guardar_y_aplicar)

    # selector de colores nativo
    def elegir_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color_actual = color.name()

    # guarda y aplica al momento
    def guardar_y_aplicar(self):
        """
        guardamos ajustes actuales y actualizamos interfaz al momento
        """
        tema_seleccionado = self.ui.tipo_color.currentText()
        neon_activo = self.ui.activar_neon.isChecked()

        ajustes = self.settings_manager.cargar_ajustes()
        ajustes["tema"] = tema_seleccionado
        ajustes["neon_activo"] = neon_activo
        ajustes["neon_color"] = self.color_actual

        self.settings_manager.guardar_ajustes_completos(ajustes)

        #aplicar a ambas ventanas
        ThemeManager.apply_theme(self, tema_seleccionado)
        gestionar_estilo_neon(self, neon_activo, self.color_actual)
        self.main_window.aplicar_configuracion_visual()
        self.close()