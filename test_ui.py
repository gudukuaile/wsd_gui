from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication,QMessageBox,QFileDialog
from my_fun import My_DB
from PySide2.QtCore import QTimer, Slot
from PySide2 import QtCore

class Stats:
    def __init__(self):

        
        # 从文件中加载UI定义

        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load('mainw.ui')
        print(self.ui)
        QMessageBox.information(self.ui,
                                "消息框标题",
                                "请将系统的短日期格式设置为yyyy/M/d \n"
                                "长时间格式设置为h:mm:ss",
                                )
        # self.ui.conn.clicked.connect(self.on_conn_clicked)
        QtCore.QMetaObject.connectSlotsByName(self.ui.conn)

    # 连接数据库
    @Slot()
    def on_conn_clicked(self):
        fileName1, filetype = QFileDialog.getOpenFileName(self.ui,
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


app = QApplication()
stats = Stats()
stats.ui.show()
app.exec_()
