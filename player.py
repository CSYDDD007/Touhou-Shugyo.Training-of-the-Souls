import pygame
import bullet
import functions
import effect

from pygame.locals import *
from const import *
from math import *
from random import *
from global_var import *
import SoundEffect

fireFrame = 0
floatgunFrame = 0
floatgunAngle = 0

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.hitbox = pygame.Surface((4,4))
        self.hitbox.fill((255,255,255))
        self.rect = self.hitbox.get_rect() # hitbox
        self.tx = 384.0/2*1.5 # center position x
        self.ty = 1000.0/2*1.5 # center position y
        self.life = 4.0 # life point
        self.boom = 2.0 # boom point
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
        self.lowSpeed = 4 # low speed for shift
        self.highSpeed = 7 # high speed for shift
        self.gethit = True # check for get hit
        self.backing = False # check for backing to the stage
        self.boomlow = False # speed for Marisa booming
        self.lastFrame = 0

    #change cartoon frame
    def LEFT(self):
        self.index = 8
        self.indexCount = 16
    def RIGHT(self):
        self.index = 16
        self.indexCount = 24
    def BACK(self):
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
        if get_value('booming') and self.boomlow:
            speed*=0.2
        self.tx += speed*x
        self.ty += speed*y
        if self.rect.top < 18*magnitude and y < 0:
            self.ty = 18*magnitude
        if self.rect.bottom > 430*magnitude and y > 0:
            self.ty = 430*magnitude
        if self.rect.left < 12*magnitude and x < 0:
            self.tx = 12*magnitude
        if self.rect.right > 372*magnitude and x > 0:
            self.tx = 372*magnitude
        
    #check for power
    def checkPower(self,floatguns):
        if self.power >= 400:
            self.power = 400
        if self.power <= 100:
            self.power = 100
        self.powerLevel = floor(self.power/100)
        if self.lastlevel < self.powerLevel:
            SoundEffect.play('powerup_sound',0.35,True)
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

    def checkLife(self):
        set_value('player_HP', self.life)
        if self.life <= 0:
            set_value('pause', True)
            set_value('deadpause', True)
            set_value('player_alive', False)

    #check for get hit
    #player will back to the stage from the bottom of screen
    def reset(self):
        if self.gethit:
            self.gethit = False
            self.backing = True
            self.tx = 192*magnitude
            self.ty = 500*magnitude
        if self.backing:
            if self.ty >= 420*magnitude:
                self.ty -= 3*magnitude
            else:
                self.ty -= 2*magnitude
        if self.ty <= 400*magnitude:
            self.backing = False

    def update(self, frame, keys, keys_last, effects, floatguns):
        global fireFrame
        self.lastFrame+=1
        if not self.immuneFrame:
            self.power += 1
        if keys[K_LSHIFT]:
            set_value('shift_down', True)
            self.itemCollectDistance=75*magnitude
        else:
            set_value('shift_down', False)
            self.itemCollectDistance=37*magnitude
        if keys[K_z] and not keys_last[K_z]:
            fireFrame=0
        if keys[K_z]:
            fireFrame+=1
        self.shiftdown = get_value('shift_down')
        self.boom = get_value('player_Boom')
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
                    self.BACK()
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
                    self.BACK()
        if keys[K_UP] and not self.backing and not (keys[K_DOWN] or keys[K_RIGHT] or keys[K_LEFT]):
            self.Movement(0, -1, False)
        if keys[K_DOWN] and not self.backing and not (keys[K_UP] or keys[K_RIGHT] or keys[K_LEFT]):
            self.Movement(0, 1, False)
        if not keys[K_LEFT] and keys_last[K_LEFT] and not self.backing:
            self.BACK()
            if keys[K_RIGHT]:
                self.RIGHT()
        if not keys[K_RIGHT] and keys_last[K_RIGHT] and not self.backing:
            self.BACK()
            if keys[K_LEFT]:
                self.LEFT()
        #update the player cartoon frame
        set_value('player_indexCount', self.indexCount)
        self.rect.center = ((self.tx, self.ty))
        set_value('player_cx', self.tx)
        set_value('player_cy', self.ty)
        self.checkImmune()
        self.checkLife()

