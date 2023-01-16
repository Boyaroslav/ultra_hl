import pygame
from random import randint
from deamon import Deamon
import threading
from button import Button
import math

pygame.init()

good_floor = [' ', 'N', 't', "s", "ty", "tg", "g", "lam"]

plankTx = pygame.image.load("textures/blocks/plank.png")
floorTx = pygame.image.load("textures/blocks/floor.png")
tileTx = pygame.image.load("textures/blocks/tile.png")
tileyeTx = pygame.image.load("textures/blocks/tile_yellow.png")
snowTx = pygame.image.load("textures/blocks/snow.png")
wallTx = pygame.image.load("textures/blocks/wall.png")
tilegrTx = pygame.image.load("textures/blocks/tile_gray.png")
greenTx = pygame.image.load("textures/blocks/green.png")
laminateTx = pygame.image.load("textures/blocks/laminate.png")

gunguy = pygame.image.load("textures/guys/normal_bad.png")
mainplTx = pygame.image.load("textures/guys/mainpl.png")
mainpl_pistoletTx = pygame.image.load("textures/guys/mainpl_pistolet.png")
main_deadTx = pygame.image.load("textures/things/dead_mainpl1.png")
mainpl_shootgunTx = pygame.image.load("textures/guys/mainpl_shootgun.png")
normal_deadTx = pygame.image.load("textures/things/normal_dead.png")
heavy_is_deadTx = pygame.image.load("textures/things/dead_primo.png")
shootgun_deadTx = pygame.image.load("textures/things/shootgun_dead.png")
el_primoTx = pygame.image.load("textures/guys/primat.png")

shootgun_manTx = pygame.image.load("textures/guys/shootgun_man.png")

#  guns

pistoletTx = pygame.image.load("textures/guns/pistolet.png")
shootgunTx = pygame.image.load("textures/guns/shootgun.png")

bulletTx = pygame.image.load("textures/particles/bullet.png")

holeTx = pygame.image.load("textures/particles/hole.png")

TIMER = 0

BULLETS_SPEED = 20

# souhds

punch_sound = pygame.mixer.Sound("sounds/hotline-miami-punch.wav")
hit = pygame.mixer.Sound("sounds/hotline-miami-hit.wav")
ammo_pickup = pygame.mixer.Sound("sounds/ammo_pickup.wav")
pistolet_fire = pygame.mixer.Sound("sounds/pistol_fire2.wav")
shootgun_fire = pygame.mixer.Sound("sounds/shotgun_dbl_fire.wav")
shootgun_empty = pygame.mixer.Sound("sounds/shotgun_empty.wav")
primo_dead_s = pygame.mixer.Sound("sounds/primo_dead_s.wav")


blocks = {
    '#': plankTx,
    ' ': floorTx,
    't': tileTx,
    'N': None,
    "s": snowTx,
    "ty": tileyeTx,
    "w": wallTx,
    "lam": laminateTx,
    "g": greenTx,
    "tg": tilegrTx
}

blocks_pth = {
    "textures/blocks/plank.png" : '#',
    "textures/blocks/floor.png" : ' ',
    "textures/blocks/tile.png" : 't',
    "textures/blocks/tile_yellow.png" : 'ty',
    "textures/blocks/snow.png": "s",
    "textures/blocks/wall.png": "w",
    "textures/blocks/tile_gray.png": "tg",
    "textures/blocks/green.png": "g",
    "textures/blocks/laminate.png": "lam"

}


guys_pth = {
    "textures/guys/normal_bad.png": gunguy,
    "textures/guys/mainpl.png": mainplTx,
    "textures/guys/primat.png": el_primoTx,
    "textures/guys/shootgun_man.png": shootgun_manTx
}

guys_name = {
    "textures/guys/normal_bad.png": "gunguy",
    "textures/guys/mainpl.png": "MAIN",
    "textures/guys/primat.png": "primat",
    "textures/guys/shootgun_man.png": "shootgunman"
}

punch = [
    pygame.image.load("textures/particles/kick/kick5.png"),
    pygame.image.load("textures/particles/kick/kick4.png"),
    pygame.image.load("textures/particles/kick/kick3.png"),
    pygame.image.load("textures/particles/kick/kick2.png"),
    pygame.image.load("textures/particles/kick/kick1.png")
]

