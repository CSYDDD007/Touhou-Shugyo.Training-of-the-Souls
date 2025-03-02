import pygame
import functions

from pygame.locals import *
from const import *
from math import *
from random import *
from global_var import *

class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = get_value('stage_1').convert_alpha()
        self.rect = self.surf.get_rect()
        self.tx = 0.0
        self.ty = 0.0
        self.type = 0
        self.speedx = 0.0
        self.speedy = 6.0
        self.x_adj = 0.0
        self.frame = 0
        self.spellCard = False

    def initialize(self, posx, posy):
        self.tx = posx
        self.ty = posy
        self.posx = posx

    def alterSpeed(self, speedx, speedy):
        self.speedx = speedx
        self.speedy = speedy

    def checkValid(self,speed):
        if self.ty >= 360*3:
            self.ty = -360

    def truePos(self):
        self.rect.centerx = self.tx
        self.rect.centery = self.ty

    def movement(self, speed):
        self.tx += self.speedx+speed
        self.ty += self.speedy
        if not get_value('screen_shaking'):
            self.tx = self.posx
        self.truePos()

    def update(self, screen, speed):
        self.frame += 1
        self.movement(speed)
        self.checkValid(speed)
        screen.blit(self.surf,(self.tx,self.ty))

class spellAttackImage(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.length=1000
        self.width=640-96
        self.Image=pygame.Surface((self.length,self.width)).convert_alpha()
        self.Image.fill((0,0,0,0))
        self.subImage=pygame.Surface((256,32)).convert_alpha()
        self.subImage.fill((0,0,0,0))
        self.subImage.blit(get_value('spellcardAttack'),(0,0))
        self.lastFrame=0
        self.maxFrame=240
        self.movingSpeed=4
        self.midSign=900
        self.alpha=256
        self.midAlphaSign=200
    
    def imageAlpha(self):
        if self.lastFrame < 30:
            self.alpha=self.lastFrame*8
        elif self.lastFrame > 210:
            self.alpha=(240-(self.lastFrame-210)*8)
        else:
            self.alpha=255
        self.Image.set_alpha(self.alpha)
    def update(self,screen,speed):
        self.checkValid()
        self.Image.fill((0,0,0,0))
        self.lastFrame+=1
        self.midSign+=self.movingSpeed
        for i in range(0,10):
            for j in range(0,12):
                if i%2==1:
                    x=1000+160*1.5*j-self.midSign
                    y=i*64
                    if x<1000:
                        self.Image.blit(self.subImage,(x,y))
                else:
                    x=0-160*1.5*j+self.midSign
                    y=i*64
                    if x+160*1.5>0:
                        self.Image.blit(self.subImage,(x,y))
        self.imageAlpha()
        self.draw(screen)
    def checkValid(self):
        if self.lastFrame>=self.maxFrame:
            self.kill()
    
    def draw(self,screen):
        functions.drawImage(self.Image,(768/2-50,350),250,screen)
        
class Spell_NPC(Background):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((623,900)).convert_alpha()
        self.surf.fill((0,0,0,0))
        self.surf.blit(get_value('Cirno_Spell'), (0,0))
        self.lastFrame = 0
        self.maxFrame = 240
            
    def initial(self,tx,ty,name):
        self.tx=tx
        self.ty=ty
        if name=='cirno':
            self.surf = pygame.Surface((623,900),pygame.SRCALPHA).convert_alpha()
            self.surf.fill((0,0,0,0))
            self.surf.blit(get_value('Cirno_Spell'), (0,0))
        else:
            self.surf = pygame.Surface((426*1.8,519*1.8),pygame.SRCALPHA).convert_alpha()
            self.surf.fill((0,0,0,0))
            self.surf.blit(get_value('cat_spell'), (0,0))
            self.surf = pygame.transform.smoothscale(self.surf, (426*1.8,519*1.8))
            
    def update(self,screen,speed):
        self.lastFrame += 1
        self.checkValid()
        self.movement()
        self.draw(screen)
        
    def setSpeed(self,angle,speed):
        s=sin(radians(angle))
        c=cos(radians(angle))        
        self.speedy=s*speed
        self.speedx=c*speed
        self.angle=angle
    
    def movement(self):
        if self.lastFrame < 35:
            speed = 30*abs(cos(radians(self.lastFrame*(90/35))))
            self.setSpeed(self.angle,speed)
        elif self.lastFrame == 35:
            self.setSpeed(self.angle,1)
        elif self.lastFrame > 210:
            speed = 30*sin(radians((self.lastFrame-210)*3))
            self.setSpeed(self.angle,speed)
        self.tx += self.speedx
        self.ty += self.speedy

    def draw(self,screen):
        #return
        screen.blit(self.surf,(self.tx,self.ty))

    def checkValid(self):
        if self.lastFrame > self.maxFrame:
            self.kill()

class Cirno_Background(Background):
    def __init__(self):
        super().__init__()
        self.surf = get_value('cirno_fumo').convert_alpha()
        self.speedy = 3.0

    def checkValid(self,speed):
        if self.ty >= 1040:
            self.ty = -260
            
class Lake_Background(Background):
    def __init__(self):
        super().__init__()
        self.surf = get_value('lake_background')[0].convert_alpha()
        self.rect = self.surf.get_rect()
        self.idx=0
        self.lastFrame=0
        self.speedy=0.0
        
    def update(self,screen,speed):
        self.lastFrame+=1
        if self.lastFrame==3:
            self.lastFrame=0
            self.idx+=1
        if self.idx>=len(get_value('lake_background')):
            self.idx=0
        self.surf = get_value('lake_background')[self.idx].convert_alpha()
        self.movement(speed)
        screen.blit(self.surf,(self.tx,self.ty))

    def movement(self, speed):
        self.tx += speed
        self.ty += speed
        if self.tx < -18:
            self.tx -= speed
        elif self.tx > 6:
            self.tx -= speed
        if self.ty < -18:
            self.ty -= speed
        elif self.ty > 6:
            self.ty -= speed
        if not get_value('screen_shaking'):
            self.tx = -12
            self.ty = 0
        self.truePos()
        


    

