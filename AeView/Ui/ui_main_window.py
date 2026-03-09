# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_windowQFVsQp.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QFrame,
    QHBoxLayout, QLabel, QLineEdit, QListView,
    QPlainTextEdit, QProgressBar, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1160, 845)
        Form.setMinimumSize(QSize(600, 600))
        Form.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
        Form.setStyleSheet(u"")
        self.verticalLayout_8 = QVBoxLayout(Form)
        self.verticalLayout_8.setSpacing(15)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(15, 15, 15, 15)
        self.outer_frame = QFrame(Form)
        self.outer_frame.setObjectName(u"outer_frame")
        self.outer_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.outer_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.outer_frame)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.main_container = QFrame(self.outer_frame)
        self.main_container.setObjectName(u"main_container")
        self.main_container.setFrameShape(QFrame.Shape.StyledPanel)
        self.main_container.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.main_container)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 2)
        self.add_buttom = QPushButton(self.main_container)
        self.add_buttom.setObjectName(u"add_buttom")
        self.add_buttom.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout.addWidget(self.add_buttom)

        self.del_buttom = QPushButton(self.main_container)
        self.del_buttom.setObjectName(u"del_buttom")
        self.del_buttom.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout.addWidget(self.del_buttom)

        self.del_all_buttom = QPushButton(self.main_container)
        self.del_all_buttom.setObjectName(u"del_all_buttom")
        self.del_all_buttom.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout.addWidget(self.del_all_buttom)

        self.horizontalSpacer = QSpacerItem(100, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.settings = QPushButton(self.main_container)
        self.settings.setObjectName(u"settings")
        self.settings.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout.addWidget(self.settings)

        self.exit_buttom = QPushButton(self.main_container)
        self.exit_buttom.setObjectName(u"exit_buttom")
        self.exit_buttom.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout.addWidget(self.exit_buttom)


        self.verticalLayout_5.addLayout(self.horizontalLayout)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.file_type = QComboBox(self.main_container)
        self.file_type.addItem("")
        self.file_type.addItem("")
        self.file_type.addItem("")
        self.file_type.addItem("")
        self.file_type.setObjectName(u"file_type")

        self.verticalLayout_3.addWidget(self.file_type)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.listView = QListView(self.main_container)
        self.listView.setObjectName(u"listView")
        self.listView.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.verticalLayout_2.addWidget(self.listView)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.progressBar = QProgressBar(self.main_container)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)

        self.verticalLayout.addWidget(self.progressBar)

        self.plainTextEdit = QPlainTextEdit(self.main_container)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setReadOnly(True)

        self.verticalLayout.addWidget(self.plainTextEdit)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.verticalLayout_2.setStretch(0, 65)
        self.verticalLayout_2.setStretch(1, 35)

        self.verticalLayout_3.addLayout(self.verticalLayout_2)


        self.verticalLayout_4.addLayout(self.verticalLayout_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.main_container)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.int_order = QLineEdit(self.main_container)
        self.int_order.setObjectName(u"int_order")
        self.int_order.setCursor(QCursor(Qt.CursorShape.ArrowCursor))

        self.horizontalLayout_2.addWidget(self.int_order)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.pushButton = QPushButton(self.main_container)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout_2.addWidget(self.pushButton)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)


        self.verticalLayout_5.addLayout(self.verticalLayout_4)


        self.verticalLayout_6.addLayout(self.verticalLayout_5)


        self.verticalLayout_7.addWidget(self.main_container)


        self.verticalLayout_8.addWidget(self.outer_frame)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.add_buttom.setText(QCoreApplication.translate("Form", u"A\u00f1adir", None))
        self.del_buttom.setText(QCoreApplication.translate("Form", u"Eliminar", None))
        self.del_all_buttom.setText(QCoreApplication.translate("Form", u"Eliminar todo", None))
        self.settings.setText(QCoreApplication.translate("Form", u"Ajustes", None))
        self.exit_buttom.setText(QCoreApplication.translate("Form", u"Salir", None))
        self.file_type.setItemText(0, QCoreApplication.translate("Form", u"Archivos de anomal\u00edas combinadas", None))
        self.file_type.setItemText(1, QCoreApplication.translate("Form", u"Informes detallados de anomal\u00edas", None))
        self.file_type.setItemText(2, QCoreApplication.translate("Form", u"Fichero de agrupaci\u00f3n porteman", None))
        self.file_type.setItemText(3, QCoreApplication.translate("Form", u"Fichero de informaci\u00f3n de vanos", None))

        self.progressBar.setFormat("")
        self.label.setText(QCoreApplication.translate("Form", u"Orden de trabajo:", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"Procesar archivos", None))
    # retranslateUi

