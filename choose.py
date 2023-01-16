import PyQt5
import pygame
import sys
from PyQt5.QtWidgets import QPushButton, QApplication, QWidget, QLineEdit, QVBoxLayout, QHBoxLayout, QLabel
import os
from map_redactor import *

app = QApplication([])

class Example(QWidget):
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.names = os.listdir("maps")
        self.initUI()

    def initUI(self):
        #self.showFullScreen()
        self.setGeometry(300, 300, 300, 300)
        self.setLayout(QVBoxLayout(self))
        self.main_widget = QWidget(self)
        news = []
        for i in self.names:
            if len(i) > 3:
                if i[:3] == "new" and i[3:-3].isdecimal():
                    news.append(int(i[3:-3]))
                elif i[:3] == "new":
                    news.append(0)
        if len(news) > 0:
            news.sort()
            for i in range(len(news)):
                if i != 0:
                    if news[i] != news[i - 1] + 1:
                        i -= 1
                        break
            name = f"new{str(news[i] + 1)}.py"
        else:
            name = "new.py"
        self.main_widget.move(self.size().width() // 3, self.size().height() // 10)
        self.main_widget.resize(self.size().width() // 3, self.size().height() // 10 * 9)
        self.main_widget.setLayout(QVBoxLayout(self))
        self.file = QLineEdit(name, self)
        self.file.textChanged.connect(self.mode_change)
        self.main_widget.layout().addWidget(self.file)
        self.label = QLabel("Создать новую", self)
        self.main_widget.layout().addWidget(self.label)
        self.filling = QLineEdit("Заполнение", self)
        self.main_widget.layout().addWidget(self.filling)
        self.x_button = QLineEdit("x", self)
        self.y_button = QLineEdit("y", self)
        self.x_y_widget = QWidget()
        self.x_y_widget.setLayout(QHBoxLayout(self))
        self.x_y_widget.layout().addWidget(self.x_button)
        self.x_y_widget.layout().addWidget(self.y_button)
        self.main_widget.layout().addWidget(self.x_y_widget)
        self.music = QLineEdit("Музыка", self)
        self.main_widget.layout().addWidget(self.music)
        self.weather = QLineEdit("Погода", self)
        self.main_widget.layout().addWidget(self.weather)
        self.go_button = QPushButton("Запустить", self)
        self.main_widget.layout().addWidget(self.go_button)
        self.go_button.clicked.connect(self.run)

    def run(self):
        if self.file.text() in self.names:
            ROOT = Redactor(filename=f"maps/{self.file.text()}")
        else:
            ROOT = Redactor(filename=f"maps/{self.file.text()}", x=int(self.x_button.text()),
                            y=int(self.y_button.text()), bl=self.filling.text(), weather=self.weather.text() if self.weather.text() != "Нет" else None, music=self.music.text() if self.music.text() != "Нет" else None)
        self.root.root_buffer = ROOT


    def mode_change(self):
        if self.file.text() in self.names:
            self.filling.hide()
            self.x_y_widget.hide()
            self.music.hide()
            self.weather.hide()
            self.label.setText("Файл найден")
        else:
            self.music.show()
            self.weather.show()
            self.filling.show()
            self.x_y_widget.show()
            self.label.setText("Создать новую")

STARTED = 0


def start(root):
    global STARTED
    pygame.init()
    if STARTED == 0:
        STARTED = 1
        ex = Example(root)
        ex.show()
        app.exec()