def draw_punches(self):
    j = 0
    for i in range(0, len(self.bad_punch) - j):
        try:
            if int(self.bad_punch[i][-1] / 100 * 5) - 1 < 0:
                del self.bad_punch[i]
                j += 1

            t = punch[int(self.bad_punch[i][-1] / 100 * 5) - 1]

            b = t.get_rect()
            rot = pygame.transform.rotate(t, -255 + self.bad_punch[i][2])
            rot_rect = b.copy()
            rot_rect.center = rot.get_rect().center
            rot = rot.subsurface(rot_rect).copy()


            self.root.blit(rot, (self.bad_punch[i][0] - self.cx - 50, self.bad_punch[i][1] - self.cy - 50))
            self.bad_punch[i][-1] -= int(self.bad_punch[i][-1] / 100 * 5)
            if check_punch(rot, self.guys[0].x - (self.bad_punch[i][0]), self.guys[0].y - (self.bad_punch[i][1])) and not self.im_lose:
                self.im_lose = 1
                self.dead_rot = self.bad_punch[i][2]
                hit.play()
        except:
            pass

    for i in range(0, len(self.good_punch)):
        try:
            if int(self.good_punch[i][-1] / 100 * 5) - 1 < 0:
                del self.good_punch[i]
                j += 1

            t = punch[int(self.good_punch[i][-1] / 100 * 5) - 1]

            b = t.get_rect()
            rot = pygame.transform.rotate(t,  -225 + self.good_punch[i][2])
            rot_rect = b.copy()
            rot_rect.center = rot.get_rect().center
            rot = rot.subsurface(rot_rect).copy()
            #rot.fill((255, 255, 255))
            self.root.blit(rot, (self.good_punch[i][0] - self.cx, self.good_punch[i][1] - self.cy))

            self.good_punch[i][-1] -= int(self.good_punch[i][-1] / 100 * 5)
            for guy in range(1, len(self.guys)):
                if check_punch(rot, self.guys[guy].x - (self.good_punch[i][0]), self.guys[guy].y - (self.good_punch[i][1])):
                    self.guys[guy].get_lose(-255 + self.good_punch[i][2])
                    self.deads.append(self.guys[guy])
                    del self.guys[guy]
                    hit.play()

        except:
            pass

def check_punch(punch, x, y):
    t = pygame.Surface((40, 40))
    pygame.draw.circle(t, (255, 255, 255), (20, 20), 20)
    t = pygame.mask.from_surface(t)
    return pygame.mask.from_surface(punch).overlap(t, (x - 20, y - 20))

def draw_shoots(self):
    for i in self.good_shoots:
        i.logic(self)
        i.draw(self)
    for i in self.bad_shoots:
        i.logic(self)
        i.draw(self)

def draw_trash(self): # рисуем мелкие детальки

    for i in self.trash:
        self.root.blit(i[0], (i[1] - self.cx, i[2] - self.cy))


def in_screen(p, cx, cy, size):
    if p[0] >= cx and p[0] <= cx + size[0]:
        if p[1] >= cy and p[1] <= cy + size[1]:
            return 1
    return 0

def show_map(root, map, cam, size=50, csize=(0,0), draw_shadow=0):
    if type(map) != type(root):
        for y in range(0, len(map)):
            for x in range(0, len(map[0])):
                if blocks[map[y][x]] == None:
                    pass
                else:
                    root.blit(blocks[map[y][x]], (size * x - cam[0], size * y - cam[1]))
    else:
        root.blit(map, (-cam[0], -cam[1]))

def show_things(root, th, cam):
    for i in th:
        root.blit(i[0], (i[3][0] - cam[0], i[3][1] - cam[1]))

def mask_from_blocks(root):
    x = root.bsize * len(root.map[0])
    y = root.bsize * len(root.map)

    surf = pygame.Surface((x, y))
    for y in range(0, len(root.map)):
        for x in range(0, len(root.map[0])):
            if root.map[y][x] not in good_floor:
                pygame.draw.rect(surf, (255, 255, 255), (x * root.bsize, y * root.bsize, root.bsize, root.bsize))
    root.bl_mask = pygame.mask.from_surface(surf)

