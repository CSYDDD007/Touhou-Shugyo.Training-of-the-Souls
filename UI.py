import pygame
import functions
import SoundManager
import ImageManager
import effect

from pygame.locals import *
from const import *
from math import *
from random import *
from global_var import *

pygame.mixer.init()
class MENU():
    def __init__(self, intro=True):
        self.image = pygame.image.load('resource/image/menu_back.jpg').convert_alpha()
        self.intro_image = pygame.image.load('resource/image/intro.png').convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (640,480))
        self.intro = intro
        self.pages = [MenuSelectPage(self)]
        self.lastFrame = 0
        SoundManager.BGM_Play("Menu", -1, 1)
        self.effects = pygame.sprite.Group()
        self.mod_text = ImageManager.stot("Regular_font", 24, "Selected Mod: None", WHITE, BLACK, 1)
        self.mod_path = ''
        
    def load_mod_text(self, mod_path):
        self.mod_text = ImageManager.stot("Regular_font", 24, "Selected Mod: {}".format(mod_path), WHITE, BLACK, 1)
        self.mod_path = mod_path

    def update(self, screen, pressed_keys, last_pressed_keys):
        if self.intro and pressed_keys[K_z]:
            self.intro = False
            SoundManager.play('ok_sound',0.35,True)
        if self.intro:
            screen.fill(WHITE)
            screen.blit(self.intro_image, (0, 0))
            return
        screen.blit(self.image, (0, 0))
        if not get_value('entering_game'):
            self.pages[-1].update(screen, pressed_keys, last_pressed_keys)
        screen.blit(self.mod_text, (0, 0))
        self.effects.update(screen)
        self.lastFrame = (self.lastFrame+1)%100
        if self.lastFrame%2==0:
            new_effect = effect.SpellLeaf(0,uniform(1.0,2.0),(randint(0, 720),-30),randint(90,160),randint(3,5), (randint(0,255),randint(0,255),randint(0,255)))
            new_effect.omiga = 3
            self.effects.add(new_effect)
            
    
class MenuSelectPage():
    def __init__(self,master):
        self.master=master
        self.image = get_value('Select_Image')
        self.title_1 = ImageManager.getImage("Menu", "Title_1")
        self.title_2 = ImageManager.getImage("Menu", "Title_2")
        self.r1 = self.title_1.get_rect(midtop=(320, 30))
        self.r2 = self.title_2.get_rect(midtop=(320, 80))
        self.selectIndex = 0
        self.angle = 0
        self.wait = 10
        self.npc = pygame.transform.rotozoom(ImageManager.getImage("Portrait","Cirno")[4],0,0.7).convert_alpha()
        self.button_dicts = {"Game":-200, "Practice":-250, "Mod":-300, "Option":-350, "Quit":-400}
        
    def update(self, screen, pressed_keys, last_keys):
        self.selection(pressed_keys, last_keys)
        self.draw(screen)
        
    def selection(self, pressed_keys, last_keys):
        if self.wait:
            self.wait -= 1
            return
        if pressed_keys[K_UP] and not last_keys[K_UP]:
            if self.selectIndex:
                self.selectIndex -= 1
                SoundManager.play('select_sound',0.35,True)
            else:
                SoundManager.play('invalid_sound',0.5,True)
        if pressed_keys[K_DOWN] and not last_keys[K_DOWN]:
            if self.selectIndex < 4:
                self.selectIndex += 1
                SoundManager.play('select_sound',0.35,True)
            else:
                SoundManager.play('invalid_sound',0.5,True)
        if pressed_keys[K_z] and not last_keys[K_z]:
            if self.selectIndex in (0, 1):
                if self.master.mod_path != '':
                    self.master.pages.append(RankSelectPage(self.master, Nodes.load(self.master.mod_path), self.selectIndex==1))
                    SoundManager.play('ok_sound',0.35,True)
                    self.master.selectIndex = self.selectIndex
                else:
                    SoundManager.play('invalid_sound',0.5,True)
            elif self.selectIndex == 2:
                self.master.pages.append(ModSelectPage(self.master))
                SoundManager.play('ok_sound',0.35,True)
                self.master.selectIndex = self.selectIndex
            elif self.selectIndex == 3:
                self.master.pages.append(OptionMenuPage(self.master))
                SoundManager.play('ok_sound',0.35,True)
                self.master.selectIndex = self.selectIndex
            elif self.selectIndex == 4:
                set_value('running',False)
        if pressed_keys[K_ESCAPE] and not last_keys[K_ESCAPE] and self.selectIndex!=5:
            self.selectIndex = 4
            SoundManager.play('cancel_sound',0.35,True)
                
    def draw(self, screen):
        self.angle = (self.angle+2)%360
        idx = 0
        for i in self.button_dicts:
            if idx==self.selectIndex:
                self.button_dicts[i]+=(30-self.button_dicts[i])/10
            else:
                self.button_dicts[i]-=(self.button_dicts[i])/10
            screen.blit(ImageManager.getImage("Menu", i)[idx==self.selectIndex], (30+self.button_dicts[i], 180+60*idx))
            idx+=1
        screen.blit(self.title_1, self.r1)
        screen.blit(self.title_2, self.r2)
        functions.drawImage(self.npc,(500,330),self.angle,screen)
        
