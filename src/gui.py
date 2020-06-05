import functools
from time import sleep

from PyQt5 import uic
from PyQt5.QtCore import Qt, QBasicTimer, QTimer, QThread
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QWidget, QFileDialog
from PyQt5.uic.properties import QtCore

from src.state import State


class Thread(QThread):
    def __init__(self, sentences_with_timings):
        super().__init__()
        self.sentences_with_timings = sentences_with_timings


class Karaoke(QWidget):
    def __init__(self, parent, state):
        super().__init__(parent)
        uic.loadUi("src/karaoke.ui", self)

        self.state = state
        self.timer = QTimer()

        self.verticalLayout.setAlignment(Qt.AlignHCenter)
        self.open.clicked.connect(self.start)
        self.setFocusPolicy(Qt.StrongFocus)

    def start(self):
        self.clear()
        file = QFileDialog.getOpenFileName(self, "Открыть .kar файл", "", "Караоке (*.kar)")[0]
        if not file:
            return
        sentences_with_timings = self.state.run(file)
        self.title_label.setText(self.state.track_name)
        delay = 0
        for pair in sentences_with_timings:
            delay += pair[1] * 1000
            timer_callback = functools.partial(self.show_sentence, sentence=pair[0])
            self.timer.singleShot(delay, timer_callback)

    def clear(self):
        self.timer.stop()
        self.lyricsLabel.setText("")
        self.title_label.setText("Ничего не играет")
        self.timer = QTimer()

    def show_sentence(self, sentence):
        text = ""
        for pair in sentence:
            text += pair[0] + " "
        print(text)
        self.lyricsLabel.setText(text)
        word_delay = 0
        for word_timeout in sentence:
            word_delay += word_timeout[1] * 1000
            timer_callback = functools.partial(self.highlight_word, word=word_timeout[0])
            self.timer.singleShot(word_delay, timer_callback)

    def highlight_word(self, word):
        text = self.lyricsLabel.text()
        text.replace(word, "<font color=\"#AE5D5D\"; >{}</font>".format(word))
        print(1)
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
        self.setWindowTitle('Karaoke')
        self.resize(600, 600)
        self.center()
        self.show()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)
