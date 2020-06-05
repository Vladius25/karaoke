from PyQt5.QtCore import QObject, pyqtSignal


class Signals(QObject):
    need_sentences = pyqtSignal(str)
    need_word_highlight = pyqtSignal(str)

    def __init__(self):
        super(Signals, self).__init__()
