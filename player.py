import pygame
import bullet
import functions
import effect
import obj

from pygame.locals import *
from const import *
from math import *
from random import *
from global_var import *
import ImageManager
import SoundManager

fireFrame = 0
floatgunFrame = 0
floatgunAngle = 0

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.hitbox = pygame.Surface((4,4))
        self.hitbox.fill((255,255,255))
        self.rect = self.hitbox.get_rect() # hitbox
        self.x = 192
        self.y = 600
        self.life = 40 # life point
        self.boom = 20 # boom point
        self.immune = False # unhitable by bullets
        self.itemCollectDistance=100 # distance to collect items
        self.immuneFrame = 0 # frame for immune
        self.index = 0 # cartoon frame
        self.indexCount = 8 # max cartoon frame
        self.power = 100 # power point
        self.lastlevel = 1 # check for power change
        self.powerLevel = 1 # power level
        self.score = 0 # score get
        self.distx = 1.5 # distance x for floatGun
        self.disty = 1.5 # distance y for floatGun
        self.distTimes = 1.5 # distance times for floatGun
        self.shiftdown = False # check for shift down
        self.lowSpeed = 2 # low speed for shift
        self.highSpeed = 5 # high speed for shift
        self.gethit = True # check for get hit
        self.backing = False # check for backing to the stage
        self.boomlow = False # speed for Marisa booming
        self.booming = False # isBooming
        self.isAlive = True # check for pausing
        self.lastFrame = 0

    #change cartoon frame
    def LEFT(self):
        self.index = 8
        self.indexCount = 16
    def RIGHT(self):
        self.index = 16
        self.indexCount = 24
    def IDLE(self):
        self.index = 0
        self.indexCount = 8

    #moving
    #x:horizontal, y:vertical, c:check for booming
    def Movement(self, x, y, c):
        if not self.shiftdown:
            speed = self.highSpeed
            if c:
                speed = sqrt(self.highSpeed)
        else:
            speed = self.lowSpeed
            if c:
                speed = sqrt(self.lowSpeed)
        if self.booming and self.boomlow:
            speed*=0.2
        self.x += speed*x
        self.y += speed*y
        if self.rect.top < 24 and y < 0:
            self.y = 24
        if self.rect.bottom > 448-24 and y > 0:
            self.y = 448-24
        if self.rect.left < 16 and x < 0:
            self.x = 16
        if self.rect.right > 384-16 and x > 0:
            self.x = 384-16
        
    #check for power
    def checkPower(self,floatguns):
        if self.power >= 400:
            self.power = 400
        if self.power <= 100:
            self.power = 100
        self.powerLevel = floor(self.power/100)
        if self.lastlevel < self.powerLevel:
            SoundManager.play('powerup_sound',0.35,True)
        if len(floatguns) < self.powerLevel:
            #floatguns.empty()
            for i in range(len(floatguns), self.powerLevel):
                if self.__class__.__name__ == 'REIMU':
                    new_floatgun = REIMU_FLOATGUN(i+1)
                else:
                    new_floatgun = MARISA_FLOATGUN(i+1)
                floatguns.add(new_floatgun)
        elif len(floatguns) > self.powerLevel:
            for i in floatguns:
                if i.idx > self.powerLevel:
                    i.kill()
        self.lastlevel = self.powerLevel
        set_value('player_power', self.power)
        set_value('player_firelevel', self.powerLevel)

    def checkImmune(self):
        if self.immuneFrame:
            self.immuneFrame -= 1
            
    def checkBooming(self):
        if self.booming:
            self.booming -= 1

    def checkLife(self):
        if self.life <= 0 and self.isAlive:
            set_value('state', 'pause')
            set_value('load_pauseScreen', True)
            self.isAlive = False

    #check for get hit
    #player will back to the stage from the bottom of screen
    def reset(self):
        if self.gethit:
            self.gethit = False
            self.backing = True
            self.x = 192
            self.y = 500
        if self.backing:
            if self.y >= 420:
                self.y -= 3
            else:
                self.y -= 2
        if self.y <= 400:
            self.backing = False

    def update(self, frame, keys, keys_last, effects, floatguns):
        global fireFrame
        self.lastFrame+=1
        if keys[K_LSHIFT]:
            self.itemCollectDistance=75
            self.shiftdown = True
        else:
            self.itemCollectDistance=37
            self.shiftdown = False
        if keys[K_z] and not keys_last[K_z] or not keys[K_z]:
            fireFrame=0
        if keys[K_z]:
            fireFrame+=1
        self.checkPower(floatguns)
        self.reset()
        #update the player movement
        if keys[K_LEFT] and not self.backing:
            if keys[K_UP]:
                self.Movement(-1, -1, True)
            elif keys[K_DOWN]:
                self.Movement(-1, 1, True)
            else:
                self.Movement(-1, 0, False)
            if keys[K_LEFT] and not keys_last[K_LEFT]:
                self.LEFT()
                if keys[K_RIGHT]:
                    self.IDLE()
        if keys[K_RIGHT] and not self.backing:
            if keys[K_UP]:
                self.Movement(1, -1, True)
            elif keys[K_DOWN]:
                self.Movement(1, 1, True)
            else:
                self.Movement(1, 0, False)
            if keys[K_RIGHT] and not keys_last[K_RIGHT]:
                self.RIGHT()
                if keys[K_LEFT]:
                    self.IDLE()
        if keys[K_UP] and not self.backing and not (keys[K_DOWN] or keys[K_RIGHT] or keys[K_LEFT]):
            self.Movement(0, -1, False)
        if keys[K_DOWN] and not self.backing and not (keys[K_UP] or keys[K_RIGHT] or keys[K_LEFT]):
            self.Movement(0, 1, False)
        if not keys[K_LEFT] and keys_last[K_LEFT] and not self.backing:
            self.IDLE()
            if keys[K_RIGHT]:
                self.RIGHT()
        if not keys[K_RIGHT] and keys_last[K_RIGHT] and not self.backing:
            self.IDLE()
            if keys[K_LEFT]:
                self.LEFT()
        #update the player cartoon frame
        set_value('player_indexCount', self.indexCount)
        self.rect.center = ((self.x, self.y))
        set_value('player_tx', self.x)
        set_value('player_ty', self.y)
        self.checkImmune()
        self.checkBooming()
        self.checkLife()

