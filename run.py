import sys
from pathlib import Path

from PyQt5.QtWidgets import QApplication

from src.gui import KaraokeWindow

if __name__ == "__main__":
    app = QApplication([])
    snake = KaraokeWindow(
        str(Path.home()) if len(sys.argv) < 2 else sys.argv[1]
    )
    sys.exit(app.exec_())
