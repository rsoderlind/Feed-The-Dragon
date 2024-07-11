#import pygame
import pygame, random

#initialize pygame
pygame.init()

#set display surface
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 500

display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("Feed the Dragon!")

#set clock
FPS = 60
clock = pygame.time.Clock()

#set game values
VELOCITY = 5

#PLAYER_STARTING_LIVES = 1
PLAYER_VELOCITY = 5
COIN_STARTING_VELOCITY = 5
COIN_ACCELERATION = 3
BUFFER_DISTANCE = 100

score = 0
player_lives = 2
coin_velocity = COIN_STARTING_VELOCITY

#set colors
GREEN = (0, 255, 0)
DARKGREEN = (10, 50, 10)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#set fonts
font = pygame.font.Font("AttackGraffiti.ttf", 32)

#set text
score_text = font.render("Score: " + str(score), True, GREEN, DARKGREEN)
score_rect = score_text.get_rect()
score_rect.topleft = (10, 10)

title_text = font.render("Feed the Dragon!", True, GREEN, WHITE)
title_rect = title_text.get_rect()
title_rect.centerx = (WINDOW_WIDTH//2)
title_rect.y = 10

lives_text = font.render("Lives: " + str(player_lives), True, GREEN, DARKGREEN)
lives_rect = lives_text.get_rect()
lives_rect.topright = (WINDOW_WIDTH - 10, 10)

game_over_text = font.render("Game Over!", True, GREEN, DARKGREEN)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

continue_text = font.render("Press any key to continue!", True, GREEN, DARKGREEN)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT - 200)

#set sounds and music
coin_sound = pygame.mixer.Sound("coin_sound.wav")
miss_sound = pygame.mixer.Sound("miss_sound.wav")
miss_sound.set_volume(.1)

#background music
pygame.mixer.music.load("ftd_background_music.wav")

player_image = pygame.image.load("dragon_right.png")
player_rect = player_image.get_rect()
player_rect.left = 32
player_rect.centery = WINDOW_HEIGHT//2

coin_image = pygame.image.load("coin.png")
coin_rect = coin_image.get_rect()
coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
coin_rect.y = random.randint(64, WINDOW_HEIGHT - 32)

#play music
pygame.mixer.music.play()

#main game loop
running = True
while running:
    #check to see if user wants to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #set running to false
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_rect.top > 64:
        player_rect.y -= VELOCITY

    if keys[pygame.K_DOWN] and player_rect.bottom < WINDOW_HEIGHT:
        player_rect.y += VELOCITY

    if coin_rect.x < 1:
        player_lives -= 1
        print(player_lives)
        print(score)
        coin_rect.x += WINDOW_WIDTH + BUFFER_DISTANCE
        coin_rect.y = random.randint(64, WINDOW_HEIGHT - 32)
        miss_sound.play()

    else:
        #move the coin
        coin_rect.x -= coin_velocity

    if player_rect.colliderect(coin_rect):
        score += 1
        coin_sound.play()
        coin_velocity += COIN_ACCELERATION
        coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
        coin_rect.y = random.randint(64, WINDOW_HEIGHT - 32)

        #update HUD
        score_text = font.render("Score: " + str(score), True, GREEN, DARKGREEN)

    if player_lives == 0 or player_lives < 0:
        lives_text = font.render("Lives " + str(player_lives), True, GREEN, DARKGREEN)
        display_surface.blit(lives_text, lives_rect)
        display_surface.blit(continue_text, continue_rect)
        display_surface.blit(game_over_text, game_over_rect)
        pygame.display.update()

        #pause the game until player presses a key
        pygame.mixer.music.stop()
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    score =0
                    player_lives = 2
                    player_rect.y = WINDOW_HEIGHT//2
                    coin_velocity = COIN_STARTING_VELOCITY
                    pygame.mixer.music.play(-1, 0.0)
                    is_paused = False
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False
    #update HUD
    score_text = font.render("Score: " + str(score), True, GREEN, DARKGREEN)
    lives_text = font.render("Lives " + str(player_lives), True, GREEN, DARKGREEN)

    display_surface.fill(BLACK)

    #blit HUD to screen
    display_surface.blit(score_text, score_rect)
    display_surface.blit(title_text, title_rect)
    display_surface.blit(lives_text, lives_rect)

    pygame.draw.line(display_surface, WHITE, (0, 64), (WINDOW_WIDTH, 64), 2)

    #blit assets
    display_surface.blit(player_image, player_rect)
    display_surface.blit(coin_image, coin_rect)

    #update display
    pygame.display.update()
    clock.tick(FPS)

#quit game
pygame.quit()