#博丽 灵梦
class REIMU(Player):
    def __init__(self):
        super().__init__()
        self.hitbox = pygame.Surface((4,4)).convert_alpha()
        self.hitbox.fill((255,255,255))
        self.rect = self.hitbox.get_rect()
        self.image = get_value('Player_Reimu') # reimu sprite sheet
        self.fireFrame=0 #update the shooting interval

    def update(self, playerGuns, lasers, frame, keys, keys_last, effects, enemy_bullets, items, floatguns):
        #self.FloatGun()
        global floatgunFrame
        floatgunFrame=(floatgunFrame+1)%36
        super().update(frame, keys, keys_last, effects, floatguns)
        if get_value('plot'):
            return
        if keys[K_z] and not self.backing:
            self.fire(playerGuns)
            if fireFrame%4==0:
                SoundEffect.play('shoot_sound',0.2,True)
        if keys[K_x] and not keys_last[K_x] and get_value('player_Boom')>=1 and not get_value('booming'):
            self.dream_seal(playerGuns,enemy_bullets,effects,items)
            set_value('player_Boom', self.boom-1)
            self.immuneFrame = 300
            set_value('booming', True)

    #shooting   
    def fire(self, playerGuns):
        if fireFrame%3==0:
            self.main_fire(playerGuns)

    #主子弹
    def main_fire(self, playerGuns):
        for i in range(-1,2,2):
            new_fire=bullet.reimuMainSatsu()
            new_fire.initial(self.tx+14*i,self.ty)
            playerGuns.add(new_fire)
                    
    #梦想封印
    def dream_seal(self ,playerGuns,enemy_bullets,effects,items):
        for i in range(0,8):
            new_boom = bullet.Dream_Seal()
            new_boom.initial(self.tx, self.ty, i*45,enemy_bullets,effects,items,i)
            playerGuns.add(new_boom)
        SoundEffect.play('playerSpell_sound',0.4)
    
        
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
            functions.drawImage(self.hitbox,self.rect.center,270,screen)
        else:
            functions.drawImage(self.image[self.index], self.rect.center, 270, screen)
        
class FLOATGUN(pygame.sprite.Sprite):
    def __init__(self, idx):
        super().__init__()
        self.image = get_value('ReimuFloatGun')
        self.rect = self.image.get_rect()
        self.idx = idx
        self.create_pos = [[0,-60],[0,-60],[0,-70],[0,-60]]
        self.target_pos_1 = [[0,-60],[0,-40],[-35,60],[-15,-60],[-55,20],[-30,-55],[-60,20],[-45,-50]]
        self.target_pos_2 = [[35,60],[15,-60],[55,20],[30,-55],[60,20],[45,-50]]
        self.target_pos_3 = [[0,70],[0,-60],[-20,60],[-15,-60]]
        self.target_pos_4 = [[20,60],[15,-60]]
        self.angle_list = [[270],[240,300],[240,300,270],[240,300,260,280]]
        self.gunCircle = 1
        self.tx = 0
        self.ty = 0
        self.fireFrame = -1
        self.px = -10
        self.py = -10
        
    def update(self, screen, player, bullets, lasers, keys, keys_last):
        shift = keys[K_LSHIFT]
        if self.idx==1:
            dx = self.target_pos_1[(player.powerLevel-1)*2+shift][0]-self.tx
            dy = self.target_pos_1[(player.powerLevel-1)*2+shift][1]-self.ty
        elif self.idx==2:
            dx = self.target_pos_2[(player.powerLevel-2)*2+shift][0]-self.tx
            dy = self.target_pos_2[(player.powerLevel-2)*2+shift][1]-self.ty
        elif self.idx==3:
            dx = self.target_pos_3[(player.powerLevel-3)*2+shift][0]-self.tx
            dy = self.target_pos_3[(player.powerLevel-3)*2+shift][1]-self.ty
        elif self.idx==4:
            dx = self.target_pos_4[(player.powerLevel-4)*2+shift][0]-self.tx
            dy = self.target_pos_4[(player.powerLevel-4)*2+shift][1]-self.ty
        
        self.tx += dx/5*0.8
        self.ty += dy/5*0.8
        if self.px==-10:
            self.px = player.tx
            self.py = player.ty
        else:
            dx = player.tx-self.px
            dy = player.ty-self.py
            dx*=0.4
            dy*=0.4
            self.px+=dx
            self.py+=dy
        
        self.rect.center = ((self.tx+self.px, self.ty+self.py))
        if keys[K_z] and not get_value('plot') and not player.backing:
            self.fire(bullets, lasers, shift, player)
        self.draw(screen)
    
    def fire(self, bullets, lasers, shift, player):
        pass
    
    def draw(self, screen):
        functions.drawImage(self.image, self.rect.center, floatgunFrame*10, screen)
        #self.gunCircle = (self.gunCircle+1)%36
                    
