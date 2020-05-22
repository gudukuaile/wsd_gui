from PySide2.QtCore import *
from PySide2.QtGui import QColor
from PySide2.QtWidgets import *
from stacked_demo import Ui_Dialog
from my_fun import My_DB

class MyStacked(QDialog,Ui_Dialog):
    Signal_OneParameter = Signal(str,str)

    def __init__(self,items):
        super(MyStacked, self).__init__()
        self.setupUi(self)
        self.treeWidget.setColumnCount(2)
        self.treeWidget.setHeaderLabels(['key', 'value'])
        self.treeWidget.setColumnWidth(0,200)

        # self.pushButton.click().connect()

        # self.treeWidget.itemClicked.connect(self.set_date)
        for k, v in items.items():
            d = v[0].strftime('%Y/%m/%d %H:%M:%S')
            new_d = v[1].strftime('%Y/%m/%d %H:%M:%S')
            item = QTreeWidgetItem(self.treeWidget)
            item.setBackgroundColor(0,QColor(127,255,212))
            item.setText(0, str(k))
            item.setText(1, str(v[2]))
            item2 = QTreeWidgetItem(item)
            item3 = QTreeWidgetItem(item)
            item2.setText(0, d)
            item3.setText(0, new_d)

        self.treeWidget.expandAll()


    @Slot()
    def on_treeWidget_clicked(self):
        self.aa = self.treeWidget.currentItem()
        citem = self.treeWidget.currentItem()
        self.start_date = citem.child(0).text(0)
        self.end_date = citem.child(1).text(0)

        start_date = (QDateTime.fromString(self.start_date, 'yyyy/M/d h:mm:ss'))
        end_date = (QDateTime.fromString(self.end_date, 'yyyy/M/d h:mm:ss'))
        self.dateTimeEdit.setDateTime(start_date)
        self.dateTimeEdit_2.setDateTime(end_date)

    @Slot()
    def on_pushButton_clicked(self):

        index = self.treeWidget.indexOfTopLevelItem(self.aa)
        self.treeWidget.takeTopLevelItem(index)
        # print(self.start_date)
        # print(self.end_date)
        # My_DB.ins_tb(start_date=self.start_date,end_date=self.end_date)
        self.emit_date()

    def emit_date(self):
        print(f"次窗口{self.start_date}，{self.end_date}")
        self.Signal_OneParameter.emit(self.start_date,self.end_date)