class OptionMenuPage():
    def __init__(self, master):
        self.master = master
        self.selectIndex = 0
        BGM_Volume = get_value('BGM_Volume')
        SE_Volume = get_value('SE_Volume')
        self.change_bgm(BGM_Volume)
        self.change_se(SE_Volume)
        self.lastFrame = 0
        self.button_dicts = {"BGM Volume":-250, "SE Volume":-200, "Default":-150, "Quit":-100}
        self.num_lists = [-250, -200]
        
    def update(self, screen, pressed_keys, last_keys):
        self.lastFrame += 1
        if self.lastFrame == 150:
            self.lastFrame = 0
            SoundManager.play('miss_sound',1.0,True)
        self.selection(pressed_keys, last_keys)
        self.draw(screen)
        
    def change_bgm(self, BGM_Volume):
        self.BGM_Text = [ImageManager.stot("Regular_font", 32, '{}%'.format(BGM_Volume), (255,255,255), (0,0,0), 2), ImageManager.stot("Regular_font", 32, '{}%'.format(BGM_Volume), (255,255,255), (0,0,0), 2)]
        self.BGM_Text[0].blit(ImageManager.getImage("Texture", 1), (0,0), special_flags=3)
        self.BGM_Rect = self.BGM_Text[0].get_rect(topright=(600,80))
    
    def change_se(self, SE_Volume):
        self.SE_Text = [ImageManager.stot("Regular_font", 32, '{}%'.format(SE_Volume), (255,255,255), (0,0,0), 2), ImageManager.stot("Regular_font", 32, '{}%'.format(SE_Volume), (255,255,255), (0,0,0), 2)]
        self.SE_Text[0].blit(ImageManager.getImage("Texture", 1), (0,0), special_flags=3)
        self.SE_Rect = self.SE_Text[0].get_rect(topright=(600,160))
        
    def selection(self, pressed_keys, last_keys):
        BGM_Volume = get_value('BGM_Volume')
        SE_Volume = get_value('SE_Volume')
        if pressed_keys[K_UP] and not last_keys[K_UP]:
            if self.selectIndex:
                self.selectIndex -= 1
                SoundManager.play('select_sound',0.35,True)
            else:
                SoundManager.play('invalid_sound',0.5,True)
        if pressed_keys[K_DOWN] and not last_keys[K_DOWN]:
            if self.selectIndex < 3:
                self.selectIndex += 1
                SoundManager.play('select_sound',0.35,True)
            else:
                SoundManager.play('invalid_sound',0.5,True)
        if self.selectIndex == 0 and pressed_keys[K_LEFT] and not last_keys[K_LEFT]:
            if BGM_Volume:
                BGM_Volume -= 5
                set_value('BGM_Volume',BGM_Volume)
                self.change_bgm(BGM_Volume)
                SoundManager.play('ok_sound',0.35,True)
                pygame.mixer.music.set_volume(BGM_Volume/100)
            else:
                SoundManager.play('invalid_sound',0.5,True)
                
        if self.selectIndex == 0 and pressed_keys[K_RIGHT] and not last_keys[K_RIGHT]:
            if BGM_Volume < 100:
                BGM_Volume += 5
                set_value('BGM_Volume',BGM_Volume)
                self.change_bgm(BGM_Volume)
                SoundManager.play('ok_sound',0.35,True)
                pygame.mixer.music.set_volume(BGM_Volume/100)
            else:
                SoundManager.play('invalid_sound',0.5,True)
                
        if self.selectIndex == 1 and pressed_keys[K_LEFT] and not last_keys[K_LEFT]:
            if SE_Volume:
                SE_Volume -= 5
                set_value('SE_Volume',SE_Volume)
                self.change_se(SE_Volume)
                SoundManager.play('ok_sound',0.35,True)
            else:
                SoundManager.play('invalid_sound',0.5,True)
                
        if self.selectIndex == 1 and pressed_keys[K_RIGHT] and not last_keys[K_RIGHT]:
            if SE_Volume < 100:
                SE_Volume += 5
                set_value('SE_Volume',SE_Volume)
                self.change_se(SE_Volume)
                SoundManager.play('ok_sound',0.35,True)
            else:
                SoundManager.play('invalid_sound',0.5,True)
                
        if self.selectIndex == 2 and pressed_keys[K_z] and not last_keys[K_z]:
            BGM_Volume = 100
            SE_Volume = 80
            set_value('BGM_Volume',BGM_Volume)
            self.change_bgm(BGM_Volume)
            pygame.mixer.music.set_volume(BGM_Volume/100)
            set_value('SE_Volume',80)
            self.change_se(SE_Volume)
            SoundManager.play('ok_sound',0.35,True)

        if self.selectIndex != 3 and pressed_keys[K_ESCAPE] and not last_keys[K_ESCAPE]:
            self.selectIndex = 3
            SoundManager.play('cancel_sound',0.35,True)

        if self.selectIndex == 3 and pressed_keys[K_z] and not last_keys[K_z]:
            self.master.pages.pop()
            SoundManager.play('cancel_sound',0.35,True)
            del self

    def draw(self, screen):
        idx = 0
        for i in self.button_dicts:
            if idx==self.selectIndex:
                self.button_dicts[i]+=(30-self.button_dicts[i])/10
            else:
                self.button_dicts[i]-=(self.button_dicts[i])/10
            screen.blit(ImageManager.getImage("Menu", i)[idx==self.selectIndex], (30+self.button_dicts[i], 80+80*idx))
            idx+=1
        for i in range(0, 2):
            if i==self.selectIndex:
                self.num_lists[i]+=(30-self.num_lists[i])/10
            else:
                self.num_lists[i]-=(self.num_lists[i])/10
        screen.blit(self.BGM_Text[self.selectIndex==0], (self.BGM_Rect.x+self.num_lists[0], self.BGM_Rect.y))
        screen.blit(self.SE_Text[self.selectIndex==1], (self.SE_Rect.x+self.num_lists[1], self.SE_Rect.y))
            
        

