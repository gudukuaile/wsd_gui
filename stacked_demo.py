# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'stacked_demo.ui'
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


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(600, 450)
        self.horizontalLayout = QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.stackedWidget = QStackedWidget(Dialog)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.horizontalLayout_2 = QHBoxLayout(self.page)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.treeWidget = QTreeWidget(self.page)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        self.treeWidget.setObjectName(u"treeWidget")

        self.horizontalLayout_3.addWidget(self.treeWidget)

        self.widget = QWidget(self.page)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.label)

        self.dateTimeEdit = QDateTimeEdit(self.widget)
        self.dateTimeEdit.setObjectName(u"dateTimeEdit")

        self.horizontalLayout_4.addWidget(self.dateTimeEdit)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_5.addWidget(self.label_2)

        self.dateTimeEdit_2 = QDateTimeEdit(self.widget)
        self.dateTimeEdit_2.setObjectName(u"dateTimeEdit_2")
        self.dateTimeEdit_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.dateTimeEdit_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.pushButton = QPushButton(self.widget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setAutoRepeat(False)
        self.pushButton.setAutoExclusive(False)
        self.pushButton.setFlat(False)

        self.verticalLayout_2.addWidget(self.pushButton)


        self.horizontalLayout_3.addWidget(self.widget)

        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 1)

        self.horizontalLayout_2.addLayout(self.horizontalLayout_3)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.verticalLayout = QVBoxLayout(self.page_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.stackedWidget.addWidget(self.page_2)

        self.horizontalLayout.addWidget(self.stackedWidget)


        self.retranslateUi(Dialog)

        self.stackedWidget.setCurrentIndex(0)
        self.pushButton.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"\u5f00\u59cb\u65f6\u95f4", None))
        self.dateTimeEdit.setDisplayFormat(QCoreApplication.translate("Dialog", u"yyyy/M/d H:mm:ss", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"\u7ed3\u675f\u65f6\u95f4", None))
        self.dateTimeEdit_2.setDisplayFormat(QCoreApplication.translate("Dialog", u"yyyy/M/d H:mm:ss", None))
        self.pushButton.setText(QCoreApplication.translate("Dialog", u"\u63d2\u5165", None))
    # retranslateUi

