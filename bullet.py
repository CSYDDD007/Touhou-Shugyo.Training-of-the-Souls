import pygame
import functions
import item
import effect
import obj

from const import *
from math import *
from random import *
from global_var import *
import SoundManager
import ImageManager

def createItem(x,y):
    x_now=x
    y_now=y
    if x_now<16:
        x_now=16
    if x_now>(384-16):
        x_now=(384-16)
    new_item=item.item(8, x_now, y_now)
    new_item.follow=True
    get_value('items').add(new_item)

#灵梦的札弹
class reimuMainSatsu(obj.OBJ):
    def __init__(self, x, y):
        super().__init__()
        self.x, self.y = x, y
        self.setSpeed(40,270)
        self.rect = pygame.Rect(0,0,16,64)
        self.image = ImageManager.getImage('Player', 'Reimu_Main_Satsu')[4]
        self.damage = get_value('Reimu_Main_Bullet')
        self.lastFrame = 0
        self.maxFrame = 100
        self.out_of_wall = False

    def update(self,screen):
        self.lastFrame += 1
        if self.lastFrame > self.maxFrame:
            self.kill()
            return
        self.checkValid()
        self.movement()
        functions.drawImage(self.image,(self.x,self.y),0,screen)
        
#灵梦的诱导弹
class reimuTargetSatsu(obj.OBJ):
    def __init__(self, x, y, angle):
        super().__init__()
        self.x, self.y = x, y
        self.setSpeed(10, angle)
        self.rect = pygame.Rect(0,0,16,16)
        self.image = ImageManager.getImage('Player', 'Reimu_Target_Satsu')[0]
        self.damage = get_value('Reimu_Satsu')
        self.out_of_wall = False
        self.navi = True
        self.lastFrame = 0

    def target(self):
        enemy_pos = get_value('enemypos')
        if enemy_pos[2] == 10000:
            return
        tx, ty = enemy_pos[0], enemy_pos[1]
        ta = functions.get_target_angle((0,0), (tx-self.x,ty-self.y))
        now_angle = self.angle+360 if self.angle < 0 else self.angle
        target_angle = ta+360 if ta < 0 else ta
        da = target_angle-now_angle
        if abs(da) < 7:
            return
        if da<0:
            if abs(da)>180:
                self.setSpeed(10, self.angle+7)
            else:
                self.setSpeed(10, self.angle-7)
        else:
            if da>180:
                self.setSpeed(10, self.angle-7)
            else:
                self.setSpeed(10, self.angle+7)

    def update(self,screen):
        self.lastFrame += 1
        self.checkValid()
        if self.lastFrame > 5:
            self.target()
        self.movement()
        self.countRot()
        functions.drawImage(self.image,(self.x,self.y),self.rot,screen)
        
#灵梦的封魔针
class reimuShiftSatsu(obj.OBJ):
    def __init__(self,x,y):
        super().__init__()
        self.x, self.y = x, y
        self.setSpeed(40,270)
        self.rect = pygame.Rect(0,0,16,64)
        self.image = ImageManager.getImage('Player', 'Reimu_Shift_Bullet')
        self.damage = get_value('Reimu_Pin')
        self.lastFrame = 0
        self.maxFrame = 120
        self.out_of_wall = False

    def update(self,screen):
        self.lastFrame+=1
        if self.lastFrame>=self.maxFrame:
            self.kill()
            return
        image = self.image[self.lastFrame%2]
        self.movement()
        self.checkValid()
        functions.drawImage(image,(self.x, self.y), 0, screen)
        
