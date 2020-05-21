# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""
import random

from PySide2.QtCore import QTimer, Slot
from PySide2.QtGui import QBrush,QColor

from PySide2.QtWidgets import QMainWindow,QApplication,QFileDialog,QMessageBox,QTableWidgetItem,QHeaderView,\
    QPushButton,QAbstractButton,QAbstractItemView

from Ui_mainw import Ui_MainWindow

from datetime import date


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """
        # self.conn = ''   #
        # print(id(self.conn))
        # sel_tb = '' #选中的表
        # one_high = ''   #温度上限
        # one_low = ''    #温度下限
        YEAR = str(date.today().year)
        MONTH = str(date.today().month)
        self.is_double_clicked = False
        self.sel_name = 'HE410N8115'  # 默认选择阴凉库1
        bgbruse = ''  # 保存单元格的默认笔刷
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.year.setText(YEAR)
        self.month.setText(MONTH)
        QMessageBox.information(self,
                                "消息框标题",
                                "请将系统的短日期格式设置为yyyy/M/d \n"
                                "长时间格式设置为h:mm:ss",
                                )



    # @Slot()是一个装饰器，标志着这个函数是一个slot(槽)
    @Slot()
    def output(self):
        print("Button clicked")


def main():
    import sys
    app = QApplication(sys.argv)
    m = MainWindow()
    m.show()
    sys.exit(app.exec_())



if __name__ == '__main__':
    main()
