from utils.data_manager import DataManager
from scripts.ui_manifester import UIManifester

from PyQt5.QtWidgets import QApplication, QSystemTrayIcon
from PyQt5.QtGui import QIcon
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    manager = DataManager('data/data.txt')

    tray_icon = QSystemTrayIcon(QIcon("showgo.PNG"), app)
    tray_icon.show()
    app.setWindowIcon(QIcon("icon.icns"))

    window = UIManifester(manager, 10)
    window.show()
    sys.exit(app.exec_())
