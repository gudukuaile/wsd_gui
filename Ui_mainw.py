# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Ui_mainw.ui'
##
## Created by: Qt User Interface Compiler version 5.14.2
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
        MainWindow.resize(800, 600)
        self.centralWidget = QWidget(MainWindow)
        self.centralWidget.setObjectName(u"centralWidget")
        self.horizontalLayout = QHBoxLayout(self.centralWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.groupBox = QGroupBox(self.centralWidget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.conn = QPushButton(self.groupBox)
        self.conn.setObjectName(u"conn")

        self.verticalLayout.addWidget(self.conn)

        self.del_all = QPushButton(self.groupBox)
        self.del_all.setObjectName(u"del_all")
        self.del_all.setEnabled(False)

        self.verticalLayout.addWidget(self.del_all)

        self.up_all = QPushButton(self.groupBox)
        self.up_all.setObjectName(u"up_all")
        self.up_all.setEnabled(False)

        self.verticalLayout.addWidget(self.up_all)

        self.groupBox_2 = QGroupBox(self.groupBox)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setEnabled(False)
        self.groupBox_2.setMaximumSize(QSize(200, 200))
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.show_bt = QPushButton(self.groupBox_2)
        self.show_bt.setObjectName(u"show_bt")

        self.verticalLayout_2.addWidget(self.show_bt)

        self.view_tb = QPushButton(self.groupBox_2)
        self.view_tb.setObjectName(u"view_tb")

        self.verticalLayout_2.addWidget(self.view_tb)

        self.up_tb = QPushButton(self.groupBox_2)
        self.up_tb.setObjectName(u"up_tb")

        self.verticalLayout_2.addWidget(self.up_tb)

        self.ins_tb = QPushButton(self.groupBox_2)
        self.ins_tb.setObjectName(u"ins_tb")

        self.verticalLayout_2.addWidget(self.ins_tb)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.tui = QPushButton(self.groupBox)
        self.tui.setObjectName(u"tui")

        self.verticalLayout.addWidget(self.tui)


        self.horizontalLayout.addWidget(self.groupBox)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label = QLabel(self.centralWidget)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(100, 50))
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setMargin(0)

        self.verticalLayout_3.addWidget(self.label)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.centralWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(100, 16777215))
        self.label_2.setTextFormat(Qt.AutoText)
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_2.setWordWrap(False)

        self.horizontalLayout_2.addWidget(self.label_2)

        self.start_dt = QDateTimeEdit(self.centralWidget)
        self.start_dt.setObjectName(u"start_dt")

        self.horizontalLayout_2.addWidget(self.start_dt)

        self.label_1 = QLabel(self.centralWidget)
        self.label_1.setObjectName(u"label_1")
        self.label_1.setMaximumSize(QSize(100, 16777215))
        self.label_1.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label_1)

        self.end_dt = QDateTimeEdit(self.centralWidget)
        self.end_dt.setObjectName(u"end_dt")

        self.horizontalLayout_2.addWidget(self.end_dt)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.table = QTableWidget(self.centralWidget)
        self.table.setObjectName(u"table")

        self.verticalLayout_3.addWidget(self.table)


        self.horizontalLayout.addLayout(self.verticalLayout_3)

        MainWindow.setCentralWidget(self.centralWidget)
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName(u"statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        # self.tui.clicked.connect(MainWindow.close)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u6e29\u6e7f\u5ea6", None))
        self.conn.setText(QCoreApplication.translate("MainWindow", u"\u8fde\u63a5\u6570\u636e\u5e93", None))
        self.del_all.setText(QCoreApplication.translate("MainWindow", u"\u5220\u9664\u6240\u6709", None))
        self.up_all.setText(QCoreApplication.translate("MainWindow", u"\u4fee\u6539\u6240\u6709", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\u8be6\u7ec6\u529f\u80fd", None))
        self.show_bt.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793a\u6240\u6709\u5e93", None))
        self.view_tb.setText(QCoreApplication.translate("MainWindow", u"\u6d4f\u89c8\u6570\u636e", None))
        self.up_tb.setText(QCoreApplication.translate("MainWindow", u"\u4fee\u6539", None))
        self.ins_tb.setText(QCoreApplication.translate("MainWindow", u"\u63d2\u5165\u6570\u636e", None))
        self.tui.setText(QCoreApplication.translate("MainWindow", u"\u9000\u51fa", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u5e93\u8868", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u65f6\u95f4:", None))
        self.start_dt.setDisplayFormat(QCoreApplication.translate("MainWindow", u"yyyy/M/d h:mm", None))
        self.label_1.setText(QCoreApplication.translate("MainWindow", u"\u7ed3\u675f\u65f6\u95f4:", None))
        self.end_dt.setDisplayFormat(QCoreApplication.translate("MainWindow", u"yyyy/M/d h:mm", None))
    # retranslateUi