def render_bl(root, draw_shadow=1):

    root.bl_surf = pygame.Surface(((len(root.map[0]) + 1) * root.bsize, (len(root.map) + 1) * root.bsize + 15), pygame.SRCALPHA)
    if draw_shadow:
        root.bl_shad = pygame.Surface(((len(root.map[0]) + 1) * root.bsize, (len(root.map) + 1) * root.bsize + 15), pygame.SRCALPHA)
    #  15 на случай теней
    if draw_shadow:
        shr = pygame.Surface((15, 50))
        shr.fill((0, 0, 0))
        shd = pygame.Surface((50, 15))
        shd.fill((0, 0, 0))
        shsq = pygame.Surface((15, 15))
        shsq.fill((0, 0, 0))

    for y in range(0, len(root.map)):
        for x in range(0, len(root.map[0])):
            if blocks[root.map[y][x]] == None:
                pass
            else:
                buf = pygame.transform.scale(blocks[root.map[y][x]], (root.bsize, root.bsize))
                root.bl_surf.blit(buf, (root.bsize * x, root.bsize * y))
                if draw_shadow:
                    if root.map[y][x] not in good_floor:
                        if y + 1 < len(root.map) and x + 1 < len(root.map[0]):
                            if root.map[y + 1][x + 1] in good_floor:
                                pygame.draw.rect(root.bl_shad, (0, 0, 0), (root.bsize * (x + 1), root.bsize * (y + 1), 15, 15))

                        if y + 1 < len(root.map):
                            if root.map[y + 1][x] in good_floor:
                                pygame.draw.rect(root.bl_shad, (0, 0, 0),
                                                 (root.bsize * x + 15, root.bsize * (y + 1), root.bsize - 15, 15))
                        if x + 1 < len(root.map[0]):
                            if root.map[y][x + 1] in good_floor:
                                pygame.draw.rect(root.bl_shad, (0, 0, 0),
                                                 (root.bsize * (x + 1), root.bsize * y + 15, 15, root.bsize - 15))
        if draw_shadow:
            pygame.draw.rect(root.bl_shad, (0, 0, 0), (len(root.map[0]) * root.bsize, y * root.bsize, 15, root.bsize))
    if draw_shadow:
        for x in range(0, len(root.map[0])):
            if root.map[-1][x] not in good_floor:
                pygame.draw.rect(root.bl_shad, (0, 0, 0), (x * root.bsize + 15, len(root.map) * root.bsize, root.bsize, 15))
    if draw_shadow:
        root.bl_shad.set_alpha(30)



def check_collide(pos, th):

    x = pos[0] - th[3][0]
    y = pos[1] - th[3][1]
    s = pygame.Surface((40, 40))
    pygame.draw.circle(s, (255, 255, 255), (20, 20), 20)
    m = pygame.mask.from_surface(s)

    return (th[1].overlap(m, (x - 20, y - 20)))

def check_all_collides(pos, ths, level_is_done=1): # -1 - можешь проходить после конца игры 0 - можешь проходить 1 - не можешь
    for i in ths:
        if (i[-2] == 1) or (i[-2] == -1 and (level_is_done == 1)):
            if check_collide(pos, i):
                return True
    return False

PART_BLOCK = None

def get_settings():
    CONFIG = {}

    for i in open("settings.conf").readlines():
        if '=' in i:
            CONFIG[i.split('=')[0].rstrip()] = eval(i.split("=")[1].lstrip())

    return CONFIG


def show_weather(root, map, weather, N=10, update=1):
    if not weather:
        return 0
    if weather == "SNOW":
        global PART_BLOCK
        if update or not PART_BLOCK:
            PART_BLOCK = pygame.Surface((root.bsize, root.bsize))
            sp = pygame.Surface((2, 2))
            sp.fill((255, 255, 255))
            for i in range(N):
                PART_BLOCK.blit(sp, (randint(2, root.bsize - 2), randint(2, root.bsize - 2)))
                PART_BLOCK.set_alpha(50)
        for y in range(0, len(map)):
            for x in range(0, len(map[0])):

                if map[y][x] in ["N", 's']:
                    if x * root.bsize - root.cx >= -root.bsize:
                        if y * root.bsize - root.cy >= -root.bsize:
                            if x * root.bsize - root.cx > root.size[0]:
                                y = (y + 1) % len(map)
                                x = 0
                            elif y * root.bsize - root.cy > root.size[1]:
                                return
                            else:
                                root.root.blit(PART_BLOCK, (x * root.bsize - root.cx, y * root.bsize - root.cy))
    
SCREEN = ()

