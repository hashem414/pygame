import pygame
import pygame.sprite

is_flying = False
is_game_over = False


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 3):
            img = pygame.image.load(f'Images/pngwing{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False
        self.died_image = pygame.image.load('Images/pngwing3.png')  # Load the died bird image
        self.is_dead = False

    def update(self):
        global is_flying, is_game_over
        if is_flying:
            # gravity
            self.vel += 0.7
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 784:
                self.rect.y += int(self.vel)

        if is_game_over is False:
            # jump
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked is False:
                self.clicked = True
                self.vel = -10
                is_flying = True  # Set is_flying to True when the bird jumps

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            # handle the animation
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            # rotate the bird
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)

    def on_hit(self):
        self.is_dead = True
        self.image = self.died_image