#灵符[梦想封印]
class Dream_Seal(obj.OBJ):
    def __init__(self, x, y, colorNum):
        super().__init__()
        self.x, self.y = x, y
        self.colorNum = colorNum
        self.angle = colorNum*45
        self.image = pygame.transform.smoothscale(ImageManager.getImage('Bullet', 'create_effect')[colorNum], (96,96))
        self.rect = pygame.Rect(0,0,96,96)
        self.damage = int(get_value('Dream Seal')/600)
        self.lastFrame = 0
        self.maxFrame = randint(280,340)
        self.cancelable = False
        
    def checkValid(self):
        if self.rect.top>=448 or self.rect.bottom<=0-80 or self.rect.right<=0-80 or self.rect.left>=384:
            self.doKill()
            
    def Circular_Motion(self):
        cx, cy = get_value('player').x, get_value('player').y
        self.angle = (self.angle+6)%360
        radius = 100 + 85 * cos((self.lastFrame+90)*0.04)
        self.x = cx+radius*functions.cos(self.angle)
        self.y = cy+radius*functions.sin(self.angle)
        self.rect.center = (self.x, self.y)

    def target(self):
        enemy_pos = get_value('enemypos')
        if enemy_pos[2] == 10000:
            self.setSpeed(0, 0)
            return
        tx, ty = enemy_pos[0], enemy_pos[1]
        ta = functions.get_target_angle((0,0), (tx-self.x,ty-self.y))
        self.setSpeed(10, ta)
        
    def update(self,screen):
        self.lastFrame+=1
        if self.lastFrame%3==0:
            new_effect = effect.Dream_seal_flying_effect(self.x+randint(-5,5),self.y+randint(-5,5),self.colorNum)
            get_value('effects1').add(new_effect)
        
        if self.lastFrame > self.maxFrame:
            self.doKill()
            return
        if self.lastFrame < self.maxFrame-60:
            self.Circular_Motion()
        else:
            self.cancelable=True
            self.target()
            self.movement()
        functions.drawImage(self.image, (self.x, self.y), 0, screen)
        hit=pygame.sprite.spritecollide(self, get_value('bullets'), False)
        for b in hit:
            if not b.destroyable:
                continue
            new_vanish = effect.bulletVanish(b.x,b.y,b.color)
            get_value('effects').add(new_vanish)
            createItem(b.x,b.y)
            b.kill()

    def doKill(self):
        set_value('screen_shaking', True)
        SoundManager.play('enemyShoot_sound1',0.25)
        for _ in range(0,6):
            new_effect = effect.Dream_seal_effect(self.x, self.y)
            get_value('effects').add(new_effect)
        self.kill()
        
#魔理沙的能量弹
class marisaMainBullet(obj.OBJ):
    def __init__(self,x,y):
        super().__init__()
        self.x, self.y = x, y
        self.setSpeed(40, -90)
        self.rect = pygame.Rect(0,0,16,48)
        self.image = ImageManager.getImage("Player", "Marisa_Main_Bullet")[0]
        self.damage = get_value('Marisa_Main_Bullet')
        self.out_of_wall = False
        
    def update(self,screen):
        self.movement()
        self.checkValid()
        functions.drawImage(self.image,(self.x,self.y),0,screen)

#魔理沙的激光
class marisaLaser(obj.OBJ):
    def __init__(self):
        super().__init__()
        self.image = ImageManager.getImage('Player', 'Marisa_Laser')
        self.damage = get_value('Marisa_Laser')
        self.lastFrame=-1
        self.maxFrame=0
        self.index=0
        self.length=0
        self.maxlength=256*3
        self.pos1 = 0
        self.pos2 = 256
        self.pos3 = 256*2
        self.pos4 = 256*3
        self.hit=False
        
    def initial(self,x,y,angle,idx):
        self.x=x
        self.y=y
        self.angle=angle
        self.index=(angle-270)/10
        self.idx=idx
        self.posx=get_value('player').x-x
        self.posy=get_value('player').y-y
        self.img = self.image
        self.floatgunFrame = 0
        
    def update(self,screen):
        self.lastFrame+=1
        self.draw(screen)

    def draw(self,screen):
        self.pos1 -= 16
        if self.pos1 <= -512:
            self.pos1 = 512
        self.pos2 -= 16
        if self.pos2 <= -512:
            self.pos2 = 512
        self.pos3 -= 16
        if self.pos3 <= -512:
            self.pos3 = 512
        self.pos4 -= 16
        if self.pos4 <= -512:
            self.pos4 = 512
        if not self.hit:
            self.maxlength = 256*3
        self.length+=16
        if self.length > self.maxlength:
            self.length = self.maxlength
        self.image = pygame.Surface((16, self.length)).convert_alpha()
        self.rect = self.image.get_rect()
        self.image.fill((0,0,0,0))
        self.image.blit(self.img,(0,self.pos1+256))
        self.image.blit(self.img,(0,self.pos2+256))
        self.image.blit(self.img,(0,self.pos3+256))
        self.image.blit(self.img,(0,self.pos4+256))
        #img.fill((255,255,255))
        if self.angle != 270:
            self.image = pygame.transform.rotate(self.image, -self.angle-90).convert_alpha()
            origin = self.image.get_rect(midbottom=(self.x+self.length*functions.sin(5),self.y))
        else:
            origin = self.image.get_rect(midbottom=(self.x,self.y))
        origin = self.image.get_rect(midbottom=(self.x+self.length*functions.sin(5)*self.index,self.y))
        self.rect = origin
        screen.blit(self.image, origin)
        light = pygame.transform.rotozoom(ImageManager.getImage('Bullet', 'create_effect')[4], 0, self.floatgunFrame)
        light.set_alpha(200)
        functions.drawImage(light, (self.x, self.y), 0, screen)
        