def fill_screen(root, weather, static=(20, 0, 20), update = 0):
    if static:
        root.root.fill(static)
        return 0
    if update:
        global SCREEN
        if weather == "SNOW":
            SCREEN = (randint(240, 255), randint(250, 255), randint(240, 255))
        elif weather == "MIAMI":
            if not SCREEN:
                SCREEN = (200, 100, 240)
            SCREEN = ((SCREEN[0] - 1) % 255, (SCREEN[1] + 2) % 255, (SCREEN[2] + 1) % 255)
        elif weather == "MIAMI2":
            if not SCREEN:
                SCREEN = (0, 0, 0)
            SCREEN = ((SCREEN[0] + 3) % 254, (SCREEN[1]+ 1) % 254, (SCREEN[2] + 2) % 254)
        else:
            pass
    if SCREEN:
        root.root.fill(SCREEN)

def show_guns(self, guns):
    for gun in self.guns:
        if gun[0] == "pistolet":
            self.root.blit(pistoletTx, (gun[1] - self.cx, gun[2] - self.cy + self.wavevec))
        elif gun[0] == "shootgun":
            self.root.blit(shootgunTx, (gun[1] - self.cx, gun[2] - self.cy + self.wavevec))
def teleport(self):
    x = self.guys[0].x // self.bsize
    y = self.guys[0].y // self.bsize
    if self.last_t == [x, y]:
        return
    if self.level_not_done:
        if [x, y] in self.rports:
            d = Deamon(draw_blackout, 1)
            n = threading.Thread(target=d.run, args=(self, []))
            n.start()
            self.guys[0].x = self.bports[self.rports.index([x, y])][0] * self.bsize + 30
            self.guys[0].y = self.bports[self.rports.index([x, y])][1] * self.bsize + 30
            #self.last_t = [x, y]
    else:
        if [x, y] in self.bports:
            d = Deamon(draw_blackout, 1)
            n = threading.Thread(target=d.run, args=(self, []))
            n.start()
            self.guys[0].x = self.rports[self.bports.index([x, y])][0] * self.bsize + 30
            self.guys[0].y = self.rports[self.bports.index([x, y])][1] * self.bsize + 30
            #self.last_t = [x, y]

def draw_ports(self):
    for p in range(0, len(self.rports)):
        pygame.draw.rect(self.root, (200, 0, 0), (self.rports[p][0] * self.bsize - self.cx, self.rports[p][1] * self.bsize - self.cy, self.bsize, self.bsize))
        pygame.draw.rect(self.root, (0, 0, 200), (self.bports[p][0] * self.bsize - self.cx, self.bports[p][1] * self.bsize - self.cy, self.bsize, self.bsize))



def draw_blackout(self):
    hard = 0
    maxhard = 100
    timer = 100
    tb = 0
    surf = pygame.Surface(self.size)

    for i in range(0, 100):
        if tb % 200 == 0:
            hard += maxhard // timer
            pygame.draw.rect(surf, (0, 0, 0), (0, 0, self.size[0], self.size[1]))
            surf.set_alpha(hard % 255)
        tb += 1
        self.root.blit(surf, (0, 0))

        if self.DISPLAY_NEED_TO_BE_FLIPED:
            pygame.display.update()

        if not self.WINDOW_RUNNING or not self.RUN_DEM:
            return

    for i in range(100, 0, -1):
        hard -= maxhard // timer
        pygame.draw.rect(surf, (0, 0, 0), (0, 0, self.size[0], self.size[1]))
        surf.set_alpha(hard % 255)
        self.root.blit(surf, (0, 0))
        if self.DISPLAY_NEED_TO_BE_FLIPED:
            pygame.display.update()
        if not self.WINDOW_RUNNING or not self.RUN_DEM:
            return



