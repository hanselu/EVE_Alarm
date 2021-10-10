from copy import deepcopy
from threading import Thread

from PySide2.QtCore import QTimer, Qt
from PySide2.QtGui import QIcon, QColor
from PySide2.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QHeaderView
from ui_mainwindow import Ui_MainWindow

import common
import eve
import config


setting = config.get_config()


def autoTable(table: QTableWidget):
    # 自动缩放单元格
    # table.resizeColumnsToContents()
    # table.resizeRowsToContents()
    # 表格宽度随父窗口的缩放自动缩放
    table.horizontalHeader().setStretchLastSection(True)

    table.horizontalHeader().sectionResizeMode(QHeaderView.Stretch)


def set_table_item(item_txt: str, distance: int) -> QTableWidgetItem:
    item = QTableWidgetItem(item_txt)
    item.setTextAlignment(Qt.AlignCenter)
    # print(setting)
    waring_lever1 = setting['warning_level']['level_a']
    waring_lever2 = setting['warning_level']['level_b']
    waring_lever3 = setting['warning_level']['level_c']
    # print(waring_lever1)
    # print(waring_lever2)
    # print(waring_lever3)
    if distance < waring_lever1['distance']:
        item.setBackground(QColor(
            waring_lever1['color'][0], waring_lever1['color'][1], waring_lever1['color'][2]))
    elif distance < waring_lever2['distance']:
        item.setBackground(QColor(
            waring_lever2['color'][0], waring_lever2['color'][1], waring_lever2['color'][2]))
    elif distance < waring_lever3['distance']:
        item.setBackground(QColor(
            waring_lever3['color'][0], waring_lever3['color'][1], waring_lever3['color'][2]))

    return item


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QIcon('pibc.png'))
        # self.setWindowTitle(f'馒狗预警 {CurrentLocation}')

        # 初始化timer及相关变量
        self.timer = QTimer(self)
        self.timer_flag = False
        self.timer.timeout.connect(self.btn_Manual_Clicked)

        # 变量初始化
        self.local = '未知'
        self.last_local = '未知'
        self.alarm_list = []
        self.last_alarm_list = []

        # UI初始化并显示数据
        self.init_ui()

        # 信号和槽初始化
        self.btn_Auto.clicked.connect(self.btn_Auto_Clicked)
        self.btn_Manual.clicked.connect(self.btn_Manual_Clicked)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.show()

    def init_ui(self):
        self.init_table()
        self.update_alarms()

    def update_dat(self):
        # print('刷新数据')
        self.last_local = self.local
        self.local = eve.get_local()
        # print(f'当前在 {self.local}')
        self.last_alarm_list = deepcopy(self.alarm_list)
        self.alarm_list = eve.get_alarm_list(self.local)

    def init_table(self):
        header_labels = ['时间', '地点', '距离', '入口']
        self.table_Waring.setColumnCount(len(header_labels))
        self.table_Waring.setHorizontalHeaderLabels(header_labels)
        self.table_Waring.verticalHeader().setHidden(True)

    def show_alarm(self):

        if self.alarm_list:
            # 调试，输出预警列表
            # print('----调试信息----')
            # for a in self.alarm_list:
            #     d = len(esi.cal_route(current_location, a.solar_system))
            #     print(a, f'{d}跳')
            # print('----调试信息----')

            min_jump = setting['ignore_distance']
            min_index = 0
            self.table_Waring.clearContents()
            self.table_Waring.setRowCount(len(self.alarm_list))
            for i, alarm in enumerate(self.alarm_list):
                # 找出最近的预警
                distance = alarm.distance()
                if distance < min_jump and alarm.dt < setting['special_overtime']:
                    min_jump = distance
                    min_index = i

                # 时间
                # item = QTableWidgetItem(format_dt(time.time() - alarm.ts))
                # item.setTextAlignment(Qt.AlignCenter)
                self.table_Waring.setItem(i, 0, set_table_item(
                    common.ts_to_str_format(alarm.ts), distance))

                # 地点
                # item = QTableWidgetItem(alarm.location)
                # item.setTextAlignment(Qt.AlignCenter)
                self.table_Waring.setItem(
                    i, 1, set_table_item(alarm.solar_system, distance))

                # 距离
                # item = QTableWidgetItem(f'{jump_count}跳')
                # item.setTextAlignment(Qt.AlignCenter)
                self.table_Waring.setItem(
                    i, 2, set_table_item(f'{distance}跳', distance))

                # 入口
                self.table_Waring.setItem(
                    i, 3, set_table_item(f'{alarm.enter()}', distance))

            autoTable(self.table_Waring)
            # self.resize(self.width(), 800)

            # 显示最近的预警
            nearest_alarm = self.alarm_list[min_index]

            self.txt_CurrentTime.setText(
                common.ts_to_str_format(nearest_alarm.ts))
            self.txt_Location.setText(nearest_alarm.solar_system)
            self.txt_CurrentJump.setText(f'{nearest_alarm.distance()}跳')

        else:
            self.txt_CurrentTime.setText('')
            self.txt_CurrentJump.setText('')
            self.txt_Location.setText('安详的特纳')

        # 显示本地位置
        if self.last_local != self.local:
            print(f'{self.last_local} → {self.local}')
            self.statusBar.showMessage(f'当前位置：{self.local}')
        else:
            print(f'位置未变 {self.local}')

    # 槽函数

    def actionTopmost_Triggered(self):
        """
        窗口置顶槽函数
        :return:
        """
        if self.actionTopmost.isChecked():
            print('置顶')
            self.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.show()
        else:
            print('取消置顶')
            self.setWindowFlags(Qt.Window)
            self.show()

    def btn_Manual_Clicked(self):
        # print(f'{int(common.get_ts())} 按下按钮')
        thread = Thread(target=self.update_alarms)
        thread.start()
        # self.update_alarms()

    def btn_Auto_Clicked(self):
        pass
        if self.timer_flag:
            self.timer_flag = False
            self.timer.stop()
            self.btn_Auto.setText('开始刷新')
            self.btn_Manual.setEnabled(True)
        else:
            self.timer_flag = True
            self.update_alarms()
            self.timer.start(5000)
            self.btn_Auto.setText('停止刷新')
            self.btn_Manual.setEnabled(False)

    def update_alarms(self):
        self.update_dat()
        self.show_alarm()
