import pygame
import functions
import SoundEffect

from const import *
from math import *
from random import *
from global_var import *

class Reimu_main_fire_effect(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = get_value('Reimu_Main_Satsu')
        self.frame = 0
        self.part = 1
        self.interval = 5
        self.speed = 4
        self.tx = 0
        self.ty = 0

    def initial(self, tx, ty):
        self.tx = tx
        self.ty = ty

    def update(self, screen):
        self.frame += 1
        self.ty -= self.speed
        if self.frame % self.interval == 0:
            self.part += 1
        if self.part == 5:
            self.kill()
        else:
            functions.drawImage(self.image[self.part], (self.tx,self.ty), 270, screen)

class Reimu_target_fire_effect(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = get_value('Reimu_Target_Satsu')
        self.frame = 0
        self.part = 0
        self.interval = 5
        self.speed = 4
        self.tx = 0
        self.ty = 0

    def initial(self, tx, ty):
        self.tx = tx
        self.ty = ty

    def update(self, screen):
        self.frame += 1
        self.ty -= self.speed
        if self.frame % self.interval == 0:
            self.part += 1
        if self.part == 4:
            self.kill()
        else:
            functions.drawImage(self.image[self.part], (self.tx,self.ty), self.frame*-12, screen)

class Reimu_shift_fire_effect(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = []
        for i in range(0,2):
            image = pygame.Surface((16, 96)).convert_alpha()
            image.fill((0, 0, 0, 0))
            image.blit(get_value('Reimu_Shift_Satsu')[i], (0, 0))
            self.image.append(image)
        for i in range(0,4):
            image = pygame.Surface((16, 96)).convert_alpha()
            image.fill((0, 0, 0, 0))
            image.blit(get_value('Reimu_Shift_Satsu')[1], (0, 0))
            image.set_alpha(160-i*32)
            self.image.append(image)
        self.frame = 0
        self.part = 0
        self.interval = 3
        self.speed = 4
        self.tx = 0
        self.ty = 0

    def initial(self, tx, ty):
        self.tx = tx
        self.ty = ty

    def update(self, screen):
        self.frame += 1
        self.ty -= self.speed
        if self.frame % self.interval == 0:
            self.part += 1
        if self.part == 6:
            self.kill()
        else:
            functions.drawImage(self.image[self.part], (self.tx,self.ty), 270, screen)
            
class Dream_seal_flying_effect(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.lastFrame=0
        self.maxFrame=15
        self.tx=0.0
        self.ty=0.0
        
    def initial(self,tx,ty,colorNum):
        self.effect=pygame.transform.smoothscale(get_value('bullet_create')[colorNum], (84,84))
        self.effect.set_alpha(160)
        self.rect = self.effect.get_rect()
        self.rect.centerx=tx
        self.rect.centery=ty
        
    def update(self,screen):
        self.lastFrame+=1
        if self.lastFrame % 5==0:
            self.effect.set_alpha(self.effect.get_alpha()-20)
        if self.lastFrame>self.maxFrame:
            self.kill()
        img = pygame.transform.rotozoom(self.effect, 0, 1-self.lastFrame/20)
        img.set_alpha(240-self.lastFrame*4)
        functions.drawImage(img, self.rect.center, 270, screen)
        
class Dream_seal_effect(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.lastFrame=0
        self.maxFrame=60
        self.tx=0.0
        self.ty=0.0
        self.speedx=uniform(-5,5)
        self.speedy=uniform(-5,5)
        
    def initial(self,tx,ty,colorNum):
        self.effect=pygame.transform.smoothscale(get_value('bullet_create')[colorNum], (128,128))
        #self.effect.set_alpha(128)
        self.rect = self.effect.get_rect()
        self.rect.centerx=tx
        self.rect.centery=ty
        
    def movement(self):
        self.rect.centerx += self.speedx
        self.rect.centery += self.speedy
        
    def update(self,screen):
        self.lastFrame+=1
        if self.lastFrame == 5:
            set_value('screen_shaking', False)
        if self.lastFrame>self.maxFrame:
            set_value('booming', False)
            self.kill()
        self.movement()
        img = pygame.transform.rotozoom(self.effect, 0, 1-self.lastFrame/60)
        img.set_alpha(240-self.lastFrame*4)
        functions.drawImage(img, self.rect.center, 270, screen)
            
class Marisa_main_fire_effect(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.effect = get_value('Marisa_Main_Bullet')
        self.pos=(0,0)
        self.lastFrame=0
        self.index = 1
        
    def initial(self, pos):
        self.pos = pos
    
    def update(self, screen):
        self.lastFrame += 1
        if self.lastFrame%5==0:
            self.index+=1
        if self.index==4:
            self.kill()
        else:
            functions.drawImage(self.effect[self.index], self.pos, 270, screen)
        
class Marisa_missile_effect(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.effect = get_value('Marisa_Missile')
        self.pos = (0,0)
        self.lastFrame=0
        self.index=1
        
    def initial(self, pos):
        self.pos = pos
        
    def update(self, screen):
        self.lastFrame += 1
        if self.lastFrame%2==0:
            self.index+=1
        if self.index==8:
            self.kill()
        else:
            functions.drawImage(self.effect[self.index], self.pos, 270, screen)
            
class Master_spark_effect(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.effect = get_value('Master_Spark_Wave')
        self.posx=0
        self.posy=0
        self.lastFrame=0
        self.maxFrame=60
        self.speedx=0
        self.speedy=0
        
    def setSpeed(self,angle):
        s=sin(radians(angle))
        c=cos(radians(angle))
        self.speedy=s*80
        self.speedx=c*80
        
        
    def initial(self,pos,angle):
        self.posx = pos[0]
        self.posy = pos[1]
        self.angle = angle
        self.setSpeed(angle)
        
    def update(self,screen):
        self.lastFrame+=1
        if self.lastFrame > self.maxFrame:
            self.kill()
        self.posx += self.speedx
        self.posy += self.speedy
        functions.drawImage(self.effect, (self.posx, self.posy), self.angle, screen)
        

#my computer is so bad :(
#FPS becomes 10 when wave is excuting
class Stage_Begin_Surface(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.lastFrame=0
        self.maxFrame=360
        
    def initial(self,index):
        self.index=index
        self.effect=get_value('stage_%d_surface'%index)
        
    def update(self,screen):
        self.lastFrame+=1
        if self.lastFrame > self.maxFrame:
            self.kill()
        if self.lastFrame < 60:
            self.effect.set_alpha(self.lastFrame*4)
        elif self.lastFrame == 60:
            self.effect.set_alpha(255)
        elif self.lastFrame > 300:
            self.effect.set_alpha(255-((self.lastFrame-300)*4))
        functions.drawImage(self.effect,(384*magnitude/2+min(self.lastFrame/5,24)-24,300),270,screen)

class wave(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pos = [0, 0]
        self.radius = 0
        self.lastFrame = 0
        self.maxFrame = 75
        self.maxRadius = 3600  
        self.width = 10

    def initial(self, pos, bullets):
        self.pos=pos
        self.bullets = bullets

    def update(self, screen, effects):
        self.lastFrame += 1
        self.radius = round(self.maxRadius*(self.lastFrame/self.maxFrame))
        
        sub_image = screen.subsurface(pygame.Rect(32*magnitude, 16*magnitude, 384*magnitude, 448*magnitude)).convert_alpha()
        mask_image = pygame.Surface((384*magnitude, 448*magnitude), pygame.SRCALPHA).convert_alpha()
        mask_image.fill((0,0,0,0))
        
        pygame.draw.circle(sub_image, (0, 0, 0, 0), self.pos,self.radius,1800)
        sub_image.blit(mask_image, (0, 0))
        pixels = pygame.surfarray.pixels2d(screen)
        pixels ^= 2**32-1
        del pixels
        screen.blit(sub_image, (32*magnitude, 16*magnitude))
        
        if self.lastFrame == 40:
            for b in self.bullets:
                new_vanish = bulletVanish()
                new_vanish.initial(b.image, b.rect.center, b.angle)
                effects.add(new_vanish)
                b.kill()
        if self.maxFrame<=self.lastFrame:
            self.kill()

class bulletVanish(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.lastFrame=0
        self.c_pos=0
        self.part=0
        self.angle=0
        self.dAngle = randint(0, 360)
        self.effect = get_value('bulletsVanish')
        self.index = 0

    def initial(self,image,c_pos,angle):
        self.image=image
        self.c_pos=c_pos
        self.angle=angle

    def update(self,screen):
        self.lastFrame+=1
        self.part=1-self.lastFrame/24
        tempImage=pygame.transform.rotozoom(self.image,self.angle,self.part).convert_alpha()
        tempImage.set_alpha(168*self.part)
        functions.drawImage(tempImage, self.c_pos, 270, screen)
        #functions.drawImage(self.effect[self.index], self.c_pos, self.dAngle, screen)
        if self.lastFrame % 3 == 0:
            self.index += 1
        if self.lastFrame>=24:
            self.kill()


class enemyDeath(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frame = 0
        self.c_pos = 0
        self.part = 0
        self.angle = randint(0, 360)
        self.colorDict={'red':0,'blue':1,'yellow':2,'green':3}
        

    def initial(self, c_pos, color):
        self.c_pos = c_pos
        self.effect = get_value('enemyDeath')[self.colorDict.get(color)]

    def update(self, screen):
        self.frame += 1
        tempImage=pygame.transform.smoothscale(self.effect, (64+self.part*7, 48-self.part))
        tempImage.set_alpha(240-12*self.part)
        for i in range(0, 3):
            functions.drawImage(tempImage, self.c_pos, self.angle+120*i, screen)
        if self.frame % 3 == 0:
            self.part += 6
        if self.frame >= 24:
            self.kill()
            
class Ghost_flame_effect(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.effect = pygame.Surface((24,24)).convert_alpha()
        self.effect.fill((0,0,0,0))
        self.rect=self.effect.get_rect()
        self.colorDict = [(221,170,170), (170,204,170), (170,187,221), (238,221,170)]
        self.lastFrame=0
        self.maxFrame=60
        
    def initial(self,tx,ty,colorNum):
        self.rect.center=(tx,ty)
        pygame.draw.circle(self.effect, self.colorDict[colorNum], (12,12), 12)
        
    def movement(self):
        self.rect.centerx += uniform(0,1)*6-3
        self.rect.centery += uniform(0,1)*-1
        
    def checkValid(self):
        if self.lastFrame > self.maxFrame:
            self.kill()
        
    def update(self, screen):
        self.lastFrame+=1
        self.movement()
        self.checkValid()
        img = pygame.transform.rotozoom(self.effect, 0, self.maxFrame/(self.lastFrame+60))
        img.set_alpha(168-self.lastFrame*2)
        functions.drawImage(img, self.rect.center, 270, screen)
        
class Particle(pygame.sprite.Sprite):
    def __init__(self,color,pos,radius):
        super().__init__()
        self.surf = pygame.Surface((radius*2,radius*2)).convert_alpha()
        self.surf.fill((0,0,0,0))
        pygame.draw.circle(self.surf, color, (radius,radius), radius)
        self.rect = self.surf.get_rect()
        self.speedx = randint(-4, 4)
        self.speedy = randint(-4, 4)
        if self.speedx == 0:
            self.speedx=1
        if self.speedy == 0:
            self.speedy=1
        self.lastFrame=0
        self.maxFrame=60
        self.rect.center = pos
        
    def movement(self):
        self.rect.centerx += self.speedx
        self.rect.centery += self.speedy
        
    def checkValid(self):
        if self.lastFrame >= self.maxFrame:
            self.kill()
            
    def update(self, screen):
        self.lastFrame+=1
        self.movement()
        self.checkValid()
        self.surf.set_alpha(256-self.lastFrame/self.maxFrame*256)
        screen.blit(self.surf, self.rect)
        
class Item_Show_Score(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.lastFrame=0
        self.maxFrame=40
        self.numDict={'0':'〇','1':'一','2':'二','3':'三','4':'四','5':'五','6':'六','7':'七','8':'八','9':'九'}
        
    def initial(self,score,m,tx,ty):
        self.score=str(int(score))
        self.max=m
        self.t=''
        for i in range(0,len(self.score)):
            self.t+=self.numDict.get(self.score[i])
        if m:
            self.text=scoreshowFont.render(self.t,True,(245,236,22))
        else:
            self.text=scoreshowFont.render(self.t,True,(255,255,255))
        self.text_shadow=scoreshowFont.render(self.t,True,(0,0,0))
        rect = self.text.get_rect()
        self.surf = pygame.Surface((rect.w+1,rect.h+1)).convert_alpha()
        self.surf.fill((0,0,0,0))
        for i in range(-1,2):
            for j in range(-1,2):
                if i==0 and j == 0:
                    continue
                self.surf.blit(self.text_shadow, (i,j))
        self.surf.blit(self.text, (0,0))
        self.rect = self.surf.get_rect()
        self.rect.centerx=tx
        self.rect.centery=ty
    
    def movement(self):
        self.rect.centery -= 0.7
        
    def update(self,screen):
        self.lastFrame+=1
        if self.lastFrame >= self.maxFrame:
            self.kill()
        image=self.surf.copy()
        if self.lastFrame < 20:
            image.set_alpha(self.lastFrame*10)
        else:
            image.set_alpha(400-self.lastFrame*10)
        self.movement()
        screen.blit(image, self.rect.center)
        
class Boss_Attack_Effect(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.lastFrame=0
        self.image=get_value('boss_effect_image')
        
    def update(self, screen):
        self.lastFrame+=1
        if self.lastFrame==1:
            SoundEffect.play('spellStart_sound',0.5)
        if self.lastFrame <= 45:
            pygame.draw.circle(screen, functions.get_rainbow_color(radians(self.lastFrame*2)), get_value('boss_pos'), 600-self.lastFrame*(600/45), 30)
        if self.lastFrame==70:
            SoundEffect.play('spellEnd_sound',0.5)
        elif self.lastFrame >= 70 and self.lastFrame <= 90:
            pygame.draw.circle(screen, functions.get_rainbow_color(radians(self.lastFrame*2)), get_value('boss_pos'), (self.lastFrame-70)*45, 30)
        elif self.lastFrame > 90:
            self.kill()
        
class Timer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.timerpos=0
        self.times=0
        
    def update(self, screen, player):
        if not get_value('boss_alive'):
            self.kill()
        self.times-=1
        #times = get_value('timer')
        times=self.times/60
        ifSpell = get_value('ifSpell')
        if times <= 10 and times%1==0:
            SoundEffect.play('timeout_sound',1,0)
        if not ifSpell and self.timerpos > 0:
            self.timerpos -= 1
        elif ifSpell and self.timerpos < 40:
            self.timerpos += 1
        show_times = times
        timertext = numfont.render('%.2f' % show_times, True, WHITE)
        timertext_shadow = numfont.render('%.2f' % show_times, True, BLACK)
        timertext_rect = timertext.get_rect()
        timertext_rect.midtop=(768/2/2*magnitude,self.timerpos)
        if timertext_rect.colliderect(get_value('PLAYER_rect')):
            timertext.set_alpha(160)
            timertext_shadow.set_alpha(20)
        for i in range(-1,2):
            for j in range(-1,2):
                screen.blit(timertext_shadow, timertext_shadow.get_rect(midtop=(768/2/2*magnitude+i,self.timerpos+j)))
        screen.blit(timertext, timertext.get_rect(midtop=(768/2/2*magnitude,self.timerpos)))
        
class Spell_Name(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.spellFrame=0
        
    def initial(self, name):
        spellname = name
        spelltext = spellcardfont.render(spellname, True, WHITE)
        spelltext_shadow = spellcardfont.render(spellname, False, BLACK)
        self.w,self.h = spelltext.get_size()
        self.font_image = pygame.Surface((self.w,self.h+3)).convert_alpha()
        self.font_image.fill((0,0,0,0))
        for i in range(-1,2):
            for j in range(-1,2):
                self.font_image.blit(spelltext_shadow, spelltext_shadow.get_rect(topright=(self.w+i,3+j)))
        self.font_image.blit(spelltext, spelltext.get_rect(topright=(self.w,3)))
        self.rect = self.font_image.get_rect(topright=(768/2*magnitude,0))
        
    def update(self, screen, player):
        if not get_value('ifSpell'):
            self.kill()
        self.spellFrame+=1
        if self.spellFrame < 60:
            scalerate = 3-(self.spellFrame)/30
            img = pygame.transform.smoothscale(self.font_image, (self.w*scalerate,self.h*scalerate)).convert_alpha()
            rect = img.get_rect(topright=(768/2*magnitude,800/2*magnitude))
            if self.checkCollsion(rect):
                img.set_alpha(160)
            screen.blit(img, rect)
        elif self.spellFrame >= 60 and self.spellFrame <= 150:
            rect = self.font_image.get_rect(topright=(768/2*magnitude,800/2*magnitude))
            if self.checkCollsion(rect):
                self.font_image.set_alpha(160)
            else:
                self.font_image.set_alpha(255)
            screen.blit(self.font_image, rect)
        elif self.spellFrame >= 150 and self.spellFrame <= 200:
            moverate = 800/2*magnitude-(self.spellFrame-150)*(800/50/2*magnitude)
            rect = self.font_image.get_rect(topright=(768/2*magnitude,moverate))
            if self.checkCollsion(rect):
                self.font_image.set_alpha(160)
            else:
                self.font_image.set_alpha(255)
            screen.blit(self.font_image, rect)
        else:
            if self.checkCollsion(self.rect):
                self.font_image.set_alpha(160)
            else:
                self.font_image.set_alpha(255)
            screen.blit(self.font_image, self.rect)
            
    def checkCollsion(self,rect):
        if rect.colliderect(get_value('PLAYER_rect')):
            return True
        else:
            return False
        
class SpellCard_Bonus(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.bonus = 1000000
        self.times = 0
        self.maxTimes = 0
        self.lastFrame = -1
        self.showFrame = 0
        self.b = 'bonus: '
        self.bn = 'Failed'
        self.db = 0
        self.not_bonus = False
        
    def update(self, screen, player):
        #print(self.times)
        if not get_value('ifSpell'):
            if self.lastFrame != -1:
                self.showFrame = 100
                if not self.not_bonus:
                    player.score += self.bonus
                    self.image = get_value('SpellCard_Bonus_Image')
                    SoundEffect.play('cardget_sound', 0.5, 0)
                else:
                    self.image = get_value('Bonus_Failed_Image')
            self.lastFrame = -1
            self.not_bonus = False
            if self.showFrame:
                self.showFrame-=1
                rect = self.image.get_rect()
                rect.center = (384/2*1.5, 300)
                screen.blit(self.image, rect)
            return
        #print(player.gethit)
        if player.gethit or player.immuneFrame==299 if player.__class__.__name__=='REIMU' else player.immuneFrame==359:
            self.not_bonus = True
        if self.lastFrame == -1:
            self.bonus = 1000000
            self.maxTimes = self.times
            self.db = int(self.bonus/self.maxTimes)
        if not self.not_bonus:
            self.bonus_text = middlefont.render(self.b+str(self.bonus),True,WHITE)
            self.bonus_text_shadow = middlefont.render(self.b+str(self.bonus),True,BLACK)
        else:
            self.bonus_text = middlefont.render(self.b+self.bn,True,WHITE)
            self.bonus_text_shadow = middlefont.render(self.b+self.bn,True,BLACK)
        self.rect = self.bonus_text.get_rect()
        self.rect.topright=(384*1.5-20,40)
        self.times-=1
        self.lastFrame+=1
        self.bonus-=self.db
        if self.lastFrame >= 80:
            for i in range(-1,2):
                for j in range(-1,2):
                    screen.blit(self.bonus_text_shadow, (self.rect.x+i*2, self.rect.y+j*2))
            screen.blit(self.bonus_text, self.rect)
            
        
class Boss_Name(pygame.sprite.Sprite):
    def __init__(self, name):
        super().__init__()
        self.name = spellcardfont.render(name, True, WHITE)
        self.name_shadow = spellcardfont.render(name, True, BLACK)
        
    def update(self, screen, player):
        if not get_value('boss_alive'):
            self.kill()
        for i in range(-1,2):
            for j in range(-1,2):
                screen.blit(self.name_shadow, (10+i*2,10+j*2))
        screen.blit(self.name, (10,10))

class Health_Bar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
    def initial(self, maxHealth):
        self.maxHealth = maxHealth
        
    def update(self, screen, player):
        if not get_value('show_health'):
            return
        health = get_value('boss_health')
        scale = health/self.maxHealth
        if scale >= 0.75:
            end = scale*360-270
        else:
            end = scale*360+90
        healthBar = pygame.image.load('resource/HUD/health_3.png').convert_alpha()
        healthBar = pygame.transform.smoothscale(healthBar, (240,240))
        new_image = pygame.Surface((240, 240)).convert_alpha()
        new_image.fill((0,0,0,0))
        new_image.blit(healthBar, (0, 0))
        #for i in range (0, 3):
        #    for j in range (0, 10):
        #        pygame.draw.arc(get_value('healthbar_1'), (WHITE), (14+i, 14+i, 272-i*2, 272-i*2), radians(90+j), radians(end-0.1), 1)
        for j in range(1,11):
            pygame.draw.arc(new_image, (WHITE), (12, 12, 217, 217), radians(90+j/10), radians(end-0.1+j/10), 2)
        #self.drawArc(get_value('healthbar_1'), 108, 108, 99, 7, 0, 360, WHITE)
        #pygame.draw.arc(get_value('healthbar_1'), (WHITE), (9, 9, 198, 198), radians(90), radians(end-0.1), 7)
        rect = new_image.get_rect(center=(get_value('boss_pos')[0], get_value('boss_pos')[1]))
        if rect.colliderect(get_value('PLAYER_rect')):
            new_image.set_alpha(160)
        screen.blit(new_image, rect)