#魔理沙的魔法导弹
class marisaMissile(obj.OBJ):
    def __init__(self,x,y):
        super().__init__()
        self.x, self.y = x, y
        self.setSpeed(10, -90)
        self.rect = pygame.Rect(0,0,16,48)
        self.image = ImageManager.getImage("Player", 'Marisa_Missile')
        self.damage = get_value('Marisa_Missile')
        self.lastFrame = 0
        self.part = 0
        self.out_of_wall = False

    def update(self, screen):
        self.lastFrame += 1
        if self.lastFrame%4==0:
            self.part = not self.part
        self.checkValid()
        self.movement()
        functions.drawImage(self.image[self.part], (self.x,self.y), 0, screen)
        
#恋符[大师火花]
class Master_Spark(obj.OBJ):
    def __init__(self):
        super().__init__()
        self.hitbox = pygame.Surface((720, 1280)).convert_alpha()
        self.hitbox.fill((255,255,255))
        self.rect=self.hitbox.get_rect()
        self.image=ImageManager.getImage("Player", "Master_Spark")
        self.damage = get_value('Master_Spark')
        self.lastFrame=0
        self.maxFrame=320
        
    def initial(self, effects, enemy_bullets, items):
        self.effects = effects
        self.bullets = enemy_bullets
        self.items = items
        self.angle = 270
        self.rect.midbottom = (get_value('player').x, get_value('player').y-30)
        
    def update(self,screen):
        self.lastFrame+=1
        if self.lastFrame%20==0:
            new_effect = effect.Master_spark_effect(self.rect.midbottom, self.angle)
            self.effects.add(new_effect)
        if self.lastFrame > self.maxFrame:
            set_value('screen_shaking', False)
            self.kill()
        set_value('screen_shaking', 1)
        py_index = get_value('player').indexCount
        if py_index == 8:
            if self.angle > 270:
                self.angle -= 0.05
            elif self.angle < 270:
                self.angle += 0.05    
        elif py_index == 16:
            self.angle -= 0.05
        elif py_index == 24:
            self.angle += 0.05
            
        img = pygame.transform.rotate(self.image, -self.angle+90).convert_alpha()
        h = img.get_rect().height
        w = img.get_rect().width
        self.rect.midbottom = (get_value('player').x+h*functions.sin((self.angle-270)/2), get_value('player').y-30+abs(w*functions.cos(self.angle))*0.5)
        if self.lastFrame <= 30:
            alpha = functions.dcc(0, 156, self.lastFrame, 30)
        elif self.lastFrame >= 290:
            alpha = functions.acc(156, 0, self.lastFrame-290, 30)
        else:
            alpha = 156
        img.set_alpha(alpha)
        origin = img.get_rect(midbottom=self.rect.midbottom)
        screen.blit(img, origin)
        hit=pygame.sprite.spritecollide(self, get_value('bullets'), False)
        for b in hit:
            if not b.destroyable:
                continue
            new_vanish = effect.bulletVanish(b.x,b.y,b.color)
            get_value('effects').add(new_vanish)
            createItem(b.x,b.y)
            b.kill()

         
def drawBullet(hitbox,img,pos,angle,screen):
    if get_value('test_hitbox'):
        functions.drawImage(hitbox,pos,0,screen)
    else:
        functions.drawImage(img,pos,angle,screen)

