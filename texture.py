import pygame


class Texture:
    def __init__ (self, source, scale, place, rot=0, alpha=20, color=None):
        if type(source) == type("bulochka"):
            self.txt = pygame.image.load(source)
        else:
            self.txt = source
        
        self.scale = scale
        self.p = place
        self.rot = rot
        self.alpha = alpha
        self.col = color
        if color:
            self.set_col(self.col)

        self.txt = pygame.transform.scale(self.txt, self.scale)
        #self.txt.set_alpha(self.alpha)
    
    def resize(self, x, y):
        self.scale = (x, y)
        self.txt = pygame.transform.scale(self.txt, self.scale)
    
    def set_alpha(self, alpha):
        self.alpha = alpha
        self.txt.set_alpha(alpha)
    
    def set_col(self, col):
        w, h = self.txt.get_size()
        for x in range(w):
            for y in range(h):
                r = self.txt.get_at((x, y))[0]

                g = self.txt.get_at((x, y))[1]

                b = self.txt.get_at((x, y))[2]

                a = self.txt.get_at((x, y))[3]
                
                self.txt.set_at((x, y), pygame.Color(*col, a)) 
    
    def set_coord(self, p):
        self.p = p
    
    def blit(self, root, cam=None):
        if not cam:
            root.root.blit(self.txt, self.p)
        else:
            root.root.blit(self.txt, (self.p[0] - cam[0], self.p[1] - cam[1
             ]))
