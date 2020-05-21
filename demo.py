import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

import sys

app = QApplication(sys.argv)
tree = QTreeWidget()
tree.setColumnCount(2)
tree.setHeaderLabels(['key','value'])




tree.show()
sys.exit(app.exec_())