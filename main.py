from utils.data_manager import DataManager
from scripts.ui_manifester import UIManifester

from PyQt5.QtWidgets import QApplication, QSystemTrayIcon
from PyQt5.QtGui import QIcon
import sys
import os

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    data_file = resource_path('data/data.txt')
    manager = DataManager(data_file)

    tray_icon = QSystemTrayIcon(QIcon("showgo.PNG"), app)
    tray_icon.show()

    icon_file = resource_path('img/icon.icns')
    app.setWindowIcon(QIcon(icon_file))

    window = UIManifester(manager, 10)
    window.show()
    sys.exit(app.exec_())