#博丽 灵梦
class REIMU(Player):
    def __init__(self):
        super().__init__()
        self.hitbox = pygame.Surface((4,4)).convert_alpha()
        self.hitbox.fill((255,255,255))
        self.rect = self.hitbox.get_rect()
        self.image = ImageManager.getImage("Player", "Reimu")

    def update(self, playerGuns, lasers, frame, keys, keys_last, effects, enemy_bullets, items, floatguns):
        #self.FloatGun()
        global floatgunFrame
        floatgunFrame=(floatgunFrame+1)%36
        super().update(frame, keys, keys_last, effects, floatguns)
        if get_value('dialog'):
            return
        if keys[K_z] and not self.backing:
            self.fire(playerGuns)
            if fireFrame%4==0:
                SoundManager.play('shoot_sound',0.2,True)
        if keys[K_x] and not keys_last[K_x] and self.boom>=10 and not self.booming:
            for i in get_value('boss_effect'):
                if i.__class__.__name__ == 'SpellCardBonus':
                    i.failed = True
                    break
            self.dream_seal(playerGuns,enemy_bullets,effects,items)
            self.boom -= 10
            self.immuneFrame = 300
            self.booming = 300

    #shooting   
    def fire(self, playerGuns):
        if fireFrame%3==0:
            self.main_fire(playerGuns)

    #主子弹
    def main_fire(self, playerGuns):
        for i in range(-1,2,2):
            new_fire=bullet.reimuMainSatsu(self.x+14*i,self.y)
            playerGuns.add(new_fire)
                    
    #梦想封印
    def dream_seal(self ,playerGuns,enemy_bullets,effects,items):
        for i in range(0,8):
            new_boom = bullet.Dream_Seal(self.x, self.y, i)
            playerGuns.add(new_boom)
        SoundManager.play('playerSpell_sound',0.4)
    
        
    def draw(self, screen):
        frame = self.lastFrame
        #self.power += 1
        if frame%4 == 0:
            self.index += 1
        if self.index >= self.indexCount and self.indexCount >= 16:
            self.index -= 4
        elif self.index >= self.indexCount:
            self.index = 0
        if get_value('test_hitbox'):
            functions.drawImage(self.hitbox,self.rect.center,0,screen)
        else:
            functions.drawImage(self.image[self.index], self.rect.center, 0, screen)
            

