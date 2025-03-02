import pygame
import functions
import SoundEffect
import effect
import player
import Plot

from pygame.locals import *
from const import *
from math import *
from random import *
from global_var import *

pygame.mixer.init()
class MENU():
    def __init__(self):
        self.image = pygame.image.load('resource/image/menu_back.jpg').convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (SCREENWIDTH, SCREENHEIGHT))
        #self.title = pygame.image.load('resource/font/title.png').convert_alpha()
        self.npc = get_value('Cirno_pos')
        self.selectIndex = 0
        self.selectRank = 0
        self.wait=100
        self.pages = [MenuSelectPage(self)]
        self.lastFrame = 0
        pygame.mixer.music.stop()
        pygame.mixer.music.load("resource/BGM/Concentration.mp3")
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play(-1)
        self.effects = pygame.sprite.Group()

    def update(self, screen, pressed_keys, last_pressed_keys):
        screen.blit(self.image, (0, 0))
        self.pages[len(self.pages)-1].update(screen, pressed_keys, last_pressed_keys)
        self.effects.update(screen)
        self.lastFrame = (self.lastFrame+1)%100
        if self.lastFrame%2==0:
            new_effect = effect.Particle((randint(0,255),randint(0,255),randint(0,255,)),(randint(0,1200),-4),randint(4,8))
            new_effect.maxFrame = randint(100,200)
            new_effect.speedx=randint(-4,-1)
            new_effect.speedy=randint(1,6)
            self.effects.add(new_effect)
        
            
    
class MenuSelectPage():
    def __init__(self,master):
        self.master=master
        self.image = get_value('Select_Image')
        self.title = get_value('Title_Image').copy()
        self.ts = self.title.copy()
        self.bg = pygame.Surface((1000,1000))
        self.ts.blit(self.bg,(0,0),special_flags=BLEND_RGBA_MULT)
        self.selectIndex = 0
        self.angle = 0
        self.npc = pygame.transform.rotozoom(get_value('Cirno_pos')[4],0,0.6).convert_alpha()
        
    def update(self, screen, presssed_keys, keys_last):
        self.selection(presssed_keys, keys_last)
        self.draw(screen)
        
    def selection(self, pressed_keys, last_keys):
        if pressed_keys[K_UP] and not last_keys[K_UP] and not self.master.wait:
            if self.selectIndex:
                self.selectIndex -= 1
                SoundEffect.play('select_sound',0.35,True)
            else:
                SoundEffect.play('invalid_sound',0.5,True)
        if pressed_keys[K_DOWN] and not last_keys[K_DOWN] and not self.master.wait:
            if self.selectIndex < 4:
                self.selectIndex += 1
                SoundEffect.play('select_sound',0.35,True)
            else:
                SoundEffect.play('invalid_sound',0.5,True)
        if pressed_keys[K_z] and not last_keys[K_z]:
            if self.master.wait<99 and self.master.wait:
                self.master.wait = 0
                for i in range(0,15):
                    self.image[i].set_alpha(255)
                self.ts.set_alpha(255)
                self.title.set_alpha(255)
                return
            if self.master.wait:
                return
            if self.selectIndex == 0:
                self.master.pages.append(LevelSelectPage(self.master))
                SoundEffect.play('ok_sound',0.35,True)
            elif self.selectIndex == 1:
                self.master.pages.append(ModSelectPage(self.master))
                SoundEffect.play('ok_sound',0.35,True)
            elif self.selectIndex == 4:
                set_value('running',False)
        if pressed_keys[K_ESCAPE] and not last_keys[K_ESCAPE] and self.selectIndex!=4:
            self.selectIndex = 4
            SoundEffect.play('cancel_sound',0.35,True)
                
    def draw(self, screen):
        self.angle = (self.angle+2)%360
        if self.master.wait:
            self.master.wait -= 1
            for i in range(0,15):
                self.image[i].set_alpha(255-self.master.wait*2)
            self.ts.set_alpha(255-self.master.wait*2)
            self.title.set_alpha(255-self.master.wait*2)
        else:
            for i in range(0,15):
                self.image[i].set_alpha(255)
        for i in range(0, 5):
            if i == self.selectIndex:
                screen.blit(self.image[i*2], (32, (i+1)*75+200))
            else:
                screen.blit(self.image[i*2+1], (30, (i+1)*75+200))
        for i in range(-1,2,2):
            for j in range(-1,2,2):
                screen.blit(self.ts, (200+i*2, 50+j*2))
        screen.blit(self.title, (200, 50))
        functions.drawImage(self.npc,(700,500),self.angle,screen)

