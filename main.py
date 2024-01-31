import pygame
from pygame.locals import *
import random
from button import *
from bird import *
from pipe import *
import pygame.mixer

pygame.init()
died_bird = pygame.image.load('Images/pngwing3.png')
clock = pygame.time.Clock()
fps = 200

screen_width = 720
screen_height = 900

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Wing Jump')

# define font
font = pygame.font.SysFont('Verdana', 70)

# define colours
violet = (238, 130, 238, 255)

# define game variables
ground_scroll = 0
scroll_speed = 8
is_flying = False
is_game_over = False
pipe_gap = 140
pipe_frequency = 2000  # milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False
chances = 3

# load sounds
hit_sound = pygame.mixer.Sound('audio/hit_sound.mpeg')
die_sound = pygame.mixer.Sound('audio/die.mp3')
bg_sound = pygame.mixer.Sound('audio/bgsound.mp3')
score_sound = pygame.mixer.Sound('audio/point.mp3')

# set sound volumes
hit_sound.set_volume(0.5)
die_sound.set_volume(0.5)
bg_sound.set_volume(0.3)
score_sound.set_volume(0.3)

# load images
bg = pygame.image.load('Images/backgroundsk.png')
ground_img = pygame.image.load('Images/backgroundgr.png')
button_img = pygame.image.load('Images/Gameover.jpg')
heart_img = pygame.image.load('Images/one heart.png')
heart_x = 10
heart_y = 10

# play background sound
pygame.mixer.music.load('audio/bgsound.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def draw_hearts(chances):
    for i in range(chances):
        screen.blit(heart_img, (heart_x + i * (heart_img.get_width() + 10), heart_y))


def reset_game():
    global score, scroll_speed
    pipe_group.empty()
    flappy.rect.x = 150
    flappy.rect.y = int(screen_height / 2)
    score = 0
    scroll_speed = 8
    return score


bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2))

bird_group.add(flappy)

# create restart button instance
button = Button(screen_width // 2 - 50, screen_height // 2 - 100, button_img)

run = True
while run:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Left mouse button is pressed
            if not is_game_over and not is_flying:
                is_flying = True


    # draw background
    screen.blit(bg, (0, 0))

    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)

    # draw the ground
    screen.blit(ground_img, (ground_scroll, 750))
    screen.blit(ground_img, (ground_scroll + 576, 750))

    # check the score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left \
                and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right \
                and pass_pipe is False:
            pass_pipe = True
        if pass_pipe is True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False
                score_sound.play()

    draw_text(str(score), font, violet, int(screen_width / 2), 20)
    draw_hearts(chances)

    # look for collision
    bird_collides_with_pipes = pygame.sprite.spritecollide(flappy, pipe_group, False)

    if bird_collides_with_pipes:
        for pipe in bird_collides_with_pipes:
            if flappy.rect.colliderect(pipe.rect) and not pipe.gap_bottom < flappy.rect.centery < pipe.gap_top:
                chances -= 1
                hit_sound.play()
                if chances == 0:
                    is_game_over = True
                    die_sound.play()
                else:
                    flappy.rect.x = 100
                    flappy.rect.y = int(screen_height / 2)

    # check if bird has hit the ground
    if flappy.rect.bottom >= 765:
        if chances > 0:
            chances -= 1
            flappy.rect.x = 100
            flappy.rect.y = int(screen_height / 2)
            hit_sound.play()
        else:
            is_game_over = True
            is_flying = False
            die_sound.play()

    if is_game_over is False and is_flying is True:
        # generate new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

    if flappy.rect.top <= 0:
        if chances > 0:
            chances -= 1
            flappy.rect.x = 100
            flappy.rect.y = int(screen_height / 2)
            hit_sound.play()
        else:
            is_game_over = True
            is_flying = False
            die_sound.play()

    ground_scroll -= scroll_speed
    if abs(ground_scroll) >= 576:
        ground_scroll = 0
    pipe_group.update()

    # check for game over and reset
    if is_game_over:
        if button.draw(screen):
            is_game_over = False
            score = reset_game()
            chances = 3
            ground_scroll = 0
            pipe_group.empty()
            pass_pipe = False
            flappy.is_dead = False
        else:
            is_flying = False
            scroll_speed = 0
            screen.blit(died_bird,(flappy.rect.x,flappy.rect.y))

    # check for click to start flying
    if not is_flying and not is_game_over:
        click = pygame.mouse.get_pressed()
        if click[0] == 1:
            is_flying = True

    pygame.display.update()

pygame.quit()
