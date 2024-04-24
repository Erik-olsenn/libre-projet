import pygame, sys
from pygame.locals import *
from pygame import mixer 
import subprocess
import time, os

mainClock = pygame.time.Clock()

pygame.init()
mixer.init()
pygame.display.set_caption("Menu")

screen = pygame.display.set_mode((500, 500), 0, 32)
font, small_font = pygame.font.Font("fonts/ARCADECLASSIC.ttf", 52), pygame.font.Font("fonts/ARCADECLASSIC.ttf", 16)
mixer.music.load("sounds/music.ogg")
mixer.music.set_volume(0.7) 

IMAGE_1 = pygame.image.load("images/menu_bird_1.png").convert_alpha()
IMAGE_2 = pygame.image.load("images/menu_bird_2.png").convert_alpha()
BG = pygame.image.load("images/background.png")

playing = False
paused = False

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def button(x, y, width, height, color_1, color_2, img_1, img_2, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    rect = pygame.Rect(x, y, width, height)
    on_button = rect.collidepoint(mouse)

    if on_button:
        pygame.draw.rect(screen, color_2, rect)
        screen.blit(img_2, img_2.get_rect(center = rect.center))
    else:
        pygame.draw.rect(screen, color_1, rect)
        screen.blit(img_1, img_1.get_rect(center = rect.center))

    if on_button:
        if click[0] == 1 and action != None:
            action()

def music():
    global paused, playing
    if not(playing):
        mixer.music.play(-1) 
        playing = True
    else:
        if not(paused):
            mixer.music.pause()
            paused = True
        else:
            mixer.music.unpause()
            paused = False

def play_spacebird():
    subprocess.Popen(["python", "game.py"])
    pygame.quit()
    sys.exit(0)


def main_menu():
    while True:
        screen.blit(BG, (0, 0))
        draw_text("main menu / NEAT", font, (255, 255, 255), screen, 20, 20)
        draw_text("Copyright © 2024 Erik Olsen, v 1", small_font, (255, 255, 255), screen, 20, 460)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        
        button(20, 100, 96, 96, "red", "blue", IMAGE_1, IMAGE_2, play_spacebird)
        button(20, 220, 96, 96, "red", "blue", pygame.image.load("images/coming_soon_1.png").convert_alpha(), pygame.image.load("images/coming_soon_2.png").convert_alpha())
        button(20, 340, 96, 96, "red", "blue", pygame.image.load("images/coming_soon_1.png").convert_alpha(), pygame.image.load("images/coming_soon_2.png").convert_alpha())
        button(430, 430, 50, 50, "red", "blue", pygame.image.load("images/sound_menu_1.png").convert_alpha(), pygame.image.load("images/sound_menu_2.png").convert_alpha(), music)
        pygame.display.update()
        mainClock.tick(15)



main_menu()