import os
for x in os.listdir('mods/'):
    if x.endswith(".sba_dat"):
        print(x)
import Nodes
        
class ModSelectPage():
    def __init__(self,master):
        self.master = master
        self.title = ImageManager.stot("Rank_font", 48, "Mod Select", WHITE, BLACK, 2)
        self.no_data = ImageManager.stot("Regular_font", 48, "No Files", RED, BLACK, 2)
        self.bg = pygame.Surface((640,480))
        self.angle=0
        self.ty = 0
        self.y = 0
        self.selectIndex = -1
        self.lists = []
        self.text_lists = []
        for x in os.listdir('mods/'):
            if x.endswith(".sba_dat"):
                self.lists.append(x.split('.')[0])
        for i in self.lists:
            self.text_lists.append(ImageManager.stot("Regular_font", 48, i, WHITE, BLACK, 2))
        if self.lists:
            self.selectIndex = 0
            self.chosen_bar = pygame.Surface((self.text_lists[0].get_size()[0]+20, 56)).convert_alpha()
            self.chosen_bar.fill((255,255,255,100))
            self.chosen_bar_rect = self.chosen_bar.get_rect(center = (320, 240))
        
    def update(self, screen, pressed_keys, last_keys):
        self.y += (self.ty-self.y)/5
        self.selection(pressed_keys, last_keys)
        self.draw(screen)
        
    def selection(self, pressed_keys, last_keys):
        if pressed_keys[K_UP] and not last_keys[K_UP]:
            if self.selectIndex>0:
                self.selectIndex -= 1
                SoundManager.play('select_sound',0.35,True)
                self.ty = 60*self.selectIndex
                self.chosen_bar = pygame.Surface((self.text_lists[self.selectIndex].get_size()[0]+20, 56)).convert_alpha()
                self.chosen_bar.fill((255,255,255,100))
                self.chosen_bar_rect = self.chosen_bar.get_rect(center = (320, 240))
            else:
                SoundManager.play('invalid_sound',0.5,True)
        if pressed_keys[K_DOWN] and not last_keys[K_DOWN]:
            if self.selectIndex < len(self.lists)-1 and self.selectIndex!=-1:
                self.selectIndex += 1
                SoundManager.play('select_sound',0.35,True)
                self.ty = 60*self.selectIndex
                self.chosen_bar = pygame.Surface((self.text_lists[self.selectIndex].get_size()[0]+20, 56)).convert_alpha()
                self.chosen_bar.fill((255,255,255,100))
                self.chosen_bar_rect = self.chosen_bar.get_rect(center = (320, 240))
            else:
                SoundManager.play('invalid_sound',0.5,True)
        if pressed_keys[K_z] and not last_keys[K_z] and self.selectIndex!=-1:
            self.master.pages.pop()
            self.master.load_mod_text(self.lists[self.selectIndex])
            SoundManager.play('ok_sound',0.35,True)
            del self
        if pressed_keys[K_ESCAPE] and not last_keys[K_ESCAPE]:
            self.master.pages.pop()
            SoundManager.play('cancel_sound',0.35,True)
            del self
        
    def draw(self, screen):
        self.angle = (self.angle+2)%360
        self.bg.fill(functions.get_rainbow_color(radians(self.angle)))
        title = self.title.copy()
        title.blit(self.bg,(0,0),special_flags=BLEND_RGB_MULT)
        screen.blit(title,title.get_rect(topright=(640,0)))
        
        if self.lists:
            a = self.selectIndex-1
            b = self.selectIndex+1
            self.text_lists[self.selectIndex].set_alpha(255)
            idx = 1
            for _ in range(len(self.lists)):
                if a>=0:
                    self.text_lists[a].set_alpha(255-idx*45)
                if b<len(self.lists):
                    self.text_lists[b].set_alpha(255-idx*45)
                a-=1
                b+=1
                idx+=1
            for i in range(len(self.lists)):
                screen.blit(self.text_lists[i], self.text_lists[i].get_rect(center=(320, 240+i*60-self.y)))
            screen.blit(self.chosen_bar, self.chosen_bar_rect)
        else:
            screen.blit(self.no_data, self.no_data.get_rect(center=(320, 240)))
        

