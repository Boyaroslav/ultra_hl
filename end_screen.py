from window import Window
import pygame
from game import Game

class End_screen(Window):
    def __init__(self, pl_score, max_score, bads_killed ,bads_count, time, map_name, caption="", size=(1920, 1080), defaultcol=(50, 50, 50), level_pack = []):
        super().__init__(caption, size, defaultcol)
        self.pl_score = pl_score
        self.max_score = max_score
        self.bads_killed = bads_killed
        self.bads_cound = bads_count
        self.time = time
        self.map_name = map_name
        self.font = pygame.font.Font("8bitwonderrusbylyajka_nominal.otf", 60)
        self.cool_font = pygame.font.Font('shoguns-clan.regular.ttf', 60)
        self.cool_but_buffer_font = pygame.font.Font('shoguns-clan.regular.ttf', 64)
        if level_pack:
            self.level_pack = level_pack
        else:
            self.level_pack = None
        try:
            self.next_level = level_pack[level_pack.index(map_name) + 1]
        except:
            self.next_level = None

    def loop(self):
        score = 0
        guys_killed = 0
        color = (200, 0, 130)
        cool_color = (200, 200, 0)
        exit_b = 0
        TIMER = 0
        rot = -90
        waverot = 0
        wavevec = 1

        global ROOT
        while self.WINDOW_RUNNING:
            mapt = self.cool_font.render(self.map_name[:self.map_name.rfind('.')], True, cool_color)
            maptt = self.cool_but_buffer_font.render(self.map_name[:self.map_name.rfind('.')], True, (0, 0, 0))
            surf = pygame.Surface((self.size[1], self.size[1]))

            self.root.fill((0, 0, 0))
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    quit()
                if i.type == pygame.MOUSEBUTTONDOWN:
                    if exit_b and not self.next_level:
                        from menu import Main

                        self.WINDOW_RUNNING = False
                        ROOT = Main()
                        ROOT.loop()

                    if score < self.pl_score:
                        score = self.pl_score
                    elif guys_killed < self.bads_killed:
                        guys_killed = self.bads_killed
                if i.type == pygame.KEYDOWN and self.next_level:
                    if i.key == pygame.K_SPACE:
                        self.WINDOW_RUNNING = False

                        if self.level_pack:
                            ROOT = Game(map=self.next_level, level_pack=self.level_pack)
                        else:
                            ROOT = Game(map=self.next_level)
                        ROOT.loop()
                    elif i.key == pygame.K_ESCAPE:
                        from menu import Main

                        self.WINDOW_RUNNING = False
                        ROOT = Main()
                        ROOT.loop()
            surf.blit(maptt, (self.size[0] // 6, self.size[1] // 12 - 50))
            surf.blit(mapt, (self.size[0] // 6 - 2, self.size[1] // 12 - 52))
            if score == self.pl_score:
                sct = self.font.render(f"{score}  //  {self.max_score}", True, color)
            else:
                sct = self.font.render(str(score), True, color)
            surf.blit(sct, (self.size[0] // 6, self.size[1] // 12 + 50))
            if score == self.pl_score:
                guys_t = self.font.render(f"{guys_killed}  //  {self.bads_killed}", True, color)
                surf.blit(guys_t, (self.size[0] // 6, self.size[1] // 12 + 150))
            if guys_killed == self.bads_killed:
                if not self.next_level:
                    ex = self.cool_font.render("Press any button to exit", True, cool_color)
                    surf.blit(ex, (self.size[0] // 6, self.size[1] // 12 + 450))
                    exit_b = True
                else:
                    ex = self.cool_font.render("space to next level or escape to exit", True, cool_color)
                    surf.blit(ex, (self.size[0] // 6, self.size[1] // 12 + 450))


            if score < self.pl_score:
                score += 1
            elif guys_killed < self.bads_killed:
                guys_killed += 1
            b = surf.get_rect()
            rot_ = pygame.transform.rotate(surf.copy(), 90+rot + waverot)
            rot_rect = b.copy()
            rot_rect.center = rot_.get_rect().center
            surf_ = rot_.subsurface(rot_rect).copy()
            self.root.blit(surf_, (0, 0))

            TIMER = (TIMER + 1) % 600
            if TIMER % 20 == 0:


                waverot += 1 * wavevec
                if abs(waverot) >= 2:
                    wavevec *= -1


            self.clock.tick(60)
            pygame.display.update()