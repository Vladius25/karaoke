import sys
from PyQt5.QtWidgets import QApplication

from src.gui import KaraokeWindow

if __name__ == '__main__':
    app = QApplication([])
    snake = KaraokeWindow()
    sys.exit(app.exec_())