class REIMU_FLOATGUN(FLOATGUN):
    def __init__(self, idx):
        super().__init__(idx)
        self.image = get_value('ReimuFloatGun')
        
    def fire(self, bullets, lasers, shift, player):
        #诱导弹
        if not shift:
            if fireFrame%8==0:
                new_fire=bullet.reimuTargetSatsu()
                new_fire.initial(self.angle_list[player.powerLevel-1][self.idx-1],self.tx+self.px, self.ty+self.py)
                bullets.add(new_fire)
        #封魔针
        else:
            if fireFrame%4==0:
                for i in range(-1,2,2):
                    new_fire=bullet.reimuShiftSatsu()
                    new_fire.initial(self.tx+self.px+8*i, self.ty+self.py)
                    bullets.add(new_fire)
            

#雾雨 魔里沙
class MARISA(Player):
    def __init__(self):
        super().__init__()
        self.hitbox = pygame.Surface((4,4)).convert_alpha()
        self.hitbox.fill((255,255,255))
        self.rect = self.hitbox.get_rect()
        self.image = get_value('Player_Marisa') #marisa sprite sheet
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
        if get_value('plot'):
            return
        if keys[K_z] and not keys_last[K_z]:
            self.fireFrame=0
        if keys[K_z] and not self.backing:
            self.fire(playerGuns)
            if fireFrame%4==0:
                SoundEffect.play('shoot_sound',0.2,True)
        if keys[K_x] and not keys_last[K_x] and get_value('player_Boom')>=1 and not get_value('booming'):
            self.master_spark(playerGuns, effects, enemy_bullets, items)
            set_value('player_Boom', get_value('player_Boom')-1)
            self.immuneFrame = 360
            set_value('immune', True)
                                           
    def fire(self, playerGuns):
        frame = self.fireFrame+1
        self.fireFrame += 1
        if frame%3==0:
            self.main_fire(playerGuns)
            
    def main_fire(self, playerGuns):
        new_fire=bullet.marisaMainBullet()
        new_fire.initial(self.tx-14,self.ty)
        playerGuns.add(new_fire)
        new_fire=bullet.marisaMainBullet()
        new_fire.initial(self.tx+14,self.ty)
        playerGuns.add(new_fire)
                    
    #大师火花
    def master_spark(self, playerGuns, effects, enemy_bullets, items):
        set_value('screen_shaking', True)
        new_boom = bullet.Master_Spark()
        new_boom.initial(effects, enemy_bullets, items)
        playerGuns.add(new_boom)
        SoundEffect.play('playerSpell_sound',0.4)
        set_value('booming', True)

    def draw(self, screen):
        frame = get_value('frame')
        if frame%4 == 0:
            self.index += 1
        if self.index >= self.indexCount and self.indexCount >= 16:
            self.index -= 4
        elif self.index >= self.indexCount:
            self.index = 0
        if get_value('test_hitbox'):
            functions.drawImage(self.hitbox,self.rect.center,270,screen)
        else:
            functions.drawImage(self.image[self.index], self.rect.center, 270, screen)
            
class MARISA_FLOATGUN(FLOATGUN):
    def __init__(self, idx):
        super().__init__(idx)
        self.image = get_value('Marisa_FloatGun')
        self.angle_list = [[270],[260,280],[260,280,270],[260,280,270,270]]
        self.angle=0
        
    def fire(self, bullets, lasers, shift, player):
        #激光
        if not shift:
            if len(lasers)!=player.powerLevel:
                lasers.empty()
                for i in range(player.powerLevel):
                    new_fire=bullet.marisaLaser()
                    new_fire.initial(self.tx+self.px, self.ty+self.py, self.angle_list[player.powerLevel-1][i],i+1)
                    lasers.add(new_fire)
            for i in lasers:
                if i.idx==self.idx:
                    i.tx = self.tx+self.px
                    i.ty = self.ty+self.py
                    i.floatgunFrame = floatgunFrame
                    break
        #魔法导弹
        else:
            if lasers:
                lasers.empty()
            if fireFrame%16==0 and self.idx<=2:
                new_fire=bullet.marisaMissile()
                new_fire.initial(self.tx+self.px, self.ty+self.py)
                bullets.add(new_fire)
            elif fireFrame%16==8 and self.idx>=3:
                new_fire=bullet.marisaMissile()
                new_fire.initial(self.tx+self.px, self.ty+self.py)
                bullets.add(new_fire)
                
    def draw(self, screen):
        img = pygame.transform.smoothscale(self.image, (20*floatgunFrame, 20*floatgunFrame))
        functions.drawImage(img, self.rect.center, 270, screen)
