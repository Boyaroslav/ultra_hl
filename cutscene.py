import pygame
class Cutscene:
    def __init__(self, texts=[], images=[], pos="r", text_max=10):
        self.frames = []
        self.text_max = text_max
        self.font = pygame.font.SysFont('monospace', 30)

        for i in range(len(texts)):
            self.frames.append([texts[i], images[i], pos[i]])

    def splt(self, stri, max=10):  # великая функция глебикса
        stringg = stri
        res = []
        while len(stringg) >= max:
            res.append(stringg[:max])
            stringg = stringg[max:]
        if stringg:
            res.append(stringg)
        return res

    def play(self):
        for i in self.frames:
            t = self.splt(i[0], self.text_max)

            for j in range(0, len(t)):
                t[j] = self.font.render(t[j], True, (255, 255, 255))
            yield (t, pygame.image.load(i[1]), i[2])