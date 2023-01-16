import pygame

from window import *
from button import Button
from map_driver import *
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QScrollArea, QRadioButton, QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5 import Qt, QtCore # эстетика клинкор
import os
from importlib.machinery import SourceFileLoader
import threading

app = QApplication([])

class QInput(QWidget):
    def __init__(self):
        self.label = QLabel("My text")
        self.setWindowTitle("введи текст балбес")
        self.setLayout(self.layout)
    def get_text(self):
        return self.label.text()

class RadioButtons(QWidget):
    def __init__(self, root):
        super().__init__(root)
        self.resize(345, 30)
        self.move(5, 600)
        self.setLayout(QHBoxLayout(self))
        self.always = QRadioButton("Можно проходить", self)
        self.after = QRadioButton("Только после конца", self)
        self.never = QRadioButton("Нельзя проходить", self)
        self.layout().addWidget(self.always)
        self.layout().addWidget(self.after)
        self.layout().addWidget(self.never)

    def check(self):
        if self.always.isChecked():
            return 0
        elif self.after.isChecked():
            return -1
        elif self.never.isChecked():
            return 1
class Example(QWidget):
    def __init__(self, root): #  да, я скоммуниздил его из урока
        super().__init__()
        self.root = root
        self.path = "textures/blocks/"
        self.hand_value = None
        self.initUI()

    def initUI(self):

        self.setGeometry(300, 300, 345 + 85, 630)

        self.setWindowTitle('Выберите текстуру блока')
        self.block_button = QPushButton("Блоки", self)
        self.block_button.resize(80, 30)
        self.block_button.move(5, 0)
        self.block_button.clicked.connect(lambda: self.choose_type("textures/blocks/"))
        self.guys_button = QPushButton("Противники", self)
        self.guys_button.resize(80, 30)
        self.guys_button.move(90, 0)
        self.guys_button.clicked.connect(lambda: self.choose_type("textures/guys/"))
        self.things_button = QPushButton("Вещи", self)
        self.things_button.resize(80, 30)
        self.things_button.move(175, 0)
        self.things_button.clicked.connect(lambda: self.choose_type("textures/things/"))
        self.guns_button = QPushButton("Оружие", self)
        self.guns_button.resize(80, 30)
        self.guns_button.move(260, 0)
        self.guns_button.clicked.connect(lambda: self.choose_type("textures/guns/"))
        self.hand_value = RadioButtons(self)
        self.hand_value.hide()
        self.cuts_button = QPushButton("Катсцены/скрипты", self)
        self.cuts_button.resize(80, 30)
        self.cuts_button.move(345, 0)
        self.cuts_button.clicked.connect(lambda: self.choose_type("cutscenes/"))
        self.scroll_area = QScrollArea(self)
        self.scroll_area.move(5, 40)
        self.scroll_area.resize(335, 555)
        self.vbox_widget = QWidget(self)
        self.scroll_area.setWidgetResizable(True)
        self.vbox_widget.setLayout(QVBoxLayout(self.scroll_area))
        self.scroll_area.setWidget(self.vbox_widget)
        self.choose_type("textures/blocks/")
    def choose_type(self, path, icons=True):
        textures = os.listdir(path)
        self.path = path
        for i in reversed(range(self.vbox_widget.layout().count())):
            self.vbox_widget.layout().itemAt(i).widget().setParent(None)
        if path == "textures/things/":
            self.hand_value.show()
        else:
            self.hand_value.hide()
        for t in textures:
            p = QPushButton(t, self)
            if icons:
                p.setIcon(QIcon(path + t))
                p.setIconSize(QtCore.QSize(24, 24))
            p.clicked.connect(self.choose)
            self.vbox_widget.layout().addWidget(p)
    def choose(self):
        sender = self.sender()
        if self.path == "textures/blocks/":
            self.root.hand = blocks_pth[self.path + sender.text()]
        if self.path == "textures/guys/":
            self.root.handguy = guys_name[self.path + sender.text()]
        if self.path == "textures/things/":
            b = self.hand_value.check()

            self.root.handth = [self.path + sender.text(), b]
        if self.path == "textures/guns/":
            self.root.handgun = sender.text()[:sender.text().rfind('.')]
        if self.path == "cutscenes/":
            self.root.handdiag = sender.text()


def create_qt_menu(root):
    ex = Example(root)
    ex.show()
    app.exec()