#雾雨 魔里沙
class MARISA(Player):
    def __init__(self):
        super().__init__()
        self.hitbox = pygame.Surface((4,4)).convert_alpha()
        self.hitbox.fill((255,255,255))
        self.rect = self.hitbox.get_rect()
        self.image = ImageManager.getImage('Player', 'Marisa') #marisa sprite sheet
        self.fireFrame=-1 #update the shooting interval
        self.floatImage = get_value('Marisa_FloatGun') #float gun image
        self.gunCircle = 1 #decide the float gun size
        self.angle = 0 #update dunCircle by sine
        self.boomlow=True #low speed when booming

    def update(self, playerGuns,lasers, frame, keys, keys_last, effects, enemy_bullets, items, floatguns):
        global floatgunFrame, floatgunAngle
        floatgunAngle=(floatgunAngle+12)%360
        floatgunFrame=1+sin(radians(floatgunAngle))*0.2
        super().update(frame, keys, keys_last, effects, floatguns)
        if get_value('dialog'):
            return
        if keys[K_z] and not keys_last[K_z]:
            self.fireFrame=0
        if keys[K_z] and not self.backing:
            self.fire(playerGuns)
            if fireFrame%4==0:
                SoundManager.play('shoot_sound',0.2,True)
        if keys[K_x] and not keys_last[K_x] and self.boom >= 10 and not self.booming:
            for i in get_value('boss_effect'):
                if i.__class__.__name__ == 'SpellCardBonus':
                    i.failed = True
                    break
            self.master_spark(playerGuns, effects, enemy_bullets, items)
            self.boom -= 10
            self.immuneFrame = 340
            self.booming = 340
                                           
    def fire(self, playerGuns):
        frame = self.fireFrame+1
        self.fireFrame += 1
        if frame%3==0:
            self.main_fire(playerGuns)
            
    def main_fire(self, playerGuns):
        new_fire=bullet.marisaMainBullet(self.x-14,self.y)
        playerGuns.add(new_fire)
        new_fire=bullet.marisaMainBullet(self.x+14,self.y)
        playerGuns.add(new_fire)
                    
    #大师火花
    def master_spark(self, playerGuns, effects, enemy_bullets, items):
        set_value('screen_shaking', True)
        new_boom = bullet.Master_Spark()
        new_boom.initial(effects, enemy_bullets, items)
        playerGuns.add(new_boom)
        SoundManager.play('playerSpell_sound',0.4)

    def draw(self, screen):
        frame = get_value('frame')
        if frame%4 == 0:
            self.index += 1
        if self.index >= self.indexCount and self.indexCount >= 16:
            self.index -= 4
        elif self.index >= self.indexCount:
            self.index = 0
        if get_value('test_hitbox'):
            functions.drawImage(self.hitbox,self.rect.center,0,screen)
        else:
            functions.drawImage(self.image[self.index], self.rect.center, 0, screen)
            

