import pygame
import bullet
import functions
import ImageManager
import item
import effect
import background


from const import *
from math import *
from random import *
from global_var import *
import SoundManager


class BOSS(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.hitbox = pygame.Surface((64, 64))
        self.hitbox.fill(WHITE)
        self.rect = self.hitbox.get_rect()
        self.x = 0
        self.y = 0
        self.ani_y = 0
        self.speedx = 0.0
        self.speedy = 0.0
        self.movingFrame = 0
        self.maxMovingFrame = 0
        self.moving_mode = 0
        self.lastFrame = 0
        self.maxHp = 100000
        self.hp = 100000
        self.dp = 0.0
        self.recovering = False
        self.cardNum = 1
        self.framelimit = 1200
        self.ifSpell = False
        self.spellName=[]
        self.spellFrame=-1
        self.cardBonus = 10000000
        self.framePunisment = 3700
        self.moving = False
        self.tempx=0
        self.tempy=0
        self.start_x = 0
        self.start_y = 0
        self.target_x = 0
        self.target_y = 0
        self.nimbus = ImageManager.getImage("Boss", 'boss_magic')
        self.nimbus_big_1 = ImageManager.getImage("Boss", 'boss_nimbus_big')
        self.nimbus_big_2 = ImageManager.getImage("Boss", 'boss_nimbus_big1')
        self.boss = True
        self.timer = 0
        self.isSpell = 0
        self.image = ImageManager.getImage("Mods", "Default")
        self.bgm = ''
        self.normal_back = None
        self.sp_back = None
        self.animation_interval = 8
        self.animation_frame = 0
        self.left_ani_frame = 0
        self.right_ani_frame = 0
        self.nimbus_angle = 0
        self.var = {}
        self.nodes = []
        self.updateIdx = 0
        self.idle_frame = []
        self.left_frame = []
        self.right_frame = []
        self.left_image = []
        self.right_image = []
        self.immune = False
        self.direction = 0
        self.drop_point = 0
        self.drop_power = 0
        self.tweening_nodes = []
        self.default = True
        self.rot = 0
        self.father = None
        self.invincible = 0
        set_value('boss_alive', 1)
        
    def update(self, screen, bullets, lasers, items, effects, backgrounds):
        self.timer -= 1
        self.lastFrame += 1
        set_value('boss_x', self.x)
        if not self.immune and (self.timer == 0 or self.hp <= 0):
            self.updateIdx += 1
            get_value('backgrounds').empty()
            self.normal_back.update({})
            print('Spell Broken')
            self.isSpell = 0
            self.immune = True
            functions.dropItem(self.x,self.y,0,self.drop_power)
            functions.dropItem(self.x,self.y,1,self.drop_point)
            self.drop_power = 0
            self.drop_point = 0
            for i in get_value('boss_effect'):
                if i.__class__.__name__ == 'SpellCardBonus':
                    i.fin = 100
                    if self.timer==0:
                        i.failed = True
                elif i.__class__.__name__ == 'SpellCardName':
                    i.kill()
                elif i.__class__.__name__ == 'Timer':
                    i.kill()
        self.move_to()
        self.checkDistance()
        self.draw(screen)
        self.var['self'] = self
        while self.updateIdx < len(self.nodes):
            self.nodes[self.updateIdx].update(self.var)
            if self.nodes[self.updateIdx].state in ("repeating", 'doing'):
                break
            self.updateIdx += 1
        
        set_value('boss_health', self.hp)
        set_value('boss_maxHealth', self.maxHp)
        
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
            
    def kill(self, state):
        print('killed')
        set_value('boss_alive', False)
        for i in get_value('boss_effect'):
            if i.__class__.__name__ != 'SpellCardBonus':
                i.kill()
        super().kill()
        
    def checkDistance(self):
        dist = functions.dist((get_value('player').x, get_value('player').y), (self.x, self.y))
        miniDist = get_value('enemypos')[2]
        if self.x <= 384 and self.x >= 0 and self.y <= 448 and self.y>=0 and dist<miniDist:
            set_value('enemypos',(self.x,self.y,dist))
        
    def truePos(self):
        self.rect.center = (self.x, self.y)
        
    def move_to(self):
        self.direction = 0
        if self.movingFrame:
            if self.target_x > self.start_x:
                self.direction = 1
            elif self.target_x < self.start_x:
                self.direction = -1
            self.movingFrame -= 1
            if self.moving_mode==0:
                self.x += (self.target_x-self.start_x)/self.maxMovingFrame
                self.y += (self.target_y-self.start_y)/self.maxMovingFrame
            elif self.moving_mode==1:
                self.x = functions.acc(self.start_x, self.target_x, self.maxMovingFrame-self.movingFrame, self.maxMovingFrame)
                self.y = functions.acc(self.start_y, self.target_y, self.maxMovingFrame-self.movingFrame, self.maxMovingFrame)
            elif self.moving_mode==2:
                self.x = functions.dcc(self.start_x, self.target_x, self.maxMovingFrame-self.movingFrame, self.maxMovingFrame)
                self.y = functions.dcc(self.start_y, self.target_y, self.maxMovingFrame-self.movingFrame, self.maxMovingFrame)
            elif self.moving_mode==3:
                self.x = functions.acc_dcc(self.start_x, self.target_x, self.maxMovingFrame-self.movingFrame, self.maxMovingFrame)
                self.y = functions.acc_dcc(self.start_y, self.target_y, self.maxMovingFrame-self.movingFrame, self.maxMovingFrame)
            self.truePos()
        
    def draw(self, screen):
        self.nimbus_angle = (self.nimbus_angle+5)%360
        functions.drawImage(self.nimbus, (self.x, self.y), self.nimbus_angle, screen)
        self.ani_y = functions.sin(self.lastFrame)*10
        if self.default:
            self.rot = (self.rot+531)%360
            functions.drawImage(ImageManager.getImage("Boss","Default"), (self.x,self.y), self.rot, screen)
            return
        if not self.direction:
            self.right_ani_frame = 0
            self.left_ani_frame = 0
            if self.lastFrame % self.animation_interval == 0:
                self.animation_frame = (self.animation_frame+1)%len(self.idle_frame)
            functions.drawImage(self.image[self.idle_frame[self.animation_frame]], (self.x, self.y+self.ani_y), 0, screen)

        elif self.direction == 1:
            if self.lastFrame % self.animation_interval == 0:
                self.right_ani_frame = (min(self.right_ani_frame+1, len(self.right_frame)-1))
            functions.drawImage(self.right_image[self.right_frame[self.right_ani_frame]], (self.x, self.y+self.ani_y), 0, screen)
        else:
            if self.lastFrame % self.animation_interval == 0:
                self.left_ani_frame = (min(self.left_ani_frame+1, len(self.left_frame)-1))
            functions.drawImage(self.left_image[self.left_frame[self.left_ani_frame]], (self.x, self.y+self.ani_y), 0, screen)