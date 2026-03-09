# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settingsUrlRdz.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(774, 247)
        Form.setStyleSheet(u"")
        self.verticalLayout_3 = QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.outer_frame = QFrame(Form)
        self.outer_frame.setObjectName(u"outer_frame")
        self.outer_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.outer_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.outer_frame)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.main_frame = QFrame(self.outer_frame)
        self.main_frame.setObjectName(u"main_frame")
        self.main_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.main_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.main_frame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.back_button = QPushButton(self.main_frame)
        self.back_button.setObjectName(u"back_button")

        self.horizontalLayout.addWidget(self.back_button)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.boton_guardar = QPushButton(self.main_frame)
        self.boton_guardar.setObjectName(u"boton_guardar")

        self.horizontalLayout.addWidget(self.boton_guardar)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.cambiar_color_neon = QPushButton(self.main_frame)
        self.cambiar_color_neon.setObjectName(u"cambiar_color_neon")

        self.verticalLayout_2.addWidget(self.cambiar_color_neon)

        self.activar_neon = QCheckBox(self.main_frame)
        self.activar_neon.setObjectName(u"activar_neon")

        self.verticalLayout_2.addWidget(self.activar_neon)


        self.verticalLayout_4.addLayout(self.verticalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.main_frame)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.tipo_color = QComboBox(self.main_frame)
        self.tipo_color.addItem("")
        self.tipo_color.addItem("")
        self.tipo_color.addItem("")
        self.tipo_color.setObjectName(u"tipo_color")

        self.verticalLayout.addWidget(self.tipo_color)


        self.verticalLayout_4.addLayout(self.verticalLayout)


        self.horizontalLayout_2.addLayout(self.verticalLayout_4)


        self.verticalLayout_5.addWidget(self.main_frame)


        self.verticalLayout_3.addWidget(self.outer_frame)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.back_button.setText(QCoreApplication.translate("Form", u"Atras", None))
        self.boton_guardar.setText(QCoreApplication.translate("Form", u"Guardar", None))
        self.cambiar_color_neon.setText(QCoreApplication.translate("Form", u"cambiar color neon", None))
        self.activar_neon.setText(QCoreApplication.translate("Form", u"Activar neon", None))
        self.label.setText(QCoreApplication.translate("Form", u"Tema:", None))
        self.tipo_color.setItemText(0, QCoreApplication.translate("Form", u"defecto", None))
        self.tipo_color.setItemText(1, QCoreApplication.translate("Form", u"retro", None))
        self.tipo_color.setItemText(2, QCoreApplication.translate("Form", u"moderno", None))

    # retranslateUi

