import sys
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox
from PySide6.QtCore import Qt, QRect, QStringListModel

from AeView.Ui.ui_main_window import Ui_Form
from AeView.Style.style_utils import gestionar_estilo_neon, ThemeManager
from settings import SettingsWindow
from AeCore.Worker import Worker
from AeCore.AeUtils.settings_manager import SettingsManager


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setMouseTracking(True)
        self.ui.outer_frame.setMouseTracking(True)

        # conexiones principales
        self.ui.exit_buttom.clicked.connect(self.close)
        self.ui.pushButton.clicked.connect(self.start_process)

        self.ui.add_buttom.clicked.connect(self.anadir_ruta)
        self.ui.del_buttom.clicked.connect(self.eliminar_ruta)
        self.ui.del_all_buttom.clicked.connect(self.eliminar_todas)

        self.ui.file_type.currentIndexChanged.connect(self.actualizar_vista_lista)

        # boton de ajustes
        self.ui.settings.clicked.connect(self.abrir_ajustes)
        self.ventana_ajustes = None

        self.drag_pos = None
        self.resize_dir = ""
        self.start_geometry = QRect()
        self.start_mouse_pos = None

        self.margin = 15
        self.setMinimumSize(800, 600)

        self.list_model = QStringListModel()
        self.ui.listView.setModel(self.list_model)

        self.settings_manager = SettingsManager()

        self.rutas_por_tipo = {0: [], 1: [], 2: [], 3: []}

        # carga inicial de datos
        ajustes = self.settings_manager.cargar_ajustes()
        rutas_guardadas = ajustes.get("rutas_guardadas", {})
        for i in range(4):
            self.rutas_por_tipo[i] = rutas_guardadas.get(str(i), [])

        self.ui.file_type.setCurrentIndex(ajustes.get("tipo_archivo_seleccionado", 0))
        self.ui.int_order.setText(ajustes.get("orden_trabajo_texto", ""))

        self.actualizar_vista_lista()

        # forzamos el repintado inicial del tema y neon
        self.aplicar_configuracion_visual()

    #lee los ajustes y recarga el aspecto grafico entero
    def aplicar_configuracion_visual(self):
        """
        leemos los ajustes guardados en settings manager

        refresca los estilos css y aplica el efecto neon y repintamos con repaint() para
        actualizar al momento la pantalla
        """
        ajustes = self.settings_manager.cargar_ajustes()
        tema = ajustes.get("tema", "defecto")
        neon_activo = ajustes.get("neon_activo", False)
        neon_color = ajustes.get("neon_color", "#00beff")

        #aplicamos el tema css
        ThemeManager.apply_theme(self, tema)

        # limpiamos la cache del motor de estilos
        self.style().unpolish(self)
        self.style().polish(self)

        # aplicamos el neon siempre despues de refrescar el css
        gestionar_estilo_neon(self, neon_activo, neon_color)

        # usamos repaint en lugar de update para obligar a dibujar el frame en el acto
        self.ui.outer_frame.repaint()
        self.repaint()

    # abre la ventana de ajustes
    def abrir_ajustes(self):
        if self.ventana_ajustes is None:
            self.ventana_ajustes = SettingsWindow(self)
            self.ventana_ajustes.setWindowModality(Qt.ApplicationModal)
        self.ventana_ajustes.show()

    def actualizar_vista_lista(self):
        idx = self.ui.file_type.currentIndex()
        self.list_model.setStringList(self.rutas_por_tipo.get(idx, []))

    def anadir_ruta(self):
        """
        abrimos un QMessageBox para selecionar entre archivos o carpetas y dependiendo de ello se añade una cosao u la otra
        """
        idx = self.ui.file_type.currentIndex()

        if idx == 1:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Tipo de entrada")
            msg_box.setText("¿Qué deseas añadir?")
            btn_folder = msg_box.addButton("Carpeta", QMessageBox.ActionRole)
            btn_files = msg_box.addButton("Archivos", QMessageBox.ActionRole)
            msg_box.addButton("Cancelar", QMessageBox.RejectRole)
            msg_box.exec()

            if msg_box.clickedButton() == btn_folder:
                ruta = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta")
                if ruta and ruta not in self.rutas_por_tipo[idx]:
                    self.rutas_por_tipo[idx].append(ruta)
                self.actualizar_vista_lista()
            elif msg_box.clickedButton() == btn_files:
                rutas, _ = QFileDialog.getOpenFileNames(
                    self,
                    "Seleccionar archivos Excel",
                    "",
                    "Excel Files (*.xls *.xlsx);;All Files (*)"
                )
                if rutas:
                    for r in rutas:
                        if r not in self.rutas_por_tipo[idx]:
                            self.rutas_por_tipo[idx].append(r)
                    self.actualizar_vista_lista()
        else:
            if len(self.rutas_por_tipo[idx]) >= 1:
                QMessageBox.warning(self, "Aviso", "No se puede añadir más de un archivo de este tipo")
                return

            ruta, _ = QFileDialog.getOpenFileName(
                self,
                "Seleccionar archivo Excel",
                "",
                "Excel Files (*.xls *.xlsx);;All Files (*)"
            )
            if ruta:
                self.rutas_por_tipo[idx] = [ruta]
                self.actualizar_vista_lista()

    def eliminar_ruta(self):
        """
        elimina internamente la ruta seleccionada por el usuario y actualiza la vista
        :return:
        """
        indexes = self.ui.listView.selectedIndexes()
        if indexes:
            row = indexes[0].row()
            idx = self.ui.file_type.currentIndex()
            self.rutas_por_tipo[idx].pop(row)
            self.actualizar_vista_lista()

    def eliminar_todas(self):
        """
        permitimos eliminar todos los tipos de ruta, o solo un tipo de archivo
        """
        #cremos el cuadro
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Eliminar rutas")
        msg_box.setText("¿Qué rutas deseas eliminar?")

        #añadimos los botones
        btn_tipo = msg_box.addButton("Solo este tipo de archivos.", QMessageBox.ActionRole)
        btn_todo = msg_box.addButton("Todos los archivos subidos.", QMessageBox.ActionRole)
        msg_box.addButton("Cancelar", QMessageBox.RejectRole)

        msg_box.exec()

        #logica de los botones
        if msg_box.clickedButton() == btn_tipo:
            idx = self.ui.file_type.currentIndex()
            self.rutas_por_tipo[idx] = []
            self.actualizar_vista_lista()
            self.ui.plainTextEdit.appendPlainText(">>> Sistema: Lista vaciada.")
        elif msg_box.clickedButton() == btn_todo:
            #vaciamos el diccionario completo
            for i in self.rutas_por_tipo:
                self.rutas_por_tipo[i] = []
            self.actualizar_vista_lista()
            self.ui.plainTextEdit.appendPlainText(">>> Sistema: Todas las listas han sido eliminadas.")

    def start_process(self):
        """
        iniciamos el procesamiento del backend pidiendo la carpeta de salida

        pillamos la configuracion  y conectamos señales lanzando el hilo y desactivando el boton principal
        para evitar errores
        """
        carpeta_salida = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta de Salida")

        if not carpeta_salida:
            return

        config = {
            "rutas_maestras": self.rutas_por_tipo,
            "orden_trabajo": self.ui.int_order.text(),
            "carpeta_salida": carpeta_salida
        }
        self.worker = Worker(config)

        #conectamos las señales de progreso
        self.worker.progress.connect(self.update_progress_ui)
        self.worker.finished.connect(self.on_finished)
        self.worker.error_signal.connect(self.on_error)

        # Iniciamos el hilo y bloqueamos el botón para evitar clics duplicados
        self.worker.start()
        self.ui.pushButton.setEnabled(False)
        self.ui.plainTextEdit.appendPlainText(f">>> Sistema: Iniciando proceso. Salida en: {carpeta_salida}")

    def update_progress_ui(self, value, message):
        """
        actualizamos los componentes visuales de progreso desde la señal del backend

        :param value: porcentaje numerico para la barra de progreso
        :param message: el mensaje descriptivo para el log
        """
        self.ui.progressBar.setValue(value)
        self.ui.plainTextEdit.appendPlainText(message)

    def on_finished(self, result):
        self.ui.plainTextEdit.appendPlainText(">>> Sistema: Proceso finalizado correctamente.")
        self.ui.pushButton.setEnabled(True)

    def on_error(self, error_msg):
        self.ui.plainTextEdit.appendPlainText(f"!!! ERROR: {error_msg}")
        self.ui.pushButton.setEnabled(True)

    def closeEvent(self, event):
        """
        sirve para pillar las cosas antes de que la ventana se cierre y poder guardar el estado actual del programa
        """
        combo_index = self.ui.file_type.currentIndex()
        orden_texto = self.ui.int_order.text()

        self.settings_manager.guardar_ajustes(self.rutas_por_tipo, combo_index, orden_texto)
        event.accept()

    def mouseDoubleClickEvent(self, event):
        """
        doble click para maximizar la ventana
        """

        if event.button() == Qt.LeftButton:
            pos = event.position().toPoint()
            rect = self.rect()

            if (pos.x() <= self.margin or pos.x() >= rect.width() - self.margin or
                    pos.y() <= self.margin or pos.y() >= rect.height() - self.margin):

                if self.isMaximized():
                    self.showNormal()
                else:
                    self.showMaximized()
            event.accept()

    def mousePressEvent(self, event):
        """
        gestiona el presionar raton, viendo si el usuario ha pinchado en la ventana y dependiendo de ello
        la ventana se mueve o se redimensiona
        """
        if event.button() == Qt.LeftButton:
            pos = event.position().toPoint()
            rect = self.rect()

            l = pos.x() <= self.margin
            r = pos.x() >= rect.width() - self.margin
            t = pos.y() <= self.margin
            b = pos.y() >= rect.height() - self.margin

            self.resize_dir = ""
            if t:
                self.resize_dir += "top"
            elif b:
                self.resize_dir += "bottom"

            if l:
                self.resize_dir += ("_" if self.resize_dir else "") + "left"
            elif r:
                self.resize_dir += ("_" if self.resize_dir else "") + "right"

            if self.resize_dir:
                self.start_geometry = self.geometry()
                self.start_mouse_pos = event.globalPosition().toPoint()
            else:
                self.drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """
        gestiona el movimiento del raton para actualizar el cursor, posteriormente tambien ejecuta la matematica para mover
        o cambiar el tamaño de la ventana
        """
        pos = event.position().toPoint()
        rect = self.rect()
        g_pos = event.globalPosition().toPoint()

        if not self.drag_pos and not self.resize_dir:
            l = pos.x() <= self.margin
            r = pos.x() >= rect.width() - self.margin
            t = pos.y() <= self.margin
            b = pos.y() >= rect.height() - self.margin

            if (r and b) or (l and t):
                self.setCursor(Qt.SizeFDiagCursor)
            elif (r and t) or (l and b):
                self.setCursor(Qt.SizeBDiagCursor)
            elif r or l:
                self.setCursor(Qt.SizeHorCursor)
            elif b or t:
                self.setCursor(Qt.SizeVerCursor)
            else:
                self.setCursor(Qt.ArrowCursor)

        if self.resize_dir:
            dx = g_pos.x() - self.start_mouse_pos.x()
            dy = g_pos.y() - self.start_mouse_pos.y()

            x = self.start_geometry.x()
            y = self.start_geometry.y()
            w = self.start_geometry.width()
            h = self.start_geometry.height()

            if "left" in self.resize_dir:
                new_w = max(self.minimumWidth(), w - dx)
                if new_w > self.minimumWidth(): x += dx; w = new_w
            elif "right" in self.resize_dir:
                w = max(self.minimumWidth(), w + dx)

            if "top" in self.resize_dir:
                new_h = max(self.minimumHeight(), h - dy)
                if new_h > self.minimumHeight(): y += dy; h = new_h
            elif "bottom" in self.resize_dir:
                h = max(self.minimumHeight(), h + dy)

            self.setGeometry(x, y, w, h)

        elif self.drag_pos:
            self.move(g_pos - self.drag_pos)

        event.accept()
    #restablecemos el cursor a su modo normal y finalizamos cualquier accion
    def mouseReleaseEvent(self, event):
        self.drag_pos = None
        self.resize_dir = ""
        self.setCursor(Qt.ArrowCursor)
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())