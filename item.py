import pygame,sys
import random
import math
from const import *

import functions
import effect
from global_var import *
import SoundEffect as SE

class item(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.hitbox = pygame.Surface((16,16))
        self.hitbox.fill((255,255,255))
        self.rect = self.hitbox.get_rect()
        self.tx = 0.0
        self.ty = 0.0
        self.type = 0
        self.speedx = 0.0
        self.speedy = -3.0
        self.distance = 10000
        self.lastFrame = 0
        self.rotationAngle = 0
        self.image = 0
        self.alias = 0
        self.followPlayer = False
        self.followSpeed = 20.0
        self.m = False
        self.my=0.0

    def initial(self,tx,ty):
        self.tx=tx
        self.ty=ty
        self.image = get_value('item_image')[self.type]
        self.alias = get_value('item_image')[self.type+8]
        self.truePos()

    def truePos(self):
        self.rect.centerx=round(self.tx)
        self.rect.centery=round(self.ty)

    def movement(self):
        self.tx+=round(self.speedx)
        self.ty+=round(self.speedy)
        self.truePos()

    def selfTarget(self, speed):
        px = get_value('player_cx')
        py = get_value('player_cy')
        mx = self.tx
        my = self.ty
        dx = px-mx
        dy = py-my
        dist = math.sqrt(dx**2 + dy**2)
        times = dist/speed
        if dist==0:
            times=1
        self.speedx = dx/times
        self.speedy = dy/times

    def checkValid(self, player, screen):
        if self.rect.top>=900+20:#vertical
            self.kill()
        if self.rect.right<=30-20 or self.rect.left>=810+20:#horizontal
            self.kill()
        if self.distance<=10:
            self.doBonus(player,screen)
            self.countMax()
            self.kill()

    def checkDistance(self):
        px = get_value('player_cx')
        py = get_value('player_cy')
        mx = self.tx
        my = self.ty
        dx = px-mx
        dy = py-my
        self.distance = math.sqrt(dx**2 + dy**2)
    
    def countMax(self):
        if self.type==1:
            count = get_value('score_item_count')
            set_value('score_item_count', count+1)
            if count >= get_value('score_item_bound'):
                set_value('score_item_bound', get_value('score_item_bound')+10)
                set_value('maximum_score',get_value('maximum_score')+100)

    def update(self, screen, player, effects):
        if player.ty <= 250 and not self.followPlayer:
            self.followPlayer=True
            self.m=True
        if self.distance<=player.itemCollectDistance and not self.followPlayer:
            self.followPlayer=True
            if get_value('player_cy')>896:
                self.my=896
            else:
                self.my=get_value('player_cy')
        self.lastFrame += 1
        if self.lastFrame<=60:
            if not self.followPlayer or self.lastFrame<=30:
                self.speedy+=0.10
        self.movement()
        self.checkValid(player,effects)
        self.checkDistance()
        if self.followPlayer and self.lastFrame>=30:
            self.selfTarget(self.followSpeed)
        self.draw(screen)
        
    def createSubtitle(self, getscore, effects):
        new_effect = effect.Item_Show_Score()
        new_effect.initial(getscore,self.m,self.tx,self.ty)
        effects.add(new_effect)

    def doBonus(self, player, effects):
        maxscore = get_value('maximum_score')
        getscore = 0
        if self.my > 250 and not self.m:
            getscore = self.my-250
            getscore = getscore/646
        getscore = 1-getscore
        getscore *= maxscore
        if self.type == 0 and player.power < 400:
            player.power += 2

        if self.type == 1:
            player.score += int(getscore)
            self.createSubtitle(getscore,effects)

        if self.type == 2:
            player.score += int(getscore)
            self.createSubtitle(getscore,effects)

        if self.type == 3:
            if player.power <= 300:
                player.power += 100
            else:
                player.power = 400

        if self.type == 4:
            player.score += 20000

        if self.type == 5:
            player.power = 400

        if self.type == 6:
            player.life += 1

        if self.type == 7:
            player.score += maxscore//100

        if not get_value('item_getting'):
            if self.type != 6:
                SE.play('item_get',0.35,True)
                set_value('item_getting', True)

    def draw(self,screen):
        if self.ty<12:
            functions.drawImage(self.alias,(self.rect.centerx, 12),270,screen)
        else:
            if self.type!=7:
                if self.lastFrame<=48:
                    if self.lastFrame%2==0:
                        self.rotationAngle-=45
                    functions.drawImage(self.image,self.rect.center,self.rotationAngle,screen)
                else:
                    functions.drawImage(self.image,self.rect.center,270,screen)
            else:
                functions.drawImage(self.image,self.rect.center,270,screen)
