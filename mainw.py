# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
使用pyside2重构之前的pyqt5
pyinstaller -Fw wmian.py打包exe程序
"""
import random
import sys

from PySide2.QtCore import QTimer,Slot,QDateTime,QDate
from PySide2.QtGui import QBrush,QColor
from PySide2.QtWidgets import QMainWindow,QApplication,QFileDialog,QMessageBox,QTableWidgetItem,QHeaderView,\
    QPushButton,QAbstractButton,QAbstractItemView,QDialog
from Ui_mainw import Ui_MainWindow
from stacked_demo import Ui_Dialog
from my_fun import My_DB
from datetime import datetime



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
        self.is_double_clicked = False
        self.sel_name = 'HE410N8115'  # 默认选择阴凉库1
        bgbruse = ''  # 保存单元格的默认笔刷
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.set_date()
        QMessageBox.information(self,
                                "消息框标题",
                                "请将系统的短日期格式设置为yyyy/M/d \n"
                                "长时间格式设置为h:mm:ss",
                                )
    # 设置datetimeedit的起始时间
    def set_date(self):
        self.datef = 'yyyy/M/d h:mm:ss'
        self.start_dt.setDisplayFormat(self.datef)
        self.end_dt.setDisplayFormat(self.datef)

        # 获取当前的时间，表转换成datetime类型
        self.currentdt = QDateTime.currentDateTime().toPython()
        year = self.currentdt.year
        month = self.currentdt.month
        day = 1
        hour = 0
        minute = 0
        seccond = 0

        self.start_dt.setDateTime(QDateTime(year, month, day, hour, minute, seccond))
        self.end_dt.setDateTime(QDateTime.currentDateTime())
        # 选择日历
        self.start_dt.setCalendarPopup(True)
        self.end_dt.setCalendarPopup(True)

    # 连接数据库
    @Slot()
    def on_conn_clicked(self):
        fileName1, filetype = QFileDialog.getOpenFileName(self,
                                                          "选取文件",
                                                          "./",
                                                          "DB Files (*.mdb);;All Files (*)"
                                                          )
        # 连接数据库
        # self.__class__.conn = My_DB(fileName1)
        self.conn = My_DB(fileName1)
        # print(fileName1)
        self.set_table()
        self.show_table()
        self.del_all.setDisabled(False)
        self.up_all.setDisabled(False)
        self.groupBox_2.setDisabled(False)

    # 删除所有超标数据
    @Slot()
    def on_del_all_clicked(self):
        self.table.clear()
        # 设置表格列数
        self.table.setColumnCount(3)
        # 设置表格行数
        self.table.setRowCount(10)
        # 隐藏水平表头
        # self.tableWidget.horizontalHeader().setVisible(False)
        self.table.setHorizontalHeaderLabels(['时间', '温度', '湿度'])
        # start_date,end_date = self.get_date()
        # m = self.get_msg(mess='删除')
        # if m == 'yes':
        #     value = self.conn.del_table(start_date,end_date)
        # elif m == 'yesall':
        #     value = self.conn.del_table()
        value = self.conn.del_table()

        if value:
            QMessageBox.information(self,
                                    "消息框标题",
                                    "全部删除成功！",
                                    )
        #self.del_all.setDisabled(True)

    # 修改所有超标数据
    @Slot()
    def on_up_all_clicked(self):
        self.table.clear()
        # 设置表格列数
        self.table.setColumnCount(3)
        # 设置表格行数
        self.table.setRowCount(10)
        # 隐藏水平表头
        # self.tableWidget.horizontalHeader().setVisible(False)
        self.table.setHorizontalHeaderLabels(['时间', '温度', '湿度'])
        start_date,end_date = self.get_date()

        self.conn.up_table(start_date,end_date)
        self.show_msg('修改',start_date,end_date)

        self.up_all.setDisabled(True)

    # 显示所有库
    @Slot()
    def on_show_bt_clicked(self):
        self.set_table()
        self.show_table()

    # 显示超标数据
    @Slot()
    def on_view_tb_clicked(self):
        self.table.clear()
        # 设置表格列数
        self.table.setColumnCount(3)
        # 设置表格行数
        self.table.setRowCount(10)
        # 隐藏水平表头
        # self.tableWidget.horizontalHeader().setVisible(False)
        self.table.setHorizontalHeaderLabels(['时间', '温度', '湿度'])
        start_date,end_date = self.get_date()
        try:
            query = self.conn.show_data(self.sel_name,start_date,end_date)

            j = 0
            d = 0
            while query.next():
                # 当数据大于默认的行数时，在最后一行加入一个空行
                if j >= self.table.rowCount():
                    self.table.insertRow(j)
                for i in range(3):
                    if i == 0:
                        newitem = QTableWidgetItem(str(query.value(0).toString('yyyy/M/d h:mm:ss')))
                        self.table.setItem(j, i, newitem)
                    elif i == 1:
                        newitem = QTableWidgetItem(str(query.value(1)))
                        if query.value(1) >= self.one_high or query.value(1) <= self.one_low:
                            self.bgbruse = newitem.background()
                            newitem.setBackground(QColor(125, 32, 67))
                            self.table.setItem(j, i, newitem)  # 把数字转换成字符串
                        else:
                            self.table.setItem(j, i, newitem)
                    elif i == 2:
                        newitem = QTableWidgetItem(str(query.value(2)))
                        if query.value(2) >= self.two_high or query.value(2) <= self.two_low:
                            self.bgbruse = newitem.background()
                            newitem.setBackground(QColor(125, 32, 67))
                            self.table.setItem(j, i, newitem)  # 把数字转换成字符串
                        else:
                            self.table.setItem(j, i, newitem)

                j += 1
            self.set_color(self.table.rowCount())
        except BaseException as m:
            # print(m)
            # print(type(m))
            QMessageBox.information(self,
                                    "消息框标题",
                                    "请先选择一个需要查询的表",
                                    )

    # 详细修改
    @Slot()
    def on_up_tb_clicked(self):
        # 按年份，月份修改
        tb = 'LOGS_' + self.sel_name
        start_date,end_date = self.get_date()
        query = self.conn.show_data(self.sel_name, start_date, end_date)
        while query.next():
            # 获取当前的实际温度
            one = query.value(1)
            two = query.value(2)
            # print(one,two)
            if (one > self.one_high or one < self.one_low) and (two < self.two_high or two > self.two_low):
                # print('修改温度')
                if abs(self.one_low - one) < abs(self.one_high - one):
                    high = random.uniform(self.one_low - 1, self.one_low + 1)
                else:
                    high = random.uniform(self.one_high - 1, self.one_high + 1)
                self.conn.up_data(tb, high, query.value(0).toString('yyyy/M/d h:mm:ss'), 'one')
            elif (one < self.one_high or one > self.one_low) and (two > self.two_high or two < self.two_low):
                # print('修改湿度')
                if abs(self.two_low - two) < abs(self.two_high - two):
                    high = random.uniform(self.two_low - 1, self.two_low + 1)
                else:
                    high = random.uniform(self.two_high - 1, self.two_high + 1)
                self.conn.up_data(tb, high, query.value(0).toString('yyyy/M/d h:mm:ss'), 'two')
        QMessageBox.information(self,
                                "消息框标题",
                                "修改完毕！",
                                )

    # 插入数据
    @Slot()
    def on_ins_tb_clicked(self):

        d = QDialog()
        aa = Ui_Dialog()
        aa.setupUi(d)
        d.exec_()

        # start_date,end_date = self.get_date()
        # q_list = self.conn.ins_tb(start_date, end_date)


    # 退出
    @Slot()
    def on_tui_clicked(self):
        if not isinstance(self.conn, QPushButton):
            self.conn.db.close()
            self.close()
        else:
            self.close()


    # 设置表格
    def set_table(self):
        # 设置表格列数
        self.table.setColumnCount(6)
        # 设置表格行数
        self.table.setRowCount(10)
        # 隐藏水平表头
        # self.table.horizontalHeader().setVisible(False)
        self.table.setHorizontalHeaderLabels(['id', '名称', '温度上限', '温度下限', '湿度上限', '湿度下限'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)

    # 显示库
    def show_table(self):
        query = self.conn.select_table()
        j = 0
        while query.next():
            # 当数据大于默认的行数时，在最后一行加入一个空行
            if j >= self.table.rowCount():
                self.table.insertRow(j)
            for i in range(6):
                self.table.setItem(j, i, QTableWidgetItem(str(query.value(i))))  # 把数字转换成字符串
                # self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
            j += 1
        # self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def item_clicked_timeout(self):
        if not self.is_double_clicked:
            # print('单击')
            self.sel_name = self.table.item(self.table.currentRow(), 0).text()
            # print(self.sel_name)
            if self.sel_name in self.conn.tb_name.keys():
                self.label.setText(self.sel_name)
                # 获取温度上限
                self.one_high = float(self.conn.tb_name[self.sel_name][1])
                # 获取温度下限
                self.one_low = float(self.conn.tb_name[self.sel_name][2])
                self.two_high = float(self.conn.tb_name[self.sel_name][3])
                self.two_low = float(self.conn.tb_name[self.sel_name][4])
            else:
                self.sel_name = 'HE410N8115'
                QMessageBox.information(self,
                                        "消息框标题",
                                        "操作有误，请重新选择需要修改数据的表！",
                                        )
        else:
            self.is_double_clicked = False

    # 单击单元格
    @Slot(QTableWidgetItem)
    def on_table_itemClicked(self, item):
        if not self.is_double_clicked:
            # 一定时间后执行执行，item_clicked_timeout函数
            QTimer.singleShot(300, self.item_clicked_timeout)
        else:
            self.is_double_clicked = False

    # 双击单元格
    @Slot(QTableWidgetItem)
    def on_table_itemDoubleClicked(self, item):
        self.is_double_clicked = True
        # print('双击')
        # 判断双击的是温度还是湿度
        if self.table.currentColumn() == 1:
            # 获取当前的实际温度
            one = float(self.table.currentItem().text())
            # 需要修改成的温度
            if abs(self.one_low - one) < abs(self.one_high - one):
                high = random.uniform(self.one_low, self.one_low + 1)
            else:
                high = random.uniform(self.one_high - 1, self.one_high)
            # 设置单元格内容
            self.table.currentItem().setText(str(high))
            # 获取选中单元格的行号
            ROW = self.table.currentRow()
            # 获取此行的第0列内容
            logs_time = self.table.item(ROW, 0).text()
            tb = 'LOGS_' + self.sel_name
            self.conn.up_data(tb, high, logs_time, 'one')
            # 设置单元格内容及颜色
            newitem = QTableWidgetItem(str(high))
            newitem.setBackground(self.bgbruse)
            self.table.setItem(ROW, 1, newitem)  # 把数字转换成字符串
        elif self.table.currentColumn() == 2:
            # 获取当前的实际湿度
            two = float(self.table.currentItem().text())
            # 需要修改成的湿度
            if abs(self.two_low - two) < abs(self.two_high - two):
                high = random.uniform(self.two_low, self.two_low + 1)
            else:
                high = random.uniform(self.two_high - 1, self.two_high)
            # 设置单元格内容
            self.table.currentItem().setText(str(high))
            # 获取选中单元格的行号
            ROW = self.table.currentRow()
            # 根据行号获取时间
            logs_time = self.table.item(ROW, 0).text()
            tb = 'LOGS_' + self.sel_name
            self.conn.up_data(tb, high, logs_time, 'two')
            # 设置单元格内容及颜色
            newitem = QTableWidgetItem(str(high))
            newitem.setBackground(self.bgbruse)
            self.table.setItem(ROW, 2, newitem)  # 把数字转换成字符串

    # 获取日期
    def get_date(self):
        start_date = self.start_dt.text()
        end_date = self.end_dt.text()
        return start_date,end_date

    # 选择了哪一个按钮
    def get_msg(self, mess='修改'):
        # QMessageBox.information(self,'消息提示框','点击yes只删除设置月份，点击yesall删除所有')
        msg = QMessageBox()  # 创建一个对话框
        msg.setWindowTitle('消息提示框')  # 设置标题
        msg.setText(f'{mess}当月信息，如需{mess}所有请点击{mess}所有')  # 设置提示信息
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.YesAll)  # 添加两个标准按钮
        msg.button(QMessageBox.Yes).setText('{}'.format(mess))  # 设置按钮的文本
        msg.button(QMessageBox.YesAll).setText(f'{mess}所有')
        m = msg.exec()  # 显示提示框
        if m == QMessageBox.Yes:
            return 'yes'
        elif m == QMessageBox.YesAll:
            return 'yesall'

    # 弹窗信息
    def show_msg(self,mess,start_date,end_date):
        QMessageBox.information(self,
                                "消息框标题",
                                f"{start_date}到{end_date}之间的数据{mess}完毕！",
                                )

    # 设置缺失时间的颜色,count总共的行数
    def set_color(self,counts):

        for count in range(counts):
            print(self.table.item(count,0).text())
            if count == 0:
                d = self.table.item(0,0).text()
                d = datetime.strptime(d,'%Y/%m/%d %H:%M:%S')
            else:
                # 两个时间差
                new_d = self.table.item(count,0).text()
                new_d = datetime.strptime(new_d, '%Y/%m/%d %H:%M:%S')
                s = (new_d-d).seconds
                d = new_d
                # 时间差大于30分钟
                if s > 1800:
                    self.table.item(count-1,0).setBackground(QColor(255,0,0))
                    self.table.item(count,0).setBackground(QColor(0,255,0))


def main():
    app = QApplication(sys.argv)
    m = MainWindow()
    m.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
