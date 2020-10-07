from PySide2.QtCore import Qt
from PySide2.QtGui import QBrush, QColor

import test
from main_ui import Ui_MainWindow
from PySide2.QtWidgets import QMainWindow, QTableWidgetItem


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.alarmList = []
        self.uiInit()
        self.dataInit()
        self.btn_Start.clicked.connect(self.btnStartOnClick)
        self.btn_Save.clicked.connect(self.btnSaveOnClick)

    def uiInit(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        # self.show()
        headerLabels = ['时间', '星系', '距离', '预警人']
        self.table_Alarm.setColumnCount(len(headerLabels))
        self.table_Alarm.setHorizontalHeaderLabels(headerLabels)

        # 读取配置
        test.readSetting()
        self.txt_BaseSystem.setText(test.baseSystemName)
        self.txt_Overtime.setText(str(test.overtime))

    def dataInit(self):
        test.alarm_Init()
        self.updateAlarmList()
        # print(self.alarmList)
        self.showAlarmList()

    def updateAlarmList(self):
        self.alarmList = test.getAlarmList()

    def showAlarmList(self):
        self.table_Alarm.clear()
        self.table_Alarm.setRowCount(self.alarmList.__len__())
        self.table_Alarm.setHorizontalHeaderLabels(['时间', '星系', '距离', '预警人'])

        alarmDistance = 10
        alarmColor = QColor(255, 0, 0)
        for i, alarm in enumerate(self.alarmList):
            ts = alarm['time']
            name = alarm['name']
            distance = alarm['distance']
            charName = alarm['char']

            item = QTableWidgetItem(ts)
            item.setTextAlignment(Qt.AlignCenter)
            self.table_Alarm.setItem(i, 0, item)
            if distance <= alarmDistance:
                item.setForeground(QBrush(alarmColor))

            item = QTableWidgetItem(name)
            item.setTextAlignment(Qt.AlignCenter)
            self.table_Alarm.setItem(i, 1, item)
            if distance <= alarmDistance:
                item.setForeground(QBrush(alarmColor))

            item = QTableWidgetItem(str(distance))
            item.setTextAlignment(Qt.AlignCenter)
            self.table_Alarm.setItem(i, 2, item)
            if distance <= alarmDistance:
                item.setForeground(QBrush(alarmColor))

            item = QTableWidgetItem(charName)
            item.setTextAlignment(Qt.AlignCenter)
            self.table_Alarm.setItem(i, 3, item)
            if distance <= alarmDistance:
                item.setForeground(QBrush(alarmColor))

        self.table_Alarm.resizeColumnsToContents()
        self.table_Alarm.resizeRowsToContents()
        self.table_Alarm.horizontalHeader().setStretchLastSection(True)

    def btnStartOnClick(self):
        self.updateAlarmList()
        self.showAlarmList()

    def btnSaveOnClick(self):
        baseSystemName = self.txt_BaseSystem.text()
        overtime = int(self.txt_Overtime.text())
        # print(baseSystemName)
        # print(overtime)
        test.saveSetting(baseSystemName, overtime)

        # 保存配置后立刻更新数据
        self.updateAlarmList()
        self.showAlarmList()
