from window import *
from deamon import Deamon
import game
import level_select
import pygame
import map_redactor
import settings
from button import Button

from map_driver import draw_sun, get_settings

from random import choice
from choose import *

ex = None
        
dsun = Deamon(draw_sun, True)

class Main(Window):
    def __init__(self, caption="", size=(1920, 1080), defaultcol=(50, 50, 50), change_music=1):
        self.config = get_settings()
        super().__init__(caption, self.config["ROOT_SIZE"], defaultcol)
        pygame.init()
        self.change_music = change_music
        self.font = pygame.font.Font('8bitwonderrusbylyajka_nominal.otf', 60)
        self.root = pygame.display.set_mode(self.config["ROOT_SIZE"], pygame.FULLSCREEN)

        #self.font = pygame.font.SysFont('monospace', 15)
        self.main_font = pygame.font.Font('shoguns-clan.regular.ttf', 120)
        self.xt = choice(['Half Life', 'Hotline Miami', 'Hot Lieutenant', 'Hard Limiter', 'High Level', 'Hell Layers', 'Horizontal Launch', 'HomeLess', 'HeLicopter', 'HL', 'ultra HL', 'Hitler Lenin'])
        self.mtext = self.main_font.render(self.xt, True, (250, 100, 100))
        self.root_buffer = None
        pygame.mouse.set_visible(True)

        self.blocks = [Button(self.root, text="начать", function=self.ch_map, args=[level_select.Select], coords=(100, 200), size=(485, 120), font=self.font),
        Button(self.root, text="настройки", function=self.ch_map, args=[settings.Settings], coords=(100, 400), size=(485, 120), font=self.font),
        Button(self.root, text="редактор", function=start, args=[self], coords=(100, 600), size=(485, 120), font=self.font),
        Button(self.root, text="выйти", function=self.quit, coords=(100, 800), size=(485, 120), font=self.font)]

        #self.LOOP_DEAMONS.append(dsun)
    
    def quit(self):
        self.WINDOW_RUNNING = False
        quit()
    
    def ch_map(self, map):
        self.RUN_DEM = False
        self.WINDOW_RUNNING = False
        global ROOT

        ROOT = map()
        ROOT.loop()

    def loop(self):
        global ROOT

        if self.change_music:
            pygame.mixer.music.load("0801.wav")
            pygame.mixer.music.set_volume(self.config["MUSIC_P"])
            pygame.mixer.music.play(-1)

        color = (255, 100, 0)
        MORE_YELL = True
        COUNTER = 0
        wavex = 140


        self.DISPLAY_NEED_TO_BE_FLIPED = False
        while self.WINDOW_RUNNING:
            mpos = None
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    self.WINDOW_RUNNING = False
                    quit()

            self.root.fill((100 - (wavex) // 4, 0, 20))

            keys = pygame.key.get_pressed()
            mouse = pygame.mouse.get_pressed()
            if mouse[0]:
                mpos = pygame.mouse.get_pos()
            for i in range(0, len(self.blocks)):
                self.blocks[i].place(mpos)
            for d in range(0, len(self.LOOP_DEAMONS)):
                darr = self.root_info(self.LOOP_DEAMONS[d].keys)
                if self.LOOP_DEAMONS[d].is_async:
                    n = threading.Thread(target=self.LOOP_DEAMONS[d].run, args=(self, darr,))
                    n.start()
                    del self.LOOP_DEAMONS[d]
                else:
                    d.run(self, darr)
            


            self.nt = self.main_font.render(self.xt, True, color)

 
            self.root.blit(self.nt, (self.size[0] - 1098, 22))
            self.root.blit(self.mtext, (self.size[0] - 1100, 20))

            pygame.draw.circle(self.root, color, (1000, 400), 100)
            for i in range(5):
                pygame.draw.rect(self.root, (color[0] // 10, 0, 256 - color[0] % 256),
                                 (950 - wavex // 2 + 10 * i, 430 + i * 40, wavex - 20 * i + 100, 15 - i * 3))
            if COUNTER == 0:
                if color[0] == 200:
                    MORE_YELL = False
                if color[0] == 255:
                    MORE_YELL = True

                if MORE_YELL:
                    color = (color[0] - 1, color[1] - 1, 0)
                else:
                    color = (color[0] + 1, color[1] + 1, 0)
            COUNTER += 1
            if COUNTER == 3:
                COUNTER = 0

            if self.root_buffer:
                self.WINDOW_RUNNING = 0
                ROOT = self.root_buffer
                ROOT.loop()

            pygame.display.update()
            self.clock.tick(60)


ROOT = Main()
ROOT.loop()