class Redactor(Window):
    def __init__(self, caption="", size=(1920, 1080), defaultcol=(255, 255, 255), filename=None, x=0, y=0, music=None, weather=None, bl=None):
        if not filename:
            self.file_name = input("Введите имя файла:")
        else:
            self.file_name = filename
        print(self.file_name)

        self.spawn = None
        self.m_pressed = -10
        self.pause = False
        self.guys = []
        self.things = []
        self.handguy = None # какого чувака ща будем ставить
        self.handth = None # какую вещь ща будем ставить
        self.handgun = None # какой пистолет ща будет ставить
        self.handdiag = None # какой диалог ща будем ставить
        self.guns = []
        self.weather = None
        self.bsize = 50

        self.scenes = []
        self.exits = []

        self.music = None
        self.weather = None
        self.map_change = []
        if weather:
            self.weather = weather
        if music:
            self.music = music
        self.map_change = []
        self.rports = []
        self.bports = []


        if os.path.exists(self.file_name):
            self.map = SourceFileLoader(self.file_name[:self.file_name.rfind('.')], self.file_name).load_module().MAP
            try:
                self.spawn = SourceFileLoader(self.file_name[:self.file_name.rfind('.')],
                                              self.file_name).load_module().SPAWN
            except:
                self.spawn = None
            try:
                self.guys = SourceFileLoader(self.file_name[:self.file_name.rfind('.')],
                                             self.file_name).load_module().GUYS
            except:
                self.guys = []
            try:
                self.things = SourceFileLoader(self.file_name[:self.file_name.rfind('.')],
                                               self.file_name).load_module().THINGS
            except:
                self.things = []
            try:
                self.weather = SourceFileLoader(self.file_name[:self.file_name.rfind('.')],
                                                self.file_name).load_module().WEATHER
            except:
                self.weather = None
            try:
                self.scenes = SourceFileLoader(self.file_name[:self.file_name.rfind('.')],
                                               self.file_name).load_module().SCENES
            except:
                self.scenes = []
            try:
                self.guns = SourceFileLoader(self.file_name[:self.file_name.rfind('.')],
                                             self.file_name).load_module().GUNS
            except:
                self.guns = []
            try:
                self.rports = SourceFileLoader(self.file_name[:self.file_name.rfind('.')],
                                               self.file_name).load_module().RPORTS
                self.bports = SourceFileLoader(self.file_name[:self.file_name.rfind('.')],
                                               self.file_name).load_module().BPORTS
            except:
                self.rports = []
                self.bports = []

            try:
                self.map_change = SourceFileLoader(self.file_name[:self.file_name.rfind('.')],
                                                   self.file_name).load_module().MAP_CHANGE
            except:
                self.map_change = []
            try:
                self.music = SourceFileLoader(self.file_name[:self.file_name.rfind('.')],
                                              self.file_name).load_module().MUSIC
            except:
                self.music = None
            try:
                self.exits = SourceFileLoader(self.file_name[:self.file_name.rfind('.')],
                                              self.file_name).load_module().EXITS
            except:
                self.exits = []
            self.y = len(self.map)
            self.x = len(self.map[0])
        else:
            self.x, self.y = x, y
            self.map = [[bl for i in range(self.x)] for j in range(self.y)]
            self.music = music
            self.weather = weather

        self.bsize = 50

        self.cx, self.cy = 0, 0
        self.th_tex = {}
        self.font = pygame.font.SysFont('serif', 15)
        for t in self.things:
            self.th_tex[t[0]] = pygame.image.load(t[0])
        Window.__init__(self, caption, size, defaultcol)
        if not os.path.exists(self.file_name):
            self.save()
    def save(self):
        f = open(self.file_name, 'w')
        f.write("MAP = [\n")
        for l in range(0, len(self.map) - 1):
            f.write(str(self.map[l]) + ",\n")
        f.write(str(self.map[-1]) + "\n")

        f.write("]\n")
        if self.spawn:
            f.write("SPAWN = " + str(self.spawn) + '\n')
        if self.guys:
            f.write("GUYS = " + str(self.guys) + '\n')
        if self.things:
            f.write("THINGS = " + str(self.things) + "\n")

        if self.scenes:
            f.write("SCENES = " + str(self.scenes) + "\n")
        if self.guns:
            f.write("GUNS = " + str(self.guns) + '\n')
        if self.rports:
            f.write("RPORTS = " + str(self.rports) + '\n')
        if self.bports:
            f.write("BPORTS = " + str(self.bports) + '\n')
        if self.map_change:
            f.write('MAP_CHANGE = ' + str(self.map_change) + '\n')
        if self.exits:
            f.write('EXITS = ' + str(self.exits) + '\n')
        if self.weather:
            f.write("WEATHER = '" + str(self.weather) + "'\n")
        if self.music:
            f.write("MUSIC = '" + str(self.music) + "'\n")
        if not self.weather:
            self.weather = input("введи погоду:")
        if self.weather:
            f.write("WEATHER = '" + str(self.weather) + "'\n")
        if not self.music:
            self.music = input("введите файл музыки (можно пропустить):")
        if self.music:
            f.write("MUSIC = '" + str(self.music) + "'\n")

        f.close()


    def loop(self):
        is_clicked = False
        self.hand = '#'
        hands = {
            pygame.K_1: '#',
            pygame.K_2: ' ',
            pygame.K_3: 'N',
            pygame.K_r: 'spawn', # pygame.K_r / 1082
            pygame.K_e: 'exit',
            pygame.K_b: 'gunguy', # pygame.K_b / 1080
            pygame.K_n: 'thing',  # смени на pygame_K_n / 1090. Мой старый почему то отзывается только на 1090
            pygame.K_7: 'bl',
            pygame.K_8: 'guy',
            pygame.K_9: 'th',
            pygame.K_0: 'diag',
            pygame.K_m: 'sc',
            pygame.K_p: 'pp',
            pygame.K_q: 'rp', # pygame.K_q / 1081
            pygame.K_a: 'bp', # pygame.K_a / 1092
            pygame.K_l: 'cm' # гениальный костыль для смены карты. И не надо было нам телепортов
        }
        t = []
        for i in hands:
            print(f"{i}: {hands[i]}")

        while self.WINDOW_RUNNING:
            mpos = False
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    quit()
                if i.type == pygame.MOUSEBUTTONDOWN:
                    self.m_pressed = i.button
                if i.type == pygame.MOUSEBUTTONUP:
                    self.m_pressed = -10
                if i.type == pygame.MOUSEBUTTONDOWN:
                    is_clicked = i.button + 1
                    mpos = pygame.mouse.get_pos()
                if i.type == pygame.MOUSEBUTTONUP:
                    is_clicked = False
                if i.type == pygame.KEYDOWN:
                    print(i.key)
                    if i.key in hands:
                        self.hand = hands[i.key]

                    if i.key == pygame.K_s: # pygame.K_s / 1099
                        self.save()
                    if i.key == pygame.K_TAB:
                        create_qt_menu(self)
                    if i.key == pygame.K_ESCAPE:
                        self.pause = not self.pause

            self.root.fill(self.col)

            show_map(self.root, self.map, [self.cx, self.cy], size=self.bsize)
            mouse = pygame.mouse.get_pos()
            block = [(self.cx + mouse[0]) // self.bsize, (self.cy + mouse[1]) // self.bsize]

            if block[0] >= 0 and block[0] < self.x:
                if block[1] >= 0 and block[1] < self.y:
                    pygame.draw.rect(self.root, (255, 255, 255), (block[0] * self.bsize - self.cx, block[1] * self.bsize - self.cy, self.bsize, self.bsize), 3)
                    if is_clicked == 2 and not self.pause:
                        print(self.hand)
                        if self.map[block[1]][block[0]] != self.hand:
                            if self.hand == "spawn":
                                self.spawn = block
                            elif self.hand == "exit":
                                if block not in self.exits:
                                    self.exits.append(block)

                            elif self.hand == "gunguy":
                                if self.map[block[0]][block[1]] in good_floor:
                                    self.guys.append([self.handguy, mouse[0] + self.cx - 50, mouse[1] + self.cy - 50]) # 50 тк стандарт текстуры перса 100*100px
                                    is_clicked = False
                            elif self.hand == "thing":
                                if not self.handth:
                                    continue

                                y = self.handth[1]

                                if self.handth[0] not in self.th_tex:
                                    self.th_tex[self.handth[0]] = pygame.image.load(self.handth[0])
                                self.things.append([self.handth[0], y, mouse[0] + self.cx, mouse[1] + self.cy])
                                is_clicked = False
                            elif self.hand == "bl":
                                create_qt_menu(self, "blocks")

                            elif self.hand == "guy":
                                create_qt_menu(self, "guys")
                                if self.map[block[0]][block[1]] in good_floor:
                                    self.guys.append([self.handguy, mouse[0] + self.cx - 50, mouse[1] + self.cy - 50])
                            elif self.hand == "th":
                                create_qt_menu(self, "things")
                            elif self.hand == "diag":
                                create_qt_menu(self, "cutscenes")
                            elif self.hand == "sc":
                                isd = 1
                                for s in self.scenes:
                                    if s[1] == block[0] and s[2] == block[1]:
                                        isd = 0
                                if isd:
                                    self.scenes.append([self.handdiag, *block])
                            elif self.hand == 'pp':
                                if self.handgun:
                                    if self.handgun == "pistolet":
                                        bulls = 10
                                    elif self.handgun == "shootgun":
                                        bulls = 5
                                    self.guns.append([self.handgun, mouse[0] + self.cx, mouse[1] + self.cy, bulls])
                                is_clicked = -10

                            elif self.hand == 'rp':
                                self.rports.append(block)
                                is_clicked = -1
                            elif self.hand == 'bp': # синий/красный будет перемещать вас на синий/красный портал с таким же индексом
                                is_clicked = -1
                                self.bports.append(block) # в порталы красные мы заходим после заистки этажа. В синие, когда зачищен весь уровень

                            elif self.hand == 'cm':
                                self.map_change.append([input(), *block])

                            else:
                                self.map[block[1]][block[0]] = self.hand
                    if is_clicked == 4:
                        if self.hand in ["gunguy", "bl", "guy", "th"]:
                            for g in range(0, len(self.guys)):
                                pygame.draw.rect(self.root, (255, 255, 255), ((mouse[0] + self.cx - self.guys[g][1] - 50), (mouse[1] + self.cx - self.guys[g][2] - 50), 50, 50))
                                if (abs(mouse[0] + self.cx - self.guys[g][1] - 50) < 30) and (abs(mouse[1] + self.cx - self.guys[g][2] - 50) < 30):
                                    del self.guys[g]
                                    break


            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                self.cx += 5
            if keys[pygame.K_LEFT]:
                self.cx -= 5
            if keys[pygame.K_UP]:
                self.cy -= 5
            if keys[pygame.K_DOWN]:
                self.cy += 5
            for g in self.guys:
                if g[0] == "gunguy":
                    self.root.blit(gunguy, (g[1] - self.cx, g[2] - self.cy))
                elif g[0] == "primat":
                    self.root.blit(el_primoTx, (g[1] - self.cx, g[2] - self.cy))
                elif g[0] == "shootgunman":
                    self.root.blit(shootgun_manTx, (g[1] - self.cx, g[2] - self.cy))
            for t in self.things:
                self.root.blit(self.th_tex[t[0]], (t[2] - self.cx, t[3] - self.cy))
            for p in self.rports:
                pygame.draw.rect(self.root, (200, 0, 0), (p[0] * self.bsize - self.cx, p[1] * self.bsize - self.cy, self.bsize, self.bsize))
            for p in self.bports:
                pygame.draw.rect(self.root, (0, 0, 200), (p[0] * self.bsize - self.cx, p[1] * self.bsize - self.cy, self.bsize, self.bsize))

            for s in self.scenes:
                pygame.draw.rect(self.root, (255, 100, 100), (s[1] * self.bsize - self.cx, s[2] * self.bsize - self.cy, self.bsize, self.bsize), 2)
            for gun in self.guns:
                if gun[0] == "pistolet":
                    self.root.blit(pistoletTx, (gun[1] - self.cx, gun[2] - self.cy))
                elif gun[0] == "shootgun":
                    self.root.blit(shootgunTx, (gun[1] - self.cx, gun[2] - self.cy))

            #  рисуем призрачное отображение
            ghost = None
            if self.hand == "pp":
                if self.handgun == "pistolet":
                    ghost = pygame.Surface((20, 20))
                    ghost.blit(pistoletTx, (0, 0))

            elif self.hand == "thing":
                ghost = pygame.image.load(self.handth[0])

            elif self.hand == "gunguy":
                if self.handguy == "primat":
                    ghost = el_primoTx.copy()
                if self.handguy == "gunguy":
                    ghost = gunguy.copy()
                if self.handguy == "shootgunman":
                    ghost = shootgun_manTx.copy()


            else:
                try:
                    ghost = pygame.Surface((50, 50))
                    if blocks[self.hand]:
                        ghost.blit(blocks[self.hand], (0, 0))
                except:
                    pass
            if ghost:
                ghost.set_alpha(50)
                self.root.blit(ghost, mouse)

            if self.pause:
                draw_menu_redactor(self)



            pygame.display.update()
            self.clock.tick(60)

if __name__ == "__main__": # глеб ты че дебил?
    pygame.init()
    root = Redactor()
    root.loop()