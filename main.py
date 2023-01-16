import pygame
import threading
from deamon import Deamon
from shaders import *

from menu import *
pygame.init()
import os
os.environ['SDL_VIDEO_CENTERED'] = '1'
os.environ['SDL_VIDEO_WINDOW_POS'] = '{},{}'.format(100,200)

ROOT = None

pygame.init()

if __name__ == "__main__":
    pygame.mouse.set_visible(True)
    ROOT = Main()
    ROOT.loop()