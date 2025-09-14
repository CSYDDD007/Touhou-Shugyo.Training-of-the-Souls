import pygame
import math
import obj
from const import *

import functions
import effect
from global_var import *
import SoundManager as SE
import ImageManager

class item(obj.OBJ):
    def __init__(self, type, x, y):
        super().__init__()
        self.follow = False
        self.x = x
        self.y = y
        self.type = type
        if type>=4 and type<=7:
            SE.play("bonus_sound", 1.0, 1)
        self.image :pygame.Surface = ImageManager.getImage("Item", 'items')[type]
        self.alias = ImageManager.getImage("Item", 'signs')[type]
        self.rect = self.image.get_rect(center = (x, y))
        self.speedy = -3
        self.omiga = 36
        self.m = False

    def selfTarget(self, speed, player):
        dx = player.x-self.x
        dy = player.y-self.y
        times = self.dist/speed
        if self.dist==0:
            times=1
        self.speedx = dx/times
        self.speedy = dy/times

    def checkValid(self, player, screen):
        if self.rect.top>=448+8:#vertical
            self.kill()
        if self.rect.right<=0 or self.rect.left>=384+8:#horizontal
            self.kill()
        if self.dist<=10:
            self.doBonus(player,screen)
            self.countMax()
            self.kill()

    def countMax(self):
        if self.type==1:
            count = get_value('score_item_count')
            set_value('score_item_count', count+1)
            if count >= get_value('score_item_bound'):
                set_value('score_item_bound', get_value('score_item_bound')+10)
                set_value('maximum_score',get_value('maximum_score')+100)

    def update(self, screen, player, effects):
        self.lastFrame += 1
        self.dist = functions.dist((player.x, player.y), (self.x, self.y))
        if player.y <= 120 and not self.follow:
            self.follow=True
            self.m=True
        if self.dist<=player.itemCollectDistance and not self.follow:
            self.follow=True
            self.my = min(448, player.y)
        if self.lastFrame<=120:
            self.speedy+=0.05
            self.countRot()
        self.checkValid(player,effects)
        if self.lastFrame >= 60:
            self.rot = 0
        if self.follow and self.lastFrame>=60:
            self.selfTarget(20,player)
        self.movement()
        self.draw(screen)
        
    def createSubtitle(self, getscore, effects):
        new_effect = effect.Item_Show_Score(self.x,self.y-20,str(int(getscore)),self.m)
        effects.add(new_effect)

    def doBonus(self, player, effects):
        maxscore = get_value('maximum_score')
        if self.type in (1,3) and not self.m:
            t = self.my
        else:
            t = 0
        getscore = functions.acc(maxscore, maxscore/10, t, 448)
        if self.type == 0:
            player.power += 2
            if player.power > 400:
                player.power = 400
                self.m=True
                self.createSubtitle(maxscore/50, effects)

        elif self.type == 1:
            player.score += int(getscore)
            self.createSubtitle(getscore,effects)

        elif self.type == 2:
            player.power += 100
            if player.power > 400:
                if player.power >= 500:
                    self.m=True
                    self.createSubtitle(maxscore/10, effects)
                player.power = 400

        elif self.type == 3:
            player.score += int(maxscore)
            self.createSubtitle(maxscore,effects)

        elif self.type == 4:
            player.life += 2
            if player.life > 90:
                player.score += int(maxscore/5)
                self.m=True
                self.createSubtitle(int(maxscore/5),effects)
                player.life = 90

        elif self.type == 5:
            player.boom += 2
            if player.boom > 80:
                player.score += int(maxscore/5)
                self.m=True
                self.createSubtitle(int(maxscore/5),effects)
                player.boom = 80

        elif self.type == 6:
            player.life += 10
            if player.life > 90:
                player.score += int(maxscore)
                self.m=True
                self.createSubtitle(int(maxscore),effects)
                player.life = 90

        elif self.type == 7:
            player.boom += 10
            if player.boom > 80:
                player.score += int(maxscore)
                self.m=True
                self.createSubtitle(int(maxscore),effects)
                player.boom = 80

        elif self.type == 8:
            player.score += int(maxscore/100)

        elif self.type == 9:
            if player.power == 400:
                self.m=True
                self.createSubtitle(int(maxscore), effects)
            player.power = 400

        if not get_value('item_getting'):
            SE.play('item_get',0.35,True)
            set_value('item_getting', True)

    def draw(self,screen):
        if self.rect.bottom<0:
            functions.drawImage(self.alias,(self.x, 12),0,screen)
        else:
            functions.drawImage(self.image,self.rect.center,self.rot,screen)
