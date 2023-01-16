from window import *
from button import Button

CONFIG = {}

for i in open("settings.conf").readlines():
    if '=' in i:
        CONFIG[i.split('=')[0].rstrip()] = eval(i.split("=")[1].lstrip())


class Settings(Window):
    def __init__(self, caption="", size=(1920, 1080), defaultcol=(50, 50, 50)):
        super().__init__(caption, size, defaultcol)
        self.font = pygame.font.SysFont('monospace', 60)
        self.buttons = [Button(self.root, "назад", self.ret, args=[], coords=(550, 50), size=(180, 80), font=self.font, color=(0, 0, 0)),
                        Button(self.root, f"громкость музыки: {CONFIG['MUSIC_P']}", self.do_noth, args=[], coords=(self.size[0] // 4, 200), size=(800, 80), font=self.font, color=(0, 0, 0)),
                        Button(self.root, "-", self.ch_vol, args=[-10], coords=(self.size[0] // 4 - 90, 200), size=(80, 80), font=self.font, color=(0, 0, 0)),
                        Button(self.root, "+", self.ch_vol, args=[10], coords=(self.size[0] // 4 + 810, 200), size=(80, 80), font=self.font, color=(0, 0, 0)),
                        Button(self.root, f"громкость звуков: {CONFIG['SOUND_P']}", self.do_noth, args=[],
                               coords=(self.size[0] // 4, 350), size=(800, 80), font=self.font, color=(0, 0, 0)),
                        Button(self.root, "-", self.ch_vol_s, args=[-10], coords=(self.size[0] // 4 - 90, 350),
                               size=(80, 80), font=self.font, color=(0, 0, 0)),
                        Button(self.root, "+", self.ch_vol_s, args=[10], coords=(self.size[0] // 4 + 810, 350),
                               size=(80, 80), font=self.font, color=(0, 0, 0)),
                        Button(self.root, "запомнить", self.ret_flush, args=[], coords=(550 - 400, 50), size=(340, 80), font=self.font, color=(0, 0, 0)),
                        Button(self.root, f"рисовать мини карту: {CONFIG['DRAW_MINI_MAP']}", self.ch_mimi_map, args=[], coords=(self.size[0] // 4 - 90, 500), size=(980, 80), font=self.font, color=(0, 0, 0)),
                        Button(self.root, f"Только сюжетные карты: {CONFIG['MAPS_PACK']}", self.ch_lvl_map, args=[], coords=(self.size[0] // 4 - 90, 700), size=(980, 80), font=self.font, color=(0, 0, 0))]
    def do_noth(self):
        return

    def ret_flush(self):
        f = open('settings.conf', 'w')
        for l in CONFIG:
            f.write(f"{l} = {CONFIG[l]}\n")
        f.close()
        self.ret()

    def ch_lvl_map(self):
        global CONFIG
        CONFIG["MAPS_PACK"] = not CONFIG["MAPS_PACK"]
        self.buttons[-1].set_text(f"Только сюжетные карты: {CONFIG['MAPS_PACK']}")
        self.mpos = None


    def ch_vol(self, n):
        global CONFIG
        CONFIG["MUSIC_P"] = n + CONFIG["MUSIC_P"]
        if CONFIG["MUSIC_P"] < 0:
            CONFIG["MUSIC_P"] = 0
        elif CONFIG["MUSIC_P"] > 100:
            CONFIG["MUSIC_P"] = 100


        self.buttons[1].set_text(f"громкость музыки: {CONFIG['MUSIC_P']}")
        pygame.mixer.music.set_volume(CONFIG["MUSIC_P"] / 100)
        self.mpos = None

    def ch_vol_s(self, n):
        global CONFIG
        CONFIG["SOUND_P"] = n + CONFIG["SOUND_P"]
        if CONFIG["SOUND_P"] < 0:
            CONFIG["SOUND_P"] = 0
        elif CONFIG["SOUND_P"] > 100:
            CONFIG["SOUND_P"] = 100

        self.buttons[4].set_text(f"громкость звуков: {CONFIG['SOUND_P']}")
        #pygame.mixer.music.set_volume(CONFIG["SOUND_P"] / 100)
        self.mpos = None

    def ch_mimi_map(self):
        global CONFIG
        CONFIG["DRAW_MINI_MAP"] = not CONFIG["DRAW_MINI_MAP"]
        self.buttons[-2].set_text(f"рисовать мини карту: {CONFIG['DRAW_MINI_MAP']}")
        self.mpos = None

    def ret(self):
        import menu
        self.WINDOW_RUNNING = False
        #self.RUN_DEM = False
        global ROOT

        ROOT = menu.Main(change_music=0)
        ROOT.loop()

    
    def loop(self):

        mpos = None
        self.mpos = None
        while self.WINDOW_RUNNING:
            self.root.fill(self.col)
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    quit()
                if i.type == pygame.MOUSEBUTTONDOWN:
                    self.mpos = i.pos
                if i.type == pygame.MOUSEBUTTONUP:
                    self.mpos = None
            for j in self.buttons:
                j.place(self.mpos, 1)
            
            pygame.display.update()
            self.clock.tick(20)

