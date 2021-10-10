# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindowpSGXXr.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(343, 293)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.txt_CurrentTime = QLabel(self.centralwidget)
        self.txt_CurrentTime.setObjectName(u"txt_CurrentTime")
        font = QFont()
        font.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        font.setPointSize(28)
        font.setBold(True)
        font.setWeight(75)
        self.txt_CurrentTime.setFont(font)
        self.txt_CurrentTime.setStyleSheet(u"color: rgb(255, 170, 127);")
        self.txt_CurrentTime.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.txt_CurrentTime)

        self.txt_Location = QLabel(self.centralwidget)
        self.txt_Location.setObjectName(u"txt_Location")
        self.txt_Location.setFont(font)
        self.txt_Location.setStyleSheet(u"color: rgb(255, 85, 127);")
        self.txt_Location.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.txt_Location)

        self.txt_CurrentJump = QLabel(self.centralwidget)
        self.txt_CurrentJump.setObjectName(u"txt_CurrentJump")
        self.txt_CurrentJump.setFont(font)
        self.txt_CurrentJump.setAutoFillBackground(False)
        self.txt_CurrentJump.setStyleSheet(u"color: rgb(0, 170, 255);")
        self.txt_CurrentJump.setFrameShape(QFrame.NoFrame)
        self.txt_CurrentJump.setFrameShadow(QFrame.Plain)
        self.txt_CurrentJump.setScaledContents(False)
        self.txt_CurrentJump.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.txt_CurrentJump)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 1)
        self.horizontalLayout_2.setStretch(2, 1)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.table_Waring = QTableWidget(self.centralwidget)
        self.table_Waring.setObjectName(u"table_Waring")
        self.table_Waring.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.verticalLayout.addWidget(self.table_Waring)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.btn_Auto = QPushButton(self.centralwidget)
        self.btn_Auto.setObjectName(u"btn_Auto")
        font1 = QFont()
        font1.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        font1.setPointSize(14)
        font1.setBold(True)
        font1.setWeight(75)
        self.btn_Auto.setFont(font1)

        self.horizontalLayout.addWidget(self.btn_Auto)

        self.btn_Manual = QPushButton(self.centralwidget)
        self.btn_Manual.setObjectName(u"btn_Manual")
        self.btn_Manual.setFont(font1)

        self.horizontalLayout.addWidget(self.btn_Manual)

        self.btn_Setting = QPushButton(self.centralwidget)
        self.btn_Setting.setObjectName(u"btn_Setting")
        self.btn_Setting.setFont(font1)

        self.horizontalLayout.addWidget(self.btn_Setting)


        self.verticalLayout.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName(u"statusBar")
        self.statusBar.setSizeGripEnabled(False)
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u9992\u72d7\u9884\u8b66", None))
        self.txt_CurrentTime.setText(QCoreApplication.translate("MainWindow", u"4\u5206\u949f", None))
        self.txt_Location.setText(QCoreApplication.translate("MainWindow", u"ZK-YQ3", None))
        self.txt_CurrentJump.setText(QCoreApplication.translate("MainWindow", u"5 \u8df3", None))
        self.btn_Auto.setText(QCoreApplication.translate("MainWindow", u"\u81ea\u52a8\u5237\u65b0", None))
        self.btn_Manual.setText(QCoreApplication.translate("MainWindow", u"\u624b\u52a8\u5237\u65b0", None))
        self.btn_Setting.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e", None))
    # retranslateUi

