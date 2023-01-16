
from deamon import Deamon
from texture import Texture
from random import randint
import pygame
import time

BG_COLORS = [
    (50, 0, 150),
    (200, 200, 255),
    (100, 100, 150),
    (0, 0, 150),
    (0, 0, 255)
]

I = BG_COLORS[0]
IND = 0
step = 30
IT = 0 # iteration

def animate_bg(root):
    global IND
    global IT
    global I
    SPEED = [((-BG_COLORS[IND][0] + BG_COLORS[((IND + 1) % len(BG_COLORS))][0]) // step),
        ((-BG_COLORS[IND][1] + BG_COLORS[((IND + 1) % len(BG_COLORS))][1]) // step),
        ((-BG_COLORS[IND][2] + BG_COLORS[((IND + 1) % len(BG_COLORS))][2])) // step]
    
    I = (int(I[0] + SPEED[0]) % 255,
        int(I[1] + SPEED[1]) % 255,
        int(I[2] + SPEED[2]) % 255
    )
    IT += 1

    if IT == step:
        IT = 0
        IND = (IND + 1) % len(BG_COLORS)
        I = BG_COLORS[IND]
    root.col = I
    print(I)

def smoke(root, size):
    t = Texture("smoke.png", size, (30, 30), color=(200, 0, 0))
    t.set_col((255 - I[0], 255 - I[1], 255 - I[2]))
    t.set_alpha(50)

    t.blit(root)

def particle(root, N=10):
    parts = []
    bsize = root.bsize
    snow_blocks = []

    timer = 0
    for y in range(0, len(root.map)):
        for x in range(0, len(root.map[0])):
            if root.map[y][x] in ["N"]:
                snow_blocks.append([y, x])
    snow_parts = [] 

    while 1:
        if timer % 30 == 0:
            for i in range(0, len(snow_blocks)):
                n = []
                for j in range(N):
                    n.append([randint(x * bsize, (x + 1) * bsize), randint(y * bsize, (y + 1) * bsize)])
                snow_parts += n
            timer = 0
        for i in snow_parts:
            pygame.draw.rect(root.root, (255, 255, 255), [i[1], i[2], 2, 2])
            print(i)
        timer += 1
BG = Deamon(animate_bg, 0)
SNOW = Deamon(particle, 1)
SMOKE = Deamon(smoke, 0, ['SIZE'])
