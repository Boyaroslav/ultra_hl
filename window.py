import pygame
import threading

class Window:
    def __init__(self, caption="", size=(800, 600), defaultcol=(50, 50, 50)):
        self.LOOP_DEAMONS = []
        self.root = pygame.display.set_mode(size)
        self.size = size
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(caption)
        self.col = defaultcol
        self.WINDOW_RUNNING = True
        self.RUN_DEM = True

    def root_info(self, need):
        values = {
            'SIZE': self.size,
            'COLOR': self.col
        }
        new = []
        for i in range(0, len(need)):
            new.append(values[need[i]])
        return new
    
    def loop(self):

        while self.WINDOW_RUNNING:
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    quit()
            self.root.fill(self.col)
            for d in self.LOOP_DEAMONS:
                darr = self.root_info(d.keys)
                if d.is_async:
                    n = threading.Thread(target=d.run, args=(self, darr,))
                    del d
                else:
                    d.run(self, darr)
    
            pygame.display.update()
            self.clock.tick(60)