import pygame
import functions
import SoundManager
import ImageManager
import obj

from const import *
from math import *
from random import *
from global_var import *

class Reimu_main_fire_effect(obj.OBJ):
    def __init__(self,x,y):
        super().__init__()
        self.x, self.y = x, y
        self.setSpeed(3, 270)
        self.image = ImageManager.getImage('Player', 'Reimu_Main_Satsu')
        self.lastFrame = 0

    def update(self, screen):
        self.lastFrame += 1
        part = int(self.lastFrame//5)
        if part == 4:
            self.kill()
            return
        self.movement()
        functions.drawImage(self.image[part], (self.x, self.y), 0, screen)

class Reimu_target_fire_effect(obj.OBJ):
    def __init__(self,x,y,rot):
        super().__init__()
        self.x, self.y = x, y
        self.setSpeed(3, 270)
        self.image = ImageManager.getImage('Player', 'Reimu_Target_Satsu')
        self.lastFrame = 0
        self.rot = rot
        self.omiga = 20

    def update(self, screen):
        self.lastFrame += 1
        part = self.lastFrame//5
        if part == 4:
            self.kill()
            return
        self.movement()
        self.countRot()
        functions.drawImage(self.image[part], (self.x,self.y), self.rot, screen)

class Reimu_shift_fire_effect(obj.OBJ):
    def __init__(self,x,y):
        super().__init__()
        self.x, self.y = x, y
        self.setSpeed(3, 270)
        self.image = ImageManager.getImage("Player", 'Reimu_Shift_Bullet')
        self.lastFrame = 0

    def update(self, screen):
        self.lastFrame += 1
        if self.lastFrame == 20:
            self.kill()
            return
        self.movement()
        img = self.image[0].copy()
        img.set_alpha(functions.dcc(255, 0, self.lastFrame, 20))
        functions.drawImage(img, (self.x, self.y), 0, screen)
            
class Dream_seal_flying_effect(obj.OBJ):
    def __init__(self,x,y,colorNum):
        super().__init__()
        self.x, self.y = x, y
        self.image = pygame.transform.smoothscale(ImageManager.getImage('Bullet', 'create_effect')[colorNum], (84,84))
        self.lastFrame=0
        
    def update(self,screen):
        self.lastFrame+=1
        if self.lastFrame > 15:
            self.kill()
            return
        zoom = functions.linear(1, 0, self.lastFrame, 15)
        alpha = 255*zoom
        img = pygame.transform.rotozoom(self.image, 0, zoom)
        img.set_alpha(alpha)
        functions.drawImage(img, (self.x,self.y), 0, screen)
        
class Dream_seal_effect(obj.OBJ):
    def __init__(self,x,y):
        super().__init__()
        self.x, self.y = x, y
        self.setSpeed(randint(3,5), randint(0,360))
        self.image = pygame.transform.smoothscale(ImageManager.getImage('Bullet', 'create_effect')[randint(0,7)], (84,84))
        self.lastFrame=0
        self.maxFrame=60
        
    def update(self,screen):
        self.lastFrame+=1
        if self.lastFrame == 5:
            set_value('screen_shaking', False)
        if self.lastFrame>self.maxFrame:
            set_value('booming', False)
            self.kill()
            return
        self.movement()
        zoom = functions.linear(1, 0, self.lastFrame, 60)
        alpha = 255*zoom
        img = pygame.transform.rotozoom(self.image, 0, zoom)
        img.set_alpha(alpha)
        functions.drawImage(img, (self.x, self.y), 0, screen)
            
class Marisa_main_fire_effect(obj.OBJ):
    def __init__(self,x,y):
        super().__init__()
        self.x, self.y = x, y
        self.image = ImageManager.getImage("Player", "Marisa_Main_Bullet")[1:]
        self.lastFrame = 0

    def update(self, screen):
        self.lastFrame += 1
        part = int(self.lastFrame//4)
        if part==3:
            self.kill()
            return
        img = self.image[part].copy()
        img.set_alpha(functions.dcc(255, 0, self.lastFrame, 12))
        functions.drawImage(img, (self.x,self.y), 0, screen)
      
class Marisa_missile_effect(obj.OBJ):
    def __init__(self,x,y):
        super().__init__()
        self.x, self.y = x, y
        self.image = ImageManager.getImage("Player", 'Marisa_Missile')[2:]
        self.lastFrame = 0

    def update(self, screen):
        self.lastFrame += 1
        part = int(self.lastFrame//2)
        if part == 8:
            self.kill()
            return
        functions.drawImage(self.image[part], (self.x,self.y), 0, screen)
            
class Master_spark_effect(obj.OBJ):
    def __init__(self,pos,angle):
        super().__init__()
        self.image = ImageManager.getImage('Player', "Master_Spark_Effect")
        self.x, self.y = pos
        self.setSpeed(30, angle)
        self.out_of_wall = False
        
    def update(self,screen):
        self.movement()
        self.checkValid()
        functions.drawImage(self.image, (self.x, self.y), -self.angle+90, screen)
        
class EnterGameAnimation:
    def __init__(self):
        self.lastFrame = 0
        self.waitFrame = randint(0,10)
        self.maxFrame = 120
        self.angle = 0
        set_value('entering_game', True)
        self.bg = pygame.image.load('resource/image/loading_bg.png').convert_alpha()
        self.bg = pygame.transform.smoothscale(self.bg, (640,480)).convert_alpha()
        self.bg_left = pygame.Surface((320,480)).convert_alpha()
        self.bg_left.blit(self.bg, (0,0), (0,0,320,480))
        pygame.draw.rect(self.bg_left, (0,0,0), pygame.Rect(315,0,5,480))
        self.bg_right = pygame.Surface((320,480)).convert_alpha()
        self.loadtext = pygame.image.load('resource/image/loading.png').convert_alpha()
        fuka = pygame.image.load('resource/image/fuka.png').convert_alpha()
        self.fuka = pygame.transform.rotozoom(fuka, 0, 0.2).convert_alpha()
        
    def update(self, screen):
        if self.lastFrame == 60 and self.waitFrame:
            self.waitFrame -= 1
            self.lastFrame -= 1
        self.lastFrame += 1
        self.angle += 5
        if self.lastFrame == 61:
            set_value('state', 'game')
            functions.initialize()
        if self.lastFrame > self.maxFrame:
            set_value('battle_music', True)
            set_value('entering_game', False)
            set_value('entering_game_effect', None)
            del self
            return
        i = functions.sin(self.lastFrame/self.maxFrame*180)*320
        self.bg_right.blit(self.bg, (0,0), (320,0,320,480))
        pygame.draw.rect(self.bg_right, (0,0,0), pygame.Rect(0,0,5,480))
        self.bg_right.blit(self.loadtext, self.loadtext.get_rect(bottomright=(320-(640-525),470)))
        functions.drawImage(self.fuka, (320-(640-575), 430), self.angle, self.bg_right)
        screen.blit(self.bg_left, (-320+i, 0))
        screen.blit(self.bg_right, (640-i, 0))
        
class StageFadeInFadeOut(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.lastFrame = 0
        self.maxFrame = 180
        self.effect = pygame.Surface((384,448)).convert_alpha()
        self.effect.fill((0,0,0))
        
    def update(self, screen):
        self.lastFrame += 1
        if self.lastFrame > 180:
            self.kill()
            return
        if self.lastFrame <= 60:
            alpha = functions.linear(0, 255, self.lastFrame, 60)
        elif self.lastFrame > 60 and self.lastFrame <= 120:
            alpha=255
        else:
            alpha = functions.linear(255, 0, self.lastFrame-120, 60)
        self.effect.set_alpha(alpha)
        screen.blit(self.effect, (0,0))

class Stage_Begin_Surface(obj.OBJ):
    def __init__(self):
        super().__init__()
        self.lastFrame = 0
        self.surf = get_value('stage')
        self.x = 192+40

    def update(self, screen):
        self.lastFrame += 1
        if self.lastFrame > 180:
            self.kill()
        if self.lastFrame < 60:
            self.x = functions.dcc(192+40, 192, self.lastFrame, 60)
            alpha = functions.linear(0, 255, self.lastFrame, 60)
        elif self.lastFrame > 120:
            self.x = functions.acc(192, 192-40, self.lastFrame-120, 60)
            alpha = functions.linear(255, 0, self.lastFrame-120, 60)
        else:
            alpha = 255
        self.surf.set_alpha(alpha)
        screen.blit(self.surf, self.surf.get_rect(center=(self.x, 224)))


#my computer is so bad :(
#FPS becomes 10 when wave is excuting
class wave(obj.OBJ):
    def __init__(self, x, y, radius):
        super().__init__()
        self.x, self.y = x, y
        self.lastFrame = 0
        self.radius = radius

    def update(self, screen, bullets, lasers):
        self.lastFrame += 1
        if self.lastFrame > 60:
            self.kill()
            return
        radius = functions.dcc(0, self.radius, self.lastFrame, 60)
        width = functions.dcc(10, 30, self.lastFrame, 60)
        pygame.draw.circle(screen, functions.get_rainbow_color(radians(self.lastFrame*10)), (self.x,self.y), int(radius), int(width))
        for b in get_value('bullets'):
            if b.destroyable and functions.dist((self.x,self.y), (b.x,b.y)) <= radius+30:
                new_vanish = bulletVanish(b.x,b.y,b.color)
                get_value('effects').add(new_vanish)
                b.kill()

class bulletVanish(obj.OBJ):
    def __init__(self,x,y,color):
        super().__init__()
        self.color = pygame.Surface((64,64)).convert_alpha()
        color = bullet_colorDict[color]
        self.color.fill(color)
        self.image = ImageManager.getImage("Bullet", 'bullet_vanish')
        self.img_list = []
        for i in self.image:
            s = i.copy()
            s.blit(self.color, (0,0), special_flags=3)
            self.img_list.append(s)
        self.lastFrame=0
        self.rect = self.image[0].get_rect(center=(x,y))


    def update(self,screen):
        self.lastFrame += 1
        part = int(self.lastFrame//2)
        if part == 8:
            self.kill()
            return
        screen.blit(self.img_list[part], self.rect)

class enemyDeath(obj.OBJ):
    def __init__(self,pos,idx):
        super().__init__()
        self.x, self.y = pos
        self.image = ImageManager.getImage('Enemy','death_effect').copy()
        self.color = enemy_color_list[idx]
        color = pygame.Surface((64,64)).convert_alpha()
        color.fill(self.color)
        self.image.blit(color, (0,0), special_flags=3)
        self.lastFrame = 0
        self.rot = randint(0,360)

    def update(self, screen):
        self.lastFrame += 1
        if self.lastFrame == 10:
            self.kill()
            return
        w, h = functions.dcc(32,16,self.lastFrame,10), functions.dcc(32,128,self.lastFrame,10)
        img = pygame.transform.smoothscale(self.image, (w,h))
        img.set_alpha(functions.acc(200,100,self.lastFrame,10))
        functions.drawImage(img, (self.x,self.y), self.rot, screen)
        
            
class Ghost_flame_effect(obj.OBJ):
    def __init__(self,x,y,idx):
        super().__init__()
        self.effect = pygame.Surface((16,16)).convert_alpha()
        self.effect.fill((0,0,0,0))
        self.x, self.y = x, y
        color = enemy_color_list[idx]
        pygame.draw.circle(self.effect, color, (8,8), 8)
        self.lastFrame=0
        self.maxFrame=60
        self.speedy = randint(-3, -1)
        
    def update(self, screen):
        self.lastFrame+=1
        if self.lastFrame == 60:
            self.kill()
            return
        self.speedx = randint(-3,3)
        self.movement()
        self.checkValid()
        size = functions.linear(1,0,self.lastFrame,60)
        img = pygame.transform.rotozoom(self.effect, 0, size)
        alpha = functions.linear(156,0,self.lastFrame,60)
        img.set_alpha(alpha)
        functions.drawImage(img, (self.x,self.y), 0, screen)
        
class Particle(obj.OBJ):
    def __init__(self,color,pos,radius):
        super().__init__()
        self.x, self.y = pos
        self.surf = pygame.Surface((radius*2,radius*2)).convert_alpha()
        self.surf.fill((0,0,0,0))
        pygame.draw.circle(self.surf, color, (radius,radius), radius)
        self.rect = self.surf.get_rect(center=pos)
        self.setSpeed(randint(2,3), randint(0,360))
        self.lastFrame = 0
        self.out_of_wall = False

    def update(self, screen):
        self.lastFrame+=1
        if self.lastFrame == 60:
            self.kill()
            return
        self.movement()
        self.checkValid()
        alpha = functions.acc(255,0,self.lastFrame,60)
        self.surf.set_alpha(alpha)
        screen.blit(self.surf, self.rect)
        
class Damage_Show_Text(obj.OBJ):
    def __init__(self, damage, pos):
        super().__init__()
        self.x, self.y = pos
        self.text = str(damage)
        self.damage_text = ImageManager.stot("Regular_font", 16, '-'+str(damage), (200,0,0), (0,0,0), 1, 1)
        self.lastFrame = 0
        
    def update(self, screen):
        self.lastFrame += 1
        if self.lastFrame == 20:
            self.kill()
        if not get_value('damage_show'):
            return
        y = functions.dcc(self.y, self.y-20, self.lastFrame, 20)
        alpha = functions.dcc(255,0,self.lastFrame,20)
        self.damage_text.set_alpha(alpha)
        functions.drawImage(self.damage_text, (self.x,y), 0, screen)
        
class Item_Show_Score(obj.OBJ):
    def __init__(self,x,y,score,m):
        super().__init__()
        self.lastFrame=0
        self.maxFrame=40
        self.numDict={'0':'〇','1':'一','2':'二','3':'三','4':'四','5':'五','6':'六','7':'七','8':'八','9':'九'}
        self.x, self.y = x, y
        text = ''
        for i in score:
            text+=self.numDict[i]
        color = (255,255,0) if m else (255,255,255)
        self.text = ImageManager.stot("Regular_font", 12, score, color, (0,0,0), 1)

    def update(self, screen):
        self.lastFrame += 1
        if self.lastFrame == 40:
            self.kill()
            return
        y = functions.dcc(self.y, self.y-20, self.lastFrame, 40)
        alpha = functions.dcc(255,0,self.lastFrame,40)
        self.text.set_alpha(alpha)
        functions.drawImage(self.text, (self.x,y), 0, screen)
        
class BossName_Effect(pygame.sprite.Sprite):
    def __init__(self, name, cnt):
        super().__init__()
        self.effect = ImageManager.stot("Regular_font", 16, name, (0,255,0), (0,0,0), 2)
        self.star = pygame.transform.rotozoom(ImageManager.getImage("Boss", "Spellcard_Sign"), 0, 0.8)
        self.nsp = cnt
        
    def update(self, screen, player):
        screen.blit(self.effect, (0,0))
        for i in range(self.nsp):
            screen.blit(self.star, (5+i*16, 30))
        
class Timer(pygame.sprite.Sprite):
    def __init__(self, time, spellcard):
        super().__init__()
        self.time = time*60
        self.ty = 0
        self.spellcard = spellcard
        self.lastFrame = 0
        
    def update(self, screen, player):
        self.time -= 1
        self.lastFrame += 1
        if self.time == 0:
            self.kill()
            return
        if self.time<= 300 and self.time % 60 == 0:
            SoundManager.play("timeout_sound2", 1.0)
        elif self.time<=600 and self.time % 60 == 0:
            SoundManager.play("timeout_sound1", 1.0)
        if self.spellcard and self.lastFrame > 100 and self.lastFrame <= 140:
            self.ty = functions.acc_dcc(6, 36, self.lastFrame-100, 40)
        text = ImageManager.stot("Regular_font", 24, "{:.2f}".format(self.time/60), WHITE, BLACK, 2)
        screen.blit(text, text.get_rect(midtop=(192, self.ty)))
        
class SpellCardName(pygame.sprite.Sprite):
    def __init__(self, name):
        super().__init__()
        self.effect = ImageManager.stot("Regular_font", 12, name, WHITE, BLACK, 2)
        self.lastFrame = 0
        self.rect = self.effect.get_rect(topright=(444, 0))
        
    def update(self, screen, player):
        self.lastFrame += 1
        if self.lastFrame <= 60:
            img = pygame.transform.smoothscale(self.effect, (self.rect.w*functions.acc(3, 1, self.lastFrame, 60), self.rect.h*functions.acc(3, 1, self.lastFrame, 60))).convert_alpha()
            screen.blit(img, img.get_rect(topright=(382, 410)))
        elif self.lastFrame > 60 and self.lastFrame <= 100:
            screen.blit(self.effect, self.effect.get_rect(topright=(382, 410)))
        elif self.lastFrame > 100 and self.lastFrame <= 140:
            screen.blit(self.effect, self.effect.get_rect(topright=(382, functions.acc_dcc(410, 0, self.lastFrame-100, 40))))
        elif self.lastFrame > 140:
            screen.blit(self.effect, self.effect.get_rect(topright=(382, 0)))
            
        
class SpellCardBonus(pygame.sprite.Sprite):
    def __init__(self, bonus, waitTime, maxTime):
        super().__init__()
        self.bonus = bonus
        self.b_t = ImageManager.stot("Regular_font", 12, "Bonus", WHITE, BLACK, 2)
        self.f_t = ImageManager.stot("Regular_font", 12, "Failed", WHITE, BLACK, 2)
        self.b_effect = ImageManager.getImage("BattleUI", "Get_Spell_Card")
        self.f_effect = ImageManager.getImage("BattleUI", "Bonus_Failed")
        self.waitTime = waitTime*60
        self.maxTime = maxTime*60
        self.time = maxTime*60
        self.lastFrame = 0
        self.failed = 0
        self.fin = 0
        self.play = 0
        
    def update(self, screen, player):
        self.lastFrame += 1
        if self.fin:
            if not self.play:
                self.play=1
                if self.failed:
                    SoundManager.play('enemyDead_sound', 1)
                else:
                    SoundManager.play('cardget_sound', 1)
                    get_value('player').score+=int(self.bonus*(self.time/self.maxTime))
            self.fin -= 1
            if self.fin == 0:
                self.kill()
                return
            if not self.failed:
                screen.blit(self.b_effect, self.b_effect.get_rect(center=(192, 120)))
                bonus_text = ImageManager.stot("Regular_font", 24, str(int(self.bonus*(self.time/self.maxTime))), WHITE, BLACK, 2)
                screen.blit(bonus_text, bonus_text.get_rect(center=(192, 160)))
            else:
                screen.blit(self.f_effect, self.f_effect.get_rect(center=(192, 220)))
            return
        if self.lastFrame >= 140:
            if self.waitTime:
                self.waitTime -= 1
            else:
                self.time -= 1
            if not self.failed:
                bonus_text = ImageManager.stot("Regular_font", 12, str(int(self.bonus*(self.time/self.maxTime))), WHITE, BLACK, 2)
                screen.blit(self.b_t, self.b_t.get_rect(topright=(320, 20)))
                screen.blit(bonus_text, bonus_text.get_rect(topright=(380, 20)))
            else:
                screen.blit(self.f_t, self.f_t.get_rect(topright=(380, 20)))
                
class MagicSpell(pygame.sprite.Sprite):
    def __init__(self, pos, radius, color, time):
        super().__init__()
        self.radius = radius
        self.color = color
        self.pos = pos
        self.time = time
        self.lastFrame = 0
        
    def update(self, screen):
        self.lastFrame += 1
        if self.lastFrame == 1:
            SoundManager.play('spellStart_sound', 1.0)
        if self.lastFrame > self.time:
            self.kill()
            return
        radius = functions.dcc(self.radius, 4, self.lastFrame, self.time)
        theta = randint(0,360)
        if self.lastFrame < self.time/2 and self.lastFrame % 2 == 0:
            get_value('effects').add(SpellLeaf(0, uniform(1,2), (self.pos[0]+self.radius*functions.cos(theta)*0.8, self.pos[1]+self.radius*functions.sin(theta)*0.8), theta+180, randint(2,5), self.color))
        pygame.draw.circle(screen, self.color, self.pos, radius, int(functions.dcc(20,5,self.lastFrame, self.time)))
        
class SpellMagic(pygame.sprite.Sprite):
    def __init__(self, pos, color):
        super().__init__()
        self.pos = pos
        self.color = color
        self.lastFrame = 0
        
    def update(self, screen):
        self.lastFrame += 1
        if self.lastFrame == 1:
            for i in range(12):
                get_value('effects').add(SpellLeaf(0, uniform(1,2), self.pos, i*30, randint(3,5), self.color))
            SoundManager.play('spellEnd_sound', 1.0)
        if self.lastFrame > 60:
            self.kill()
            return
        radius = functions.dcc(0, 600, self.lastFrame, 60)
        pygame.draw.circle(screen, self.color, self.pos, radius, int(functions.dcc(5,20,self.lastFrame, 60)))
        
class BossExplosion(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.radius = 0
        self.width = 5
        self.lastFrame = 0
        SoundManager.play('bossDead_sound', 1.0)
        set_value('screen_shaking', 30)
        for i in range(0, 12):
            get_value('effects').add(SpellLeaf(0, uniform(1, 2), self.pos, i*30, randint(3, 5), (randint(0,255),randint(0,255),randint(0,255))))
        
    def update(self, screen):
        self.lastFrame += 1
        if self.lastFrame > 60:
            self.kill()
            return
        self.radius = functions.dcc(0, 800, self.lastFrame, 60)
        pygame.draw.circle(screen, functions.get_rainbow_color(radians(self.lastFrame*10)), self.pos, self.radius, 30)
        
class SpellLeaf(obj.OBJ):
    def __init__(self, type, size, pos, angle, speed, color=None):
        super().__init__()
        self.surf = pygame.Surface((32,32)).convert_alpha()
        self.surf.fill((0,0,0,0))
        self.img = ImageManager.getImage("Boss", 'boss_effect')
        if type:
            self.surf.blit(self.img, (0,0), (32,0,32,32))
        else:
            self.surf.blit(self.img, (0,0), (0,0,32,32))
            self.color = pygame.Surface((32,32)).convert_alpha()
            self.color.fill(color)
            self.surf.blit(self.color, (0,0), special_flags=3)
        self.x, self.y = pos
        self.lastFrame = 0
        self.surf = pygame.transform.smoothscale(self.surf, (32*size, 32*size)).convert_alpha()
        self.omiga = randint(5, 10)*(-1 if randint(0, 1)==1 else 1)
        self.setSpeed(speed, angle)
        
    def update(self, screen):
        self.lastFrame += 1
        if self.lastFrame > 60:
            self.kill()
            return
        self.checkValid()
        self.movement()
        self.countRot()
        img = self.surf.copy()
        img.set_alpha(functions.linear(255, 0, self.lastFrame, 60))
        functions.drawImage(img, (self.x, self.y), self.rot, screen)