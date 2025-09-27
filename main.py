from utils.data_manager import DataManager
from scripts.ui_manifester import UIManifester

from PyQt5.QtWidgets import QApplication
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    manager = DataManager('data/data.txt')
    window = UIManifester(manager, 10)
    window.show()
    sys.exit(app.exec_())
