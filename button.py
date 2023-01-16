import pygame

class Button:
    def __init__(self, root=None, text="ты не назвал меня", function=None, args = [], coords=(0, 0), size=(100, 50), fsize=15, font=None, color=(255, 255, 255), fcolor=(255, 255, 255), border=0):
        self.root = root
        self.text = text
        self.function = function
        self.args = args
        self.coords = coords
        self.size = size
        self.fsize = fsize
        self.font = font
        self.color = color
        self.fcolor = fcolor
        self.border = border
        self.t = self.font.render(self.text, True, self.fcolor)
        self.ts = self.font.render(self.text, True, (200, 0, 50))
    
    def place(self, p=None, borders=0):
        if self.border:
            pygame.draw.rect(self.root, self.fcolor, (self.coords[0] - self.border, self.coords[1] - self.border, self.size[0] + self.border * 2, self.size[1] * self.border * 2))
        if borders:
            pygame.draw.rect(self.root, self.color, (*self.coords, *self.size))

        self.root.blit(self.t, (self.coords[0], self.coords[1]))
        if p:
            if p[0] >= self.coords[0] and p[1] >= self.coords[1]:
                if p[0] <= self.coords[0] + self.size[0] and p[1] <= self.coords[1] + self.size[1]:
                    self.function(*self.args)

    def set_text(self, n):
        self.text = n
        self.t = self.font.render(self.text, True, self.fcolor)
        self.ts = self.font.render(self.text, True, (200, 0, 50))

