import pygame
import random
import sys

pygame.init()
pygame.mixer.init()

WIDTH = 900
HEIGHT = 600
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Звёздная схватка")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 70, 70)
YELLOW = (255, 220, 50)

rocket_image = pygame.image.load("pngwing.com (2).png").convert_alpha()
rocket_image = pygame.transform.scale(rocket_image, (70, 90))

rocket_rect = rocket_image.get_rect()
rocket_rect.x = WIDTH // 2 - 35
rocket_rect.y = HEIGHT - 120

enemy_image = pygame.image.load("pngwing.com.png").convert_alpha()
enemy_image = pygame.transform.scale(enemy_image, (60, 60))

start_image = pygame.image.load("start.jpg")
start_image = pygame.transform.scale(start_image, (WIDTH, HEIGHT))

play_image = pygame.image.load("play.png").convert_alpha()
play_image = pygame.transform.scale(play_image, (130, 130))

play_rect = play_image.get_rect()
play_rect.center = (WIDTH // 2, HEIGHT // 2 + 100)

victory_image = pygame.image.load("victory_background.jpg")
victory_image = pygame.transform.scale(victory_image, (WIDTH, HEIGHT))

gameover_image = pygame.image.load("gameover_background.jpg")
gameover_image = pygame.transform.scale(gameover_image, (WIDTH, HEIGHT))

font = pygame.font.Font("start_font.ttf", 28)
small_font = pygame.font.Font("start_font.ttf", 18)

laser_sound = pygame.mixer.Sound("laser.mp3")
victory_sound = pygame.mixer.Sound("victory_music.mp3")
gameover_sound = pygame.mixer.Sound("gameover_music.mp3")

laser_sound.set_volume(0.3)
victory_sound.set_volume(0.6)
gameover_sound.set_volume(0.6)

pygame.mixer.music.load("game_music.mp3")
pygame.mixer.music.set_volume(0.25)

rocket_speed = 5
laser_speed = 10
enemy_speed = 3

lasers = []
enemies = []

score = 0
lives = 3

stars = []

for i in range(100):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    size = random.randint(1, 3)
    speed = random.randint(2, 6)

    stars.append([x, y, size, speed])


def draw_space():
    screen.fill(BLACK)

    for star in stars:
        star[1] = star[1] + star[3]

        if star[1] > HEIGHT:
            star[1] = 0
            star[0] = random.randint(0, WIDTH)

        pygame.draw.circle(
            screen,
            WHITE,
            (star[0], star[1]),
            star[2]
        )


def show_start_screen():
    menu = True

    while menu:
        screen.blit(start_image, (0, 0))
        screen.blit(play_image, play_rect)

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if play_rect.collidepoint(event.pos):
                    menu = False

        clock.tick(FPS)


pygame.time.set_timer(pygame.USEREVENT, 1400)

show_start_screen()

pygame.mixer.music.play(-1)

running = True

while running:
    clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:

                laser = pygame.Rect(
                    rocket_rect.centerx - 3,
                    rocket_rect.top,
                    6,
                    25
                )

                lasers.append(laser)
                laser_sound.play()

        if event.type == pygame.USEREVENT:

            enemy = enemy_image.get_rect()

            enemy.x = random.randint(
                0,
                WIDTH - enemy.width
            )

            enemy.y = -60

            enemies.append(enemy)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        rocket_rect.x = rocket_rect.x - rocket_speed

    if keys[pygame.K_RIGHT]:
        rocket_rect.x = rocket_rect.x + rocket_speed

    if keys[pygame.K_UP]:
        rocket_rect.y = rocket_rect.y - rocket_speed

    if keys[pygame.K_DOWN]:
        rocket_rect.y = rocket_rect.y + rocket_speed

    if rocket_rect.left < 0:
        rocket_rect.left = 0

    if rocket_rect.right > WIDTH:
        rocket_rect.right = WIDTH

    if rocket_rect.top < 50:
        rocket_rect.top = 50

    if rocket_rect.bottom > HEIGHT:
        rocket_rect.bottom = HEIGHT

    for laser in lasers[:]:
        laser.y = laser.y - laser_speed

        if laser.bottom < 0:
            lasers.remove(laser)

    for enemy in enemies[:]:
        enemy.y = enemy.y + enemy_speed

        if enemy.top > HEIGHT:
            enemies.remove(enemy)
            lives = lives - 1

    for laser in lasers[:]:

        for enemy in enemies[:]:

            if laser.colliderect(enemy):
                score = score + 1
                print("Так держать!")

                lasers.remove(laser)
                enemies.remove(enemy)

                break

    for enemy in enemies[:]:

        if enemy.colliderect(rocket_rect):
            enemies.remove(enemy)
            lives = lives - 1

    draw_space()

    screen.blit(rocket_image, rocket_rect)

    for enemy in enemies:
        screen.blit(enemy_image, enemy)

    for laser in lasers:
        pygame.draw.rect(
            screen,
            RED,
            laser
        )

    score_text = font.render(
        "Очки: " + str(score),
        True,
        WHITE
    )

    screen.blit(score_text, (10, 550))

    lives_text = font.render(
        "Жизни: " + str(lives),
        True,
        YELLOW
    )

    screen.blit(lives_text, (10, 510))

    rule_text = small_font.render(
        "Набери 20 очков | SPACE - выстрел",
        True,
        WHITE
    )

    screen.blit(rule_text, (250, 20))

    pygame.display.flip()

    if score >= 20:
        pygame.mixer.music.stop()
        victory_sound.play()

        screen.blit(victory_image, (0, 0))
        pygame.display.flip()

        pygame.time.delay(5000)

        running = False

    if lives <= 0:
        pygame.mixer.music.stop()
        gameover_sound.play()

        screen.blit(gameover_image, (0, 0))
        pygame.display.flip()

        pygame.time.delay(3000)

        running = False

pygame.quit()
sys.exit()
