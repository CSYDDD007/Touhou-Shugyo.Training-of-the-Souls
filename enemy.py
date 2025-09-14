import pygame
import bullet
import obj
import effect
import functions
import item

from pygame.math import Vector2
from const import *
from math import *
from random import *
from global_var import *
import SoundManager as SE
import ImageManager

#Am I Stupid?
class Enemy(obj.OBJ):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 0, 32, 32)
        self.lastFrame = 0 #current frame
        self.maxFrame = 0 #maximum exist frame
        self.color='red' #color of enemy
        self.gethit=False #if enemy get hit, play hit animation frame
        self.gethitNum=0 #hit animation frame
        self.interval = 5
        self.colorNum = 0
        self.frame = 0
        self.part = 0
        self.idx = 0
        self.nodes = {}
        self.var = {}
        self.cnt = 0
        self.healthBar = None
        self.father = None
        self.out_of_wall = False
        self.boss = False
        self.power_num = 0
        self.point_num = 10
        self.invincible = 0
        self.tweening_nodes = []
        
    def initial(self, x, y, type, hp):
        self.x = x
        self.y = y
        self.typeIdx = type
        self.image = ImageManager.getImage("Enemy", type)
        self.lastHp = -1
        self.hp = hp
        self.maxHp = hp
        self.truePos()
        
    def checkDistance(self):
        dist = functions.dist((get_value('player').x, get_value('player').y), (self.x, self.y))
        miniDist = get_value('enemypos')[2]
        if self.x <= 384 and self.x >= 0 and self.y <= 448 and self.y>=0 and dist<miniDist:
            set_value('enemypos',(self.x,self.y,dist))

    def update(self, screen, bullets, lasers, items, effects, backgrounds):
        self.lastFrame += 1
        if self.invincible:
            self.invincible -= 1
        if self.hp <= 0:
            self.killEffect()
            self.doKill()
            return
        if self.lastFrame >= 100:
            self.checkValid()
        if self.nodes:
            self.var['self'] = self
            self.nodes['update'].update(self.var)
            #print(self.nodes['update'].type)
            #print(self.tx, self.nodes['__init__'])
        self.movement()
        self.checkDistance()
        self.tweening()
        self.draw(screen)
        if self.typeIdx >= 15 and self.typeIdx <= 18 and self.lastFrame % 5 == 0:
            new_effect = effect.Ghost_flame_effect(self.x, self.y, self.typeIdx)
            effects.add(new_effect)
            
    def set_var(self, var_name, value, var):
        cmd = 'result = ' + str(value)
        exec(cmd, globals(), var)
        self.var[var_name] = var['result']
        print('ggg')
            
    def tweening(self):
        vars = {'self':self}
        for i in self.tweening_nodes:
            i[2]+=1
            if i[2]>i[3]:
                self.tweening_nodes.remove(i)
                continue
            if i[4]==0:
                vars['result']=functions.linear(i[0], i[1], i[2], i[3])
            elif i[4]==1:
                vars['result']=functions.acc(i[0], i[1], i[2], i[3])
            elif i[4]==2:
                vars['result']=functions.dcc(i[0], i[1], i[2], i[3])
            elif i[4]==3:
                vars['result']=functions.acc_dcc(i[0], i[1], i[2], i[3])
            exec("self.{}=result".format(i[5]), globals(), vars)
            
    def draw(self, screen):
        if self.typeIdx <= 14:
            self.draw_Fairy(screen)
        elif self.typeIdx <= 18:
            self.draw_Ghost(screen)
        elif self.typeIdx <= 22:
            self.draw_YinYangYu(screen)
        elif self.typeIdx <= 26:
            self.draw_Small_YinYangYu(screen)
        elif self.typeIdx <= 30:
            self.draw_Kedama(screen)
        if get_value('enemy_draw_healthbar'):
            self.DrawHealthbar(screen)
        if get_value('enemy_show_health_value'):
            self.ShowHealthValue(screen)
    
    def draw_Fairy(self, screen):
        self.part = (self.lastFrame//self.interval)%5
        self.cnt -= 1
        if int(self.speedx) == 0:
            self.idx = self.part
            self.cnt = 0
        elif self.idx <= 10 and self.cnt<=0:
            if self.idx <= 4:
                self.idx = 5
            else:
                self.idx += 1
            self.cnt = 5
        elif self.idx == 11 and self.cnt<=0:
            self.idx = 8
            self.cnt = 5
        if self.gethit:
            self.gethitNum=12
            self.gethit=False
        else:
            self.gethitNum=0
        img = self.image[self.idx+self.gethitNum]
        if self.speedx<0:
            img = pygame.transform.flip(img,True,False)
        functions.drawImage(img, (self.x,self.y), 0, screen)
    
    def draw_Ghost(self, screen):
        self.frame += 1
        if self.frame >= self.interval:
            self.frame = 0
            self.part = (self.part+1)%8
        if self.gethit:
            self.gethitNum=8
            self.gethit=False
        else:
            self.gethitNum=0
        functions.drawImage(self.image[self.part+self.gethitNum], (self.x,self.y), 0, screen)
    
    def draw_Kedama(self, screen):
        self.frame += 1
        if self.gethit:
            self.gethitNum=1
            self.gethit=False
        else:
            self.gethitNum=0
        if self.frame >= self.interval:
            self.frame = 0
        self.rot += 15
        functions.drawImage(self.image[self.gethitNum], (self.x,self.y), self.rot, screen)
    
    def draw_YinYangYu(self, screen):
        self.frame += 1
        if self.frame >= self.interval:
            self.frame = 0
        if self.gethit:
            self.gethitNum=1
            self.gethit=False
        else:
            self.gethitNum=0
        self.rot += 15
        functions.drawImage(self.image[self.gethitNum], (self.x,self.y), self.rot, screen)
    
    def draw_Small_YinYangYu(self, screen):
        self.frame += 1
        if self.frame >= self.interval:
            self.frame = 0
        if self.gethit:
            self.gethitNum=1
            self.gethit=False
        else:
            self.gethitNum=0
        self.rot += 5
        balls = ImageManager.getImage("Enemy","balls")
        functions.drawImage(self.image[self.gethitNum], (self.x,self.y), self.rot*3, screen)
        functions.drawImage(balls[self.typeIdx-23], (self.x,self.y), -self.rot, screen)
        functions.drawImage(balls[self.typeIdx-27], (self.x,self.y), self.rot, screen)
    
    def DrawHealthbar(self, screen):
        healthbar = pygame.Surface((50, 8)).convert_alpha()
        healthbar.fill((0,0,0))
        health = max(self.hp,0)/self.maxHp
        health = pygame.Surface((health*50, 8)).convert_alpha()
        health.fill((128,255,128))
        healthbar.blit(health,(0,0))
        screen.blit(healthbar,(self.x-25,self.rect.y-10))
        pygame.draw.rect(screen,(255,255,255),pygame.Rect(self.x-25,self.rect.y-10,50,8),2)
        
    def ShowHealthValue(self, screen):
        if self.lastHp != self.hp:
            self.lastHp = self.hp
            self.health_text = ImageManager.stot("Regular_font", 12, f"{int(max(0,self.hp))}/{self.maxHp}", WHITE, BLACK, 1)
        health_text_rect = self.health_text.get_rect(center=(self.x,self.rect.y-15))
        screen.blit(self.health_text,health_text_rect)
        
    def changeType(self, type):
        self.typeIdx = type
        self.image = ImageManager.getImage("Enemy", type)
        self.rect = self.image[0].get_rect()

    def doKill(self):
        if len(self.nodes) == 2:
            self.var['self'] = self
            self.nodes['kill'].update(self.var)
        functions.dropItem(self.x,self.y,0,self.power_num)
        functions.dropItem(self.x,self.y,1,self.point_num)
        self.kill()
    
    def killEffect(self):
        SE.play('enemyDead_sound',0.5,1)
        new_effect = effect.enemyDeath((self.x,self.y), self.typeIdx)
        get_value('effects').add(new_effect)