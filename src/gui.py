import functools
from time import sleep

from PyQt5 import uic
from PyQt5.QtCore import Qt, QBasicTimer, QTimer, QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QWidget, QFileDialog
from PyQt5.uic.properties import QtCore

from src import Signals
from src.state import State


class Thread(QThread):
    def __init__(self, state, signal):
        super().__init__()
        self.state = state
        self.signal = signal

    def run(self):
        for i, sentence in enumerate(self.state.sentences):
            self.signal.need_sentences.emit(sentence)
            for word, time in self.state.words_with_timings[i]:
                self.signal.need_word_highlight.emit(word)
                sleep(time)
        self.signal.need_sentences.emit("")


class Karaoke(QWidget):
    def __init__(self, parent, state):
        super().__init__(parent)
        uic.loadUi("src/karaoke.ui", self)

        self.signals = Signals.Signals()
        self.signals.need_sentences.connect(self.show_sentences)
        self.signals.need_word_highlight.connect(self.highlight_word)

        self.state = state

        self.verticalLayout.setAlignment(Qt.AlignHCenter)
        self.open.clicked.connect(self.start)
        self.setFocusPolicy(Qt.StrongFocus)

        self.thread = None

    def start(self):
        self.clear()
        file = QFileDialog.getOpenFileName(self, "Открыть .kar файл", "", "Караоке (*.kar)")[0]
        if not file:
            return
        self.state.run(file)
        self.title_label.setText(self.state.track_name)
        self.thread = Thread(self.state, self.signals)
        self.thread.start()

    def clear(self):
        self.lyricsLabel.setText("")
        self.title_label.setText("Ничего не играет")
        self.state.stop()
        if self.thread:
            self.thread.terminate()

    def show_sentences(self, sentence):
        self.lyricsLabel.setText(sentence)

    def highlight_word(self, word):
        text = self.lyricsLabel.text()
        text = text.replace(word, "<font color=\"#AE5D5D\"; >{}</font>".format(word))
        self.lyricsLabel.setText(text)


class KaraokeWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.state = State()
        self.karaoke = Karaoke(self, self.state)
        self.initUI()

    def initUI(self):
        self.setCentralWidget(self.karaoke)

        self.setObjectName("window")
        self.setStyleSheet("#window { background-image: url(images/background.jpg); }")
        self.setWindowTitle('Караоке')
        self.resize(600, 600)
        self.center()
        self.show()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)
