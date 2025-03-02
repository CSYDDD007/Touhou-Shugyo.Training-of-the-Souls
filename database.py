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

    Sanae_Image = pygame.image.load('resource/NPC/Sanae Kochiya.png')
    Sanae_Image = Sanae_Image.convert_alpha()
    Sanae_pos = []
    for i in range(0, 5):
        new_image = pygame.Surface((694, 830)).convert_alpha()
        new_image.fill((0, 0, 0, 0))
        new_image.blit(Sanae_Image, (0, 0), (i*694, 0, 694, 830))
        new_image = pygame.transform.rotozoom(new_image, 0, 0.5)
        all_pos.append(new_image)
        Sanae_pos.append(new_image)
    for i in range(0, 4):
        new_image = pygame.Surface((694, 830)).convert_alpha()
        new_image.fill((0, 0, 0, 0))
        new_image.blit(Sanae_Image, (0, 0), (i*694, 830, 694, 830))
        new_image = pygame.transform.rotozoom(new_image, 0, 0.5)
        all_pos.append(new_image)
    set_value('Sanae_pos', Sanae_pos)
    
    Sakuya_Image = pygame.image.load('resource/NPC/Sakuya Izayoi.png').convert_alpha()
    Sakuya_pos = []
    for i in range(0,2):
        for j in range(0,3):
            new_image = pygame.Surface((1650//3, 1806//2)).convert_alpha()
            new_image.fill((0,0,0,0))
            new_image.blit(Sakuya_Image, (0,0), (j*1650//3, i*1806//2, 1650//3, 1806//2))
            new_image = pygame.transform.rotozoom(new_image, 0, 0.5)
            all_pos.append(new_image)
            Sakuya_pos.append(new_image)
    set_value('Sakuya_pos', Sakuya_pos)
    
    Remilia_Image = pygame.image.load('resource/NPC/Remilia Scarlet.png').convert_alpha()
    Remilia_pos = []
    for i in range(0,2):
        for j in range(0,3):
            new_image = pygame.Surface((2106//3, 1734//2)).convert_alpha()
            new_image.fill((0,0,0,0))
            new_image.blit(Remilia_Image, (0,0), (j*2106//3, i*1734//2, 2106//3, 1734//2))
            new_image = pygame.transform.rotozoom(new_image, 0, 0.5)
            all_pos.append(new_image)
            Remilia_pos.append(new_image)
    set_value('Remilia_pos', Remilia_pos)
    
    Flandre_Image = pygame.image.load('resource/NPC/Flandre Scarlet.png').convert_alpha()
    Flandre_pos = []
    for i in range(0,2):
        for j in range(0,4):
            new_image = pygame.Surface((2332//4, 1709//2)).convert_alpha()
            new_image.fill((0,0,0,0))
            new_image.blit(Flandre_Image, (0,0), (j*2332//4, i*1709//2, 2332//4, 1709//2))
            new_image = pygame.transform.rotozoom(new_image, 0, 0.5)
            all_pos.append(new_image)
            Flandre_pos.append(new_image)
    set_value('Flandre_pos', Flandre_pos)
    
    Reisen_Image = pygame.image.load('resource/NPC/Reisen Udongein Inaba.png').convert_alpha()
    Reisen_pos = []
    for i in range(0,2):
        for j in range(0,4):
            new_image = pygame.Surface((2260//4, 1862//2)).convert_alpha()
            new_image.fill((0,0,0,0))
            new_image.blit(Reisen_Image, (0,0), (j*2260//4, i*1862//2, 2260//4, 1862//2))
            new_image = pygame.transform.rotozoom(new_image, 0, 0.5)
            all_pos.append(new_image)
            Reisen_pos.append(new_image)
    set_value('Reisen_pos', Reisen_pos)
    
    Aya_Image = pygame.image.load('resource/NPC/Aya Shameimaru.png').convert_alpha()
    Aya_pos = []
    for i in range(0,5):
        new_image = pygame.Surface((2220//5, 880)).convert_alpha()
        new_image.fill((0,0,0,0))
        new_image.blit(Aya_Image, (0,0), (i*2220//5, 0, 2220//5, 880))
        new_image = pygame.transform.rotozoom(new_image, 0, 0.5)
        all_pos.append(new_image)
        Aya_pos.append(new_image)
    set_value('Aya_pos', Aya_pos)
    
    Alice_Image = pygame.image.load('resource/NPC/Alice Margatroid.png').convert_alpha()
    Alice_pos = []
    for i in range(0,4):
        new_image = pygame.Surface((1824//4, 881)).convert_alpha()
        new_image.fill((0,0,0,0))
        new_image.blit(Alice_Image, (0,0), (i*1824//4, 0, 1824//4, 881))
        new_image = pygame.transform.rotozoom(new_image, 0, 0.5)
        all_pos.append(new_image)
        Alice_pos.append(new_image)
    set_value('Alice_pos', Alice_pos)
    
    Eiki_Image = pygame.image.load('resource/NPC/Eiki Shiki.png').convert_alpha()
    Eiki_pos = []
    for i in range(0,5):
        new_image = pygame.Surface((2720//5, 840)).convert_alpha()
        new_image.fill((0,0,0,0))
        new_image.blit(Eiki_Image, (0,0), (i*2720//5, 0, 2720//5, 840))
        new_image = pygame.transform.rotozoom(new_image, 0, 0.5)
        all_pos.append(new_image)
        Eiki_pos.append(new_image)
    set_value('Eiki_pos', Eiki_pos)
    
    Eirin_Image = pygame.image.load('resource/NPC/Eirin Yagokoro.png').convert_alpha()
    Eirin_pos = []
    for i in range(0,3):
        new_image = pygame.Surface((1710//3, 1920//2)).convert_alpha()
        new_image.fill((0,0,0,0))
        new_image.blit(Eirin_Image, (0,0), (i*1710//3, 0, 1710//3, 1920//2))
        new_image = pygame.transform.rotozoom(new_image, 0, 0.5)
        all_pos.append(new_image)
        Eirin_pos.append(new_image)
    for i in range(0,2):
        new_image = pygame.Surface((1710//3, 1920//2)).convert_alpha()
        new_image.fill((0,0,0,0))
        new_image.blit(Eirin_Image, (0,0), (i*1710//3, 1920//2, 1710//3, 1920//2))
        new_image = pygame.transform.rotozoom(new_image, 0, 0.5)
        all_pos.append(new_image)
        Eirin_pos.append(new_image)
    set_value('Eirin_pos', Eirin_pos)
    
    Fujiwara_Image = pygame.image.load('resource/NPC/Fujiwara no Mokou.png').convert_alpha()
    Fujiwara_pos = []
    for i in range(0,4):
        new_image = pygame.Surface((2580//4, 853)).convert_alpha()
        new_image.fill((0,0,0,0))
        new_image.blit(Fujiwara_Image, (0,0), (i*2580//4, 0, 2580//4, 853))
        new_image = pygame.transform.rotozoom(new_image, 0, 0.5)
        all_pos.append(new_image)
        Fujiwara_pos.append(new_image)
    set_value('Fujiwara_pos', Fujiwara_pos)
    
    Hong_Image = pygame.image.load('resource/NPC/Hong Meiling.png').convert_alpha()
    Hong_pos = []
    for i in range(0,2):
        for j in range(0,4):
            new_image = pygame.Surface((2776//4, 1948//2)).convert_alpha()
            new_image.fill((0,0,0,0))
            new_image.blit(Hong_Image, (0,0), (j*2776//4, i*1948//2, 2776//4, 1948//2))
            new_image = pygame.transform.rotozoom(new_image, 0, 0.45)
            all_pos.append(new_image)
            Hong_pos.append(new_image)
    set_value('Hong_pos', Hong_pos)
    
    Kaguya_Image = pygame.image.load('resource/NPC/Kaguya Houraisan.png').convert_alpha()
    Kaguya_pos = []
    for i in range(0,4):
        new_image = pygame.Surface((1884//4, 859)).convert_alpha()
        new_image.fill((0,0,0,0))
        new_image.blit(Kaguya_Image, (0,0), (i*1884//4, 0, 1884//4, 859))
        new_image = pygame.transform.rotozoom(new_image, 0, 0.5)
        all_pos.append(new_image)
        Kaguya_pos.append(new_image)
    set_value('Kaguya_pos', Kaguya_pos)

    Chen_Image = pygame.image.load('resource/NPC/Chen.png').convert_alpha()
    Chen_pos = []
    for i in range(0,4):
        new_image = pygame.Surface((2340//4, 842)).convert_alpha()
        new_image.fill((0,0,0,0))
        new_image.blit(Chen_Image, (0,0), (i*2340//4, 0, 2340//4, 842))
        new_image = pygame.transform.rotozoom(new_image, 0, 0.5)
        all_pos.append(new_image)
        Chen_pos.append(new_image)
    set_value('Chen_pos', Chen_pos)
    
    Keine_Image = pygame.image.load('resource/NPC/Keine Kamishirasawa.png').convert_alpha()
    Keine_pos = []
    for i in range(0,3):
        new_image = pygame.Surface((1551//3, 1870//2)).convert_alpha()
        new_image.fill((0,0,0,0))
        new_image.blit(Keine_Image, (0,0), (i*1551//3, 0, 1551//3, 1870//2))
        new_image = pygame.transform.rotozoom(new_image, 0, 0.5)
        all_pos.append(new_image)
        Keine_pos.append(new_image)
    for i in range(0,2):
        new_image = pygame.Surface((1551//3, 1870//2)).convert_alpha()
        new_image.fill((0,0,0,0))
        new_image.blit(Keine_Image, (0,0), (i*1551//3, 1870//2, 1551//3, 1870//2))
        new_image = pygame.transform.rotozoom(new_image, 0, 0.5)
        all_pos.append(new_image)
        Keine_pos.append(new_image)
    set_value('Keine_pos', Keine_pos)
    
    Koishi_Image = pygame.image.load('resource/NPC/Koishi Komeiji.png').convert_alpha()
    Koishi_pos = []
    for i in range(0,2):
        for j in range(0,2):
            new_image = pygame.Surface((1100//2, 1580//2)).convert_alpha()
            new_image.fill((0,0,0,0))
            new_image.blit(Koishi_Image, (0,0), (j*1100//2, i*1580//2, 1100//2, 1580//2))
            new_image = pygame.transform.rotozoom(new_image, 0, 0.5)
            all_pos.append(new_image)
            Koishi_pos.append(new_image)
    set_value('Koishi_pos', Koishi_pos)

    Mystia_Image = pygame.image.load('resource/NPC/Mystia Lorelei.png').convert_alpha()
    Mystia_pos = []
    for i in range(0,4):
        new_image = pygame.Surface((2128//4, 856)).convert_alpha()
        new_image.fill((0,0,0,0))
        new_image.blit(Mystia_Image, (0,0), (i*2128//4, 0, 2128//4, 856))
        new_image = pygame.transform.rotozoom(new_image, 0, 0.5)
        all_pos.append(new_image)
        Mystia_pos.append(new_image)
    set_value('Mystia_pos', Mystia_pos)
    
    Nitori_Image = pygame.image.load('resource/NPC/Nitori Kawashiro.png').convert_alpha()
    Nitori_pos = []
    for i in range(0,5):
        new_image = pygame.Surface((2720//5, 840)).convert_alpha()
        new_image.fill((0,0,0,0))
        new_image.blit(Nitori_Image, (0,0), (i*2720//5, 0, 2720//5, 840))
        new_image = pygame.transform.rotozoom(new_image, 0, 0.5)
        all_pos.append(new_image)
        Nitori_pos.append(new_image)
    set_value('Nitori_pos', Nitori_pos)
    
    Patchouli_Image = pygame.image.load('resource/NPC/Patchouli Knowledge.png').convert_alpha()
    Patchouli_pos = []
    for i in range(0,3):
        for j in range(0,3):
            new_image = pygame.Surface((1737//3, 1748//2)).convert_alpha()
            new_image.fill((0,0,0,0))
            new_image.blit(Patchouli_Image, (0,0), (j*1737//3, i*1748//2, 1737//3, 1748//2))
            new_image = pygame.transform.rotozoom(new_image, 0, 0.5)
            all_pos.append(new_image)
            Patchouli_pos.append(new_image)
    set_value('Patchouli_pos', Patchouli_pos)
    
    Ran_Image = pygame.image.load('resource/NPC/Ran Yakumo.png').convert_alpha()
    Ran_pos = []
    for i in range(0,4):
        new_image = pygame.Surface((2867//4, 969)).convert_alpha()
        new_image.fill((0,0,0,0))
        new_image.blit(Ran_Image, (0,0), (i*2867//4, 0, 2867//4, 969))
        new_image = pygame.transform.rotozoom(new_image, 0, 0.5)
        all_pos.append(new_image)
        Ran_pos.append(new_image)
    set_value('Ran_pos', Ran_pos)
    
    Satori_Image = pygame.image.load('resource/NPC/Satori Komeiji.png').convert_alpha()
    Satori_pos = []
    for i in range(0,5):
        new_image = pygame.Surface((2470//5, 830)).convert_alpha()
        new_image.fill((0,0,0,0))
        new_image.blit(Satori_Image, (0,0), (i*2470//5, 0, 2470//5, 830))
        new_image = pygame.transform.rotozoom(new_image, 0, 0.5)
        all_pos.append(new_image)
        Satori_pos.append(new_image)
    set_value('Satori_pos', Satori_pos)

    Ringo_Image = pygame.image.load('resource/NPC/Ringo.png').convert_alpha()
    Ringo_pos = []
    for i in range(0,2):
        for j in range(0,2):
            new_image = pygame.Surface((900//2, 1660//2)).convert_alpha()
            new_image.fill((0,0,0,0))
            new_image.blit(Ringo_Image, (0,0), (j*900//2, i*1660//2, 900//2, 1660//2))
            new_image = pygame.transform.rotozoom(new_image, 0, 0.5)
            all_pos.append(new_image)
            Ringo_pos.append(new_image)
    set_value('Ringo_pos', Ringo_pos)
    
    Seiran_Image = pygame.image.load('resource/NPC/Seiran.png').convert_alpha()
    Seiran_pos = []
    for i in range(0,2):
        for j in range(0,2):
            new_image = pygame.Surface((1300//2, 1680//2)).convert_alpha()
            new_image.fill((0,0,0,0))
            new_image.blit(Seiran_Image, (0,0), (j*1300//2, i*1680//2, 1300//2, 1680//2))
            new_image = pygame.transform.rotozoom(new_image, 0, 0.5)
            all_pos.append(new_image)
            Seiran_pos.append(new_image)
    set_value('Seiran_pos', Seiran_pos)
    
    Tewi_Image = pygame.image.load('resource/NPC/Tewi Inaba.png').convert_alpha()
    Tewi_pos = []
    for i in range(0,3):
        new_image = pygame.Surface((1815//3, 1640//2)).convert_alpha()
        new_image.fill((0,0,0,0))    
        new_image.blit(Tewi_Image, (0,0), (i*1815//3, 0, 1815//3, 1640//2))
        new_image = pygame.transform.rotozoom(new_image, 0, 0.5)
        all_pos.append(new_image)
        Tewi_pos.append(new_image)
    for i in range(0,2):
        new_image = pygame.Surface((1815//3, 1640//2)).convert_alpha()
        new_image.fill((0,0,0,0))
        new_image.blit(Tewi_Image, (0,0), (i*1815//3, 1640//2, 1815//3, 1640//2))
        new_image = pygame.transform.rotozoom(new_image, 0, 0.5)
        all_pos.append(new_image)
        Tewi_pos.append(new_image)
    set_value('Tewi_pos', Tewi_pos)

    Youmu_Image = pygame.image.load('resource/NPC/Youmu Konpaku.png').convert_alpha()
    for i in range(0,3):
        for j in range(0,2):
            new_image = pygame.Surface((1434//2, 2478//3)).convert_alpha()
            new_image.fill((0,0,0,0))
            new_image.blit(Youmu_Image, (0,0), (j*1434//2, i*2478//3, 1434//2, 2478//3))
            new_image = pygame.transform.rotozoom(new_image, 0, 0.5)
            all_pos.append(new_image)

    Yukari_Image = pygame.image.load('resource/NPC/Yukari Yakumo.png').convert_alpha()
    Yukari_pos = []
    for i in range(0,4):
        new_image = pygame.Surface((2584//4, 967)).convert_alpha()
        new_image.fill((0,0,0,0))
        new_image.blit(Yukari_Image, (0,0), (i*2584//4, 0, 2584//4, 967))
        new_image = pygame.transform.rotozoom(new_image, 0, 0.5)
        all_pos.append(new_image)
        Yukari_pos.append(new_image)
    set_value('Yukari_pos', Yukari_pos)

    Yuyuko_Image = pygame.image.load('resource/NPC/Yuyuko Saigyouji.png').convert_alpha()
    Yuyuko_pos = []
    for i in range(0,3):
        new_image = pygame.Surface((2013//3, 1808//2)).convert_alpha()
        new_image.fill((0,0,0,0))
        new_image.blit(Yuyuko_Image, (0,0), (i*2013//3, 0, 2013//3, 1808//2))
        new_image = pygame.transform.rotozoom(new_image, 0, 0.5)
        all_pos.append(new_image)
        Yuyuko_pos.append(new_image)
    for i in range(0,2):
        new_image = pygame.Surface((2013//3, 1808//2)).convert_alpha()
        new_image.fill((0,0,0,0))
        new_image.blit(Yuyuko_Image, (0,0), (i*2013//3, 1808//2, 2013//3, 1808//2))
        new_image = pygame.transform.rotozoom(new_image, 0, 0.5)
        all_pos.append(new_image)
        Yuyuko_pos.append(new_image)
    set_value('Yuyuko_pos', Yuyuko_pos)

    #random.shuffle(all_pos)
    set_value('all_pos',all_pos)
    set_value('Title_Image', image(
        pygame.image.load('resource/font/title.png').convert_alpha(),
        (850,302),
        zoom=(850/1.5,302/1.5)
    ))
    Select_Image = pygame.image.load('resource/font/Select.png').convert_alpha()
    Select = []
    for i in range(0, 16):
        for j in range(0,2):
            new_image = pygame.Surface((130, 32)).convert_alpha()
            new_image.fill((0, 0, 0, 0))
            if i >= 3:
                new_image.blit(Select_Image, (0, 0), (j*130, (i+3)*32, 130, 32))
            else:
                new_image.blit(Select_Image, (0, 0), (j*130, i*32, 130, 32))
            new_image = pygame.transform.smoothscale(new_image, (130*magnitude, 32*magnitude))
            Select.append(new_image)
    set_value('Select_Image', Select)
    set_value('Rank_Image', image(
        pygame.image.load('resource/font/rank.png').convert_alpha(),
        (758, 120),
        zoom=(758/1.5, 124/1.5)
    ))
    set_value('Mod_Image',image(
        pygame.image.load('resource/font/mod.png').convert_alpha(),
        (792, 124),
        zoom=(792/1.5, 124/1.5)
    ))
    Rank_Select_Image = pygame.image.load('resource/font/Rank_Select.png').convert_alpha()
    Rank_Select = []
    for i in range(0, 5):
        for j in range(0,2):
            new_image = pygame.Surface((260, 99)).convert_alpha()
            new_image.fill((0, 0, 0, 0))
            new_image.blit(Rank_Select_Image, (0, 0), (j*260, i*99, 260, 99))
            new_image = pygame.transform.rotozoom(new_image, 0, 2)
            Rank_Select.append(new_image)
    set_value('Rank_Select', Rank_Select)
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


def loadUIImage():
    HUD_Image = pygame.image.load('resource/HUD/HUD.png').convert_alpha()
    Rank_Show = []
    for i in range(0, 5):
        new_image = pygame.Surface((156, 32)).convert_alpha()
        new_image.fill((0, 0, 0, 0))
        new_image.blit(HUD_Image, (0, 0), (520 ,636+i*32, 156, 32))
        new_image = pygame.transform.smoothscale(new_image, (187, 38))
        Rank_Show.append(new_image)
    set_value('Rank_Show', Rank_Show)

    fuka = pygame.image.load('resource/image/fuka.png').convert_alpha()
    #fuka = pygame.transform.smoothscale(fuka, (66, 180))
    set_value('fuka', fuka)
    set_value('titleImage',image(
        og=pygame.image.load('resource/image/TaiJi.png').convert_alpha(),
        size=(88,88),
        zoom=(88*1.2,88*1.2),
    ))
    set_value('titleImage1',image(
        og=fuka,
        size=(180,492),
        zoom=(30*magnitude,82*magnitude),
    ))
    SpellCard_Bonus = pygame.image.load('resource/HUD/Spellcard_Bonus.png').convert_alpha()
    set_value('SpellCard_Bonus_Image',image(
        og=SpellCard_Bonus,
        size=(450,56),
        #zoom=(225,28)
    ))
    Bonus_Failed = pygame.image.load('resource/HUD/Bonus_Failed.png').convert_alpha()
    set_value('Bonus_Failed_Image',image(
        og=Bonus_Failed,
        size=(300,59),
        #zoom=(150,28)
    ))
    new_title = pygame.Surface((175*magnitude,200*magnitude)).convert_alpha()
    
    text1 = titlefont.render('东', True, (255,255,255))
    text2 = titlefont.render('方', True, (255,255,255))
    text3 = titlefont.render('修', True, (255,255,255))
    text4 = titlefont.render('行', True, (255,255,255))
    text5 = titlefont.render('记', True, (255,255,255))
    new_title.fill((0,0,0,0))
    new_title.blit(text1, (25*magnitude,0))
    new_title.blit(text2, (100*magnitude,0))
    new_title.blit(text3, (0,75*magnitude))
    new_title.blit(text4,(125*magnitude,75*magnitude))
    new_title.blit(text5,(25*magnitude,150*magnitude))
    set_value('title',new_title)
    text1 = titlefont.render('东', True, (0,0,0))
    text2 = titlefont.render('方', True, (0,0,0))
    text3 = titlefont.render('修', True, (0,0,0))
    text4 = titlefont.render('行', True, (0,0,0))
    text5 = titlefont.render('记', True, (0,0,0))
    new_title1 = pygame.Surface((175*magnitude,200*magnitude)).convert_alpha()
    new_title1.fill((0,0,0,0))
    new_title1.blit(text1, (25*magnitude,0))
    new_title1.blit(text2, (100*magnitude,0))
    new_title1.blit(text3, (0,75*magnitude))
    new_title1.blit(text4,(125*magnitude,75*magnitude))
    new_title1.blit(text5,(25*magnitude,150*magnitude))
    set_value('titleShadow',new_title1)
    
    stage_1 = spellcardfont.render('STAGE 1  妖怪之森', True, LIGHTBLUE)
    stage_1_shadow = spellcardfont.render('STAGE 1  妖怪之森', True, BLACK)
    stage_1_title = TitleFont.render('林中的修行者', True, WHITE)
    stage_1_title_shadow = TitleFont.render('林中的修行者', True, BLACK)
    stage_1_surface = pygame.Surface((450, 200)).convert_alpha()
    stage_1_surface.fill((0, 0, 0, 0))
    for i in range(-1,2):
        for j in range(0,2):
            functions.drawImage(stage_1_shadow, (225+i*2, 20+j*2), 270, stage_1_surface)
            functions.drawImage(stage_1_title_shadow, (225+i*2, 120+j*2), 270, stage_1_surface)
    functions.drawImage(stage_1, (225+i*2, 20+j*2), 270, stage_1_surface)
    functions.drawImage(stage_1_title, (225+i*2, 120+j*2), 270, stage_1_surface)
    set_value('stage_1_surface', stage_1_surface)
    stage_2 = spellcardfont.render('STAGE 2  雾之湖上空', True, LIGHTBLUE)
    stage_2_shadow = spellcardfont.render('STAGE 2  雾之湖上空', True, BLACK)
    stage_2_title = TitleFont.render('湖中的挑战者', True, WHITE)
    stage_2_title_shadow = TitleFont.render('湖中的挑战者', True, BLACK)
    stage_2_surface = pygame.Surface((450, 200)).convert_alpha()
    stage_2_surface.fill((0, 0, 0, 0))
    for i in range(-1,2):
        for j in range(0,2):
            functions.drawImage(stage_2_shadow, (225+i*2, 20+j*2), 270, stage_2_surface)
            functions.drawImage(stage_2_title_shadow, (225+i*2, 120+j*2), 270, stage_2_surface)
    functions.drawImage(stage_2, (225+i*2, 20+j*2), 270, stage_2_surface)
    functions.drawImage(stage_2_title, (225+i*2, 120+j*2), 270, stage_2_surface)
    set_value('stage_2_surface', stage_2_surface)


def loadPauseText():
    sword = image(
        og=pygame.image.load('resource/image/sword.png').convert_alpha(),
        size=(1200,1200),
        zoom=(350,350),
        angle=225,
    )
    sword = pygame.transform.flip(sword, True, False)
    set_value('sword', sword)
    pause_text = textfont.render('Pause Menu', True, WHITE)
    pause_text_shadow = textfont.render('Pause Menu', True, BLACK)
    pause_text1 = textfont.render('暂时停止', True, WHITE)
    pause_text1_shadow = textfont.render('暂时停止', True, BLACK)
    pause_surface = pygame.Surface((200, 100)).convert_alpha()
    pause_surface.fill((0, 0, 0, 0))
    for i in range(-1,2):
        for j in range(0,2):
            pause_surface.blit(pause_text_shadow, (10+i*2, 20+j*2))
            pause_surface.blit(pause_text1_shadow, (10+i*2, 60+j*2))
    pause_surface.blit(pause_text, (10, 20))
    pause_surface.blit(pause_text1, (10, 60))
    set_value('pause_surface', pause_surface)
    
    finish_text = textfont.render('Finish Menu', True, WHITE)
    finish_text_shadow = textfont.render('Finish Menu', True, BLACK)
    finish_text1 = textfont.render('游戏结束', True, WHITE)
    finish_text1_shadow = textfont.render('游戏结束', True, BLACK)
    finish_surface = pygame.Surface((200, 100)).convert_alpha()
    finish_surface.fill((0, 0, 0, 0))
    for i in range(-1,2):
        for j in range(0,2):
            finish_surface.blit(finish_text_shadow, (10+i*2, 20+j*2))
            finish_surface.blit(finish_text1_shadow, (10+i*2, 60+j*2))
    finish_surface.blit(finish_text, (10, 20))
    finish_surface.blit(finish_text1, (10, 60))
    set_value('finish_surface', finish_surface)
    
    gameover_text = textfont.render('Game Over', True, RED)
    gameover_text_shadow = textfont.render('Game Over', True, BLACK)
    gameover_text1 = textfont.render('满身创痍', True, RED)
    gameover_text1_shadow = textfont.render('满身创痍', True, BLACK)
    gameover_surface = pygame.Surface((250, 100)).convert_alpha()
    gameover_surface.fill((0, 0, 0, 0))
    for i in range(-1,2):    
        for j in range(0,2):
            gameover_surface.blit(gameover_text_shadow, (10+i*2, 20+j*2))
            gameover_surface.blit(gameover_text1_shadow, (10+i*2, 60+j*2))
    gameover_surface.blit(gameover_text, (10, 20))
    gameover_surface.blit(gameover_text1, (10, 60))
    set_value('gameover_surface', gameover_surface)
    
    return_game_text = textfont.render('Return to Game', True, WHITE)
    return_game_text_unselected = textfont.render('Return to Game', True, GRAY)
    return_game_text_shadow = textfont.render('Return to Game', True, BLACK)
    return_game_text1 = textfont.render('解除停止', True, WHITE)
    return_game_text1_unselected = textfont.render('解除停止', True, GRAY)
    return_game_text1_shadow = textfont.render('解除停止', True, BLACK)
    return_game_surface = pygame.Surface((250, 100)).convert_alpha()
    return_game_surface.fill((0, 0, 0, 0))
    for i in range(-1,2):
        for j in range(0,2):
            return_game_surface.blit(return_game_text_shadow, (10+i*2, 20+j*2))
            return_game_surface.blit(return_game_text1_shadow, (10+i*2, 60+j*2))
    return_game_surface.blit(return_game_text, (10, 20))
    return_game_surface.blit(return_game_text1, (10, 60))
    set_value('return_game_surface', return_game_surface)
    return_game_unselected_surface = pygame.Surface((250, 100)).convert_alpha()
    return_game_unselected_surface.fill((0, 0, 0, 0))
    for i in range(-1,2):
        for j in range(0,2):
            return_game_unselected_surface.blit(return_game_text_shadow, (10+i*2, 20+j*2))
            return_game_unselected_surface.blit(return_game_text1_shadow, (10+i*2, 60+j*2))
    return_game_unselected_surface.blit(return_game_text_unselected, (10, 20))
    return_game_unselected_surface.blit(return_game_text1_unselected, (10, 60))
    set_value('return_game_unselected_surface', return_game_unselected_surface)
    
    retry_text = textfont.render('Retry', True, WHITE)
    retry_text_unselected = textfont.render('Retry', True, GRAY)
    retry_text_shadow = textfont.render('Retry', True, BLACK)
    retry_text1 = textfont.render('稳定道心', True, WHITE)
    retry_text1_unselected = textfont.render('稳定道心', True, GRAY)
    retry_text1_shadow = textfont.render('稳定道心', True, BLACK)
    retry_surface = pygame.Surface((350, 100)).convert_alpha()
    retry_surface.fill((0, 0, 0, 0))
    for i in range(-1,2):
        for j in range(0,2):
            retry_surface.blit(retry_text_shadow, (10+i*2, 20+j*2))
            retry_surface.blit(retry_text1_shadow, (10+i*2, 60+j*2))
    retry_surface.blit(retry_text, (10, 20))
    retry_surface.blit(retry_text1, (10, 60))
    set_value('retry_surface', retry_surface)
    retry_unselected_surface = pygame.Surface((250, 100)).convert_alpha()
    retry_unselected_surface.fill((0, 0, 0, 0))
    for i in range(-1,2):
        for j in range(0,2):
            retry_unselected_surface.blit(retry_text_shadow, (10+i*2, 20+j*2))
            retry_unselected_surface.blit(retry_text1_shadow, (10+i*2, 60+j*2))
    retry_unselected_surface.blit(retry_text_unselected, (10, 20))
    retry_unselected_surface.blit(retry_text1_unselected, (10, 60))
    set_value('retry_unselected_surface', retry_unselected_surface)
    
    return_title_text = textfont.render('Return to Title', True, WHITE)
    return_title_text_unselected = textfont.render('Return to Title', True, GRAY)
    retuen_title_text_shadow = textfont.render('Return to Title', True, BLACK)
    return_title_text1 = textfont.render('返回主页', True, WHITE)
    return_title_text1_unselected = textfont.render('返回主页', True, GRAY)
    return_title_text1_shadow = textfont.render('返回主页', True, BLACK)
    return_title_surface = pygame.Surface((250, 100)).convert_alpha()
    return_title_surface.fill((0, 0, 0, 0))
    for i in range(-1,2):
        for j in range(0,2):
            return_title_surface.blit(retuen_title_text_shadow, (10+i*2, 20+j*2))
            return_title_surface.blit(return_title_text1_shadow, (10+i*2, 60+j*2))
    return_title_surface.blit(return_title_text, (10, 20))
    return_title_surface.blit(return_title_text1, (10, 60))
    set_value('return_title_surface', return_title_surface)
    return_title_unselected_surface = pygame.Surface((250, 100)).convert_alpha()
    return_title_unselected_surface.fill((0, 0, 0, 0))
    for i in range(-1,2):
        for j in range(0,2):
            return_title_unselected_surface.blit(retuen_title_text_shadow, (10+i*2, 20+j*2))
            return_title_unselected_surface.blit(return_title_text1_shadow, (10+i*2, 60+j*2))
    return_title_unselected_surface.blit(return_title_text_unselected, (10, 20))
    return_title_unselected_surface.blit(return_title_text1_unselected, (10, 60))
    set_value('return_title_unselected_surface', return_title_unselected_surface)
    
    restart_text = textfont.render('Restart', True, WHITE)
    restart_text_unselected = textfont.render('Restart', True, GRAY)
    restart_text_shadow = textfont.render('Restart', True, BLACK)
    restart_text1 = textfont.render('重入轮回', True, WHITE)
    restart_text1_unselected = textfont.render('重入轮回', True, GRAY)
    restart_text1_shadow = textfont.render('重入轮回', True, BLACK)
    restart_surface = pygame.Surface((250, 100)).convert_alpha()
    restart_surface.fill((0, 0, 0, 0))
    for i in range(-1,2):
        for j in range(0,2):
            restart_surface.blit(restart_text_shadow, (10+i*2, 20+j*2))
            restart_surface.blit(restart_text1_shadow, (10+i*2, 60+j*2))
    restart_surface.blit(restart_text, (10, 20))
    restart_surface.blit(restart_text1, (10, 60))
    set_value('restart_surface', restart_surface)
    restart_unselected_surface = pygame.Surface((250, 100)).convert_alpha()
    restart_unselected_surface.fill((0, 0, 0, 0))
    for i in range(-1,2):
        for j in range(0,2):
            restart_unselected_surface.blit(restart_text_shadow, (10+i*2, 20+j*2))
            restart_unselected_surface.blit(restart_text1_shadow, (10+i*2, 60+j*2))
    restart_unselected_surface.blit(restart_text_unselected, (10, 20))
    restart_unselected_surface.blit(restart_text1_unselected, (10, 60))
    set_value('restart_unselected_surface', restart_unselected_surface)
    

def loadBackgroundImage():
    #HUD background
    background = get_value('loadscreen')
    background_list = []
    new_image = pygame.Surface((32*magnitude, 480*magnitude)).convert_alpha()
    new_image.fill((0, 0, 0, 0))
    new_image.blit(background, (0, 0), (0, 0, 32*magnitude, 480*magnitude))
    background_list.append(new_image)
    new_image = pygame.Surface((384*magnitude, 16*magnitude)).convert_alpha()
    new_image.fill((0, 0, 0, 0))
    new_image.blit(background, (0, 0), (32*magnitude, 0, 384*magnitude, 16*magnitude))
    background_list.append(new_image)
    new_image = pygame.Surface((384*magnitude, 16*magnitude)).convert_alpha()
    new_image.fill((0, 0, 0, 0))
    new_image.blit(background, (0, 0), (32*magnitude, 464*magnitude, 384*magnitude, 16*magnitude))
    background_list.append(new_image)
    new_image = pygame.Surface((224*magnitude, 480*magnitude)).convert_alpha()
    new_image.fill((0, 0, 0, 0))
    new_image.blit(background, (0, 0), (416*magnitude, 0, 224*magnitude, 480*magnitude))
    background_list.append(new_image)
    set_value('background', background_list)
    
    new_image = pygame.image.load('resource/image/forest_1.jpg').convert_alpha()
    set_value('stage_1', new_image)
    new_image = pygame.image.load('resource/image/cirno_fumo_1.jpg').convert_alpha()
    new_image = pygame.transform.smoothscale(new_image, (260, 260))
    set_value('cirno_fumo', new_image)
    lake=[]
    dark_mask = pygame.Surface((768+24,896+24)).convert_alpha()
    dark_mask.fill((0,0,0,48))
    for i in range(1,182):#182
        new_image = image(
            og=pygame.image.load('resource/background/lake ('+str(i)+').jpg').convert_alpha(),
            size=(768+24,896),
            crop_area=(0,0,(384+12)*magnitude,448*magnitude),
        )
        #pygame.image.save(new_image, 'resource/background/lake ('+str(i)+').jpg')
        new_image.blit(dark_mask, (0,0))
        lake.append(new_image)
    set_value('lake_background',lake)


def loadPlayerImage():
    Player_Reimu_Image = pygame.image.load('resource/player/P001/playerImage.png').convert_alpha()
    Player_Reimu = []
    for i in range (0, 3):
        for j in range (0, 8):
            Player_Reimu.append(image(
                Player_Reimu_Image,
                size=(32,48),
                crop_area=(j*32,i*48,32,48),
                zoom=(32*magnitude,48*magnitude),
            ))
    set_value('Player_Reimu', Player_Reimu)

    Reimu_Object_Image = pygame.image.load('resource/player/P001/Object_th16.png')

    Reimu_Main_Satsu = []
    Reimu_Main_Satsu.append(image(
        Reimu_Object_Image,
        size=(64,16),
        crop_area=(192,0,64,16),
        zoom=(64*magnitude,16*magnitude),
        angle=90
    ))
    for i in range(0, 4):
        Reimu_Main_Satsu.append(image(
            Reimu_Object_Image,
            size=(16,16),
            crop_area=(i*16,0,16,16),
            zoom=(16*magnitude,16*magnitude),
            angle=90))
    set_value('Reimu_Main_Satsu', Reimu_Main_Satsu)
    
    Reimu_Target_Satsu = []
    for i in range(0, 4):
        Reimu_Target_Satsu.append(image(
            Reimu_Object_Image,
            size=(16,16),
            crop_area=(i*16,16,16,16),
            zoom=(16*magnitude,16*magnitude),
            angle=90,
            alpha=200
        ))
    set_value('Reimu_Target_Satsu', Reimu_Target_Satsu)
    
    Reimu_Shift_Satsu = []
    for i in range(0, 2):
        Reimu_Shift_Satsu.append(image(
            Reimu_Object_Image,
            size=(64,16),
            crop_area=(i*64,32,64,16),
            zoom=(64*magnitude,16),
            angle=90,
        ))
    set_value('Reimu_Shift_Satsu', Reimu_Shift_Satsu)

    set_value('ReimuFloatGun', image(
        Reimu_Object_Image,
        size=(16,16),
        crop_area=(64,0,16,16),
        zoom=(16*magnitude,16*magnitude)
    ))

    Player_Marisa_Image = pygame.image.load('resource/player/P002/playerImage.png').convert_alpha()
    Player_Marisa = []
    for i in range (0, 3):
        for j in range (0, 8):
            Player_Marisa.append(image(
                Player_Marisa_Image,
                size=(32,48),
                crop_area=(j*32,i*48,32,48),
                zoom=(32*magnitude,48*magnitude),
            ))
    set_value('Player_Marisa', Player_Marisa)
    
    Marisa_Object = pygame.image.load('resource/player/P002/Object_th17.png').convert_alpha()
    
    Marisa_Main_Bullet = []
    for i in range(0, 4):
        Marisa_Main_Bullet.append(image(
            Marisa_Object,
            size=(32,16),
            crop_area=(32*i+8,0,32,16),
            zoom=(32*magnitude,16*magnitude),
            angle=90,
            alpha=160
        ))
    set_value('Marisa_Main_Bullet', Marisa_Main_Bullet)
    
    set_value('Marisa_Laser', image(
        Marisa_Object,
        size=(256,16),
        crop_area=(8,32,256,16),
        zoom=(256*magnitude,16*magnitude),
        angle=90,
        #alpha=200
    ))
    
    Marisa_Missile = []
    for i in range(0, 2):
        Marisa_Missile.append(image(
            og=Marisa_Object,
            size=(48,16),
            crop_area=(8,48+i*16,48,16),
            zoom=(48*magnitude,16*magnitude),
            angle=90
        ))
    for i in range(0, 8):
        Marisa_Missile.append(image(
            og=Marisa_Object,
            size=(32,32),
            crop_area=(32*i+8,80,32,32),
            zoom=(32*magnitude,32*magnitude)
        ))
    set_value('Marisa_Missile', Marisa_Missile)
    
    Marisa_All = pygame.image.load('resource/player/P002/All.png').convert_alpha()
    set_value('Master_Spark', image(
        og=Marisa_All,
        size=(256,144),
        crop_area=(288,8,256,144),
        zoom=(896,504),
        angle=90,
    ))
    # Master_Spark = pygame.Surface((896,504)).convert_alpha()
    # Master_Spark.fill((0,0,0))
    # set_value('Master_Spark', Master_Spark)
    
    
    Master_Spark_Wave = pygame.image.load('resource/player/P002/Wave.png').convert_alpha()
    Master_Spark_Wave = pygame.transform.smoothscale(Master_Spark_Wave, (240, 700))
    Master_Spark_Wave = pygame.transform.rotate(Master_Spark_Wave, 90)
    Master_Spark_Wave.set_alpha(90)
    set_value('Master_Spark_Wave', Master_Spark_Wave)
    
    Marisa_FloatGun = pygame.Surface((16, 16)).convert_alpha()
    Marisa_FloatGun.fill((0,0,0,0))
    Marisa_FloatGun.blit(Marisa_Object, (0,0), (72, 16, 16, 16))
    Marisa_FloatGun = pygame.transform.smoothscale(Marisa_FloatGun, (24, 24))
    set_value('Marisa_FloatGun', image(
        og=Marisa_Object,
        size=(16,16),
        crop_area=(72,16,16,16),
        zoom=(24,24),
    ))
enemy_list = {}
class EnemyAssets:
    pass

def loadEnemyImage():
    nimbus=pygame.image.load('resource/enemy/nimbus1.png').convert_alpha()
    nimbus=pygame.transform.smoothscale(nimbus,(256,64))
    set_value('nimbus',nimbus)
    red_effect=pygame.Surface((1000,1000)).convert_alpha()
    red_effect.fill((255,0,0))
    #I finally understand how to use special_flags...
    fairy=[]
    sunflower_fairy = []
    fairy_image=image(
        og=pygame.image.load('resource/enemy/fairy.png').convert_alpha(),
        size=(512,192),
        zoom=(512*magnitude,192*magnitude),
    )
    for k in range(0,2):
        if k:
            for i in range(3):
                fairy_image.blit(red_effect,(0,0),special_flags=pygame.BLEND_RGBA_MULT)
        for i in range(0,4):
            for j in range(0,12):
                fairy.append(image(
                    og=fairy_image,
                    size=(32*magnitude,32*magnitude),
                    crop_area=(j*32*magnitude,i*32*magnitude,32*magnitude,32*magnitude),
                ))
        for i in range(0, 8):
            sunflower_fairy.append(image(
                og=fairy_image,
                size=(64*magnitude,64*magnitude),
                crop_area=(i*64*magnitude,128*magnitude,64*magnitude,64*magnitude),
            ))
        for i in range(0, 2):
            for j in range(0, 2):
                sunflower_fairy.append(image(
                    og=fairy_image,
                    size=(64*magnitude,64*magnitude),
                    crop_area=((j*64+384)*magnitude,i*64*magnitude,64*magnitude,64*magnitude),
            ))
    set_value('fairy',fairy)
    set_value('sunflower_fairy', sunflower_fairy)
    
    corroded_fairy=[]
    corrodedflower_fairy = []
    corroded_fairy_image=image(
        og=pygame.image.load('resource/enemy/corroded_fairy.png').convert_alpha(),
        size=(512,192),
        zoom=(512*magnitude,192*magnitude),
    )
    for k in range(0,2):
        if k:
            for i in range(3):
                corroded_fairy_image.blit(red_effect,(0,0),special_flags=pygame.BLEND_RGBA_MULT)
        for i in range(0,4):
            for j in range(0,12):
                corroded_fairy.append(image(
                    og=corroded_fairy_image,
                    size=(32*magnitude,32*magnitude),
                    crop_area=(j*32*magnitude,i*32*magnitude,32*magnitude,32*magnitude),
                ))
        for i in range(0, 8):
            corrodedflower_fairy.append(image(
                og=corroded_fairy_image,
                size=(64*magnitude,64*magnitude),
                crop_area=(i*64*magnitude,128*magnitude,64*magnitude,64*magnitude),
            ))
        for i in range(0, 2):
            for j in range(0, 2):
                corrodedflower_fairy.append(image(
                    og=corroded_fairy_image,
                    size=(64*magnitude,64*magnitude),
                    crop_area=((j*64+384)*magnitude,i*64*magnitude,64*magnitude,64*magnitude),
                ))
    set_value('corroded_fairy',corroded_fairy)
    set_value('corrodedflower_fairy', corrodedflower_fairy)
    
    sp_fairy=[]
    sp_fairy_image=image(
        og=pygame.image.load('resource/enemy/sp_fairy.png').convert_alpha(),
        size=(192,192),
        zoom=(192*magnitude,192*magnitude),
    )
    for k in range(0,2):
        if k:
            for i in range(3):
                sp_fairy_image.blit(red_effect,(0,0),special_flags=pygame.BLEND_RGBA_MULT)
        for i in range(0,6):
            for j in range(0,4):
                sp_fairy.append(image(
                    og=sp_fairy_image,
                    size=(48*magnitude,32*magnitude),
                    crop_area=(j*48*magnitude,i*32*magnitude,48*magnitude,32*magnitude),
                ))
    set_value('sp_fairy',sp_fairy)
    
    mid_fairy=[]
    mid_fairy_image=image(
        og=pygame.image.load('resource/enemy/mid_fairy.png').convert_alpha(),
        size=(192,288),
        zoom=(192*magnitude,288*magnitude),
    )
    for k in range(0,2):
        if k:
            for i in range(3):
                mid_fairy_image.blit(red_effect,(0,0),special_flags=pygame.BLEND_RGBA_MULT)
        for i in range(0,6):
            for j in range(0,4):
                mid_fairy.append(image(
                    og=mid_fairy_image,
                    size=(48*magnitude,48*magnitude),
                    crop_area=(j*48*magnitude,i*48*magnitude,48*magnitude,48*magnitude),
                ))
    set_value('mid_fairy',mid_fairy)
    
    ghost=[]
    ghost_image=image(
        og=pygame.image.load('resource/enemy/ghost.png').convert_alpha(),
        size=(256,128),
        zoom=(256*magnitude,128*magnitude)
    )
    for k in range(0,2):
        if k:
            for i in range(3):
                ghost_image.blit(red_effect,(0,0),special_flags=pygame.BLEND_RGBA_MULT)
        for i in range(0,4):
            for j in range(0,8):
                ghost.append(image(
                    og=ghost_image,
                    size=(32*magnitude,32*magnitude),
                    crop_area=(j*32*magnitude,i*32*magnitude,32*magnitude,32*magnitude),
                ))
    set_value('ghost',ghost)
    kedama=[]
    kedama_image=image(
        og=pygame.image.load('resource/enemy/kedama.png').convert_alpha(),
        size=(64,64),
        zoom=(64*magnitude,64*magnitude)
    )
    for k in range(0,2):
        if k:
            for i in range(3):
                kedama_image.blit(red_effect,(0,0),special_flags=pygame.BLEND_RGBA_MULT)
        for i in range(0,2):
            for j in range(0,2):
                kedama.append(image(
                    og=kedama_image,
                    size=(32*magnitude,32*magnitude),
                    crop_area=(j*32*magnitude,i*32*magnitude,32*magnitude,32*magnitude),
                ))
    set_value('kedama',kedama)

    yinyangyu=[]
    small_yinyangyu=[]
    yinyangyu_image=image(
        og=pygame.image.load('resource/enemy/ball.png').convert_alpha(),
        size=(256,64),
        zoom=(256*magnitude,64*magnitude)
    )
    for k in range(0,2):
        if k:
            for i in range(3):
                yinyangyu_image.blit(red_effect,(0,0),special_flags=pygame.BLEND_RGBA_MULT)
        for i in range(0,4): 
            yinyangyu.append(image(
                og=yinyangyu_image,
                size=(32*magnitude,32*magnitude),
                crop_area=(i*32*magnitude,0,32*magnitude,32*magnitude),
            ))
            small_yinyangyu.append(image(
                og=yinyangyu_image,
                size=(32*magnitude,32*magnitude),
                crop_area=((i*32+128)*magnitude,0,32*magnitude,32*magnitude),
            ))
        for i in range(0,4):
            nimbus=image(
                og=yinyangyu_image,
                size=(32*magnitude,32*magnitude),
                crop_area=(i*32*magnitude,32*magnitude,32*magnitude,32*magnitude),
            )
            nimbus.set_alpha(200)
            nimbus=pygame.transform.smoothscale(nimbus,(48*magnitude,48*magnitude))
            yinyangyu.append(nimbus)
            small_yinyangyu.append(image(
                og=yinyangyu_image,
                size=(32*magnitude,32*magnitude),
                crop_area=((i*32+128)*magnitude,32*magnitude,32*magnitude,32*magnitude),
            ))
    set_value('yinyangyu',yinyangyu)
    set_value('small_yinyangyu',small_yinyangyu)
    
    paleflower_fairy = []
    paleflower_fairy_image=image(
        og=pygame.image.load('resource/enemy/paleflower_fairy.png').convert_alpha(),
        size=(512,128),
        zoom=(512*magnitude,128*magnitude)
    )
    for k in range(0,2):
        if k:
            for i in range(3):
                paleflower_fairy_image.blit(red_effect,(0,0),special_flags=pygame.BLEND_RGBA_MULT)
        for i in range(0, 8):
            paleflower_fairy.append(image(
                og=paleflower_fairy_image,
                size=(64*magnitude,64*magnitude),
                crop_area=(i*64*magnitude,0,64*magnitude,64*magnitude),
            ))
        for i in range(0, 4):
            paleflower_fairy.append(image(
                og=paleflower_fairy_image,
                size=(64*magnitude,64*magnitude),
                crop_area=(i*64*magnitude,64*magnitude,64*magnitude,64*magnitude),
            ))
    set_value('paleflower_fairy', paleflower_fairy)


    cirno_boss_image = pygame.image.load('resource/enemy/boss_Cirno_Flight.png').convert_alpha()
    cirno_boss = []
    for i in range(0, 3):
        for j in range(0, 4):
            new_image = pygame.Surface((64, 64)).convert_alpha()
            new_image.fill((0,0,0,0))
            new_image.blit(cirno_boss_image, (0, 0), (j*64, i*64, 64, 64))
            new_image = pygame.transform.smoothscale(new_image, (128, 128))
            cirno_boss.append(new_image)
    set_value('cirno_boss', cirno_boss)
    
    cat_boss_image = pygame.image.load('resource/image/IMG_0359.png').convert_alpha()
    cat_boss = pygame.transform.rotozoom(cat_boss_image, 0, 0.8)
    cat_boss_plot = pygame.transform.rotozoom(cat_boss_image, 0, 2.0)
    set_value('cat_boss', cat_boss)
    set_value('cat_boss_plot', cat_boss_plot)
    cat = pygame.image.load('resource/image/steve_1.png').convert_alpha()
    cat = pygame.transform.rotozoom(cat, 0, 1.8).convert_alpha()
    set_value('cat_spell',cat)
    
    boss_magic = pygame.image.load('resource/enemy/boss_magic.png').convert_alpha()
    boss_magic = pygame.transform.smoothscale(boss_magic, (384,384)).convert_alpha()
    boss_magic.set_alpha(200)
    set_value('boss_magic', boss_magic)
    
    spell_card_attack = pygame.image.load('resource/image/spellcardAttack.png').convert_alpha()
    set_value('spell_card_attack', spell_card_attack)
    
    enemyDeath = pygame.image.load('resource/enemy/enemy_death.png').convert_alpha()
    enemyDeath_1 = pygame.image.load('resource/enemy/enemy_death_1.png').convert_alpha()
    enemyDeath_image = []
    for i in range(0,2):
        new_image=pygame.Surface((64,64)).convert_alpha()
        new_image.fill((0,0,0,0))
        new_image.blit(enemyDeath, (0,0), (i*64,0,64,64))
        enemyDeath_image.append(new_image)
    for i in range(0,2):
        new_image=pygame.Surface((64,64)).convert_alpha()
        new_image.fill((0,0,0,0))
        new_image.blit(enemyDeath_1, (0,0), (i*64,0,64,64))
        enemyDeath_image.append(new_image)
    set_value('enemyDeath', enemyDeath_image)


def loadBulletImage():
    all = pygame.image.load('resource/bullet/bullet_all.png').convert_alpha()
    #激光
    laser = []
    for i in range (0, 16):
        new_image = pygame.Surface((16, 14)).convert_alpha()
        new_image.fill((0, 0, 0, 0))
        new_image.blit(all, (0, 0), (i*16, 1, 16, 14))
        new_image = pygame.transform.smoothscale(new_image, (16, 16))
        laser.append(new_image)
    set_value('laser', laser)
    #麟弹
    scale_bullet = []
    for i in range (0, 16):
        scale_bullet.append(image(
        og=all,
        size=(16,16),
        crop_area=(i*16,16,16,16),
        zoom=(24,24)
    ))
    set_value('scale_bullet', scale_bullet)
    #环玉
    orb_bullet = []
    for i in range (0, 16):
        new_image = pygame.Surface((16, 16)).convert_alpha()
        new_image.fill((0, 0, 0, 0))
        new_image.blit(all, (0, 0), (i*16, 32, 16, 16))
        new_image = pygame.transform.smoothscale(new_image, (24, 24))
        orb_bullet.append(new_image)
    set_value('orb_bullet', orb_bullet)
    #小玉
    small_bullet = []
    for i in range (0, 16):
        new_image = pygame.Surface((16, 16)).convert_alpha()
        new_image.fill((0, 0, 0, 0))
        new_image.blit(all, (0, 0), (i*16, 48, 16, 16))
        new_image = pygame.transform.smoothscale(new_image, (24, 24))
        small_bullet.append(new_image)
    set_value('small_bullet', small_bullet)
    #米弹
    rice_bullet = []
    for i in range (0, 16):
        new_image = pygame.Surface((16, 16)).convert_alpha()
        new_image.fill((0, 0, 0, 0))
        new_image.blit(all, (0, 0), (i*16, 64, 16, 16))
        new_image = pygame.transform.smoothscale(new_image, (24, 24))
        rice_bullet.append(new_image)
    set_value('rice_bullet', rice_bullet)
    #链弹
    chain_bullet = []
    for i in range (0, 16):
        new_image = pygame.Surface((16, 16)).convert_alpha()
        new_image.fill((0, 0, 0, 0))
        new_image.blit(all, (0, 0), (i*16, 80, 16, 16))
        new_image = pygame.transform.smoothscale(new_image, (24, 24))
        chain_bullet.append(new_image)
    set_value('chain_bullet', chain_bullet)
    #针弹
    pin_bullet = []
    for i in range (0, 16):
        new_image = pygame.Surface((16, 16)).convert_alpha()
        new_image.fill((0, 0, 0, 0))
        new_image.blit(all, (0, 0), (i*16, 96, 16, 16))
        new_image = pygame.transform.smoothscale(new_image, (24, 24))
        pin_bullet.append(new_image)
    set_value('pin_bullet', pin_bullet)
    #札弹
    satsu_bullet = []
    for i in range (0, 16):
        new_image = pygame.Surface((16, 16)).convert_alpha()
        new_image.fill((0, 0, 0, 0))
        new_image.blit(all, (0, 0), (i*16, 112, 16, 16))
        new_image = pygame.transform.smoothscale(new_image, (24, 24))
        satsu_bullet.append(new_image)
    set_value('satsu_bullet', satsu_bullet)
    #铳弹
    gun_bullet = []
    for i in range (0, 16):
        new_image = pygame.Surface((16, 16)).convert_alpha()
        new_image.fill((0, 0, 0, 0))
        new_image.blit(all, (0, 0), (i*16, 128, 16, 16))
        new_image = pygame.transform.smoothscale(new_image, (24, 24))
        #new_image.set_alpha(200)
        gun_bullet.append(new_image)
    set_value('gun_bullet', gun_bullet)
    #杆菌弹
    bact_bullet = []
    for i in range (0, 16):
        new_image = pygame.Surface((16, 16)).convert_alpha()
        new_image.fill((0, 0, 0, 0))
        new_image.blit(all, (0, 0), (i*16, 144, 16, 16))
        new_image = pygame.transform.smoothscale(new_image, (24, 24))
        bact_bullet.append(new_image)
    set_value('bact_bullet', bact_bullet)
    #星弹（小）
    star_bullet = []
    for i in range (0, 16):
        new_image = pygame.Surface((16, 16)).convert_alpha()
        new_image.fill((0, 0, 0, 0))
        new_image.blit(all, (0, 0), (i*16, 160, 16, 16))
        new_image = pygame.transform.smoothscale(new_image, (24, 24))
        star_bullet.append(new_image)
    set_value('star_bullet', star_bullet)
    #葡萄弹
    grape_bullet = []
    for i in range (0, 2):
        for j in range(0, 8):
            new_image = pygame.Surface((8, 8)).convert_alpha()
            new_image.fill((0, 0, 0, 0))
            new_image.blit(all, (0, 0), (j*8, i*8+192, 8, 8))
            new_image = pygame.transform.smoothscale(new_image, (12, 12))
            grape_bullet.append(new_image)
    set_value('grape_bullet', grape_bullet)
    #生成子弹
    bullet_create = []
    for i in range(0, 8):
        new_image = pygame.Surface((32, 32)).convert_alpha()
        new_image.fill((0, 0, 0, 0))
        new_image.blit(all, (0, 0), (i*32, 208, 32, 32))
        new_image = pygame.transform.smoothscale(new_image, (48, 48))
        bullet_create.append(new_image)
    #点弹
    dot_bullet = []
    for i in range (0, 2):
        for j in range(0, 8):
            new_image = pygame.Surface((8, 8)).convert_alpha()
            new_image.fill((0, 0, 0, 0))
            new_image.blit(all, (0, 0), (j*8, i*8+240, 8, 8))
            new_image = pygame.transform.smoothscale(new_image, (12, 12))
            dot_bullet.append(new_image)
    set_value('dot_bullet', dot_bullet)


    all_2 = pygame.image.load('resource/bullet/bullet_all_2.png').convert_alpha()
    #all_2 = pygame.transform.smoothscale(all_2, (256, 612))
    #星弹（大）
    big_star_bullet = []
    for i in range(0, 8):
        new_image = pygame.Surface((32, 32)).convert_alpha()
        new_image.fill((0, 0, 0, 0))
        new_image.blit(all_2, (0, 0), (i*32, 0, 32, 32))
        new_image = pygame.transform.smoothscale(new_image, (48, 48))
        big_star_bullet.append(new_image)
    set_value('big_star_bullet', big_star_bullet)
    #中玉
    mid_bullet = []
    for i in range(0, 8):
        new_image = pygame.Surface((32, 32)).convert_alpha()
        new_image.fill((0, 0, 0, 0))
        new_image.blit(all_2, (0, 0), (i*32, 32, 32, 32))
        new_image = pygame.transform.smoothscale(new_image, (48, 48))
        mid_bullet.append(new_image)
    set_value('mid_bullet', mid_bullet)
    #蝶弹
    butterfly_bullet = []
    for i in range(0, 8):
        new_image = pygame.Surface((32, 32)).convert_alpha()
        new_image.fill((0, 0, 0, 0))
        new_image.blit(all_2, (0, 0), (i*32, 64, 32, 32))
        new_image = pygame.transform.smoothscale(new_image, (48, 48))
        butterfly_bullet.append(new_image)
    set_value('butterfly_bullet', butterfly_bullet)
    #刀弹
    knife_bullet = []
    for i in range(0, 8):
        new_image = pygame.Surface((32, 32)).convert_alpha()
        new_image.fill((0, 0, 0, 0))
        new_image.blit(all_2, (0, 0), (i*32, 96, 32, 32))
        new_image = pygame.transform.smoothscale(new_image, (48, 48))
        knife_bullet.append(new_image)
    set_value('knife_bullet', knife_bullet)
    #椭弹
    ellipse_bullet = []
    for i in range(0, 8):
        new_image = pygame.Surface((32, 32)).convert_alpha()
        new_image.fill((0, 0, 0, 0))
        new_image.blit(all_2, (0, 0), (i*32, 128, 32, 32))
        new_image = pygame.transform.smoothscale(new_image, (48, 48))
        ellipse_bullet.append(new_image)
    set_value('ellipse_bullet', ellipse_bullet)
    #子弹生成
    for i in range(0, 8):
        new_image = pygame.Surface((32, 32)).convert_alpha()
        new_image.fill((0, 0, 0, 0))
        new_image.blit(all_2, (0, 0), (i*32, 160, 32, 32))
        new_image = pygame.transform.smoothscale(new_image, (48, 48))
        bullet_create.append(new_image)
    set_value('bullet_create', bullet_create)
    #大玉
    big_bullet = []
    for i in range(0, 4):
        new_image = pygame.Surface((64, 72)).convert_alpha()
        new_image.fill((0, 0, 0, 0))
        new_image.blit(all_2, (0, 0), (i*64, 192, 64, 72))
        new_image = pygame.transform.smoothscale(new_image, (96, 108))
        big_bullet.append(new_image)
    set_value('big_bullet', big_bullet)
    #心弹
    heart_bullet = []
    #heart_bullet_image = pygame.image.load('resource/heart_bullet.png').convert_alpha()
    for i in range(0, 8):
        new_image = pygame.Surface((32, 32)).convert_alpha()
        new_image.fill((0, 0, 0, 0))
        #new_image.blit(heart_bullet_image, (0, 0), (i*32, 0, 32, 32))
        new_image.blit(all_2, (0, 0), (i*32, 264, 32, 32))
        new_image = pygame.transform.smoothscale(new_image, (48, 48))
        heart_bullet.append(new_image)
    set_value('heart_bullet', heart_bullet)
    #箭弹
    arrow_bullet = []
    for i in range(0, 8):
        new_image = pygame.Surface((32, 32)).convert_alpha()
        new_image.fill((0, 0, 0, 0))
        new_image.blit(all_2, (0, 0), (i*32, 296, 32, 32))
        new_image = pygame.transform.smoothscale(new_image, (48, 48))
        arrow_bullet.append(new_image)
    set_value('arrow_bullet', arrow_bullet)
    #光弹（小）
    light_bullet = []
    for i in range(0, 8):
        new_image = pygame.Surface((32, 32)).convert_alpha()
        new_image.fill((0, 0, 0, 0))
        new_image.blit(all_2, (0, 0), (i*32, 328, 32, 32))
        new_image = pygame.transform.smoothscale(new_image, (48, 48))
        light_bullet.append(new_image)
    set_value('light_bullet', light_bullet)
    #炎弹
    fire_bullet = []
    for i in range(0, 2):
        for j in range(0, 8):
            new_image = pygame.Surface((32, 32)).convert_alpha()
            new_image.fill((0, 0, 0, 0))
            new_image.blit(all_2, (0, 0), (j*32, i*32+392, 32, 32))
            new_image = pygame.transform.smoothscale(new_image, (48, 48))
            fire_bullet.append(new_image)
    set_value('fire_bullet', fire_bullet)
    #滴弹
    drop_bullet = []
    for i in range(0, 16):
        new_image = pygame.Surface((16, 16)).convert_alpha()
        new_image.fill((0, 0, 0, 0))
        new_image.blit(all_2, (0, 0), (i*16, 456, 16, 16))
        new_image = pygame.transform.smoothscale(new_image, (24, 24))
        drop_bullet.append(new_image)
    set_value('drop_bullet', drop_bullet)
    #双星弹
    double_star_bullet = []
    for i in range(0, 8):
        new_image = pygame.Surface((32, 32)).convert_alpha()
        new_image.fill((0, 0, 0, 0))
        new_image.blit(all_2, (0, 0), (i*32, 488, 32, 32))
        new_image = pygame.transform.smoothscale(new_image, (48, 48))
        double_star_bullet.append(new_image)
    set_value('double_star_bullet', double_star_bullet)
    #光玉（大）
    big_light_bullet = []
    for i in range(0, 2):
        for j in range(0, 4):
            new_image = pygame.Surface((64, 72)).convert_alpha()
            new_image.fill((0, 0, 0, 0))
            new_image.blit(all_2, (0, 0), (j*64, i*72+520, 64, 72))
            new_image = pygame.transform.smoothscale(new_image, (96, 108))
            big_light_bullet.append(new_image)
    set_value('big_light_bullet', big_light_bullet)
    bulletVanish = pygame.image.load('resource/bullet/vanish_blue.png').convert_alpha()
    bulletVanish.set_alpha(96)
    bulletV = []
    for i in range(0,2):
        for j in range(0,4):
            bulletV.append(image(
                og = bulletVanish,
                size=(64,64),
                crop_area=(j*64,i*64,64,64)
            ))
    set_value('bulletsVanish', bulletV)


def loadImage():
    item = pygame.image.load('resource/image/item.png').convert_alpha()
    item_image = []
    for i in range(0, 16):
        item_image.append(image(
            og=item,
            size=(16,16),
            crop_area=(16*i,0,16,16),
            zoom=(16*magnitude,16*magnitude),
        ))
    item_image[7].set_alpha(120)
    set_value('item_image', item_image)
    sign = pygame.image.load('resource/HUD/sign.png').convert_alpha()
    lifesign = []
    boomsign = []
    for i in range(0,2):
        for j in range(0,6):
            new_image = image(og=sign,size=(32,40),crop_area=(j*32,i*40,32,40),zoom=(16*magnitude,20*magnitude))
            if not i:
                lifesign.append(new_image)
            else:
                boomsign.append(new_image)
    set_value('lifesign', lifesign)
    set_value('boomsign', boomsign)
    healthBar = pygame.image.load('resource/HUD/health.png').convert_alpha()
    new_image = pygame.Surface((216, 216)).convert_alpha()
    new_image.fill((0,0,0,0))
    new_image.blit(healthBar, (0, 0))
    set_value('healthbar', new_image)
    healthBar = pygame.image.load('resource/HUD/health_1.png').convert_alpha()
    new_image = pygame.Surface((216, 216)).convert_alpha()
    new_image.fill((0,0,0,0))
    new_image.blit(healthBar, (0, 0))
    set_value('healthbar_1', new_image)
    spell = pygame.image.load('resource/image/spellcardAttack.png').convert_alpha()
    new_image = pygame.Surface((128,16)).convert_alpha()
    new_image.fill((0,0,0,0))
    new_image.blit(spell, (0,0))
    new_image = pygame.transform.smoothscale(new_image, (256, 32)).convert_alpha()
    set_value('spellcardAttack', new_image)
    set_value('Cirno_Spell',image(
        og=pygame.image.load('resource/NPC/Cirno_Spell.png').convert_alpha(),
        size=(623,900),
        #zoom=(400,577)
    ))
    set_value('textbox',image(
        og=pygame.image.load('resource/text/textbox.png').convert_alpha(),
        size=(662,475)
    ))
    boss_effect_image = pygame.image.load('resource/image/boss_effect.png').convert_alpha()
    boss_effect = []
    for i in range(0, 3):
        boss_effect.append(image(
            og=boss_effect_image,
            size=(32,32),
            crop_area=(i*32,0,32,32),
        ))
    set_value('boss_effect_image', boss_effect)
    
    grid_image = pygame.Surface((40*magnitude,40*magnitude),pygame.SRCALPHA)
    pygame.draw.rect(grid_image,WHITE,(0,0,40*magnitude,40*magnitude),border_radius=10)
    pygame.draw.line(grid_image,(0,0,0,128),(6,12),(40*magnitude-6,12),2)
    pygame.draw.line(grid_image,(0,0,0,128),(6,40*magnitude-12),(40*magnitude-6,40*magnitude-12),2)
    pygame.draw.line(grid_image,(0,0,0,128),(12,6),(12,40*magnitude-6),2)
    pygame.draw.line(grid_image,(0,0,0,128),(40*magnitude-12,6),(40*magnitude-12,40*magnitude-6),2)
    set_value('grid_image',grid_image)
    
    test_image = pygame.Surface((40*magnitude,40*magnitude),pygame.SRCALPHA)
    pygame.draw.rect(test_image,WHITE,(0,0,40*magnitude,40*magnitude),border_radius=10)
    pygame.draw.polygon(test_image,(255,0,0,128),[(12,12),(12,40*magnitude-12),(40*magnitude-12,40*magnitude/2)])
    set_value('test_image',test_image)
    
    background_image = pygame.Surface((40*magnitude,40*magnitude),pygame.SRCALPHA)
    pygame.draw.rect(background_image,WHITE,(0,0,40*magnitude,40*magnitude),border_radius=10)
    pygame.draw.line(background_image,TEAL,(10,0),(10,40*magnitude),5)
    pygame.draw.line(background_image,TEAL,(40*magnitude-10,0),(40*magnitude-10,40*magnitude),5)
    set_value('background_image',background_image)
    
    new_image = pygame.image.load('resource/image/transparent.jpg').convert_alpha()
    new_image = pygame.transform.rotozoom(new_image,0,0.4)
    new_image.fill((0,0,0))
    set_value('transparent_image',new_image)
    
    loadMenuImage()
    loadUIImage()
    loadPauseText()
    loadBackgroundImage()
    loadBulletImage()
    loadEnemyImage()
    loadPlayerImage()


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
'''
from PIL import Image, ImageTk

def edit_mode_loadImage():
    name_lists=['folder','wait','repeat','object','bullet','stagegroup','stage','action','enemy','audio','sound']
    lists={}
    for i in range(len(name_lists)):
        #print('d'+name_lists[i]+'.png')
        img=Image.open('resource/icon/'+name_lists[i]+'.png')
        img=img.resize((40,40),Image.LANCZOS)
        img1=img.resize((20,20),Image.LANCZOS)
        img=ImageTk.PhotoImage(img)
        img1=ImageTk.PhotoImage(img1)
        lists[name_lists[i]]=img
        lists[name_lists[i]+'small']=img1
    return lists
'''