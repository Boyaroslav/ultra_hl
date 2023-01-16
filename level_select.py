from window import *
import os
from importlib.machinery import SourceFileLoader
from button import Button
import sys
from game import Game
from map_driver import *

# сюжетные карты
LEVELS = ['first_map.py', 'second_map.py']


class Select(Window):
    def __init__(self, caption="", size=(1900, 1080), defaultcol=(150, 100, 0)):
        super().__init__(caption, size, defaultcol)
        self.config = get_settings()
        self.root = pygame.display.set_mode(size, pygame.FULLSCREEN)
        if self.config["MAPS_PACK"]:
            self.lvls = LEVELS
        else:
            self.lvls = list(filter(lambda x: x[-3:] == ".py",os.listdir("maps/")))
        self.index = 0

        self.font = pygame.font.SysFont('monospace', 40)
        self.buttons = [Button(self.root, "назад", self.ret, args=[], coords=(1700, 10), size=(150, 60), font=self.font)]
        self.cx, self.cy = 0, 0 # отображение мини карты
    
    def ret(self):
        import menu
        self.WINDOW_RUNNING = False
        #self.RUN_DEM = False
        global ROOT

        ROOT = menu.Main()

        ROOT = menu.Main(change_music=0)

        ROOT.loop()

    def render_mini_map(self, name):
        if not self.config["DRAW_MINI_MAP"]:
            return
        f = SourceFileLoader(name, 'maps/' + name).load_module()
        self.map = f.MAP
        self.bsize = 20
        self.bl_shad = None
        x = (len(self.map[0]))
        if x * self.bsize > 200:
            x = int(200 // self.bsize)
        y = (len(self.map))
        if y * self.bsize > 200:
            y = int(200 // self.bsize)

        self.bl_surf = pygame.Surface((x, y), pygame.SRCALPHA)
        render_bl(self, 0)


    
    def loop(self):
        CHANGING = False
        mpos = 0
        buf_root = pygame.Surface((600, 1000))
        self.bl_surf = pygame.Surface((10, 10))
        x = self.size[0] // 3 - 50
        if self.config["DRAW_MINI_MAP"]:
            buf_root.fill((255, 255, 255))
            self.render_mini_map(self.lvls[self.index % len(self.lvls)])
        while self.WINDOW_RUNNING:
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    quit()
                if i.type == pygame.MOUSEBUTTONDOWN:
                    mpos = i.pos
                if i.type == pygame.MOUSEBUTTONUP:
                    mpos = None
                if i.type == pygame.KEYDOWN and CHANGING == 0:
                    if i.key == pygame.K_RIGHT:
                        CHANGING = 10
                        #self.index += 1
                    if i.key == pygame.K_LEFT:
                        CHANGING = -10
                        #self.index -= 1
                    if i.key == pygame.K_RETURN:
                        if CHANGING == 0:
                            self.WINDOW_RUNNING = False
                            global ROOT
                            ROOT = Game(map=self.lvls[self.index], level_pack=LEVELS)
                            ROOT.loop()

                    if i.key == pygame.K_a:
                        self.cx += self.bsize

                    if i.key == pygame.K_w:
                        self.cy += self.bsize
                    if i.key == pygame.K_s:
                        self.cy -= self.bsize
                    if i.key == pygame.K_d:
                        self.cx -= self.bsize



            self.root.fill(self.col)
            for d in self.LOOP_DEAMONS:
                darr = self.root_info(d.keys)
                if d.is_async:
                    n = threading.Thread(target=d.run, args=(self, darr,))
                    del d
                else:
                    d.run(self, darr)
            
            for i in self.buttons:
                i.place(mpos)
            
            name = self.font.render(self.lvls[self.index % len(self.lvls)][:-3], True, (255, 255, 255))
            name_b = self.font.render(self.lvls[self.index % len(self.lvls)][:-3], True, (50, 50, 50))
            if self.config["DRAW_MINI_MAP"]:
                buf_root.fill((230, 218, 166))
                buf_root.blit(self.bl_surf, (self.cx, self.cy))
            if CHANGING == 0:

                pygame.draw.rect(self.root, (230, 218, 166), (x, 40, 600, 1000))
                self.root.blit(buf_root, (x, 40))
            elif CHANGING < 0:
                x -= 40
                CHANGING += 1
                pygame.draw.rect(self.root, (255, 255, 255), (x, 40, 600, 1000))
                pygame.draw.rect(self.root, (255, 255, 255), (self.size[0] + x, 40, 600, 1000))
                if CHANGING == 0:
                    self.index -= 1
                    x = self.size[0] // 3 - 50
                    self.render_mini_map(self.lvls[self.index % len(self.lvls)])
                    self.cx, self.cy = 0, 0
            elif CHANGING > 0:
                x += 40
                CHANGING -= 1
                pygame.draw.rect(self.root, (255, 255, 255), (x, 40, 600, 1000))
                pygame.draw.rect(self.root, (255, 255, 255), (-500 + x, 40, 600, 1000))
                if CHANGING == 0:
                    self.index += 1
                    x = self.size[0] // 3 - 50
                    if self.config["DRAW_MINI_MAP"]:
                        self.render_mini_map(self.lvls[self.index % len(self.lvls)])
                        self.cx, self.cy = 0, 0
            self.root.blit(name_b, (x, 550))
            self.root.blit(name, (x, 540))

            self.index = self.index % len(self.lvls)

            
    
            pygame.display.update()
            self.clock.tick(60)