#敌人子弹
class Bullet(obj.OBJ):
    def __init__(self):
        super().__init__()
        self.act_frame = 30
        self.acceleration = 0.05
        self.accel_angle = -90
        self.max_speed = 0
        self.ifDrawCreate = True
        self.graze = True
        self.color = 'red'
        self.var = {}
        self.nodes = {}
        self.tweening_nodes = []
        self.destroyable = True
        self.out_of_wall = False
        self.stay_on_create = False
        self.maxFrame = -1
        self.checkFrame = 120

    def initial(self, x, y, stay_on_create=False, destroyable=True, out_of_wall=False, maxFrame=-1, act_frame = 0, acceleration = 0, accel_angle=0, max_speed=0):
        self.x, self.y = x, y
        self.stay_on_create = stay_on_create
        self.destroyable = destroyable
        self.out_of_wall = out_of_wall
        self.maxFrame = maxFrame
        self.act_frame = act_frame
        self.acceleration = acceleration
        self.accel_angle = accel_angle
        self.max_speed = max_speed

    def update(self, screen, bullets, effects):
        self.lastFrame += 1
        if self.maxFrame != -1 and self.lastFrame > self.maxFrame:
            self.kill()
            return
        if self.nodes:
            self.var['self'] = self
            self.nodes['update'].update(self.var)
        if self.act_frame != 0 and self.lastFrame >= self.act_frame:
            spx, spy = functions.get_speed_in_angle(self.acceleration, self.accel_angle)
            self.speedx += spx
            self.speedy += spy
            if functions.get_speed_from_components(self.speedx, self.speedy) > self.max_speed:
                self.angle = functions.get_target_angle((0,0),(self.speedx,self.speedy))
                self.speedx, self.speedy = functions.get_speed_in_angle(self.max_speed, self.angle)
        if not self.stay_on_create or self.lastFrame > 8:
            self.movement()
        self.tweening()
        if self.lastFrame > self.checkFrame:
            self.checkValid()
        self.countRot()
        self.drawBullet(screen)
    
    def set_var(self, var_name, value, var):
        cmd = 'result = ' + str(value)
        exec(cmd, globals(), var)
        self.var[var_name] = var['result']
        
    def tweening(self):
        vars = {'self':self}
        for i in self.tweening_nodes:
            if i[2]==i[3]:
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
            i[2]+=1

    def loadType(self, type):
        self.type = bullet_typeDict.get(type)
        if self.type is None:
            set_value('running', False)
            return
        self.img = ImageManager.getImage("Bullet",type)
        if self.type <= 1:
            self.size = 'mini'
            self.hitbox = pygame.Surface((6,6))
            self.rect = self.hitbox.get_rect()
            self.w, self.h = self.hitbox.get_size()
            self.createMax = 12
        elif self.type > 1 and self.type <= 13:
            self.size = 'small'
            self.hitbox = pygame.Surface((8,8))
            self.rect = self.hitbox.get_rect()
            self.w, self.h = self.hitbox.get_size()
            self.createMax = 24
        elif self.type > 13 and self.type <= 23:
            self.size = 'middle'
            self.hitbox = pygame.Surface((12,12))
            self.rect = self.hitbox.get_rect()
            self.w, self.h = self.hitbox.get_size()
            self.createMax = 48
        else:
            self.size = 'big'
            self.hitbox = pygame.Surface((52,52))
            self.rect = self.hitbox.get_rect()
            self.w, self.h = self.hitbox.get_size()
            self.createMax = 96
                
    def loadColor(self, color):
        self.color = color
        if self.size in ('mini', 'small'):
            index = small_bullet_colorDict.get(color)
            self.image = self.img[index]
            if self.ifDrawCreate:
                self.createImg = ImageManager.getImage("Bullet",'create_effect')[small_createDict[index]]
        elif self.size == 'middle':
            index = mid_bullet_colorDict.get(color)
            self.image = self.img[index]
            if self.ifDrawCreate:
                self.createImg = ImageManager.getImage("Bullet",'create_effect')[index]
        elif self.size == 'big':
            index = big_bullet_colorDict.get(color)
            self.image = self.img[index]
            if self.ifDrawCreate:
                self.createImg = ImageManager.getImage("Bullet",'create_effect')[big_createDict[index]]
                
    def drawBullet(self, screen):
        if self.ifDrawCreate and self.lastFrame <= 8:
            self.part = functions.dcc(self.createMax*2, self.createMax, self.lastFrame, 8)
            self.tempImg = pygame.transform.rotozoom(self.createImg, 0, self.part/48)
            self.tempImg.set_alpha(functions.dcc(100, 200, self.lastFrame, 8))
            functions.drawImage(self.tempImg, (self.x,self.y), 0, screen)
        if self.lastFrame > 8:
            drawBullet(self.hitbox,self.image,(self.x,self.y),self.rot,screen)