class RankSelectPage():
    def __init__(self,master,rank_lists,isPractice):
        self.master = master
        self.title = ImageManager.stot("Rank_font", 48, "Rank Select", WHITE, BLACK, 2)
        self.no_data = ImageManager.stot("Regular_font", 48, "No Data", RED, BLACK, 2)
        self.bg = pygame.Surface((640,480))
        self.rank_lists = rank_lists
        self.text_lists = []
        self.selectIndex = -1
        self.isPractice = isPractice
        if self.rank_lists != []:
            for i in self.rank_lists[0].children:
                if i.name == 'Main':
                    self.rank_lists = i.children
                    break
        for i in self.rank_lists:
            self.selectIndex = 0
            self.text_lists.append(ImageManager.stot("Rank_font", 48, i.text, WHITE, i.color, 2))
        self.len = len(self.rank_lists)
        self.ty = 0
        self.y = 0
        self.angle = 0
        if self.selectIndex != -1:
            self.chosen_bar = pygame.Surface((self.text_lists[0].get_size()[0]+20, 56)).convert_alpha()
            self.chosen_bar.fill((255,255,255,100))
            self.chosen_bar_rect = self.chosen_bar.get_rect(center = (320, 240))
    
    def update(self, screen, pressed_keys, last_keys):
        self.y += (self.ty-self.y)/10
        self.selection(pressed_keys, last_keys)
        self.draw(screen)
        
    def selection(self, pressed_keys, last_keys):
        if pressed_keys[K_UP] and not last_keys[K_UP]:
            if self.selectIndex and self.selectIndex != -1:
                self.selectIndex -= 1
                self.ty = 60*self.selectIndex
                SoundManager.play('select_sound',0.35,True)
                self.chosen_bar = pygame.Surface((self.text_lists[self.selectIndex].get_size()[0]+20, 56)).convert_alpha()
                self.chosen_bar.fill((255,255,255,100))
                self.chosen_bar_rect = self.chosen_bar.get_rect(center = (320, 240))
            else:
                SoundManager.play('invalid_sound',0.5,True)
        if pressed_keys[K_DOWN] and not last_keys[K_DOWN]:
            if self.selectIndex < self.len-1 and self.selectIndex != -1:
                self.selectIndex += 1
                self.ty = 60*self.selectIndex
                SoundManager.play('select_sound',0.35,True)
                self.chosen_bar = pygame.Surface((self.text_lists[self.selectIndex].get_size()[0]+20, 56)).convert_alpha()
                self.chosen_bar.fill((255,255,255,100))
                self.chosen_bar_rect = self.chosen_bar.get_rect(center = (320, 240))
            else:
                SoundManager.play('invalid_sound',0.5,True)
        if pressed_keys[K_z] and not last_keys[K_z] and self.selectIndex != -1:
            if self.rank_lists != []:
                set_value('load_level',True)
                self.master.node_lists = self.rank_lists[self.selectIndex].children
                set_value('rank', self.rank_lists[self.selectIndex].rank)
            if self.isPractice:
                self.master.pages.append(StageSelectPage(self.master))
            else:
                self.master.pages.append(PlayerSelectPage(self.master))
            SoundManager.play('ok_sound',0.35,True)
        if pressed_keys[K_ESCAPE] and not last_keys[K_ESCAPE]:
            self.master.pages.pop()
            SoundManager.play('cancel_sound',0.35,True)
            del self
            
    def draw(self, screen):
        self.angle = (self.angle+2)%360
        self.bg.fill(functions.get_rainbow_color(radians(self.angle)))
        title = self.title.copy()
        title.blit(self.bg,(0,0),special_flags=BLEND_RGB_MULT)
        screen.blit(title,title.get_rect(topright=(640,0)))
        if self.selectIndex != -1:
            a = self.selectIndex-1
            b = self.selectIndex+1
            self.text_lists[self.selectIndex].set_alpha(255)
            idx = 1
            for _ in range(len(self.text_lists)):
                if a>=0:
                    self.text_lists[a].set_alpha(255-idx*45)
                if b<len(self.text_lists):
                    self.text_lists[b].set_alpha(255-idx*45)
                a-=1
                b+=1
                idx+=1
            for i in range(self.len):
                screen.blit(self.text_lists[i], self.text_lists[i].get_rect(center=(320, 240+i*60-self.y)))
            screen.blit(self.chosen_bar, self.chosen_bar_rect)
        else:
            screen.blit(self.no_data, self.no_data.get_rect(center=(320,240)))

