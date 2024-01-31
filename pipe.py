import pygame

scroll_speed = 8

pipe_gap = 200

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Images/long-pipe.png')
        self.rect = self.image.get_rect()
        self.gap_top = y + int(pipe_gap / 2)
        self.gap_bottom = y - int(pipe_gap / 2)


        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()