class FLOATGUN(obj.OBJ):
    def __init__(self, idx):
        super().__init__()
        self.image = get_value('ReimuFloatGun')
        self.idx = idx
        self.create_pos = [[0,-40],[0,-40],[0,-50],[0,-40]]
        self.target_pos_1 = [[0,-40],[0,-25],[-20,40],[-10,-40],[-35,20],[-30,-35],[-45,15],[-30,-35]]
        self.target_pos_2 = [[20,40],[10,-40],[35,20],[30,-35],[45,20],[30,-35]]
        self.target_pos_3 = [[0,50],[0,-45],[-15,40],[-10,-45]]
        self.target_pos_4 = [[15,40],[10,-45]]
        self.angle_list = [[270],[240,300],[240,300,270],[240,300,260,280]]
        self.x = 0
        self.y = 0
        self.fireFrame = -1
        self.px = -10
        self.py = -10
        
    def update(self, screen, player, bullets, lasers, keys, keys_last):
        shift = keys[K_LSHIFT]
        if self.idx==1:
            dx = self.target_pos_1[(player.powerLevel-1)*2+shift][0]-self.x
            dy = self.target_pos_1[(player.powerLevel-1)*2+shift][1]-self.y
        elif self.idx==2:
            dx = self.target_pos_2[(player.powerLevel-2)*2+shift][0]-self.x
            dy = self.target_pos_2[(player.powerLevel-2)*2+shift][1]-self.y
        elif self.idx==3:
            dx = self.target_pos_3[(player.powerLevel-3)*2+shift][0]-self.x
            dy = self.target_pos_3[(player.powerLevel-3)*2+shift][1]-self.y
        elif self.idx==4:
            dx = self.target_pos_4[(player.powerLevel-4)*2+shift][0]-self.x
            dy = self.target_pos_4[(player.powerLevel-4)*2+shift][1]-self.y
        
        self.x += dx/5*0.8
        self.y += dy/5*0.8
        if self.px==-10:
            self.px = player.x
            self.py = player.y
        else:
            dx = player.x-self.px
            dy = player.y-self.py
            dx*=0.4
            dy*=0.4
            self.px+=dx
            self.py+=dy
        
        if keys[K_z] and not get_value('dialog') and not player.backing:
            self.fire(bullets, lasers, shift, player)
        self.draw(screen)
    
    def fire(self, bullets, lasers, shift, player):
        pass
    
    def draw(self, screen):
        pass
                    
class REIMU_FLOATGUN(FLOATGUN):
    def __init__(self, idx):
        super().__init__(idx)
        self.image = ImageManager.getImage('Player', 'Reimu_Floatgun')
        self.omiga = 10
        
    def fire(self, bullets, lasers, shift, player):
        #诱导弹
        if not shift:
            if fireFrame%8==0:
                new_fire=bullet.reimuTargetSatsu(self.x+self.px, self.y+self.py,self.angle_list[player.powerLevel-1][self.idx-1])
                bullets.add(new_fire)
        #封魔针
        else:
            if fireFrame%4==0:
                for i in range(-1,2,2):
                    new_fire=bullet.reimuShiftSatsu(self.x+self.px+8*i, self.y+self.py)
                    bullets.add(new_fire)
    
    def draw(self, screen):
        self.countRot()
        functions.drawImage(self.image, (self.x+self.px, self.y+self.py), self.rot, screen)

            
class MARISA_FLOATGUN(FLOATGUN):
    def __init__(self, idx):
        super().__init__(idx)
        self.image = ImageManager.getImage('Player', 'Marisa_Floatgun')
        self.angle_list = [[270],[260,280],[260,280,270],[260,280,270,270]]
        self.angle=0
        
    def fire(self, bullets, lasers, shift, player):
        #激光
        if not shift:
            if len(lasers)!=player.powerLevel:
                lasers.empty()
                for i in range(player.powerLevel):
                    new_fire=bullet.marisaLaser()
                    new_fire.initial(self.x+self.px, self.y+self.py, self.angle_list[player.powerLevel-1][i],i+1)
                    lasers.add(new_fire)
            for i in lasers:
                if i.idx==self.idx:
                    i.x = self.x+self.px
                    i.y = self.y+self.py
                    i.floatgunFrame = floatgunFrame
                    break
        #魔法导弹
        else:
            if lasers:
                lasers.empty()
            if fireFrame%8==0 and self.idx<=2:
                new_fire=bullet.marisaMissile(self.x+self.px, self.y+self.py)
                bullets.add(new_fire)
            elif fireFrame%8==4 and self.idx>=3:
                new_fire=bullet.marisaMissile(self.x+self.px, self.y+self.py)
                bullets.add(new_fire)
                
    def draw(self, screen):
        img = pygame.transform.smoothscale(self.image, (16*floatgunFrame, 16*floatgunFrame))
        functions.drawImage(img, (self.x+self.px,self.y+self.py), 0, screen)