class StageSelectPage():
    def __init__(self,master):
        self.master = master
        self.title = ImageManager.stot("Rank_font", 48, "Stage Select", WHITE, BLACK, 2)
        self.no_data = ImageManager.stot("Regular_font", 48, "No Data", RED, BLACK, 2)
        self.bg = pygame.Surface((1000,1000))
        self.bg.fill((0,0,0))
        self.selectIndex = 0
        self.text_lists = []
        for i in self.master.node_lists:
            self.text_lists.append(ImageManager.stot("Regular_font", 48, i.name, WHITE, BLACK, 2))
        self.angle = 0
        self.y = 0
        self.ty = 0
        if self.text_lists:
            self.chosen_bar = pygame.Surface((self.text_lists[0].get_size()[0]+20, 56)).convert_alpha()
            self.chosen_bar.fill((255,255,255,100))
            self.chosen_bar_rect = self.chosen_bar.get_rect(center = (320, 240))
        
    def update(self, screen, pressed_keys, last_keys):
        self.y += (self.ty-self.y)/5
        self.selection(pressed_keys, last_keys)
        self.draw(screen)
        
    def selection(self, pressed_keys, last_keys):
        if pressed_keys[K_UP] and not last_keys[K_UP]:
            if self.selectIndex and self.text_lists:
                self.selectIndex -= 1
                self.ty = self.selectIndex*60
                SoundManager.play('select_sound',0.35,True)
                self.chosen_bar = pygame.Surface((self.text_lists[self.selectIndex].get_size()[0]+20, 56)).convert_alpha()
                self.chosen_bar.fill((255,255,255,100))
                self.chosen_bar_rect = self.chosen_bar.get_rect(center = (320, 240))
            else:
                SoundManager.play('invalid_sound',0.5,True)
        if pressed_keys[K_DOWN] and not last_keys[K_DOWN]:
            if self.selectIndex < len(self.text_lists)-1 and self.text_lists:
                self.selectIndex += 1
                self.ty = self.selectIndex*60
                SoundManager.play('select_sound',0.35,True)
                self.chosen_bar = pygame.Surface((self.text_lists[self.selectIndex].get_size()[0]+20, 56)).convert_alpha()
                self.chosen_bar.fill((255,255,255,100))
                self.chosen_bar_rect = self.chosen_bar.get_rect(center = (320, 240))
            else:
                SoundManager.play('invalid_sound',0.5,True)
        if pressed_keys[K_z] and not last_keys[K_z] and self.text_lists:
            self.master.pages.append(PlayerSelectPage(self.master))
            SoundManager.play('ok_sound',0.35,True)
            set_value('load_stage',self.selectIndex+1)
        if pressed_keys[K_ESCAPE] and not last_keys[K_ESCAPE]:
            self.master.pages.pop()
            SoundManager.play('cancel_sound',0.35,True)
            del self
            
    def draw(self, screen):
        self.angle = (self.angle+2)%360
        self.bg.fill(functions.get_rainbow_color(radians(self.angle)))
        title = self.title.copy()
        title.blit(self.bg,(0,0),special_flags=BLEND_RGB_MULT)
        screen.blit(title,title.get_rect(topright=(640,0)))
        if self.text_lists:
            a = self.selectIndex-1
            b = self.selectIndex+1
            self.text_lists[self.selectIndex].set_alpha(255)
            idx = 1
            for _ in range(len(self.text_lists)):
                if a>=0:
                    self.text_lists[a].set_alpha(255-idx*45)
                if b<len(self.text_lists):
                    self.text_lists[b].set_alpha(255-idx*45)
                a-=1
                b+=1
                idx+=1
            for i in range(len(self.text_lists)):
                screen.blit(self.text_lists[i], self.text_lists[i].get_rect(center=(320, 240+i*60-self.y)))
            screen.blit(self.chosen_bar, self.chosen_bar_rect)
        else:
            screen.blit(self.no_data, self.no_data.get_rect(center=(320,240)))