def draw_sun(root):
    color = (255, 100, 0)
    MORE_YELL = True
    COUNTER = 0
    wavex = 140
    clock = pygame.time.Clock()
    while root.WINDOW_RUNNING and root.RUN_DEM:
        pygame.draw.circle(root.root, color, (1000, 400), 100)
        for i in range(5):
            pygame.draw.rect(root.root, (color[0] // 10, 0, 256 - color[0] % 256),
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
        if COUNTER == 180:
            COUNTER = 0
        if root.DISPLAY_NEED_TO_BE_FLIPED:
            pygame.display.update()
        clock.tick(144 * 10)


def draw_interface(self):
        b = str(self.score)
        for i in range(0, len(b)):

            sc = self.cool_font.render(b[i], True, (200, 100, 50))
            sc_out = self.cool_but_buffer_font.render(b[i], True, (0, 0, 0))
            self.root.blit(sc_out, (i * 30 + self.size[0] - 200, 30))
            self.root.blit(sc, (i * 30 + self.size[0] - 198, 28))
        b = str(self.real_score)
        for i in range(0, len(b)):

            sc = self.font.render(b[i], True, (200, 100, 50))
            sc_out = self.font.render(b[i], True, (0, 0, 0))
            self.root.blit(sc_out, (i * 30 + self.size[0] - 200, 30))
            self.root.blit(sc, (i * 30 + self.size[0] - 198, 28))
        if self.real_score < self.score:
            self.real_score += 50

        if self.guys[0].bullets != None:
            bl = self.cool_font.render(str(self.guys[0].bullets), True, (255, 100, 255))
            pygame.draw.rect(self.root, (50, 0, 10), (20, self.size[1] - 120, 100, 70))
            self.root.blit(bl, (50, self.size[1] - 100))


def draw_cool_texts(root): # рисуем на карте штучки шрифтовые
    for i in range(0, len(root.cool_texts)): # [x, y, surface, time]
        if i >= len(root.cool_texts):
            return
        if root.cool_texts[i][-1] <= 0:
            del root.cool_texts[i]

        else:
            b = root.cool_texts[i][0][0]
            b_s = root.cool_texts[i][0][1]
            b = pygame.transform.scale(b, (200 - 10 * root.cool_texts[i][-1], 100 - (5 * root.cool_texts[i][-1])))
            b_s = pygame.transform.scale(b_s, (200 - 10 * root.cool_texts[i][-1] - 10, 100 - (5 * root.cool_texts[i][-1]) - 10))
            root.root.blit(b_s, (root.cool_texts[i][1] - root.cx - (400 - 20 * root.cool_texts[i][-1]) // 4 + 30,
                               root.cool_texts[i][2] - 25 - root.cy))
            root.root.blit(b, (root.cool_texts[i][1] - root.cx - (400 - 20 * root.cool_texts[i][-1]) // 4 + 25, root.cool_texts[i][2] - 40 - root.cy))

            if root.TIMER % 20 == 0:
                root.cool_texts[i][-1] -= 1

def unpause(root):
    pygame.mouse.set_visible(False)
    pygame.mixer.music.unpause()
    root.pause = False
    if root.pause == 1:
        pygame.mixer.music.unpause()
        pygame.mouse.set_visible(False)
        root.pause = False
    return

def unpause_red(root):

    root.pause = False

def ret_menu(root):
    from menu import Main
    root.WINDOW_RUNNING = False
    global ROOT
    ROOT = Main()
    ROOT.loop()

def draw_pause_interface(root):
    v = pygame.Surface(root.size)
    v.fill((100, 0, 150))
    v.set_alpha(20)
    root.root.blit(v, (0, 0))
    butts = [

        Button(root.root, text="ты чо дурак играй иди", function=unpause, args=[root], coords=(root.size[0] // 4, 150), size=(root.size[0] // 2, 50), font=root.font, fcolor=(0, 0, 0)),

        Button(root.root, text="в меню", function=ret_menu, args=[root],
               coords=(root.size[0] // 4, 300), size=(root.size[0] // 2, 50), font=root.font,
               fcolor=(0, 0, 0))
    ]
    mpos = None
    if root.m_pressed == 1:
        mpos = pygame.mouse.get_pos()

    for b in butts:
        b.place(mpos, borders=1)

def draw_menu_redactor(root):
    v = pygame.Surface(root.size)
    v.fill((100, 0, 150))
    v.set_alpha(20)
    root.root.blit(v, (0, 0))
    butts = [
        Button(root.root, text="продолжаем", function=unpause, args=[root], coords=(root.size[0] // 4, 150), size=(root.size[0] // 2, 50), font=root.font, fcolor=(0, 0, 0)),
        Button(root.root, text="в меню", function=ret_menu, args=[root],
               coords=(root.size[0] // 4, 300), size=(root.size[0] // 2, 50), font=root.font,
               fcolor=(0, 0, 0)),
        Button(root.root, text="сохранить карту", function=root.save, args=[], coords=(root.size[0] // 4, 450),
               size=(root.size[0] // 2, 50), font=root.font, fcolor=(0, 0, 0))
    ]
    mpos = None
    if root.m_pressed == 1:
        mpos = pygame.mouse.get_pos()

    for b in butts:
        b.place(mpos, borders=1)