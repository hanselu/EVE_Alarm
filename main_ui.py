# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_ui.ui'
##
## Created by: Qt User Interface Compiler version 5.15.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(400, 240)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.table_Alarm = QTableWidget(self.centralwidget)
        self.table_Alarm.setObjectName(u"table_Alarm")
        self.table_Alarm.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_Alarm.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.horizontalLayout.addWidget(self.table_Alarm)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.txt_BaseSystem = QLineEdit(self.centralwidget)
        self.txt_BaseSystem.setObjectName(u"txt_BaseSystem")
        self.txt_BaseSystem.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.txt_BaseSystem)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.txt_Overtime = QLineEdit(self.centralwidget)
        self.txt_Overtime.setObjectName(u"txt_Overtime")
        self.txt_Overtime.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.txt_Overtime)

        self.btn_Save = QPushButton(self.centralwidget)
        self.btn_Save.setObjectName(u"btn_Save")

        self.verticalLayout.addWidget(self.btn_Save)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.btn_Start = QPushButton(self.centralwidget)
        self.btn_Start.setObjectName(u"btn_Start")
        self.btn_Start.setMinimumSize(QSize(0, 46))

        self.verticalLayout.addWidget(self.btn_Start)

        self.btn_Auto = QPushButton(self.centralwidget)
        self.btn_Auto.setObjectName(u"btn_Auto")
        self.btn_Auto.setMinimumSize(QSize(0, 46))

        self.verticalLayout.addWidget(self.btn_Auto)

        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(6, 1)

        self.horizontalLayout.addLayout(self.verticalLayout)

        self.horizontalLayout.setStretch(0, 4)
        self.horizontalLayout.setStretch(1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 400, 23))
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"EPT\u9884\u8b66\u76d1\u63a7", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u9884\u8b66\u661f\u7cfb", None))
        self.txt_BaseSystem.setText(QCoreApplication.translate("MainWindow", u"3-QYVE", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u9884\u8b66\u65f6\u957f", None))
        self.txt_Overtime.setText(QCoreApplication.translate("MainWindow", u"600", None))
        self.btn_Save.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u914d\u7f6e", None))
        self.btn_Start.setText(QCoreApplication.translate("MainWindow", u"\u624b\u52a8\u5237\u65b0", None))
        self.btn_Auto.setText(QCoreApplication.translate("MainWindow", u"\u81ea\u52a8\u5237\u65b0", None))
    # retranslateUi