class PlayerSelectPage():
    def __init__(self,master):
        self.master = master
        self.title = ImageManager.stot("Rank_font", 48, "Player Select", WHITE, BLACK, 2)
        self.bg = pygame.Surface((640,480))
        self.bs = pygame.Surface((640,480))
        self.bs.fill((0,0,0))
        self.Reimu_Image = ImageManager.getImage('Portrait', 'Reimu')[0]
        self.Marisa_Image = ImageManager.getImage('Portrait', 'Marisa')[0]
        self.es = self.bs.copy()
        self.R_S = self.Reimu_Image.copy()
        self.R_S.blit(self.bs, (0,0), special_flags=3)
        self.M_S = self.Marisa_Image.copy()
        self.M_S.blit(self.bs, (0,0), special_flags=3)
        self.image = [self.Reimu_Image, self.R_S, self.Marisa_Image, self.M_S]
        self.selectIndex = 0
        self.angle = 0
        
    def update(self, screen, pressed_keys, last_keys):
        self.selection(pressed_keys, last_keys)
        self.draw(screen)
        
    def selection(self, pressed_keys, last_keys):
        if pressed_keys[K_LEFT] and not last_keys[K_LEFT]:
            if self.selectIndex:
                self.selectIndex -= 1
                SoundManager.play('select_sound',0.35,True)
            else:
                SoundManager.play('invalid_sound',0.5,True)
        if pressed_keys[K_RIGHT] and not last_keys[K_RIGHT]:
            if self.selectIndex < 1:
                self.selectIndex += 1
                SoundManager.play('select_sound',0.35,True)
            else:
                SoundManager.play('invalid_sound',0.5,True)
        if pressed_keys[K_z] and not last_keys[K_z]:
            set_value('player_id',self.selectIndex+1)
            SoundManager.play('ok_sound',0.35,True)
            self.master.pages.append(PlayerInfoPage(self.master, self.selectIndex+1))
        if pressed_keys[K_ESCAPE] and not last_keys[K_ESCAPE]:
            self.master.pages.pop()
            SoundManager.play('cancel_sound',0.35,True)
            del self
            
    def draw(self, screen):
        self.angle = (self.angle+2)%360
        self.bg.fill(functions.get_rainbow_color(radians(self.angle)))
        title = self.title.copy()
        title.blit(self.bg, (0,0), special_flags=3)
        screen.blit(title,title.get_rect(topright=(640,0)))
        screen.blit(self.image[0 if self.selectIndex==0 else 1], (0,50))
        screen.blit(self.image[2 if self.selectIndex==1 else 3], (320, 50))

