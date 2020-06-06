import os

from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtWidgets import QFileSystemModel, QMenu, QDialog, QMessageBox

from src.parser import Parser
from src.processor import is_midi_file


class FileBrowser(QDialog):
    def __init__(self, state, path):
        """
        Настройка UI
        :param state: state
        :param path: путь до первоначальной директории
        """
        super(FileBrowser, self).__init__()
        uic.loadUi("ui/filebrowser.ui", self)
        self.toolButton.setArrowType(QtCore.Qt.UpArrow)
        self.toolButton.clicked.connect(self.dir_up)
        self.openButton.clicked.connect(self.open_action)
        self.state = state
        self.path = path
        self.populate()

    def populate(self):
        """
        Настраивает treeView
        """
        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.context_menu)
        self.treeView.doubleClicked.connect(self.double_click)
        self.model = QFileSystemModel()
        self.model.setRootPath((QtCore.QDir.rootPath()))
        self.treeView.setModel(self.model)
        self.set_treeView_path(self.path)
        self.treeView.selectionModel().selectionChanged.connect(self.select)
        self.treeView.setSortingEnabled(True)

    def context_menu(self):
        """
        Отображает контекстное меню по ПКМ
        """
        menu = QMenu()
        open_action = menu.addAction("Выбрать")
        open_action.triggered.connect(self.open_action)
        if os.path.isfile(self.get_path()):
            show_text = menu.addAction("Показать текст")
            show_text.triggered.connect(self.show_text)
        cursor = QtGui.QCursor()
        menu.exec_(cursor.pos())

    def get_path(self):
        """
        Возвращает путь до выбранного файла
        :return: str
        """
        index = self.treeView.currentIndex()
        return self.model.filePath(index)

    def set_treeView_path(self, path):
        """
        Устанавливает директорию, отображаемую treeView
        :param path: str
        """
        self.path = path
        self.treeView.setRootIndex(self.model.index(path))
        self.pathField.setText(path)

    def open_action(self):
        """
        Выбирает midi файл для вопсроизведения
        """
        path = (
            self.get_path() if not self.last_selected else self.last_selected
        )
        if not self.check_path(path):
            return
        self.state.file = path
        self.close()

    def double_click(self):
        """
        Обработчки двойного клика на файл
        """
        path = self.get_path()
        if os.path.isfile(path):
            self.open_action()
        else:
            self.set_treeView_path(path)

    def dir_up(self):
        """
        Обработчки кнопки перехода к директории верхнего уровня
        """
        self.set_treeView_path(os.path.dirname(self.path))

    def select(self):
        """
        Обработчик выделения
        """
        path = self.get_path()
        if os.path.isfile(path):
            self.last_selected = path
            self.fileField.setText(path)
            self.openButton.setEnabled(True)

    def check_path(self, path):
        """
        Проверяет, является файл по пути path валидным midi файлом
        :param path: str
        """
        if not is_midi_file(path):
            errorBox = QMessageBox()
            errorBox.setText("Файл не является midi файлом")
            errorBox.setIcon(QMessageBox.Critical)
            errorBox.exec()
            return False
        return True

    def show_text(self):
        """
        Открывает диалоговое окно с тектом песни
        """
        path = (
            self.get_path() if not self.last_selected else self.last_selected
        )
        if not self.check_path(path):
            return
        parser = Parser(path)
        text = parser.parse()[1]
        msgBox = QMessageBox()
        msgBox.setText("\n".join(text))
        msgBox.exec()
