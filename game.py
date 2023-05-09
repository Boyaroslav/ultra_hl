import time

from window import *
from map_driver import *
from importlib.machinery import SourceFileLoader
import math
from random import choice, randint
from shaders import SNOW
from cutscene import Cutscene# десантник степачкин
import settings

easyness = 1 # чем больше число, тем реже будет шмалять нормал гай

class Guy:
    def __init__(self, x=0, y=0, rot=90, texture=pygame.Rect((0, 0), (0, 0))):
        self.x, self.y, self.rot, self.texture = x + 50, y + 50, rot, texture
        self.block = []
        self.move = choice(['d', 'u', 'r', 'l'])
        self.timer = 0
        self.dead_rot = None
        self.dead_tx = None
        self.appendings = [] # при помощи этого мы можем выпукать из себя что то после смерти

    def get_lose(self, d):
        self.dead_rot = d
        if self.dead_tx:
            self.texture = self.dead_tx

    def standart_logic(self, root):

        if self.dead_rot != None:
            return
        #self.block = [self.x // root.bsize, self.y // root.bsize]
        if self.timer == 0:
            nx = self.x
            ny = self.y

            if self.move == 'd':
                ny += 10
                self.rot = 90
            
            if self.move == 'u':
                ny -= 10
                self.rot = -90
            
            if self.move == 'l':
                nx -= 10
                self.rot = 0

            
            if self.move == 'r':
                nx += 10
                self.rot = -180

            
            if not check_circle_col([nx, ny], root.map, 50, 15) and not check_all_collides([nx, ny], root.things):
                self.x ,self.y = nx, ny
            
            elif not check_circle_col([self.x, ny], root.map, 50, 15) and not check_all_collides([self.x, ny], root.things):
                self.y = ny
                if self.move == 'l':
                    self.move = choice(['u', 'r', 'd'])
                elif self.move == 'r':
                    self.move = choice(['d', 'u', 'l'])
            elif not check_circle_col([nx, self.y], root.map, 50, 15) and not check_all_collides([nx, self.y], root.things):
                self.x = nx
                if self.move == 'd':
                    self.move = choice(['u', 'r', 'l'])
                elif self.move == 'u':
                    self.move = choice(['d', 'r', 'l'])

        self.timer += 1
        self.timer = self.timer % 15

    
    def draw(self, root):
        root.root.blit(self.texture, (root.size[0] // 2, root.size[1] // 2))
        
    def check_col(self, x, y):
        return (math.sqrt(((x - self.x) ** 2) + ((y - self.y) ** 2)) <= 40)

def get_degree(pos, campos):
    a = campos[0] - pos[0]
    b = campos[1] - pos[1]
    c = round(math.sqrt(a * a + b * b), 6)
    try:
        cosx = a / c
    except:
        cosx = 0

    if b > 0:
        return -1*math.degrees(math.acos(cosx))
    return math.degrees(math.acos(cosx))

def check_next_move(pos, map, bsize=50, mysquare=[10, 10]):
    block1 = [pos[0] // bsize, pos[1] // bsize]

    block2 = [(pos[0] + mysquare[0]) // bsize, pos[1] // bsize]

    block3 = [pos[0] // bsize, (pos[1] + mysquare[1]) // bsize]

    block4 = [(pos[0] + mysquare[0]) // bsize, (pos[1] + mysquare[1]) // bsize]
    #print(block1, block2, block3, block4)
    return (map[block1[1]][block1[0]] in good_floor) and ((map[block2[1]][block2[0]]) in good_floor) and \
    (map[block3[1]][block3[0]] in good_floor) and (map[block4[1]][block4[0]] in good_floor)

def check_circle_col(pos, map, bsize, R, n=15):

    for a in range(0, (360 // n) * n, 360 // n):
        nx = int(pos[0] + R * math.cos(a))
        ny = int(pos[1] + R * math.sin(a))
        if not (ny // bsize >= 0 and ny // bsize < len(map)):
            return True
        if not ((nx // bsize >= 0 and nx // bsize < len(map[0]))):
            return True

        if map[ny // bsize][nx // bsize] not in good_floor:
            return True
    return False

class Bullet: # не лень наследовать, как бы это не было странно
    def __init__(self, x, y, rot, g=1):
        self.x = x
        self.y = y
        self.rot = rot
        self.texture = bulletTx
        self.im_good_bul = g

    def logic(self, root):
        self.x -= BULLETS_SPEED * math.cos(math.radians(-self.rot))
        self.y -= BULLETS_SPEED * math.sin(math.radians(-self.rot))
        try:
            if root.map[int(self.y // root.bsize)][int(self.x // root.bsize)] not in good_floor:
                root.trash.append([holeTx, int(self.x), int(self.y)])
                if self.im_good_bul:
                    del root.good_shoots[root.good_shoots.index(self)]
                    return
                del root.bad_shoots[root.bad_shoots.index(self)]
                return
            if self.im_good_bul:
                for i in range(1, len(root.guys)):

                    if root.guys[i].check_col(self.x, self.y):
                        root.guys[i].get_lose(self.rot)
                        root.deads.append(root.guys[i])
                        del root.guys[i]
                        del root.good_shoots[root.good_shoots.index(self)]
                        return
            else:
                if root.guys[0].check_col(self.x, self.y) and not root.im_lose:
                    root.im_lose = 1
                    root.dead_rot = self.rot
        except:
            pass

    def draw(self, root):
        b = self.texture.get_rect()
        rot = pygame.transform.rotate(self.texture, -90 + self.rot)
        rot_rect = b.copy()
        rot_rect.center = rot.get_rect().center
        rot = rot.subsurface(rot_rect).copy()
        root.root.blit(rot, (self.x - root.cx - 10, self.y - root.cy - 10))

class Me(Guy):
    def __init__(self, x=0, y=0, rot=90, texture=pygame.Rect((0, 0), (0, 0))):
        Guy.__init__(self, x, y, rot, texture)
        self.curtex = pygame.image.load("cursor.png")
        self.texture_hands = texture
        self.texture_pistolet = mainpl_pistoletTx
        self.texture_shootgun = mainpl_shootgunTx
        self.texture_rifle = mainpl_rifleTx

        self.gun = None
        self.me = 'me'
        self.max_force = 100
        self.force = self.max_force
        self.gun_force = 30
        self.bullets = None
        self.is_rest = 0 #  фиксю стояние в попе и бесконтрольный тимминг во время рестарта

    def logic(self, root):
        if root.im_lose:
            return
        root.cx = self.x - root.size[0] // 2
        root.cy = self.y - root.size[1] // 2 + root.offsety
        if root.offsety > 0:
            if root.TIMER % 5 == 0:
                root.offsety -= 5
        nx, ny = self.x, self.y
        if root.keys:
            if root.keys[pygame.K_LEFT]:
                nx -= 5
            if root.keys[pygame.K_RIGHT]:
                nx += 5
            if root.keys[pygame.K_UP]:
                ny -= 5
            if root.keys[pygame.K_DOWN]:
                ny += 5
            if root.keys[pygame.K_LSHIFT]:
                root.cx = root.mouse[0] - root.size[0] // 2
                root.cy = root.mouse[1] - root.size[1] // 2
            if root.keys[pygame.K_r] and self.x - root.bsize != root.spawn[0] * root.bsize and self.y - root.bsize != root.spawn[1]:
                if self.is_rest == 0:
                    root.init_level()
                    self.is_rest = 1
                    return

            #self.is_rest = 0
        if root.m_pressed:
            if root.m_pressed == 1:
                if self.gun == None:
                    if self.max_force == self.force:
                        try:
                            if root.map[int(self.y + 50 * math.sin(math.radians(self.rot))) // root.bsize][int((self.x - 50 * math.cos(math.radians(self.rot))) // root.bsize)] in good_floor:
                                punch_sound.play()
                                root.good_punch.append([self.x - 50 * math.cos(math.radians(self.rot)) - 25, self.y + 50 * math.sin(math.radians(self.rot)) - 25, self.rot, 100])
                                self.force -= 1
                        except:
                            pass
                    else:
                        pass
                if self.gun == "pistolet":
                    if self.max_force == self.force and self.bullets > 0:


                        root.good_shoots.append(Bullet(self.x,
                                                    self.y, self.rot
                                                    ))
                        self.force -= 1
                        self.bullets -= 1
                        pistolet_fire.play()

                elif self.gun == "shootgun":
                    if self.max_force == self.force and self.bullets > 0:


                        root.good_shoots.append(Bullet(self.x,
                                                    self.y, self.rot - 2
                                                    ))
                        root.good_shoots.append(Bullet(self.x,
                                                       self.y, self.rot
                                                       ))
                        root.good_shoots.append(Bullet(self.x,
                                                       self.y, self.rot + 2
                                                       ))
                        self.force -= 1
                        self.bullets -= 1
                        shootgun_fire.play()
                    elif self.bullets <= 0:
                        shootgun_empty.play()
                elif self.gun == "rifle":
                    if self.force % 10 == 0 and self.bullets > 0:


                        root.good_shoots.append(Bullet(self.x,
                                                    self.y, self.rot
                                                    ))
                        self.force -= 1
                        self.bullets -= 1
                        pistolet_fire.play()

            if root.m_pressed == 3:
                if self.gun != None:
                    root.guns.append([self.gun, self.x, self.y, self.bullets])
                    self.gun = None
                    self.bullets = None
                    root.m_pressed = -10
                    return
                try:
                    for gun in range(0, len(root.guns)):
                        if self.gun:
                            break
                        if abs((root.guns[gun][1] + 10) - self.x) < 30:
                            if abs((root.guns[gun][2] + 5) - self.y) < 30:
                                self.gun = root.guns[gun][0]
                                self.bullets = root.guns[gun][-1]
                                del root.guns[gun]
                                ammo_pickup.play()
                except:
                    pass
                root.m_pressed = -10
        adding = [True, True]
        if self.force < self.max_force:
            self.force -= 1
        if self.force < 0:
            self.force = self.max_force

        for guy in root.guys[1:]:
            if guy.dead_rot != None:
                continue
            if guy.check_col(nx, ny):
                adding = [False, False]
            elif guy.check_col(self.x, ny):
                adding[0] = False
            elif guy.check_col(nx, self.y):
                adding[1] = False
           # level_not_done 0 - уровень закончен
        if (not check_circle_col([nx, ny], root.map, 50, 15)) and (adding[0] and adding[1]) and not check_all_collides([nx, ny], root.things, root.level_not_done):
            self.x = nx
            self.y = ny
        elif not check_circle_col([self.x, ny], root.map, 50, 15) and adding[1] and not check_all_collides([self.x, ny], root.things, root.level_not_done):
            self.y = ny
        elif not check_circle_col([nx, self.y], root.map, 50, 15) and adding[0] and not check_all_collides([nx, self.y], root.things, root.level_not_done):
            self.x = nx
        
        self.rot = int(get_degree((root.mouse[0], root.mouse[1]), [root.size[0] // 2, root.size[1] // 2]))


    
    def draw(self, root):
        if root.im_lose:
            b = main_deadTx.get_rect()
            rot = pygame.transform.rotate(main_deadTx, 90 + root.dead_rot)
            rot_rect = b.copy()
            rot_rect.center = rot.get_rect().center
            rot = rot.subsurface(rot_rect).copy()
            root.root.blit(rot, (root.size[0] // 2 - 100, root.size[1] // 2 - 100))
            return
        if self.gun == "pistolet":
            self.texture = self.texture_pistolet
        elif self.gun == "shootgun":
            self.texture = self.texture_shootgun
        elif self.gun == "rifle":
            self.texture = self.texture_rifle

        elif self.gun == None:
            self.texture = self.texture_hands

        b = self.texture.get_rect()
        rot = pygame.transform.rotate(self.texture, 90+self.rot)
        rot_rect = b.copy()
        rot_rect.center = rot.get_rect().center
        rot = rot.subsurface(rot_rect).copy()
        root.root.blit(rot, (self.x - root.cx - 50, self.y - root.cy - 50))
        if root.mouse and not root.pause:
            root.root.blit(self.curtex, (root.mouse[0] - 15, root.mouse[1] - 15))


class Normal_bad(Guy):
    def __init__(self, x, y, rot, texture):
        super().__init__(x, y, rot, texture)
        self.hide = False
        self.name = "gunguy"
        self.dead_tx = normal_deadTx
        self.bullets = 10
        self.max_force = 100 * easyness // 2
        self.force = self.max_force
        self.rot_ = self.texture
        self.seeT = 0

    def get_lose(self, d):
        self.dead_rot = d
        if self.dead_tx:
            self.texture = self.dead_tx
        # какого то фига он через super() не сравботал (я про get_lose)
        self.appendings.append(['pistolet', self.x - 10, self.y - 10, self.bullets])
        self.appendings.append([800])

    def shoot(self, root):
        n = randint(0, easyness)
        v = choice(range(-5, 5)) # для рандомизации выстрелов шобы изи было ваще
        if n == 0:
            if self.max_force == self.force and self.bullets > 0:
                root.bad_shoots.append(Bullet(self.x,
                                               self.y, self.rot + v * easyness, 0
                                               ))
                self.force -= 1
                self.bullets -= 1
                pistolet_fire.play()


    def chasing(self, root, radius, speed=4):
        if root.im_lose:
            return
        if root.debug:
            pygame.draw.circle(root.root, (0, 0, 0), (self.x - root.cx, self.y - root.cy), 20)
        if math.sqrt((root.guys[0].x - self.x) ** 2 + (root.guys[0].y - self.y) ** 2) <= radius:
            self.shoot(root)
        try:
            if check_all_collides([self.x + ((root.guys[0].x - self.x) // abs((root.guys[0].x - self.x))) * speed, self.y + ((root.guys[0].y - self.y) // abs((root.guys[0].y - self.y))) * speed], root.things):
                return
        except:
            pass
        try:
            self.x = self.x + ((root.guys[0].x - self.x) // abs((root.guys[0].x - self.x))) * speed
            self.y = self.y + ((root.guys[0].y - self.y) // abs((root.guys[0].y - self.y))) * speed
        except:
            pass

    def logic(self, root):
        if self.dead_rot != None:
            return
        if self.force < self.max_force:
            self.force -= 1
        if self.force < 0:
            self.force = self.max_force
        if root.im_lose:
            see = False
        else:
            see = True # теперь я эту глебину гадость переписал
            if ((self.y - root.guys[0].y) ** 2 + (self.x - root.guys[0].x) ** 2) ** 0.5 > 1000:
                super().standart_logic(root)

            else:
                stepy = (root.guys[0].y - self.y) // 50
                stepx = (root.guys[0].x - self.x) // 50
                x, y = self.x, self.y
                for i in range(50):
                    x += stepx
                    y += stepy
                    if root.debug:
                        pygame.draw.rect(root.root, (0, 0, 0), (x - root.cx, y - root.cy, 10, 10))
                    if root.map[y // root.bsize][x // root.bsize] != " ":
                        see = False
                        break
        if not see:

            super().standart_logic(root)
        else:
            self.seeT = (self.seeT + 1)
            if self.x - root.guys[0].x == 0:
                self.rot = 90
            elif root.TIMER % 20 == 0:
                if self.x > root.guys[0].x:
                    self.rot = math.degrees(-math.atan((self.y - root.guys[0].y) / (self.x - root.guys[0].x)))
                else:
                    self.rot = 180 - math.degrees(math.atan((self.y - root.guys[0].y) / (self.x - root.guys[0].x)))
            if self.seeT >= 100 and root.TIMER % 2 == 0:
                self.chasing(root, 200, 4)


    def draw(self, root):
        for i in self.appendings:
            if i[0] == "pistolet": # да, это безумный костыль, но зато какой!
                root.guns.append(i)
                root.guys_killed += 1  # о нет, как же жаль, что это костыль
            elif type(i[0]) == type(1):
                root.score += i[0]


                root.cool_texts.append([[root.cool_font.render(str(i[0]), True, (255, 0, 100)), root.cool_but_little_font.render(str(i[0]), True, (10, 0, 10))], self.x - 50, self.y - 50, 10])

        self.appendings = []
        if root.TIMER % 20 == 0:
            b = self.texture.get_rect()
            self.rot_ = pygame.transform.rotate(self.texture, 90+self.rot)
            rot_rect = b.copy()
            rot_rect.center = self.rot_.get_rect().center
            rot = self.rot_.subsurface(rot_rect).copy()
        root.root.blit(self.rot_, (self.x - root.cx - 50, self.y - root.cy - 50))

class El_Primo(Guy):
    def __init__(self, x, y, rot, texture):
        super().__init__(x, y, rot, texture)
        self.hide = False
        self.name = "primat"
        self.max_force = 100
        self.force = self.max_force
        self.dead_tx = heavy_is_deadTx
        self.rot_ = self.texture


    def get_lose(self, d):
        self.dead_rot = d
        if self.dead_tx:
            self.texture = self.dead_tx
        # да простит меня бог за перегрузки

        self.appendings.append([1000])
        primo_dead_s.play()

    def shoot(self, root, radius):

        if self.force == self.max_force:
            root.bad_punch.append([self.x, self.y, self.rot, 100]) # x, y, rot, timer
            punch_sound.play()
        self.force -= 1
        if self.force < 0:
            self.force = self.max_force

    def chasing(self, root, radius, speed=4):
        if math.sqrt((root.guys[0].x - self.x) ** 2 + (root.guys[0].y - self.y) ** 2) <= radius + 50:
            self.shoot(root, radius)
        try:
            if check_all_collides([self.x + ((root.guys[0].x - self.x) // abs((root.guys[0].x - self.x))) * speed, self.y + ((root.guys[0].y - self.y) // abs((root.guys[0].y - self.y))) * speed], root.things):
                return
        except:
            pass
        try:
            self.x = self.x + ((root.guys[0].x - self.x) // abs((root.guys[0].x - self.x))) * speed
            self.y = self.y + ((root.guys[0].y - self.y) // abs((root.guys[0].y - self.y))) * speed
        except:
            pass

    def draw(self, root):
        for i in self.appendings:
            if type(i[0]) == type(1):
                root.score += i[0]

                root.cool_texts.append([[root.cool_font.render(str(i[0]), True, (255, 0, 100)), root.cool_but_little_font.render(str(i[0]), True, (10, 0, 10))], self.x - 50, self.y - 50, 10])

                root.guys_killed += 1 # о нет, как же жаль, что это костыль
        self.appendings = []

        if root.TIMER % 20 == 0:
            b = self.texture.get_rect()
            self.rot_ = pygame.transform.rotate(self.texture, 90+self.rot)
            rot_rect = b.copy()
            rot_rect.center = self.rot_.get_rect().center
            self.rot_ = self.rot_.subsurface(rot_rect).copy()
        root.root.blit(self.rot_, (self.x - root.cx - 50, self.y - root.cy - 50))

    def logic(self, root):
        if self.dead_rot != None:
            return
        if root.im_lose:
            see = False
        else:
            see = True # теперь я эту глебину гадость переписал
            if ((self.y - root.guys[0].y) ** 2 + (self.x - root.guys[0].x) ** 2) ** 0.5 > 2000:

                super().standartlogic(root)

            else:
                stepy = (root.guys[0].y - self.y) // 50
                stepx = (root.guys[0].x - self.x) // 50
                x, y = self.x, self.y
                for i in range(50):
                    x += stepx
                    y += stepy
                    if root.debug:
                        pygame.draw.rect(root.root, (0, 0, 0), (x - root.cx, y - root.cy, 10, 10))
                    if root.map[y // root.bsize][x // root.bsize] != " ":
                        see = False
                        break
        if not see:

            super().standart_logic(root)

        else:
            if self.x - root.guys[0].x == 0:
                self.rot = 90
            else:
                if self.x > root.guys[0].x:
                    self.rot = math.degrees(-math.atan((self.y - root.guys[0].y) / (self.x - root.guys[0].x)))
                else:
                    self.rot = 180 - math.degrees(math.atan((self.y - root.guys[0].y) / (self.x - root.guys[0].x)))
            self.chasing(root, 0, 4)


class ShootgunMan(Guy):
    def __init__(self, x, y, rot, texture):
        super().__init__(x, y, rot, texture)
        self.hide = False
        self.name = "shootgunman"
        self.dead_tx = shootgun_deadTx
        self.bullets = 5
        self.max_force = 100 * easyness // 2
        self.force = self.max_force
        self.rot_ = self.texture
        self.seeT = 0

    def draw(self, root):
        for i in self.appendings:

            if type(i[0]) == type(1):
                root.score += i[0]

                root.cool_texts.append([[root.cool_font.render(str(i[0]), True, (255, 0, 100)), root.cool_but_little_font.render(str(i[0]), True, (10, 0, 10))], self.x - 50, self.y - 50, 10])

                root.guys_killed += 1 # о нет, как же жаль, что это костыль
            elif i[0] == "shootgun":
                root.guns.append(i)
                root.guys_killed += 1
        self.appendings = []

        if root.TIMER % 20 == 0:
            b = self.texture.get_rect()
            self.rot_ = pygame.transform.rotate(self.texture, 90+self.rot)
            rot_rect = b.copy()
            rot_rect.center = self.rot_.get_rect().center
            self.rot_ = self.rot_.subsurface(rot_rect).copy()
        root.root.blit(self.rot_, (self.x - root.cx - 50, self.y - root.cy - 50))

    def logic(self, root):

        if self.dead_rot != None:
            return
        if self.force < self.max_force:
            self.force -= 1
        if self.force < 0:
            self.force = self.max_force
        if root.im_lose:
            see = False
        else:
            see = True  # теперь я эту глебину гадость переписал
            if ((self.y - root.guys[0].y) ** 2 + (self.x - root.guys[0].x) ** 2) ** 0.5 > 1000:
                super().standart_logic(root)

            else:
                stepy = (root.guys[0].y - self.y) // 50
                stepx = (root.guys[0].x - self.x) // 50
                x, y = self.x, self.y
                for i in range(50):
                    x += stepx
                    y += stepy
                    if root.debug:
                        pygame.draw.rect(root.root, (0, 0, 0), (x - root.cx, y - root.cy, 10, 10))
                    if root.map[y // root.bsize][x // root.bsize] != " ":
                        see = False
                        break
        if not see:
            super().standart_logic(root)
        else:
            self.seeT = (self.seeT + 1)
            if self.x - root.guys[0].x == 0:
                self.rot = 90
            elif root.TIMER % 20 == 0:
                if self.x > root.guys[0].x:
                    self.rot = math.degrees(-math.atan((self.y - root.guys[0].y) / (self.x - root.guys[0].x)))
                else:
                    self.rot = 180 - math.degrees(math.atan((self.y - root.guys[0].y) / (self.x - root.guys[0].x)))
            if self.seeT >= 100 and root.TIMER % 2 == 0:
                self.chasing(root, 200, 4)

    def get_lose(self, d):
        self.dead_rot = d
        if self.dead_tx:
            self.texture = self.dead_tx
        # какого то фига он через super() не сравботал (я про get_lose)
        self.appendings.append(['shootgun', self.x - 10, self.y - 10, self.bullets])
        self.appendings.append([1200])

    def shoot(self, root):
        n = randint(0, easyness)
        v = choice(range(-5, 5)) # для рандомизации выстрелов шобы изи было ваще
        if n == 0:
            if self.max_force == self.force and self.bullets > 0:
                root.bad_shoots.extend([Bullet(self.x,
                                               self.y, self.rot + v * easyness - 5, 0
                                               ),
                                       Bullet(self.x,
                                               self.y, self.rot + v * easyness, 0
                                               ),
                                       Bullet(self.x,
                                              self.y, self.rot + v * easyness + 5, 0
                                              )]
                                       )
                self.force -= 1
                self.bullets -= 1
                shootgun_fire.play()
            elif self.bullets <= 0:
                shootgun_empty.play()


    def chasing(self, root, radius, speed=4):
        if root.im_lose:
            return
        if root.debug:
            pygame.draw.circle(root.root, (0, 0, 0), (self.x - root.cx, self.y - root.cy), 20)
        if math.sqrt((root.guys[0].x - self.x) ** 2 + (root.guys[0].y - self.y) ** 2) <= radius:
            self.shoot(root)
        try:
            if check_all_collides([self.x + ((root.guys[0].x - self.x) // abs((root.guys[0].x - self.x))) * speed, self.y + ((root.guys[0].y - self.y) // abs((root.guys[0].y - self.y))) * speed], root.things):
                return
        except:
            pass
        try:
            self.x = self.x + ((root.guys[0].x - self.x) // abs((root.guys[0].x - self.x))) * speed
            self.y = self.y + ((root.guys[0].y - self.y) // abs((root.guys[0].y - self.y))) * speed
        except:
            pass

        

class Game(Window):

    def __init__(self, caption="", defaultcol=(50, 50, 50), map=None, weather=None, level_pack=None):
        self.config = get_settings()
        if level_pack:
            self.level_pack = level_pack
        size = self.config['ROOT_SIZE']
        super().__init__(caption, size, defaultcol)
        self.level_not_done = None
        self.cool_font = pygame.font.Font('shoguns-clan.regular.ttf', 30)
        self.cool_but_little_font = pygame.font.Font('shoguns-clan.regular.ttf', 28)
        self.cool_but_buffer_font = pygame.font.Font('shoguns-clan.regular.ttf', 32)

        punch_sound.set_volume(self.config['SOUND_P'] / 100)
        hit.set_volume(self.config['SOUND_P'] / 100)
        ammo_pickup.set_volume(self.config['SOUND_P'] / 100)
        pistolet_fire.set_volume(self.config['SOUND_P'] / 100)
        shootgun_fire.set_volume(self.config['SOUND_P'] / 100)
        shootgun_empty.set_volume(self.config['SOUND_P'] / 100)
        primo_dead_s.set_volume(self.config['SOUND_P'] / 100)


        self.draw_map_changers = False
        self.draw_teleports = False

        if size[0] / size[1] == 1920 / 1080:

            self.root = pygame.display.set_mode(size, pygame.FULLSCREEN, pygame.SRCALPHA)
        self.RUN_DEM = False
        if not map:
            map = "first_map"
        self.map_name = map

        self.init_level()
        self.font = pygame.font.Font("8bitwonderrusbylyajka_nominal.otf", 30)

    def get_lose(self):
        text = self.font.render("R to restart", True, (255, 255, 255))
        s = pygame.Surface(self.size)
        pygame.draw.rect(s, (200, 0, 100), (0, 0, *self.size))
        s.set_alpha(30)
        self.root.blit(s, (0, 0))
        pygame.draw.rect(self.root, (150, 0, 80), (10, 10, 350, 50))
        self.root.blit(text, (20, 20))
        if self.keys[pygame.K_r]:
            self.init_level() # нахрена?

    def change_map(self, name):
        if name == -1:
            self.WINDOW_RUNNING = False
        else:
            global ROOT
            ROOT = Game(" ", self.size, self.col, map=name)

    def init_level(self):
        f = SourceFileLoader(self.map_name, 'maps/' + self.map_name).load_module()
        self.map = f.MAP
        self.debug = 0
        self.trash = []
        self.rot = 90
        self.bsize = 50
        if not f.SPAWN:
            SPAWN = [0, 0]
        else:
            SPAWN = f.SPAWN
        self.spawn = [SPAWN[0] * self.bsize, SPAWN[1] * self.bsize]
        self.mouse = None
        self.keys = None
        self.m_pressed = -10
        self.texture = mainplTx
        self.guys = [Me(SPAWN[0] * self.bsize, SPAWN[1] * self.bsize, 90, self.texture)]
        self.max_score = 0
        self.all_guys = len(self.guys) - 1
        self.things = []  # surface, mask, weight, pos
        self.RUN_DEM = True
        self.TIMER = 0
        self.cutscenes = []
        self.cutscene = (False, None)  # (флаг выполнения катсцены, генератор новых фреймов (yield))
        self.frame = None
        self.last_script_block = [-100, -100]
        self.text_max = 10
        self.waverot = 0
        self.wavevec = 1
        self.SC_UPDT = 144
        self.last_t = None
        self.bl_mask = None
        # mask_from_blocks(self)  # эта штука на случай, если тебе понадобится маска блока
        self.bl_surf = None
        self.draw_shadows = 1
        self.bl_shad = None
        render_bl(self)
        self.rports = []
        self.bports = []

        if self.level_not_done == 0:
            self.init_music()

        self.level_not_done = 1  # 0 когда мы всех убьем
        self.bad_punch = []
        self.bad_shoots = []
        self.good_punch = []
        self.good_shoots = []
        self.im_lose = 0
        self.dead_rot = None
        self.deads = []
        self.pause = False
        self.cool_texts = []

        self.score = 0
        self.guys_killed = 0
        self.offsety = 100

        self.real_score = 0
        self.score = 0
        self.guys_killed = 0
        self.offsety = 100
        self.doning_inited = 0 # шобы музыка играла и фраер танцевал (бесконечный цикл музыки кстати)


        # self.LOOP_DEAMONS = [SNOW]
        try:
            for i in f.GUYS:
                if i[0] == "gunman":
                    self.guys.append(Normal_bad(i[1], i[2], 90, gunguy))
                elif i[0] == "primat":
                    self.guys.append(El_Primo(i[1], i[2], 90, el_primoTx))
                elif i[0] == "shootgunman":
                    self.guys.append(ShootgunMan(i[1], i[2], 90, shootgun_manTx))
        except:
            pass
        for i in range(1, len(self.guys)):
            if self.guys[i].name == "primat":
                self.max_score += 1000
            elif self.guys[i].name == "gunguy":
                self.max_score += 800
            elif self.guys[i].name == "shootgunman":
                self.max_score += 1200

        try:
            for i in f.THINGS:
                t = pygame.image.load(i[0])
                self.things.append([t, pygame.mask.from_surface(t), i[1], [i[2], i[3]]])
        except:
            pass
        try:
            self.weather = f.WEATHER
        except:
            self.weather = None
        try:
            self.scenes = f.SCENES
        except:
            self.scenes = []
        try:
            self.guns = f.GUNS
        except:
            self.guns = []
        try:
            self.SC_UPDT = f.UPDATE_TIMER
        except:
            pass
        try:
            self.rports = f.RPORTS
            self.bports = f.BPORTS
        except:
            self.rports = []
            self.bports = []
        try:
            self.music = f.MUSIC
        except:
            self.music = None

        try:
            self.map_change = f.MAP_CHANGE
        except:
            self.map_change = []
        try:
            self.exits = f.EXITS
        except:
            self.exits = []

        self.cx, self.cy = 0, 0
        self.undonable = 0

        if len(self.guys) == 1:
            self.undonable = 1

    def loop(self):
        global ROOT
        pygame.mouse.set_visible(False)
        if self.music:
            pygame.mixer.music.load(self.music)
            pygame.mixer.music.play(-1)
    def init_music(self):
        if self.music:
            pygame.mixer.music.load(self.music)
            pygame.mixer.music.play(-1)
            print(self.config["MUSIC_P"])
            pygame.mixer.music.set_volume(self.config["MUSIC_P"] / 100)

    def loop(self):
        self.init_music()
        global ROOT
        pygame.mouse.set_visible(False)

        while self.WINDOW_RUNNING:

            if not self.cutscene[0]:
                for i in pygame.event.get():
                    if i.type == pygame.QUIT:
                        self.RUN_DEM = False
                        quit()

                        # self.WINDOW_RUNNING = False
                    if i.type == pygame.MOUSEBUTTONDOWN:
                        self.m_pressed = i.button
                    if i.type == pygame.MOUSEBUTTONUP:
                        self.m_pressed = -10
                    if i.type == pygame.KEYDOWN:
                        if i.key == pygame.K_ESCAPE:
                            self.pause = not self.pause
                            if self.pause == True:
                                pygame.mixer.music.pause()
                                pygame.mouse.set_visible(True)
                            else:
                                pygame.mixer.music.unpause()
                                pygame.mouse.set_visible(False)

                # self.root.fill((20, 0, 20))
                if self.TIMER % self.SC_UPDT == 0:
                    fill_screen(self, self.weather, 0, 1)
                else:
                    fill_screen(self, self.weather, 0)
                self.mouse = pygame.mouse.get_pos()
                self.keys = pygame.key.get_pressed()
                show_map(self.root, self.bl_surf, (self.cx, self.cy)) # карта
                if self.draw_shadows and self.bl_shad:
                    show_map(self.root, self.bl_shad, (self.cx, self.cy)) # тени

                show_things(self.root, self.things, [self.cx, self.cy])

                teleport(self)
                for mc in self.map_change:
                    if self.draw_map_changers:
                        pygame.draw.rect(self.root, (0, 0, 0), (mc[1] * self.bsize - self.cx, mc[2] * self.bsize - self.cy, self.bsize, self.bsize))
                    if self.guys[0].x // self.bsize == mc[1] and self.guys[0].y // self.bsize == mc[2]:
                        self.WINDOW_RUNNING = False
                        ROOT = Game(map=mc[0])
                        ROOT.loop()
                if self.draw_teleports:
                    draw_ports(self)
                for guy in self.deads:
                    guy.draw(self)

                if len(self.guys) == 1 and not self.undonable:
                    self.level_not_done = 0

                draw_trash(self)

                show_guns(self, self.guns)

                for guy in self.guys:
                    if not self.pause:
                        guy.logic(self)
                    guy.draw(self)
                if not self.pause:
                    draw_punches(self)
                    draw_shoots(self)

                if self.TIMER % 30 == 0:
                    show_weather(self, self.map, self.weather, 15)
                else:
                    show_weather(self, self.map, self.weather, 15, 0)

                draw_cool_texts(self)

                for th in self.things:
                    check_collide([self.guys[0].x, self.guys[0].y], th)

                if self.im_lose:
                    self.get_lose()

                draw_interface(self)

                if self.level_not_done == 0:
                    text = self.font.render("go to car", True, (255, 255, 255))
                    pygame.draw.rect(self.root, (200, 0, 100), (10, 10, 300, 50))
                    self.root.blit(text, (20, 20))

                    if self.doning_inited == 0:

                        pygame.mixer.music.stop()
                        pygame.mixer.music.load("080123.wav")
                        pygame.mixer.music.play(-1)
                        self.doning_inited = 1

                    for ex in self.exits:
                        if ex[0] == self.guys[0].x // self.bsize and ex[1] == self.guys[0].y // self.bsize:
                            self.WINDOW_RUNNING = False
                            from end_screen import End_screen
                            ROOT = End_screen(self.score, self.max_score, self.guys_killed, self.all_guys, 0, self.map_name, level_pack=self.level_pack)
                            ROOT.loop()

                for s in self.scenes:
                    if s[1] == self.guys[0].x // self.bsize and s[2] == self.guys[0].y // self.bsize and s[1] != self.last_script_block[0] and s[2] != self.last_script_block[1]:

                        ss = SourceFileLoader(s[0], 'cutscenes/' + s[0]).load_module().SCRIPT
                        t = []
                        im = []
                        p = []
                        for j in ss:
                            t.append(j[0])
                            im.append(j[1])
                            p.append(j[2])
                        new = Cutscene(t, im, p)
                        ids = 1

                        self.cutscenes.append(new)
                        self.last_script_block = [self.guys[0].x // self.bsize, self.guys[0].y // self.bsize]
                        self.cutscenes = list(set(self.cutscenes))

                        self.cutscene_begun(0)

                        self.scenes.remove(s)

            else:

                for i in pygame.event.get():
                    if i.type == pygame.QUIT:
                        self.RUN_DEM = False
                        quit()
                        # self.WINDOW_RUNNING = False
                    if i.type == pygame.MOUSEBUTTONDOWN:
                        self.frame = next(self.cutscene[1], None)
                        if self.TIMER % 144 == 0:
                            fill_screen(self, self.weather, 0, 1)

                        else:
                            fill_screen(self, self.weather, 0)
                        self.mouse = pygame.mouse.get_pos()
                        self.keys = pygame.key.get_pressed()
                        show_map(self.root, self.bl_surf, (self.cx, self.cy))
                        if self.draw_shadows and self.bl_shad:
                            show_map(self.root, self.bl_shad, (self.cx, self.cy))  # тени
                        show_things(self.root, self.things, [self.cx, self.cy])

                        for guy in self.guys:
                            guy.draw(self)
                        for th in self.things:
                            check_collide([self.guys[0].x, self.guys[0].y], th)
                        for guy in self.deads:
                            guy.draw(self)

                        show_guns(self, self.guns)
                        if self.TIMER % 30 == 0:
                            show_weather(self, self.map, self.weather, 15)
                        elif self.TIMER % 2 == 0:
                            show_weather(self, self.map, self.weather, 15, 0)

                if self.frame != None:

                    if self.frame[2] == "r":
                        pygame.draw.rect(self.root, (255, 255, 255),
                                         (self.size[0] // 3 * 2 - 2, 0, self.size[0] // 3 * 2 + 2, self.size[1]))
                        pygame.draw.rect(self.root, (0, 0, 0),
                                     (self.size[0] // 3 * 2 + 3, 0, self.size[0], self.size[1]))

                        b = self.frame[1].get_rect()
                        rot = pygame.transform.rotate(self.frame[1], self.waverot)
                        rot_rect = b.copy()
                        rot_rect.center = rot.get_rect().center
                        rot = rot.subsurface(rot_rect).copy()
                        self.root.blit(rot, (self.size[0] // 6 * 5 - 40, self.size[1] // 3)) # картинка
                        texty = self.size[1] // 3 * 2
                        for texts in self.frame[0]:

                            self.root.blit(texts, (self.size[0] // 3 * 2 + 10, texty)) # текста
                            texty += 30
                    else:
                        pygame.draw.rect(self.root, (255, 255, 255),
                                     (0, 0, self.size[0] // 3 + 5, self.size[1]))
                        pygame.draw.rect(self.root, (0, 0, 0),
                                     (0, 0, self.size[0] // 3, self.size[1]))
                        b = self.frame[1].get_rect()
                        rot = pygame.transform.rotate(self.frame[1], self.waverot)
                        rot_rect = b.copy()
                        rot_rect.center = rot.get_rect().center
                        rot = rot.subsurface(rot_rect).copy()
                        self.root.blit(rot, (0, self.size[1] // 3))
                        texty = self.size[1] // 3 * 2
                        for texts in self.frame[0]:

                            self.root.blit(texts, (10, texty))
                            texty += 30
                else:
                    self.cutscene_end()
                    self.last_script_block = [-100, -100]

            if self.pause:
                draw_pause_interface(self)

            if self.TIMER % 15 == 0:
                self.waverot += 1 * self.wavevec
                if abs(self.waverot) >= 15:
                    self.wavevec *= -1
                self.bl_shad.set_alpha(self.waverot + 30)
            self.DISPLAY_NEED_TO_BE_FLIPED = 1
            if self.TIMER % 2 == 0:
                pygame.display.update()
            self.clock.tick(144)
            self.TIMER = (self.TIMER + 1) % 60
            self.DISPLAY_NEED_TO_BE_FLIPED = 0

    def cutscene_begun(self, num):
        self.cutscene = (True, self.cutscenes[num].play())
        self.frame = next(self.cutscene[1], None)

    def cutscene_end(self):
        self.cutscene = (False, None)
        self.frame = None

