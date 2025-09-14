import pygame
import functions
import random

from const import *
from global_var import *

def image(og,size,crop_area=None,angle=None,zoom=None,alpha=None):
    new_image=pygame.Surface(size).convert_alpha()
    new_image.fill((0,0,0,0))
    if crop_area:
        new_image.blit(og,(0,0),crop_area)
    else:
        new_image.blit(og,(0,0))
    if zoom:
        new_image=pygame.transform.smoothscale(new_image,zoom)
    if angle:
        new_image=pygame.transform.rotate(new_image,angle)
    if alpha:
        new_image.set_alpha(alpha)
    new_image=new_image.convert_alpha()
    return new_image

magnitude = 1.5

def loadMenuImage():
    all_pos = []
    Reimu_Hakurei_Image = pygame.image.load('resource/NPC/Reimu Hakurei.png')
    Reimu_Hakurei_Image = Reimu_Hakurei_Image.convert_alpha()
    Reimu_pos = []
    for i in range(0, 6):
        new_image = pygame.Surface((717, 868)).convert_alpha()
        new_image.fill((0, 0, 0, 0))
        new_image.blit(Reimu_Hakurei_Image, (0, 0), (i*717, 0, 717, 868))
        new_image = pygame.transform.rotozoom(new_image, 0, 0.8)
        Reimu_pos.append(new_image)
        all_pos.append(new_image)
    for i in range(0, 5):
        new_image = pygame.Surface((717, 868)).convert_alpha()
        new_image.fill((0, 0, 0, 0))
        new_image.blit(Reimu_Hakurei_Image, (0, 0), (i*717, 868, 717, 868))
        new_image = pygame.transform.rotozoom(new_image, 0, 0.8)
        Reimu_pos.append(new_image)
        all_pos.append(new_image)
    set_value('Reimu_pos', Reimu_pos)
    set_value('left_portrait', Reimu_pos[0])

    Marisa_Image = pygame.image.load('resource/NPC/Marisa.png')
    Marisa_Image = Marisa_Image.convert_alpha()
    Marisa_pos = []
    for i in range(0, 3):
        for j in range(0, 3):
            new_image = pygame.Surface((544, 883)).convert_alpha()
            new_image.fill((0, 0, 0, 0))
            new_image.blit(Marisa_Image, (0, 0), (j*544, i*883, 544, 883))
            new_image = pygame.transform.rotozoom(new_image, 0, 0.8)
            all_pos.append(new_image)
            Marisa_pos.append(new_image)
    set_value('Marisa_pos', Marisa_pos)
    set_value('right_portrait', Marisa_pos[0])

    Cirno_Image = pygame.image.load('resource/NPC/Cirno.png')
    Cirno_Image = Cirno_Image.convert_alpha()
    Cirno_pos = []
    for i in range(0, 3):
        new_image = pygame.Surface((496, 810)).convert_alpha()
        new_image.fill((0, 0, 0, 0))
        new_image.blit(Cirno_Image, (0, 0), (i*496, 0, 496, 810))
        new_image = pygame.transform.rotozoom(new_image, 0, 0.8)
        all_pos.append(new_image)
        Cirno_pos.append(new_image)
    for i in range(0, 2):
        new_image = pygame.Surface((496, 810)).convert_alpha()
        new_image.fill((0, 0, 0, 0))
        new_image.blit(Cirno_Image, (0, 0), (i*496, 810, 496, 810))
        new_image = pygame.transform.rotozoom(new_image, 0, 0.8)
        all_pos.append(new_image)
        Cirno_pos.append(new_image)
    set_value('Cirno_pos', Cirno_pos)

    set_value('Stage_Image', image(
        pygame.image.load('resource/font/stage.png').convert_alpha(),
        (830, 132),
        zoom=(830/1.5, 132/1.5)
    ))
    set_value('Player_Image', image(
        pygame.image.load('resource/font/player.png').convert_alpha(),
        (842, 132),
        zoom=(842/1.5, 132/1.5)
    ))
    set_value('PlayerInfo_Image_Reimu', image(
        pygame.image.load('resource/font/PlayerInfo_Reimu.png').convert_alpha(),
        (1130, 761),
        zoom=(1130/1.5, 761/1.5)
    ))
    set_value('PlayerInfo_Image_Marisa', image(
        pygame.image.load('resource/font/PlayerInfo_Marisa.png').convert_alpha(),
        (1130, 761),
        zoom=(1130/1.5, 761/1.5)
    ))



def loadImage():
    loadMenuImage()


def loadText():
    file = open("resource/text/stage_1_Reimu.txt", "r" ,encoding = "UTF-8")
    stage_1_Reimu = []
    for i in range(12):
        t = file.readline()
        t=t[:-1]
        stage_1_Reimu.append(t)
    file.close()
    set_value('plot_1_Reimu', stage_1_Reimu)
    
    file = open("resource/text/stage_1_Marisa.txt", "r" ,encoding = "UTF-8")
    stage_1_Marisa = []
    for i in range(8):
        t = file.readline()
        t=t[:-1]
        stage_1_Marisa.append(t)
    file.close()
    set_value('plot_1_Marisa', stage_1_Marisa)
    
    file = open("resource/text/stage_2_Reimu.txt", "r" ,encoding = "UTF-8")
    stage_2_Reimu = []
    for i in range(9):
        t = file.readline()
        t=t[:-1]
        stage_2_Reimu.append(t)
    file.close()
    set_value('plot_2_Reimu', stage_2_Reimu)
    
    file = open("resource/text/stage_2_Marisa.txt", "r" ,encoding = "UTF-8")
    stage_2_Marisa = []
    for i in range(9):
        t = file.readline()
        t=t[:-1]
        stage_2_Marisa.append(t)
    file.close()
    set_value('plot_2_Marisa', stage_2_Marisa)