class PlayerInfoPage():
    def __init__(self, master, player_id):
        self.master = master
        self.player_id = player_id
        if self.player_id == 1:
            self.image = ImageManager.getImage('Portrait', 'Reimu')[0]
            self.info = ImageManager.getImage('Menu', 'Player_Info_Reimu')
        elif self.player_id == 2:
            self.image = ImageManager.getImage('Portrait', 'Marisa')[0]
            self.info = ImageManager.getImage('Menu', 'Player_Info_Marisa')
        self.selectIndex = 0
        
    def update(self, screen, pressed_keys, last_keys):
        self.selection(pressed_keys, last_keys)
        self.draw(screen)
        
    def selection(self, pressed_keys, last_keys):
        if pressed_keys[K_z] and not last_keys[K_z]:
            SoundManager.play('ok_sound',0.35,True)
            set_value('entering_game_effect', effect.EnterGameAnimation())
            pygame.mixer.music.pause()
        if pressed_keys[K_ESCAPE] and not last_keys[K_ESCAPE]:
            self.master.pages.pop()
            SoundManager.play('cancel_sound',0.35,True)
            del self

    def draw(self, screen):
        screen.blit(self.info, (150, 50))
        screen.blit(self.image,(0,50))

angle = 0

def display_UI(screen,player):
    background = ImageManager.getImage("BattleUI", "Background")

    frame = ImageManager.stot("Regular_font", 12, "F: %d" % (get_value('frame')), WHITE, BLACK, 1)

    rank = get_value('rank')
    #showscore
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
    score_show = f"{score_show:,}"
    hi_score_show = f"{hi_score_show:,}"
    score = ImageManager.stot("Regular_font", 16, score_show, WHITE, BLACK, 1)
    hi_score = ImageManager.stot("Regular_font", 16, hi_score_show, GRAY, BLACK, 1)

    #draw UI sign
    screen.blit(background[0], (0, 0))
    screen.blit(background[1], (32, 0))
    screen.blit(background[2], (32, 464))
    screen.blit(background[3], (416, 0))


    #"FPS: %.1f" % (get_value('fps'))
    screen.blit(rank, rank.get_rect(midtop=(528, 8)))
    screen.blit(ImageManager.getImage("BattleUI", "HiScore"), (420, 48))
    screen.blit(hi_score, hi_score.get_rect(topright=(636, 48)))
    screen.blit(ImageManager.getImage("BattleUI", "Score"), (420, 76))
    screen.blit(score, score.get_rect(topright=(636, 76)))
    ######################################
    lifesign = ImageManager.getImage("BattleUI", "LifeSign")
    life = player.life
    boomsign = ImageManager.getImage("BattleUI", "BoomSign")
    boom = player.boom
    screen.blit(ImageManager.getImage("BattleUI", "Player"), (420, 120))
    screen.blit(ImageManager.getImage("BattleUI", "Piece"), (520, 140))
    for i in range (1,9):
        sign = lifesign[5 if life-i*10>=10 else int(life%10//2)*(life>i*10)]
        screen.blit(sign, ((i*14+520-14), 128))
    life = ImageManager.stot("Regular_font", 16, "{}/5".format(int(life%10//2)), WHITE, BLACK, 1)
    screen.blit(life, life.get_rect(topright=(636, 140)))

    screen.blit(ImageManager.getImage("BattleUI", "SpellCard"), (420, 160))
    screen.blit(ImageManager.getImage("BattleUI", "Piece"), (520, 180))
    for i in range (0,8):
        sign = boomsign[5 if boom-i*10>=10 else int(boom%10//2)*(boom>i*10)]
        screen.blit(sign, ((i*14+520), 168))
    boom = ImageManager.stot("Regular_font", 16, "{}/5".format(int(boom%10//2)), WHITE, BLACK, 1)
    screen.blit(boom, boom.get_rect(topright=(636, 180)))

    ########################################
    screen.blit(ImageManager.getImage("Item", "items")[0], (430, 225))
    screen.blit(ImageManager.getImage("BattleUI", "Power"), (450, 220))
    power = "{:.2f}/4.00".format(max(1.00,player.power/100))
    power = ImageManager.stot('Regular_font', 16, power, ORANGE, BLACK, 1)
    screen.blit(power, power.get_rect(topright=(636, 220)))
    
    screen.blit(ImageManager.getImage("Item", "items")[1], (430, 255))
    screen.blit(ImageManager.getImage("BattleUI", "Point"), (450, 250))
    point = f"{get_value('maximum_score'):,}"
    point = ImageManager.stot('Regular_font', 16, point, LIGHTBLUE, BLACK, 1)
    screen.blit(point, point.get_rect(topright=(636, 250)))
    
    screen.blit(ImageManager.getImage("BattleUI", "Graze"), (450, 280))
    graze = str(get_value("grazeNum"))
    graze = ImageManager.stot('Regular_font', 16, graze, GRAY, BLACK, 1)
    screen.blit(graze, graze.get_rect(topright=(636, 280)))
    #####################################
    screen.blit(ImageManager.getImage("BattleUI", "Title"), (420, 320))
    screen.blit(ImageManager.getImage("BattleUI", "FUKA"), (560, 360))
    screen.blit(ImageManager.stot('Regular_font', 14, "FPS: %.1f" % (get_value('fps')), WHITE, BLACK, 2), (560, 455))
    screen.blit(frame, (2, -5))
    global angle
    angle += 1
    if angle >= 360:
        angle = 0
    if get_value('boss_alive'):
        boss_pos = ImageManager.getImage('Boss','boss_pos')
        if get_value('boss_x')>=0 and get_value('boss_x')<=384:
            screen.blit(boss_pos, boss_pos.get_rect(midtop=(get_value('boss_x')+32,448+16)))
        pygame.draw.rect(screen, WHITE, pygame.Rect(32, 448+16+6, 384, 10))
        per = get_value('boss_health')/get_value('boss_maxHealth')*384
        pygame.draw.rect(screen, RED, pygame.Rect(32, 448+16+6, per, 10))
        pygame.draw.rect(screen, BLACK, pygame.Rect(32, 448+16+6, 384, 10), 2)
        num = ImageManager.stot("Regular_font", 16, "{}%".format(int(get_value('boss_health')/get_value('boss_maxHealth')*100)), WHITE, BLACK, 2)
        screen.blit(num, num.get_rect(topleft=(384+32,448+10)))
            
def pauseScreen(screen,idx,player):
    screen.blit(get_value('pause_screen'), (32,16))
    if get_value('finish'):
        screen.blit(ImageManager.getImage("Pause",'GameEnd'), (50,100))
        screen.blit(ImageManager.stot("Art_font", 28, "Your Score is:", WHITE, BLACK, 2), (80, 175))
        screen.blit(ImageManager.stot("Art_font", 28, "{}".format(get_value('hi_score')), WHITE, BLACK, 2), (80, 205))

    elif player.isAlive:
        screen.blit(ImageManager.getImage("Pause",'Pause'), (50,100))
        screen.blit(ImageManager.getImage("Pause",'Return')[idx!=0], (80-(idx!=0)*10,175))

    else:
        screen.blit(ImageManager.getImage("Pause",'Gameover'), (50,100))
        screen.blit(ImageManager.getImage("Pause",'Retry')[idx!=0], (80-(idx!=0)*10,175))
    screen.blit(ImageManager.getImage("Pause",'Back')[idx!=1], (80-(idx!=1)*10,250))