import os
for x in os.listdir('mods/'):
    if x.endswith(".sba_dat"):
        print(x)
import Nodes
class ModSelectPage():
    def __init__(self,master):
        self.master = master
        self.title = get_value('Mod_Image').copy()
        self.tb = self.title.copy()
        self.bg = pygame.Surface((1000,1000))
        self.tb.blit(self.bg,(0,0),special_flags=BLEND_RGBA_MULT)
        self.angle=0
        self.ty = 0
        self.y = 0
        self.select_idx = -1
        self.lists = []
        self.text_lists = []
        for x in os.listdir('mods/'):
            if x.endswith(".sba_dat"):
                self.lists.append(x.split('.')[0])
        for i in self.lists:
            self.text_lists.append(TitleFont.render(i,True,(255,255,255)))
            self.text_lists.append(TitleFont.render(i,True,(0,0,0)))
        if self.lists:
            self.select_idx = 0
        #print(len(self.text_lists))
        self.select_rect = pygame.Surface((800,50)).convert_alpha()
        self.select_rect.fill((255,255,255,128))
        
    def update(self, screen, pressed_keys, last_keys):
        self.selection(pressed_keys, last_keys)
        self.draw(screen)
        
    def selection(self, pressed_keys, last_keys):
        self.y += (self.ty-self.y)/5
        if pressed_keys[K_UP] and not last_keys[K_UP]:
            if self.select_idx>0:
                self.select_idx -= 1
                SoundEffect.play('select_sound',0.35,True)
                self.ty = 100*self.select_idx
            else:
                SoundEffect.play('invalid_sound',0.5,True)
        if pressed_keys[K_DOWN] and not last_keys[K_DOWN]:
            if self.select_idx < len(self.lists)-1 and self.select_idx!=-1:
                self.select_idx += 1
                SoundEffect.play('select_sound',0.35,True)
                self.ty = 100*self.select_idx
            else:
                SoundEffect.play('invalid_sound',0.5,True)
        if pressed_keys[K_z] and not last_keys[K_z] and self.select_idx!=-1:
            self.master.pages.append(LevelSelectPage(self.master, Nodes.load(self.lists[self.select_idx])))
            SoundEffect.play('ok_sound',0.35,True)
        if pressed_keys[K_ESCAPE] and not last_keys[K_ESCAPE]:
            self.master.pages.pop()
            SoundEffect.play('cancel_sound',0.35,True)
            del self
        
    def draw(self, screen):
        self.angle = (self.angle+2)%360
        self.bg.fill(functions.get_rainbow_color(radians(self.angle)))
        self.title = get_value('Mod_Image').copy()
        self.title.blit(self.bg,(0,0),special_flags=BLEND_RGB_MULT)
        
        if self.lists:
            a = self.select_idx-1
            b = self.select_idx+1
            self.text_lists[self.select_idx*2].set_alpha(255)
            self.text_lists[self.select_idx*2+1].set_alpha(255)
            for i in range(1,len(self.lists)+1):
                if a>=0:
                    self.text_lists[a*2].set_alpha(255-i*45)
                    self.text_lists[a*2+1].set_alpha(255-i*45)
                if b<len(self.lists):
                    self.text_lists[b*2].set_alpha(255-i*45)
                    self.text_lists[b*2+1].set_alpha(255-i*45)
                a-=1
                b+=1
        for i in range(-1,2,2):
            for j in range(-1,2,2):
                screen.blit(self.tb, (420+i*2, 20+j*2))
        screen.blit(self.title, (420, 20))
        for i in range(len(self.text_lists)//2):
            #print(i)
            for j in range(-1,2,2):
                for k in range(-1,2,2):
                    screen.blit(self.text_lists[i*2+1], (100+j*2, 100+k*2+i*100-self.y+100))
            screen.blit(self.text_lists[i*2], (100, 100+i*100-self.y+100))
        select_rect = pygame.Surface((self.text_lists[self.select_idx*2].get_width()+10, self.text_lists[self.select_idx*2].get_height()+10)).convert_alpha()
        select_rect.fill((255,255,255,128))
        screen.blit(select_rect, (100, 200))
        

class LevelSelectPage():
    def __init__(self,master,rank_lists=[]):
        self.master = master
        self.image = get_value('Rank_Select')
        self.title = get_value('Rank_Image').copy()
        self.tb = self.title.copy()
        self.bg = pygame.Surface((1000,1000))
        self.tb.blit(self.bg,(0,0),special_flags=BLEND_RGBA_MULT)
        self.rank_lists = rank_lists
        if self.rank_lists != []:
            for i in self.rank_lists[0].children:
                if i.name == 'Classes':
                    self.rank_lists = i.children
                    break
        print(len(self.rank_lists))
        self.tx = 0
        self.ty = 0
        self.x = 0
        self.y = 0
        self.angle = 0
    
    def update(self, screen, pressed_keys, last_keys):
        self.x += (self.tx-self.x)/10
        self.y += (self.ty-self.y)/10
        self.selection(pressed_keys, last_keys)
        self.draw(screen)
        
    def selection(self, pressed_keys, last_keys):
        if pressed_keys[K_LEFT] and not last_keys[K_LEFT]:
            if self.master.selectRank:
                self.master.selectRank -= 1
                self.tx = 1000*self.master.selectRank
                self.ty = 500*self.master.selectRank
                SoundEffect.play('select_sound',0.35,True)
            else:
                SoundEffect.play('invalid_sound',0.5,True)
        if pressed_keys[K_RIGHT] and not last_keys[K_RIGHT]:
            if self.master.selectRank < 4:
                self.master.selectRank += 1
                self.tx = 1000*self.master.selectRank
                self.ty = 500*self.master.selectRank
                SoundEffect.play('select_sound',0.35,True)
            else:
                SoundEffect.play('invalid_sound',0.5,True)
        if pressed_keys[K_z] and not last_keys[K_z]:
            set_value('rank_level',self.master.selectRank)
            if self.rank_lists != []:
                set_value('load_level',True)
                self.master.node_lists = self.rank_lists[self.master.selectRank].children
            self.master.pages.append(PlayerSelectPage(self.master))
            SoundEffect.play('ok_sound',0.35,True)
        if pressed_keys[K_ESCAPE] and not last_keys[K_ESCAPE]:
            self.master.selectRank=0
            self.master.pages.pop()
            SoundEffect.play('cancel_sound',0.35,True)
            del self
            
            
    def draw(self, screen):
        self.angle = (self.angle+2)%360
        self.bg.fill(functions.get_rainbow_color(radians(self.angle)))
        self.title = get_value('Rank_Image').copy()
        self.title.blit(self.bg,(0,0),special_flags=BLEND_RGB_MULT)
        for i in range(-1,2,2):
            for j in range(-1,2,2):
                screen.blit(self.tb, (450+i*2, 20+j*2))
        screen.blit(self.title,(450,20))
        for i in range(0,5):
            if i == self.master.selectRank:
                screen.blit(self.image[i*2],((i+1)*1000-self.x-750,(i+1)*500-self.y-200))
            else:
                screen.blit(self.image[i*2+1],((i+1)*1000-self.x-750,(i+1)*500-self.y-200))

class PlayerSelectPage():
    def __init__(self,master):
        self.master = master
        self.Reimu_Image = get_value('Reimu_pos')[0]
        self.Marisa_Image = get_value('Marisa_pos')[0]
        self.bs = pygame.Surface((1000,1000))
        self.bs.fill((0,0,0,0))
        self.es = self.bs.copy()
        self.R_S = self.Reimu_Image.copy()
        self.R_S.blit(self.bs, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
        self.M_S = self.Marisa_Image.copy()
        self.M_S.blit(self.bs, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
        self.image = [self.Reimu_Image, self.R_S, self.Marisa_Image, self.M_S]
        self.selectIndex = 0
        self.x=0
        self.tx=0
        self.title = get_value('Player_Image').copy()
        self.ts = self.title.copy()
        self.ts.blit(self.bs,(0,0),special_flags=pygame.BLEND_RGBA_MULT)
        self.angle = 0
        
    def update(self, screen, pressed_keys, last_keys):
        self.x += (self.tx-self.x)/5
        self.selection(pressed_keys, last_keys)
        self.draw(screen)
        
    def selection(self, pressed_keys, last_keys):
        if pressed_keys[K_LEFT] and not last_keys[K_LEFT]:
            if self.selectIndex:
                self.selectIndex -= 1
                self.tx = 0
                SoundEffect.play('select_sound',0.35,True)
            else:
                SoundEffect.play('invalid_sound',0.5,True)
        if pressed_keys[K_RIGHT] and not last_keys[K_RIGHT]:
            if self.selectIndex < 1:
                self.selectIndex += 1
                self.tx=-1500
                SoundEffect.play('select_sound',0.35,True)
            else:
                SoundEffect.play('invalid_sound',0.5,True)
        if pressed_keys[K_z] and not last_keys[K_z]:
            set_value('player_id',self.selectIndex+1)
            SoundEffect.play('ok_sound',0.35,True)
            self.master.pages.append(PlayerInfoPage(self.master, self.selectIndex+1))
        if pressed_keys[K_ESCAPE] and not last_keys[K_ESCAPE]:
            self.master.pages.pop()
            SoundEffect.play('cancel_sound',0.35,True)
            del self
            
    def draw(self, screen):
        self.angle = (self.angle+2)%360
        self.es.fill(functions.get_rainbow_color(radians(self.angle)))
        self.title = get_value('Player_Image').copy()
        self.title.blit(self.es,(0,0),special_flags=pygame.BLEND_RGB_MULT)
        for i in range(-1,2,2):
            for j in range(-1,2,2):
                screen.blit(self.ts, (400+i*2, 20+j*2))
        screen.blit(self.title, (400, 20))
        for i in range(0,2):
            if i == self.selectIndex:
                screen.blit(self.image[i*2],(1500*i+self.x+300,50))
            else:
                screen.blit(self.image[i*2+1],(1500*i+self.x+300,50))

class PlayerInfoPage():
    def __init__(self,master,player_id):
        self.master = master
        self.player_id = player_id
        if self.player_id == 1:
            self.image = pygame.transform.rotozoom(get_value('Reimu_pos')[0], 0, 0.8)
            self.info = get_value('PlayerInfo_Image_Reimu')
        elif self.player_id == 2:
            self.image = pygame.transform.rotozoom(get_value('Marisa_pos')[0], 0, 0.8)
            self.info = get_value('PlayerInfo_Image_Marisa')
        self.selectIndex = 0
        
    def update(self, screen, pressed_keys, last_keys):
        self.selection(pressed_keys, last_keys)
        self.draw(screen)
        
    def selection(self, pressed_keys, last_keys):
        if pressed_keys[K_z] and not last_keys[K_z]:
            set_value('menu', False)
            set_value('battle_music', True)
            SoundEffect.play('ok_sound',0.35,True)
            functions.initialize()
        if pressed_keys[K_ESCAPE] and not last_keys[K_ESCAPE]:
            self.master.pages.pop()
            SoundEffect.play('cancel_sound',0.35,True)
            del self

    def draw(self, screen):
        screen.blit(self.info, (210, 50))
        screen.blit(self.image,(5,100))

angle = 0

def display_UI(screen,player):
    background = get_value('background')
    
    fps = middlefont.render("FPS: %.1f" % (get_value('fps')), True, WHITE)
    fps_shadow = middlefont.render("FPS: %.1f" % (get_value('fps')), True, BLACK)


    bullet_count = numfont.render("BULLETS: %d" % (get_value('number of bullets')), True, WHITE)
    bullet_count_shadow = numfont.render("BULLETS: %d" % (get_value('number of bullets')), True, BLACK)

    frame = middlefont.render("F: %d" % (get_value('frame')), True, WHITE)
    frame_shadow = middlefont.render("F: %d" % (get_value('frame')), True, BLACK)

    rank = get_value('Rank_Show')[get_value('rank_level')]

    #showscore

    hi_score_text = numfont.render("HiScore", True, GRAY)
    hi_score_text_shadow = numfont.render("HiScore", True, BLACK)
    score_text = numfont.render("Score", True, WHITE)
    score_text_shadow = numfont.render("Score", True, BLACK)
    minimumStep = 1
    score_show = get_value('score')
    hi_score_show = get_value('hi_score')
    tempScore = player.score - score_show
    if tempScore <= 1:
        score_show = player.score
    else:
        while minimumStep <= tempScore:
            minimumStep = minimumStep*10+1
        minimumStep = round((minimumStep-1)/10)
        score_show += minimumStep
    set_value('score', score_show)
    if hi_score_show < score_show:
        hi_score_show = score_show
        set_value('hi_score', score_show)
    score_show = functions.returnScoreFormat(score_show)
    hi_score_show = functions.returnScoreFormat(hi_score_show)
    score = numfont.render(score_show, True, WHITE)
    score_shadow = numfont.render(score_show, True, BLACK)
    hi_score = numfont.render(hi_score_show, True, GRAY)
    hi_score_shadow = numfont.render(hi_score_show, True, BLACK)

    #life and boom
    lifesign = get_value('lifesign')
    life = get_value('player_HP')
    lifetext = textfont.render("剩余人数", True, PINK)
    lifeshadow = textfont.render("剩余人数", True, BLACK)
    piecetext = midtextfont.render('(碎片数)', True, WHITE)
    piecetextshadow = midtextfont.render('(碎片数)', True, BLACK)
    boomsign = get_value('boomsign')
    boom = get_value('player_Boom')
    boomtext = textfont.render("SpellCard", True, GREEN)
    boomshadow = textfont.render("SpellCard", True, BLACK)

    #firelevel, getscore and graze

    level = get_value('player_firelevel')
    power = get_value('player_power')
    powertext = textfont.render("灵力", True, ORANGE)
    powershadow = textfont.render("灵力", True, BLACK)
    if power%100!=0:
        if power%100<10:
            powerNum = numfont.render(str(level)+'.0'+str(power%100)+'/4.00', True, ORANGE)
            powerShadow = numfont.render(str(level)+'.0'+str(power%100)+'/4.00', True, BLACK)
        else:
            powerNum = numfont.render(str(level)+'.'+str(power%100)+'/4.00', True, ORANGE)
            powerShadow = numfont.render(str(level)+'.'+str(power%100)+'/4.00', True, BLACK)
    else:
        powerNum = numfont.render(str(level)+'.00'+'/4.00', True, ORANGE)
        powerShadow = numfont.render(str(level)+'.00'+'/4.00', True, BLACK)

    getscoretext = textfont.render("最大得分", True, LIGHTBLUE)
    getscoreshadow = textfont.render("最大得分", True, BLACK)
    maxgetscore = get_value('maximum_score')
    maxgetscore = functions.returnScoreFormat(maxgetscore)
    getscorenum = numfont.render(maxgetscore, True, LIGHTBLUE)
    getscorenumshadow = numfont.render(maxgetscore, True, BLACK)


    grazeText = textfont.render('Graze', True, GRAY)
    graze_shadow = textfont.render('Graze', True, BLACK)
    grazeNum = numfont.render('%d' % get_value('grazeNum'), True, WHITE)
    grazeNum_shadow = numfont.render('%d' % get_value('grazeNum'), True, BLACK)
    
    

    #draw UI sign
    screen.blit(background[0], (0, 0))
    screen.blit(background[1], (32*magnitude, 0))
    screen.blit(background[2], (32*magnitude, 464*magnitude))
    screen.blit(background[3], (416*magnitude, 0))

    

    for i in range(-1, 2):
        for j in range(-1, 2):
            screen.blit(frame_shadow, ((2+i*1)*magnitude, j*1*magnitude))
            
            screen.blit(hi_score_text_shadow, ((432+i*1)*magnitude, (48+j*1)*magnitude))#24
            screen.blit(hi_score_shadow, hi_score_shadow.get_rect(topright=((622+i*1)*magnitude, (48+j*1)*magnitude)))
            screen.blit(score_text_shadow, ((432+i*1)*magnitude, (76+j*1)*magnitude))
            screen.blit(score_shadow, score_shadow.get_rect(topright=((622+i*1)*magnitude, (76+j*1)*magnitude)))

            screen.blit(lifeshadow, ((432+i*1)*magnitude, (108+j*1)*magnitude))
            screen.blit(piecetextshadow, ((528+i*1)*magnitude, (128+j*1)*magnitude))
            screen.blit(boomshadow, ((432+i*1)*magnitude, (147+j*1)*magnitude))
            screen.blit(piecetextshadow, ((528+i*1)*magnitude, (167+j*1)*magnitude))

            screen.blit(powershadow, ((464+i*1)*magnitude, (195+j*1)*magnitude))
            screen.blit(powerShadow, powerShadow.get_rect(topright=((622+i*1)*magnitude, (192+j*1)*magnitude)))
            screen.blit(getscoreshadow, ((464+i*1)*magnitude, (221+j*1)*magnitude))
            screen.blit(getscorenumshadow, getscorenumshadow.get_rect(topright=((622+i*1)*magnitude, (218+j*1)*magnitude)))
            screen.blit(graze_shadow, ((464+i*1)*magnitude, (247+j*1)*magnitude))
            screen.blit(grazeNum_shadow, grazeNum_shadow.get_rect(topright=((622+i*1)*magnitude, (247+j*1)*magnitude)))

            screen.blit(get_value('titleShadow'), ((450+i*1)*magnitude, (270+j*1)*magnitude))
            #screen.blit(bullet_count_shadow, ((425+i*1)*magnitude, (457+j*1)*magnitude))
            screen.blit(fps_shadow, ((570+i*1)*magnitude, (460+j*1)*magnitude))

    screen.blit(rank, (500*magnitude, 28*magnitude))
    screen.blit(hi_score_text, (432*magnitude, 48*magnitude))
    screen.blit(hi_score, hi_score.get_rect(topright=(622*magnitude, 48*magnitude)))
    screen.blit(score_text, (432*magnitude, 76*magnitude))
    screen.blit(score, score.get_rect(topright=(622*magnitude, 76*magnitude)))
    ######################################
    #pygame.draw.line(screen, WHITE, (840, 195), (1260, 195), 3)
    screen.blit(lifetext, (432*magnitude, 108*magnitude))
    for i in range (0,8):
        if life-1-i >= 1:
            sign = lifesign[5]
        elif life-1-i >= 0.7:
            sign = lifesign[4]
        elif life-1-i >= 0.5:
            sign = lifesign[3]
        elif life-1-i >= 0.3:
            sign = lifesign[2]
        elif life-1-i >= 0.1:
            sign = lifesign[1]
        else:
            sign = lifesign[0]
        screen.blit(sign, ((i*14+517)*magnitude, 109*magnitude))
            
    screen.blit(piecetext, (528*magnitude, 128*magnitude))
    screen.blit(boomtext, (432*magnitude, 147*magnitude))
    for i in range (0,8):
        if boom-i >= 1:
            sign = boomsign[5]
        elif boom-i >= 0.7:
            sign = boomsign[4]
        elif boom-i >= 0.5:
            sign = boomsign[3]
        elif boom-i >= 0.3:
            sign = boomsign[2]
        elif boom-i >= 0.1:
            sign = boomsign[1]
        else:
            sign = boomsign[0]
        screen.blit(sign, ((i*14+517)*magnitude, 148*magnitude))
    screen.blit(piecetext, (528*magnitude, 167*magnitude))
    ########################################
    #pygame.draw.line(screen, WHITE, (840, 330), (1260, 330), 2)
    screen.blit(get_value('item_image')[0], (440*magnitude, 195*magnitude))
    screen.blit(powertext, (464*magnitude, 195*magnitude))
    screen.blit(powerNum, powerNum.get_rect(topright=(622*magnitude, 192*magnitude)))
    screen.blit(get_value('item_image')[1], (440*magnitude, 221*magnitude))
    screen.blit(getscoretext, (464*magnitude, 221*magnitude))
    screen.blit(getscorenum, getscorenum.get_rect(topright=(622*magnitude, 218*magnitude)))
    screen.blit(grazeText, (464*magnitude, 247*magnitude))
    screen.blit(grazeNum, grazeNum.get_rect(topright=(622*magnitude, 247*magnitude)))
    #####################################
    #pygame.draw.line(screen, WHITE, (840, 520), (1260, 520), 2)
    #screen.blit(fuka, fuka.get_rect(center=(1200, 600)))
    screen.blit(get_value('titleImage1'), (535*magnitude, 370*magnitude))
    screen.blit(get_value('titleImage'), (495*magnitude,330*magnitude))
    screen.blit(get_value('title'), (450*magnitude, 270*magnitude))
    #screen.blit(bullet_count, (425*magnitude, 457*magnitude))
    screen.blit(fps, (570*magnitude, 460*magnitude))
    #screen.blit(frame_shadow, (7, 1))
    screen.blit(frame, (2*magnitude, 0))
    global angle
    angle += 1
    if angle >= 360:
        angle = 0
    if not get_value('boss_alive'):
        #a = 1/0
        return
    else:
        pygame.draw.rect(screen, WHITE, (32*magnitude, 470*magnitude, 384*magnitude, 8*magnitude))
        if get_value('show_health'):
            h = get_value('boss_health')
            mh = get_value('boss_maxhealth')
            sh = get_value('boss_spellhealth')
            #print(h,mh,sh)
            pygame.draw.rect(screen, RED, (32*magnitude, 470*magnitude, h/mh*384*magnitude, 8*magnitude))
            pygame.draw.rect(screen, functions.get_rainbow_color(radians(angle)), (32*magnitude, 470*magnitude, sh/mh*384*magnitude if h>sh else h/mh*384*magnitude, 8*magnitude))
            health_text_shadow = middlefont.render('%.2f'%(h/mh*100 if h/mh*100<=100 else 100)+'%', True, BLACK)
            health_text = middlefont.render('%.2f'%(h/mh*100 if h/mh*100<=100 else 100)+'%', True, WHITE)
            if h > sh:
                pygame.draw.rect(screen, BLUE, (sh/mh*384*magnitude+32*magnitude, 470*magnitude, 2*magnitude, 8*magnitude))
            for i in range(-1,2):
                for j in range(-1,2):
                    screen.blit(health_text_shadow, ((420+i*1)*magnitude, (468+j*1)*magnitude))
            screen.blit(health_text, (420*magnitude, 468*magnitude))
            
def pauseScreen(screen,idx):
    screen.blit(get_value('pause_screen'), (32*magnitude,16*magnitude))
    screen.blit(get_value('sword'),(-140,100*magnitude))
    
    if get_value('finish'):
        screen.blit(get_value('finish_surface'), (70, 100*magnitude))
        screen.blit(get_value('final_result'), (140, 175*magnitude))

    elif get_value('player_alive'):
        screen.blit(get_value('pause_surface'), (70, 100*magnitude))
        if not idx:
            screen.blit(get_value('return_game_surface'), (140, 175*magnitude))
        else:
            screen.blit(get_value('return_game_unselected_surface'), (130, 175*magnitude))

    else:
        screen.blit(get_value('gameover_surface'), (70, 100*magnitude))
        if not idx:
            screen.blit(get_value('retry_surface'), (140, 175*magnitude))
        else:
            screen.blit(get_value('retry_unselected_surface'), (130, 175*magnitude))
    if idx==1:
        screen.blit(get_value('return_title_surface'), (140, 250*magnitude))
    else:
        screen.blit(get_value('return_title_unselected_surface'), (130, 250*magnitude))
    if idx==2:
        screen.blit(get_value('restart_surface'), (140, 325*magnitude))
    else:
        screen.blit(get_value('restart_unselected_surface'), (130, 325*magnitude))
