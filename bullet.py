import pygame
import functions
import item
import effect

from pygame.math import Vector2
from const import *
from math import *
from random import *
from global_var import *
import SoundEffect

def createItem(tx,ty,items):
    new_item=item.item()
    new_item.type=7
    new_item.followPlayer=True
    x_now=tx
    y_now=ty
    if x_now<16*magnitude:
        x_now=16
    if x_now>(384-16)*magnitude:
        x_now=(384-16)*magnitude
    new_item.initial(x_now,y_now)
    items.add(new_item)

#玩家子弹
class playerGun(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.hitbox = pygame.Surface((24,24))
        self.hitbox.fill((255,255,255))
        self.rect=self.hitbox.get_rect()
        self.tx=0.0 #x-corridinate
        self.ty=0.0 #y-corridinate
        self.speedx=0.0 #speed in x-corridinate
        self.speedy=0.0 #speed in y-corridinate
        self.speed=0.0 #velocity
        self.angle=0.0 #direction of velocity
        
    def countAngle(self):
        angle=Vector2(0,0).angle_to(Vector2(self.speedx,self.speedy))
        self.angle=360+angle if angle<0 else angle
    
    def selfTarget(self,tx,ty,speed):
        mycx=self.tx
        mycy=self.ty
        dist=sqrt(pow(tx-mycx,2)+pow(ty-mycy,2))#Pyth. theorem distance between player and target
        times=dist/speed
        self.speedx=(tx-mycx)/times
        self.speedy=(ty-mycy)/times

    #ensure the position is center of the bullet
    def truePos(self):
        self.rect.centerx=self.tx
        self.rect.centery=self.ty

    def movement(self):
        self.tx+=self.speedx
        self.ty+=self.speedy
        self.truePos()

    def setSpeed(self,angle,speed):
        s=sin(radians(angle))
        c=cos(radians(angle))
        self.speedy=s*speed #vertical component
        self.speedx=c*speed #horizontal component
        self.countAngle() # update direction of velocity
        self.speed=speed #update velocity

    def checkValid(self):
        if self.rect.bottom<=0 or self.rect.top>=448*magnitude:#vertical
            self.kill()
        if self.rect.right<=0 or self.rect.left>=384*magnitude:#horizontal
            self.kill()

#灵梦的札弹
class reimuMainSatsu(playerGun):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0,0,18,96)
        self.image = get_value('Reimu_Main_Satsu')[0]
        self.damage = 10000
        
    def initial(self,tx,ty):
        self.tx=tx
        self.ty=ty
        self.setSpeed(270,60)

    def update(self,screen):
        self.checkValid()
        self.movement()
        functions.drawImage(self.image,self.rect.center,270,screen)
        
#灵梦的诱导弹
class reimuTargetSatsu(playerGun):
    def __init__(self):
        super().__init__()
        self.rect=pygame.Rect(0,0,24,24)
        self.image=get_value('Reimu_Target_Satsu')[0]
        self.damage=50
        self.lastFrame=0
        self.maxFrame=360
        self.angle=0.0
        self.initAngle=0.0
        self.adjAngle=6.0

    def initial(self,angle,tx,ty):
        self.tx=tx
        self.ty=ty
        self.angle=angle
        self.setSpeed(angle,10)

    def update(self,screen):
        self.lastFrame+=1
        if self.lastFrame>=self.maxFrame:
            self.kill()
        self.target()
        self.movement()
        self.checkValid()
        functions.drawImage(self.image,self.rect.center,self.angle,screen)
    
    def target(self):
        pos=get_value('enemypos')
        tx=pos[0]
        ty=pos[1]
        self.initAngle=self.angle
        if self.lastFrame >= 20 and self.speed <= 16:#加速
            self.speed += 1
        if pos[2] != 10000:
            self.selfTarget(tx,ty,self.speed)
        self.countAngle()
        if self.adjAngle < 10:
            self.adjAngle+=0.35
        #print(self.adjAngle)
        if abs(self.initAngle-self.angle)<=self.adjAngle:
            self.setSpeed(self.angle, self.speed)
        else:
            da=self.initAngle-self.angle
            if da>0:
                if da>=180:
                    self.setSpeed(self.initAngle+self.adjAngle,self.speed)
                elif da<180:
                    self.setSpeed(self.initAngle-self.adjAngle,self.speed)
            else:
                if abs(da)>=180:
                    self.setSpeed(self.initAngle-self.adjAngle,self.speed)
                elif abs(da)<180:
                    self.setSpeed(self.initAngle+self.adjAngle,self.speed)
        
#灵梦的封魔针
class reimuShiftSatsu(playerGun):
    def __init__(self):
        super().__init__()
        self.rect=pygame.Rect(0,0,48,10)
        self.image = get_value('Reimu_Shift_Satsu')
        self.damage=80
        self.lastFrame=0
        self.maxFrame=120

    def initial(self,tx,ty):
        self.tx=tx
        self.ty=ty
        self.setSpeed(270,40)

    def update(self,screen):
        self.lastFrame+=1
        if self.lastFrame % 2 == 0:
            image = self.image[0]
        else:
            image = self.image[1]
        if self.lastFrame>=self.maxFrame:
            self.kill()
        self.movement()
        self.checkValid()
        functions.drawImage(image, self.rect.center, 270, screen)
        
#灵符[梦想封印]
class Dream_Seal(playerGun):
    def __init__(self):
        super().__init__()
        self.rect=pygame.Rect(0,0,128,128)
        self.image = get_value('bullet_create')
        self.damage=30
        self.lastFrame=0
        self.maxFrame=randint(280,340)
        self.cancelable=False
        
    def initial(self,tx,ty,angle,enemy_bullets,effects,items,colorNum):
        self.tx=tx
        self.ty=ty
        self.rect.center=(tx,ty)
        self.angle=angle
        self.speed=20
        self.bullets=enemy_bullets
        self.effects=effects
        self.items=items
        self.colorNum=colorNum
        #self.img = pygame.transform.smoothscale(self.image[self.colorNum], (200,200)).convert_alpha()
        self.img = pygame.Surface((48,48),pygame.SRCALPHA).convert_alpha()
        self.img.fill((0,0,0,0))
        self.img.blit(self.image[self.colorNum], (0,0), (0,0,48,48))
        self.img = pygame.transform.smoothscale(self.img, (150,150)).convert_alpha()
        
    def checkValid(self):
        if self.rect.top>=448*magnitude or self.rect.bottom<=0-80 or self.rect.right<=0-80 or self.rect.left>=384*magnitude:
            self.doKill()
            
    def Circular_Motion(self):
        circle_center = pygame.math.Vector2(get_value('player_cx'), get_value('player_cy'))
        self.angle = (self.angle+6)%360
        current_radius = 145 + 95 * cos((self.lastFrame+90)*0.04)
        bullet_position = circle_center + pygame.math.Vector2(current_radius * cos(radians(self.angle)), current_radius * sin(radians(self.angle)))
        self.tx = bullet_position.x
        self.ty = bullet_position.y
        self.rect.center = bullet_position
        
    def update(self,screen):
        self.lastFrame+=1
        
        if self.lastFrame%2==0:
            new_effect = effect.Dream_seal_flying_effect()
            new_effect.initial(self.tx+randint(-5,5),self.ty+randint(-5,5),self.colorNum)
            get_value('effects1').add(new_effect)
        
        if self.lastFrame > self.maxFrame:
            self.doKill()
        if self.lastFrame < self.maxFrame-60:
            self.Circular_Motion()
        elif self.lastFrame >= self.maxFrame-60:
            self.cancelable=True
            if get_value('enemypos')[2] == 10000:
                self.speedx=0
                self.speedy=-30
            else:
                self.selfTarget(get_value('enemypos')[0], get_value('enemypos')[1], 30)
            self.movement()
        #self.countAngle()
        screen.blit(self.img,(self.rect.centerx-75,self.rect.centery-75))
        #functions.drawImage(self.img, (self.rect.centerx+randint(-5,5), self.rect.centery+randint(-5,5)), self.angle, screen)
        
        hit=pygame.sprite.spritecollide(self, self.bullets, False)
        for b in hit:
            new_vanish = effect.bulletVanish()
            new_vanish.initial(b.image, b.rect.center, b.angle)
            self.effects.add(new_vanish)
            createItem(b.rect.centerx, b.rect.centery, self.items)
            b.kill()
        
            
    def doKill(self):
        set_value('screen_shaking', True)
        SoundEffect.play('enemyShoot_sound1',0.25)
        for i in range(0,4):
            new_effect = effect.Dream_seal_effect()
            new_effect.initial(self.tx,self.ty,randint(0,7))
            self.effects.add(new_effect)
        self.kill()
        
#魔理沙的能量弹
class marisaMainBullet(playerGun):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0,0,48,24)
        self.image = get_value('Marisa_Main_Bullet')[0]
        self.damage = 100
        self.lastFrame = 0
        self.maxframe = 120
        
    def initial(self,tx,ty):
        self.tx=tx
        self.ty=ty
        self.setSpeed(270,60)
        
    def update(self,screen):
        self.movement()
        self.checkValid()
        functions.drawImage(self.image,self.rect.center,270,screen)

#魔理沙的激光
class marisaLaser(playerGun):
    def __init__(self):
        super().__init__()
        self.hitbox = pygame.Surface((24, 24)).convert_alpha()
        self.hitbox.fill((255,255,255))
        self.rect = self.hitbox.get_rect()
        self.image = get_value('Marisa_Laser')
        self.damage = 50
        self.lastFrame=-1
        self.maxFrame=0
        self.index=0
        self.length=0
        self.maxlength=384*3
        self.pos1 = 0
        self.pos2 = 384
        self.pos3 = 768
        self.pos4 = 1152
        self.hit=False
        
    def initial(self,tx,ty,angle,idx):
        self.tx=tx
        self.ty=ty
        self.angle=angle
        self.index=(angle-270)/10
        self.idx=idx
        self.posx=get_value('player_cx')-tx
        self.posy=get_value('player_cy')-ty
        self.img = self.image
        self.floatgunFrame = 0
        
    def update(self,screen,enemies):
        self.lastFrame+=1
        if not get_value('player_attack') or get_value('player_backing'):
            self.kill()
        self.draw(screen)

    def draw(self,screen):
        self.pos1 -= 24
        if self.pos1 <= -768:
            self.pos1 = 768
        self.pos2 -= 24
        if self.pos2 <= -768:
            self.pos2 = 768
        self.pos3 -= 24
        if self.pos3 <= -768:
            self.pos3 = 768
        self.pos4 -= 24
        if self.pos4 <= -768:
            self.pos4 = 768
        if not self.hit:
            self.maxlength = 384*3
        self.length+=24
        if self.length > self.maxlength:
            self.length = self.maxlength
        self.image = pygame.Surface((24, self.length)).convert_alpha()
        self.rect = self.image.get_rect()
        self.image.fill((0,0,0,0))
        self.image.blit(self.img,(0,self.pos1+384))
        self.image.blit(self.img,(0,self.pos2+384))
        self.image.blit(self.img,(0,self.pos3+384))
        self.image.blit(self.img,(0,self.pos4+384))
        #img.fill((255,255,255))
        if self.angle != 270:
            self.image = pygame.transform.rotate(self.image, -self.angle-90).convert_alpha()
            origin = self.image.get_rect(midbottom=(self.tx+self.length*sin(radians(5)),self.ty))
        else:
            origin = self.image.get_rect(midbottom=(self.tx,self.ty))
        origin = self.image.get_rect(midbottom=(self.tx+self.length*sin(radians(5))*self.index,self.ty))
        self.rect = origin
        screen.blit(self.image, origin)
        light = pygame.transform.rotozoom(get_value('bullet_create')[4], 0, self.floatgunFrame)
        light.set_alpha(200)
        functions.drawImage(light, (self.tx, self.ty), 270, screen)
        
#魔理沙的魔法导弹
class marisaMissile(playerGun):
    def __init__(self):
        super().__init__()
        self.hitbox = pygame.Surface((48, 16)).convert_alpha()
        self.hitbox.fill((255,255,255))
        self.rect = self.hitbox.get_rect()
        self.image = get_value('Marisa_Missile')
        self.damage = 480
        self.lastFrame=0
        self.maxFrame=120
        self.index=1
        
    def initial(self,tx,ty):
        self.tx=tx
        self.ty=ty
        self.setSpeed(270,4)
        
    def update(self,screen):
        if self.speedy>=-24 and self.lastFrame%3==0:
            self.speedy-=1
        self.movement()
        self.checkValid()
        if self.lastFrame%3==0:
            img=self.image[abs(self.index-1)]
        functions.drawImage(img,self.rect.center,270,screen)
        
#恋符[大师火花]
class Master_Spark(playerGun):
    def __init__(self):
        super().__init__()
        self.hitbox = pygame.Surface((720, 1280)).convert_alpha()
        self.hitbox.fill((255,255,255))
        self.rect=self.hitbox.get_rect()
        self.image=get_value('Master_Spark')
        self.damage=100
        self.lastFrame=0
        self.maxFrame=320
        
    def initial(self, effects, enemy_bullets, items):
        self.effects = effects
        self.bullets = enemy_bullets
        self.items = items
        self.angle = 270
        self.rect.midbottom = (get_value('player_cx'), get_value('player_cy')-30)
        
    def update(self,screen):
        self.lastFrame+=1
        if self.lastFrame%20==0:
            new_effect = effect.Master_spark_effect()
            new_effect.initial(self.rect.midbottom, self.angle)
            self.effects.add(new_effect)
        if self.lastFrame > self.maxFrame:
            set_value('booming', False)
            set_value('screen_shaking', False)
            self.kill()

        py_index = get_value('player_indexCount')
        if py_index == 8:
            if self.angle > 270:
                self.angle -= 0.05
            elif self.angle < 270:
                self.angle += 0.05    
        elif py_index == 16:
            self.angle -= 0.05
        elif py_index == 24:
            self.angle += 0.05
            
        img = pygame.transform.rotate(self.image, -self.angle-90).convert_alpha()
        h = img.get_rect().height
        w = img.get_rect().width
        self.rect.midbottom = (get_value('player_cx')+h*sin(radians((self.angle-270))/2), get_value('player_cy')-30+abs(w*cos(radians(self.angle)))*0.5)
        if self.lastFrame <= 30:
            img.set_alpha(self.lastFrame*5)
        elif self.lastFrame >= 290:
            img.set_alpha((320-self.lastFrame)*5)
        else:
            img.set_alpha(156)
        origin = img.get_rect(midbottom=self.rect.midbottom)
        screen.blit(img, origin)
        hit=pygame.sprite.spritecollide(self, self.bullets, False)
        for b in hit:
            new_vanish = effect.bulletVanish()
            new_vanish.initial(b.image, b.rect.center, b.angle)
            self.effects.add(new_vanish)
            createItem(b.rect.centerx, b.rect.centery, self.items)
            b.kill()

         
def drawBullet(hitbox,img,pos,angle,screen):
    if get_value('test_hitbox'):
        functions.drawImage(hitbox,pos,270,screen)
    else:
        functions.drawImage(img,pos,angle,screen)

#敌人子弹
class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.hitbox = pygame.Surface((6,6)).convert_alpha()
        self.hitbox.fill((255,255,255))
        self.rect = self.hitbox.get_rect()
        self.w, self.h = self.hitbox.get_size() # check for the collision
        self.tx = 0.0
        self.ty = 0.0
        self.type = 0
        self.size = 'small'
        self.speedx = 0.0 #horizontal speed
        self.speedy = 0.0 #vertical speed
        self.speed = 0.0 #velocity
        self.angle = 0.0 #direction of velocity
        self.moveType = 0 #special movement
        self.distance = 10000.0
        self.graze = True #Having been grazed
        self.cancalable = True #Can be canceled
        self.createMax = 0 #maximum create frame
        self.lastFrame = 0 #current frame
        self.maxFrame = 0 #maximum exist frame
        self.ifDrawCreate = True #Whether to draw the create bullet effect
        self.valid=False #Whether the bullet is valid
        self.validAccurancy = (0, 0, 0, 0)
        self.edit = False #Whether the bullet is being edited

    #striaght line movement
    def initial(self, tx, ty):
        self.tx=tx
        self.ty=ty
        self.w, self.h = self.hitbox.get_size()
        self.truePos()

    #bounce back when hit the wall 
    def Bounce_initial(self,tx,ty,bounceTimes,maxFrame):
        self.tx=tx
        self.ty=ty
        self.w, self.h = self.hitbox.get_size()
        self.truePos()
        self.bounceTimes=bounceTimes
        self.maxFrame=maxFrame
        self.moveType=1

    #locus movement
    def Locus_initial(self,tx,ty,direction,stFrame,locusFrame):
        self.tx=tx
        self.ty=ty
        self.w, self.h = self.hitbox.get_size()
        self.truePos()
        self.direction=direction
        self.stFrame=stFrame
        self.locusFrame=locusFrame
        self.endFrame = self.locusFrame+self.createMax+self.stFrame
        self.moveType=2
        
    #has change in velocity
    def Accelerate_initial(self,tx,ty,slowFrame,slowSpeed,stop,fastFrame,fastSpeed):
        self.tx=tx
        self.ty=ty
        self.w, self.h = self.hitbox.get_size()
        self.truePos()
        self.slowFrame=slowFrame
        self.slowSpeed=slowSpeed
        self.stop=stop
        self.fastFrame=fastFrame
        self.fastSpeed=fastSpeed
        self.deFrame=self.createMax+self.slowFrame
        self.acFrame=self.createMax+self.slowFrame+self.stop+self.fastFrame
        self.moveType=3
        
    #has circular motion
    def Circular_initial(self,tx,ty,cx,cy,radius,cAngle):
        self.tx=tx
        self.ty=ty
        self.w, self.h = self.hitbox.get_size()
        self.truePos()
        self.cx=cx
        self.cy=cy
        self.radius=radius
        self.cAngle=cAngle
        self.moveType=4
        
    def truePos(self):
        self.rect.centerx=round(self.tx)
        self.rect.centery=round(self.ty)
        self.checkDistance()

    #check the distance between player and bullet
    #for both collision and graze
    def checkDistance(self):
        return
        if get_value('edit_mode'):
            return
        px,py = get_value('player_cx'), get_value('player_cy')
        self.distance = Vector2(px,py).distance_to(Vector2(self.tx,self.ty))
        if self.graze and (self.distance - self.w/2 <= 12*magnitude or self.distance - self.h/2 <= 12*magnitude):
            self.graze = False
            if not get_value('grazing'):
                SoundEffect.play('graze_sound',0.5,True)
                set_value('grazing',True)
            grazeNum=get_value('grazeNum')+1
            set_value('grazeNum',grazeNum)
            
        if (self.distance - self.w/2 <= 0 or self.distance-self.h/2 <= 0) and not (get_value('immune') or get_value('gethit')):
            SoundEffect.play('miss_sound',0.5,True)
            set_value('player_getHit', True)
            self.kill()

    def movement(self):
        if self.moveType == 0:
            self.Linear_Movement()
        elif self.moveType == 1:
            self.Bounce_Movement()
        elif self.moveType == 2:
            self.Locus_movement()
        elif self.moveType == 3:
            self.Accelerate_movement()
        elif self.moveType == 4:
            self.Circular_Movement()

    def Linear_Movement(self):
        if self.lastFrame >= self.createMax:
            self.tx+=self.speedx
            self.ty+=self.speedy
        self.truePos()
        self.countAngle()

    def Bounce_Movement(self):
        if self.lastFrame > self.maxFrame:
            self.kill()
        if (self.rect.bottom<=12 or self.rect.top>=896-12) and self.bounceTimes:#vertical
            self.setSpeed(360-self.angle,self.speed)
            self.bounceTimes-=1
        elif (self.rect.right<=12 or self.rect.left>=768-12) and self.bounceTimes:#horizontal
            self.setSpeed(360-self.angle+180,self.speed)
            self.bounceTimes-=1
        if self.lastFrame >= self.createMax:
            self.tx+=self.speedx
            self.ty+=self.speedy
        self.truePos()
        self.countAngle()

    def Locus_movement(self):
        if self.lastFrame >= self.createMax+self.stFrame and self.lastFrame <= self.endFrame:
            angle = self.angle+self.direction
            self.setSpeed(angle, self.speed)
        if self.lastFrame >= self.createMax:
            self.tx += self.speedx
            self.ty += self.speedy
        self.truePos()
        self.countAngle()

    def Accelerate_movement(self):
        if self.lastFrame >= self.createMax and self.lastFrame <= self.deFrame:
            self.setSpeed(self.angle, self.speed-(self.speed-self.slowSpeed)/self.slowFrame)
        elif self.lastFrame>self.deFrame+self.stop and self.lastFrame<=self.acFrame:
            self.setSpeed(self.angle, self.speed+(self.fastSpeed-self.speed)/self.fastFrame)
        if self.lastFrame >= self.createMax:
            self.tx += self.speedx
            self.ty += self.speedy
        self.truePos()
        self.countAngle()
        
    def Circular_Movement(self):
        circle_center = Vector2(self.cx, self.cy)
        self.cAngle = (self.cAngle+7)%360
        current_radius = self.radius + 20 * cos((self.lastFrame)*0.07)
        bullet_position = circle_center + Vector2(current_radius * cos(radians(self.cAngle)), current_radius * sin(radians(self.cAngle)))
        self.tx = bullet_position.x
        self.ty = bullet_position.y
        self.cx += self.speedx
        self.cy += self.speedy
        self.truePos()

    def selfTarget(self, cx, cy, speed):
        target = Vector2(cx,cy)
        me = Vector2(self.tx, self.ty)
        diff = target-me
        angle = Vector2(0,0).angle_to(diff)
        #print(angle)
        self.setSpeed(angle, speed)
        
    def returnTargetAngle(self, cx,cy):
        target = Vector2(cx,cy)
        me = Vector2(self.tx, self.ty)
        diff = target-me
        angle = Vector2(0,0).angle_to(diff)
        return angle

    def countAngle(self):
        angle=Vector2(0,0).angle_to(Vector2(self.speedx,self.speedy))
        self.angle=360+angle if angle<0 else angle

    def setSpeed(self,angle,speed):
        s=sin(radians(angle))
        c=cos(radians(angle))
        self.speedy=s*speed
        self.speedx=c*speed
        self.speed=speed
        self.countAngle()


    def update(self, screen, bullets, effects):
        self.lastFrame += 1
        self.movement()
        self.checkValid()
        self.drawBullet(screen)

    def checkValid(self):
        if self.valid:
            return
        if self.edit:
            if self.rect.bottom<=0-24 or self.rect.top>=960+24:#vertical
                self.kill()
            if self.rect.right<=0-24 or self.rect.left>=1280+24:#horizontal
                self.kill()
        else:
            if self.rect.bottom<=-6*magnitude or self.rect.top>=(448+6)*magnitude:#vertical
                self.kill()
            if self.rect.right<=-6*magnitude or self.rect.left>=(384+6)*magnitude:#horizontal
                self.kill()
                
    def loadColor(self, color):
        if self.size == 'small':
            index = small_bullet_colorDict.get(color)
            self.image = self.img[index]
            if self.ifDrawCreate:
                self.createImg = get_value('bullet_create')[small_createDict[index]]
        elif self.size == 'middle':
            index = mid_bullet_colorDict.get(color)
            self.image = self.img[index]
            if self.ifDrawCreate:
                self.createImg = get_value('bullet_create')[index]
        elif self.size == 'big':
            index = big_bullet_colorDict.get(color)
            self.image = self.img[index]
            if self.ifDrawCreate:
                self.createImg = get_value('bullet_create')[big_createDict[index]]
                
    def drawBullet(self, screen):
        if self.ifDrawCreate and self.lastFrame <= self.createMax:
            self.part = 1-(self.lastFrame+1)/(self.createMax+2)
            if self.size == 'small':
                self.part *= 2
            elif self.size == 'middle':
                self.pasrt *= 4
            elif self.size == 'big':
                self.part *= 8
            self.tempImg = pygame.transform.rotozoom(self.createImg, 0, self.part)
            self.tempImg.set_alpha(200/self.part)
            functions.drawImage(self.tempImg, self.rect.center, 270, screen)
        if self.lastFrame > self.createMax:
            drawBullet(self.hitbox,self.image,self.rect.center,self.angle,screen)

#鳞弹
class Scale_Bullet(Bullet):
    def __init__(self):
        super().__init__()
        self.hitbox = pygame.Surface((6,6))
        self.rect = self.hitbox.get_rect()
        self.hitbox.fill((255,255,255))
        self.type = 2
        self.img = get_value('scale_bullet')
        self.createMax = 8
        self.lastFrame = 0

#环玉
class Orb_Bullet(Bullet):
    def __init__(self):
        super().__init__()
        self.hitbox = pygame.Surface((8,8))
        self.rect = self.hitbox.get_rect()
        self.hitbox.fill((255,255,255))
        self.type = 2
        self.img = get_value('orb_bullet')
        self.createMax = 8
        self.lastFrame = 0

    def update(self, screen, bullets, effects):
        self.lastFrame += 1
        self.movement()
        self.checkValid()
        self.drawBullet(screen)
        
    def loadColor(self, color):
        index = small_bullet_colorDict.get(color)
        self.image = self.img[index]
        if self.ifDrawCreate:
            self.createImg = get_value('bullet_create')[small_createDict[index]]
            
    def drawBullet(self, screen):
        if self.ifDrawCreate and self.lastFrame <= self.createMax:
            self.part = 1-(self.lastFrame+1)/(self.createMax+2)
            self.part *= 2
            self.tempImg = pygame.transform.rotozoom(self.createImg, 0, self.part)
            self.tempImg.set_alpha(200/self.part)
            functions.drawImage(self.tempImg, self.rect.center, 270, screen)
        if self.lastFrame > self.createMax:
            drawBullet(self.hitbox,self.image,self.rect.center,self.angle,screen)
            
#小玉
class Small_Bullet(Bullet):
    def __init__(self):
        super().__init__()
        self.hitbox = pygame.Surface((8,8))
        self.rect = self.hitbox.get_rect()
        self.hitbox.fill((255,255,255))
        self.type = 2
        self.img = get_value('small_bullet')
        self.createMax = 8
        self.lastFrame = 0
        self.part = 0

    def update(self, screen, bullets, effects):
        self.lastFrame += 1
        self.movement()
        self.checkValid()
        self.drawBullet(screen)

    def loadColor(self, color):
        index = small_bullet_colorDict.get(color)
        self.image = self.img[index]
        if self.ifDrawCreate:
            self.createImg = get_value('bullet_create')[small_createDict[index]]


    def drawBullet(self, screen):
        if self.ifDrawCreate and self.lastFrame <= self.createMax:
            self.part = 1-(self.lastFrame+1)/(self.createMax+2)
            self.part *= 2
            self.tempImg = pygame.transform.rotozoom(self.createImg, 0, self.part)
            self.tempImg.set_alpha(200/self.part)
            functions.drawImage(self.tempImg, self.rect.center, 270, screen)
        if self.lastFrame >= self.createMax:
            drawBullet(self.hitbox,self.image,self.rect.center,self.angle,screen)
            
#米弹
class Rice_Bullet(Bullet):
    def __init__(self):
        super().__init__()
        self.hitbox = pygame.Surface((6,6))
        self.hitbox.fill((255,255,255))
        self.rect = self.hitbox.get_rect()
        self.type = 2
        self.img = get_value('rice_bullet')
        self.createMax = 8
        self.lastFrame = 0
        self.part = 0

    def update(self, screen, bullets, effects):
        self.lastFrame += 1
        self.movement()
        self.checkValid()
        self.drawBullet(screen)

    def loadColor(self, color):
        index = small_bullet_colorDict.get(color)
        self.image = self.img[index]
        if self.ifDrawCreate:
            self.createImg = get_value('bullet_create')[small_createDict[index]]


    def drawBullet(self, screen):
        if self.ifDrawCreate and self.lastFrame <= self.createMax:
            self.part = 1-(self.lastFrame+1)/(self.createMax+2)
            self.part *= 2
            self.tempImg = pygame.transform.rotozoom(self.createImg, 0, self.part)
            self.tempImg.set_alpha(200/self.part)
            functions.drawImage(self.tempImg, self.rect.center, 270, screen)
        if self.lastFrame >= self.createMax:
            drawBullet(self.hitbox,self.image,self.rect.center,self.angle,screen)
            
#链弹
class Chain_Bullet(Bullet):
    def __init__(self):
        super().__init__()
        self.hitbox = pygame.Surface((6,6))
        self.rect = self.hitbox.get_rect()
        self.hitbox.fill((255,255,255))
        self.type = 2
        self.img = get_value('chain_bullet')
        self.createMax = 8
        self.lastFrame = 0
        self.part = 0

    def update(self, screen, bullets, effects):
        self.lastFrame += 1
        if self.lastFrame > self.createMax:
            self.movement()
        self.checkValid()
        self.drawBullet(screen)

    def loadColor(self, color):
        index = small_bullet_colorDict.get(color)
        self.image = self.img[index]
        if self.ifDrawCreate:
            self.createImg = get_value('bullet_create')[small_createDict[index]]


    def drawBullet(self, screen):
        if self.ifDrawCreate and self.lastFrame <= self.createMax:
            self.part = 1-(self.lastFrame+1)/(self.createMax+2)
            self.part *= 2
            self.tempImg = pygame.transform.rotozoom(self.createImg, 0, self.part)
            self.tempImg.set_alpha(200/self.part)
            functions.drawImage(self.tempImg, self.rect.center, 270, screen)
        if self.lastFrame >= self.createMax:
            drawBullet(self.hitbox,self.image,self.rect.center,self.angle,screen)
            
#针弹
class Pin_Bullet(Bullet):
    def __init__(self):
        super().__init__()
        self.hitbox = pygame.Surface((6,6))
        self.rect = self.hitbox.get_rect()
        self.hitbox.fill((255,255,255))
        self.type = 2
        self.img = get_value('pin_bullet')
        self.createMax = 8
        self.lastFrame = 0
        self.part = 0

    def update(self, screen, bullets, effects):
        self.lastFrame += 1
        self.movement()
        self.checkValid()
        self.drawBullet(screen)

    def loadColor(self, color):
        index = small_bullet_colorDict.get(color)
        self.image = self.img[index]
        if self.ifDrawCreate:
            self.createImg = get_value('bullet_create')[small_createDict[index]]


    def drawBullet(self, screen):
        if self.ifDrawCreate and self.lastFrame <= self.createMax:
            self.part = 1-(self.lastFrame+1)/(self.createMax+2)
            self.part *= 2
            self.tempImg = pygame.transform.rotozoom(self.createImg, 0, self.part)
            self.tempImg.set_alpha(200/self.part)
            functions.drawImage(self.tempImg, self.rect.center, 270, screen)
        if self.lastFrame >= self.createMax:
            drawBullet(self.hitbox,self.image,self.rect.center,self.angle,screen)
            
#札弹
class Satsu_Bullet(Bullet):
    def __init__(self):
        super().__init__()
        self.hitbox = pygame.Surface((6,6))
        self.rect = self.hitbox.get_rect()
        self.hitbox.fill((255,255,255))
        self.type = 2
        self.img = get_value('satsu_bullet')
        self.createMax = 8
        self.lastFrame = 0
        self.part = 0

    def update(self, screen, bullets, effects):
        self.lastFrame += 1
        self.movement()
        self.checkValid()
        self.drawBullet(screen)

    def loadColor(self, color):
        index = small_bullet_colorDict.get(color)
        self.image = self.img[index]
        if self.ifDrawCreate:
            self.createImg = get_value('bullet_create')[small_createDict[index]]


    def drawBullet(self, screen):
        if self.ifDrawCreate and self.lastFrame <= self.createMax:
            self.part = 1-(self.lastFrame+1)/(self.createMax+2)
            self.part *= 2
            self.tempImg = pygame.transform.rotozoom(self.createImg, 0, self.part)
            self.tempImg.set_alpha(200/self.part)
            functions.drawImage(self.tempImg, self.rect.center, 270, screen)
        if self.lastFrame >= self.createMax:
            drawBullet(self.hitbox,self.image,self.rect.center,self.angle,screen)
            
#铳弹
class Gun_Bullet(Bullet):
    def __init__(self):
        super().__init__()
        self.hitbox = pygame.Surface((6,6))
        self.rect = self.hitbox.get_rect()
        self.hitbox.fill((255,255,255))
        self.type = 2
        self.img = get_value('gun_bullet')
        self.createMax = 8
        self.lastFrame = 0
        self.part = 0

    def update(self, screen, bullets, effects):
        self.lastFrame += 1
        self.movement()
        self.checkValid()
        self.drawBullet(screen)

    def loadColor(self, color):
        index = small_bullet_colorDict.get(color)
        self.image = self.img[index]
        if self.ifDrawCreate:
            self.createImg = get_value('bullet_create')[small_createDict[index]]


    def drawBullet(self, screen):
        if self.ifDrawCreate and self.lastFrame <= self.createMax:
            self.part = 1-(self.lastFrame+1)/(self.createMax+2)
            self.part *= 2
            self.tempImg = pygame.transform.rotozoom(self.createImg, 0, self.part)
            self.tempImg.set_alpha(200/self.part)
            functions.drawImage(self.tempImg, self.rect.center, 270, screen)
        if self.lastFrame >= self.createMax:
            drawBullet(self.hitbox,self.image,self.rect.center,self.angle,screen)
            
#杆菌弹
class Bact_Bullet(Bullet):
    def __init__(self):
        super().__init__()
        self.hitbox = pygame.Surface((6,6))
        self.rect = self.hitbox.get_rect()
        self.hitbox.fill((255,255,255))
        self.type = 2
        self.img = get_value('bact_bullet')
        self.createMax = 8
        self.lastFrame = 0
        self.part = 0

    def update(self, screen, bullets, effects):
        self.lastFrame += 1
        self.movement()
        self.checkValid()
        self.drawBullet(screen)

    def loadColor(self, color):
        index = small_bullet_colorDict.get(color)
        self.image = self.img[index]
        if self.ifDrawCreate:
            self.createImg = get_value('bullet_create')[small_createDict[index]]


    def drawBullet(self, screen):
        if self.ifDrawCreate and self.lastFrame <= self.createMax:
            self.part = 1-(self.lastFrame+1)/(self.createMax+2)
            self.part *= 2
            self.tempImg = pygame.transform.rotozoom(self.createImg, 0, self.part)
            self.tempImg.set_alpha(200/self.part)
            functions.drawImage(self.tempImg, self.rect.center, 270, screen)
        if self.lastFrame >= self.createMax:
            drawBullet(self.hitbox,self.image,self.rect.center,self.angle,screen)
            
#星弹(小)
class Star_Bullet(Bullet, pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.hitbox = pygame.Surface((8,8))
        self.rect = self.hitbox.get_rect()
        self.hitbox.fill((255,255,255))
        self.type = 4
        self.dAngle = 0
        self.lastFrame = 0
        self.img = get_value('star_bullet')
        self.createMax = 8
        self.part = 0

    def update(self, screen, bullets, effects):
        self.lastFrame += 1
        self.movement()
        self.checkValid()
        self.drawBullet(screen)

    def loadColor(self, color):
        index = small_bullet_colorDict.get(color)
        self.image = self.img[index]
        if self.ifDrawCreate:
            self.createImg = get_value('bullet_create')[small_createDict[index]]


    def drawBullet(self, screen):
        if self.ifDrawCreate and self.lastFrame <= self.createMax:
            self.part = 1-(self.lastFrame+1)/(self.createMax+2)
            self.part *= 2
            self.tempImg = pygame.transform.rotozoom(self.createImg, 0, self.part)
            self.tempImg.set_alpha(200/self.part)
            functions.drawImage(self.tempImg, self.rect.center, 270, screen)
        if self.lastFrame >= self.createMax:
            self.dAngle = (self.dAngle+3)%360
            drawBullet(self.hitbox,self.image,self.rect.center,self.dAngle,screen)
            
#葡萄弹
class Grape_Bullet(Bullet):
    def __init__(self):
        super().__init__()
        self.hitbox = pygame.Surface((6,6))
        self.rect = self.hitbox.get_rect()
        self.hitbox.fill((255,255,255))
        self.type = 2
        self.img = get_value('grape_bullet')
        self.dAngle=0
        self.createMax = 8
        self.lastFrame = 0

    def update(self, screen, bullets, effects):
        self.lastFrame += 1
        self.movement()
        self.checkValid()
        self.drawBullet(screen)
        
    def loadColor(self, color):
        index = small_bullet_colorDict.get(color)
        self.image = self.img[index]
        if self.ifDrawCreate:
            self.createImg = get_value('bullet_create')[small_createDict[index]]


    def drawBullet(self, screen):
        if self.ifDrawCreate and self.lastFrame <= self.createMax:
            self.part = 1-(self.lastFrame+1)/(self.createMax+2)
            self.part *= 2
            self.tempImg = pygame.transform.rotozoom(self.createImg, 0, self.part)
            self.tempImg.set_alpha(200/self.part)
            functions.drawImage(self.tempImg, self.rect.center, 270, screen)
        if self.lastFrame >= self.createMax:
            drawBullet(self.hitbox,self.image,self.rect.center,270,screen)
        
#点弹
class Dot_Bullet(Bullet):
    def __init__(self):
        super().__init__()
        self.hitbox = pygame.Surface((6,6))
        self.rect = self.hitbox.get_rect()
        self.hitbox.fill((255,255,255))
        self.type = 2
        self.img = get_value('dot_bullet')
        self.createMax = 8
        self.lastFrame = 0

    def update(self, screen, bullets, effects):
        self.lastFrame += 1
        self.movement()
        self.checkValid()
        self.drawBullet(screen)
        
    def loadColor(self, color):
        index = small_bullet_colorDict.get(color)
        self.image = self.img[index]
        if self.ifDrawCreate:
            self.createImg = get_value('bullet_create')[small_createDict[index]]


    def drawBullet(self, screen):
        if self.ifDrawCreate and self.lastFrame <= self.createMax:
            self.part = 1-(self.lastFrame+1)/(self.createMax+2)
            self.part *= 2
            self.tempImg = pygame.transform.rotozoom(self.createImg, 0, self.part)
            self.tempImg.set_alpha(200/self.part)
            functions.drawImage(self.tempImg, self.rect.center, 270, screen)
        if self.lastFrame >= self.createMax:
            drawBullet(self.hitbox,self.image,self.rect.center,270,screen)
        
#星弹（大）
class Big_Star_Bullet(Bullet):
    def __init__(self):
        super().__init__()
        self.hitbox = pygame.Surface((12,12))
        self.rect = self.hitbox.get_rect()
        self.hitbox.fill((255,255,255))
        self.type = 2
        self.img = get_value('big_star_bullet')
        self.createMax = 8
        self.lastFrame = 0
        self.dAngle = 0

    def update(self, screen, bullets, effects):
        self.lastFrame += 1
        self.movement()
        self.checkValid()
        if self.lastFrame % 3 == 0:
            self.dAngle += 5
        self.drawBullet(screen)
        

    def loadColor(self, color):
        index = mid_bullet_colorDict.get(color)
        self.image = self.img[index]
        if self.ifDrawCreate:
            self.createImg = get_value('bullet_create')[index]


    def drawBullet(self, screen):
        if self.ifDrawCreate and self.lastFrame <= self.createMax:
            self.part = 1-(self.lastFrame+1)/(self.createMax+2)
            self.part *= 4
            self.tempImg = pygame.transform.rotozoom(self.createImg, 0, self.part)
            self.tempImg.set_alpha(200/self.part)
            functions.drawImage(self.tempImg, self.rect.center, 270, screen)
        if self.lastFrame >= self.createMax:
            drawBullet(self.hitbox,self.image,self.rect.center,self.dAngle,screen)

#中玉
class Mid_Bullet(Bullet):
    def __init__(self):
        super().__init__()
        self.hitbox = pygame.Surface((12,12))
        self.rect = self.hitbox.get_rect()
        self.hitbox.fill((255,255,255))
        self.type = 2
        self.img = get_value('mid_bullet')
        self.createMax = 8
        self.lastFrame = 0

    def update(self, screen, bullets, effects):
        self.lastFrame += 1
        self.movement()
        self.checkValid()
        self.drawBullet(screen)
        

    def loadColor(self, color):
        index = mid_bullet_colorDict.get(color)
        self.image = self.img[index]
        if self.ifDrawCreate:
            self.createImg = get_value('bullet_create')[index]


    def drawBullet(self, screen):
        if self.ifDrawCreate and self.lastFrame <= self.createMax:
            self.part = 1-(self.lastFrame+1)/(self.createMax+2)
            self.part *= 4
            self.tempImg = pygame.transform.rotozoom(self.createImg, 0, self.part)
            self.tempImg.set_alpha(200/self.part)
            functions.drawImage(self.tempImg, self.rect.center, 270, screen)
        if self.lastFrame >= self.createMax:
            drawBullet(self.hitbox,self.image,self.rect.center,self.angle,screen)
        
#蝶弹
class Butterfly_Bullet(Bullet):
    def __init__(self):
        super().__init__()
        self.hitbox = pygame.Surface((10,10))
        self.rect = self.hitbox.get_rect()
        self.hitbox.fill((255,255,255))
        self.type = 2
        self.img = get_value('butterfly_bullet')
        self.createMax = 8
        self.lastFrame = 0

    def update(self, screen, bullets, effects):
        self.lastFrame += 1
        self.movement()
        self.checkValid()
        self.drawBullet(screen)
        

    def loadColor(self, color):
        index = mid_bullet_colorDict.get(color)
        self.image = self.img[index]
        if self.ifDrawCreate:
            self.createImg = get_value('bullet_create')[index]


    def drawBullet(self, screen):
        if self.ifDrawCreate and self.lastFrame <= self.createMax:
            self.part = 1-(self.lastFrame+1)/(self.createMax+2)
            self.part *= 4
            self.tempImg = pygame.transform.rotozoom(self.createImg, 0, self.part)
            self.tempImg.set_alpha(200/self.part)
            functions.drawImage(self.tempImg, self.rect.center, 270, screen)
        if self.lastFrame >= self.createMax:
            drawBullet(self.hitbox,self.image,self.rect.center,self.angle,screen)

#刀弹
class Knife_Bullet(Bullet):
    def __init__(self):
        super().__init__()
        self.hitbox = pygame.Surface((10,10))
        self.rect = self.hitbox.get_rect()
        self.hitbox.fill((255,255,255))
        self.type = 2
        self.img = get_value('knife_bullet')
        self.createMax = 8
        self.lastFrame = 0

    def update(self, screen, bullets, effects):
        self.lastFrame += 1
        self.movement()
        self.checkValid()
        self.drawBullet(screen)
        

    def loadColor(self, color):
        index = mid_bullet_colorDict.get(color)
        self.image = self.img[index]
        if self.ifDrawCreate:
            self.createImg = get_value('bullet_create')[index]


    def drawBullet(self, screen):
        if self.ifDrawCreate and self.lastFrame <= self.createMax:
            self.part = 1-(self.lastFrame+1)/(self.createMax+2)
            self.part *= 4
            self.tempImg = pygame.transform.rotozoom(self.createImg, 0, self.part)
            self.tempImg.set_alpha(200/self.part)
            functions.drawImage(self.tempImg, self.rect.center, 270, screen)
        if self.lastFrame >= self.createMax:
            drawBullet(self.hitbox,self.image,self.rect.center,self.angle,screen)

#椭弹
class Ellipse_Bullet(Bullet):
    def __init__(self):
        super().__init__()
        self.hitbox = pygame.Surface((10,10))
        self.rect = self.hitbox.get_rect()
        self.hitbox.fill((255,255,255))
        self.type = 2
        self.img = get_value('ellipse_bullet')
        self.createMax = 8
        self.lastFrame = 0

    def update(self, screen, bullets, effects):
        self.lastFrame += 1
        self.movement()
        self.checkValid()
        self.drawBullet(screen)
        

    def loadColor(self, color):
        index = mid_bullet_colorDict.get(color)
        self.image = self.img[index]
        if self.ifDrawCreate:
            self.createImg = get_value('bullet_create')[index]


    def drawBullet(self, screen):
        if self.ifDrawCreate and self.lastFrame <= self.createMax:
            self.part = 1-(self.lastFrame+1)/(self.createMax+2)
            self.part *= 4
            self.tempImg = pygame.transform.rotozoom(self.createImg, 0, self.part)
            self.tempImg.set_alpha(200/self.part)
            functions.drawImage(self.tempImg, self.rect.center, 270, screen)
        if self.lastFrame >= self.createMax:
            drawBullet(self.hitbox,self.image,self.rect.center,self.angle,screen)
        
#大玉
class Big_Bullet(Bullet):
    def __init__(self):
        super().__init__()
        self.hitbox = pygame.Surface((56, 56))
        self.rect = self.hitbox.get_rect()
        self.hitbox.fill((255,255,255))
        self.type = 2
        self.img = get_value('big_bullet')
        self.createMax = 8
        self.lastFrame = 0

    def update(self, screen, bullets, effects):
        self.lastFrame += 1
        self.movement()
        self.checkValid()
        self.drawBullet(screen)
        

    def loadColor(self, color):
        index = big_bullet_colorDict.get(color)
        self.image = self.img[index]
        if self.ifDrawCreate:
            self.createImg = get_value('bullet_create')[big_createDict[index]]


    def drawBullet(self, screen):
        if self.ifDrawCreate and self.lastFrame <= self.createMax:
            self.part = 1-(self.lastFrame+1)/(self.createMax+2)
            self.part *= 8
            self.tempImg = pygame.transform.rotozoom(self.createImg, 0, self.part)
            self.tempImg.set_alpha(200/self.part)
            functions.drawImage(self.tempImg, self.rect.center, 270, screen)
        if self.lastFrame >= self.createMax:
            drawBullet(self.hitbox,self.image,self.rect.center,self.angle,screen)
        
#心弹
class Heart_Bullet(Bullet):
    def __init__(self):
        super().__init__()
        self.hitbox = pygame.Surface((12,12))
        self.rect = self.hitbox.get_rect()
        self.hitbox.fill((255,255,255))
        self.type = 2
        self.img = get_value('heart_bullet')
        self.createMax = 8
        self.lastFrame = 0

    def update(self, screen, bullets, effects):
        self.lastFrame += 1
        self.movement()
        self.checkValid()
        self.drawBullet(screen)

    def loadColor(self, color):
        index = mid_bullet_colorDict.get(color)
        self.image = self.img[index]
        if self.ifDrawCreate:
            self.createImg = get_value('bullet_create')[index]

    def drawBullet(self, screen):
        if self.ifDrawCreate and self.lastFrame <= self.createMax:
            self.part = 1-(self.lastFrame+1)/(self.createMax+2)
            self.part *= 4
            self.tempImg = pygame.transform.rotozoom(self.createImg, 0, self.part)
            self.tempImg.set_alpha(200/self.part)
            functions.drawImage(self.tempImg, self.rect.center, 270, screen)
        if self.lastFrame >= self.createMax:
            drawBullet(self.hitbox,self.image,self.rect.center,self.angle,screen)

#箭弹
class Arrow_Bullet(Bullet):
    def __init__(self):
        super().__init__()
        self.hitbox = pygame.Surface((8,8))
        self.rect = self.hitbox.get_rect()
        self.hitbox.fill((255,255,255))
        self.type = 2
        self.img = get_value('arrow_bullet')
        self.createMax = 8
        self.lastFrame = 0

    def update(self, screen, bullets, effects):
        self.lastFrame += 1
        self.movement()
        self.checkValid()
        self.drawBullet(screen)
        

    def loadColor(self, color):
        index = mid_bullet_colorDict.get(color)
        self.image = self.img[index]
        if self.ifDrawCreate:
            self.createImg = get_value('bullet_create')[index]


    def drawBullet(self, screen):
        if self.ifDrawCreate and self.lastFrame <= self.createMax:
            self.part = 1-(self.lastFrame+1)/(self.createMax+2)
            self.part *= 4
            self.tempImg = pygame.transform.rotozoom(self.createImg, 0, self.part)
            self.tempImg.set_alpha(200/self.part)
            functions.drawImage(self.tempImg, self.rect.center, 270, screen)
        if self.lastFrame >= self.createMax:
            drawBullet(self.hitbox,self.image,self.rect.center,self.angle,screen)

#光弹
class Light_Bullet(Bullet):
    def __init__(self):
        super().__init__()
        self.hitbox = pygame.Surface((8,8))
        self.rect = self.hitbox.get_rect()
        self.hitbox.fill((255,255,255))
        self.type = 2
        self.img = get_value('light_bullet')
        self.createMax = 8
        self.lastFrame = 0

    def update(self, screen, bullets, effects):
        self.lastFrame += 1
        self.movement()
        self.checkValid()
        self.drawBullet(screen)
        
    def loadColor(self, color):
        index = mid_bullet_colorDict.get(color)
        self.image = self.img[index]
        if self.ifDrawCreate:
            self.createImg = get_value('bullet_create')[index]


    def drawBullet(self, screen):
        if self.ifDrawCreate and self.lastFrame <= self.createMax:
            self.part = 1-(self.lastFrame+1)/(self.createMax+2)
            self.part *= 4
            self.tempImg = pygame.transform.rotozoom(self.createImg, 0, self.part)
            self.tempImg.set_alpha(200/self.part)
            functions.drawImage(self.tempImg, self.rect.center, 270, screen)
        if self.lastFrame >= self.createMax:
            drawBullet(self.hitbox,self.image,self.rect.center,self.angle,screen)

#烈焰弹
class Fire_Bullet(Bullet):
    def __init__(self):
        super().__init__()
        self.hitbox = pygame.Surface((8,8))
        self.rect = self.hitbox.get_rect()
        self.hitbox.fill((255,255,255))
        self.type = 2
        self.img = get_value('fire_bullet')
        self.colorDict={'red':0,'purple':4,'blue':8,'orange':12}
        self.createMax = 8
        self.lastFrame = 0
        self.animFrame = 0

    def update(self, screen, bullets, effects):
        self.lastFrame += 1
        self.movement()
        self.checkValid()
        self.drawBullet(screen)

    def loadColor(self, color):
        self.index = self.colorDict.get(color)
        self.image = self.img[self.index]

    def drawBullet(self, screen):
        if self.lastFrame % 5 == 0:
            self.animFrame = (self.animFrame+1)%4
            self.image = self.img[self.index+self.animFrame]
        drawBullet(self.hitbox,self.image,self.rect.center,self.angle,screen)

#滴弹
class Drop_Bullet(Bullet):
    def __init__(self):
        super().__init__()
        self.hitbox = pygame.Surface((4,4))
        self.rect = self.hitbox.get_rect()
        self.hitbox.fill((255,255,255))
        self.type = 2
        self.img = get_value('drop_bullet')
        self.createMax = 8
        self.lastFrame = 0

    def update(self, screen, bullets, effects):
        self.lastFrame += 1
        self.movement()
        self.checkValid()
        self.drawBullet(screen)
        
    def loadColor(self, color):
        index = small_bullet_colorDict.get(color)
        self.image = self.img[index]
        if self.ifDrawCreate:
            self.createImg = get_value('bullet_create')[small_createDict[index]]

    def drawBullet(self, screen):
        if self.ifDrawCreate and self.lastFrame <= self.createMax:
            self.part = 1-(self.lastFrame+1)/(self.createMax+2)
            self.part *= 2
            self.tempImg = pygame.transform.rotozoom(self.createImg, 0, self.part)
            self.tempImg.set_alpha(200/self.part)
            functions.drawImage(self.tempImg, self.rect.center, 270, screen)
        if self.lastFrame >= self.createMax:
            drawBullet(self.hitbox,self.image,self.rect.center,270,screen)

#六角星弹
class Double_Star_Bullet(Bullet):
    def __init__(self):
        super().__init__()
        self.hitbox = pygame.Surface((12,12))
        self.rect = self.hitbox.get_rect()
        self.hitbox.fill((255,255,255))
        self.type = 2
        self.img = get_value('double_star_bullet')
        self.createMax = 8
        self.lastFrame = 0

    def update(self, screen, bullets, effects):
        self.lastFrame += 1
        self.movement()
        self.checkValid()
        self.drawBullet(screen)
        
    def loadColor(self, color):
        index = mid_bullet_colorDict.get(color)
        self.image = self.img[index]
        if self.ifDrawCreate:
            self.createImg = get_value('bullet_create')[index]

    def drawBullet(self, screen):
        if self.ifDrawCreate and self.lastFrame <= self.createMax:
            self.part = 1-(self.lastFrame+1)/(self.createMax+2)
            self.part *= 4
            self.tempImg = pygame.transform.rotozoom(self.createImg, 0, self.part)
            self.tempImg.set_alpha(200/self.part)
            functions.drawImage(self.tempImg, self.rect.center, 270, screen)
        if self.lastFrame >= self.createMax:
            drawBullet(self.hitbox,self.image,self.rect.center,self.angle,screen)

#大光弹
class Big_Light_Bullet(Bullet):
    def __init__(self):
        super().__init__()
        self.hitbox = pygame.Surface((50,50))
        self.rect = self.hitbox.get_rect()
        self.hitbox.fill((255,255,255))
        self.type = 2
        self.img = get_value('big_light_bullet')
        self.createMax = 9
        self.lastFrame = 0

    def update(self, screen, bullets, effects):
        self.lastFrame += 1
        self.movement()
        self.checkValid()
        self.drawBullet(screen)
        
    def loadColor(self, color):
        index = mid_bullet_colorDict.get(color)
        self.image = self.img[index]
        if self.ifDrawCreate:
            self.createImg = get_value('bullet_create')[index]

    def drawBullet(self, screen):
        if self.ifDrawCreate and self.lastFrame <= self.createMax:
            self.part = 1-(self.lastFrame+1)/(self.createMax+2)
            self.part *= 8
            self.tempImg = pygame.transform.rotozoom(self.createImg, 0, self.part)
            self.tempImg.set_alpha(200/self.part)
            functions.drawImage(self.tempImg, self.rect.center, 270, screen)
        if self.lastFrame >= self.createMax:
            drawBullet(self.hitbox,self.image,self.rect.center,self.angle,screen)
  
        
class Explode_Big_Star_Bullet(Big_Star_Bullet):
    def __init__(self):
        super().__init__()
        self.explodeFrame=0
        self.exAngle=randint(0,72)
        
    def update(self, screen, bullets, effects):
        self.lastFrame += 1
        self.movement()
        self.checkValid(bullets)
        if self.lastFrame % self.explodeFrame == 0:
            self.Explode(bullets)
        if self.lastFrame % 3 == 0:
            self.dAngle += 5
        self.drawBullet(screen)

    def drawBullet(self, screen):
        if self.ifDrawCreate and self.lastFrame <= self.createMax:
            self.part = 1-(self.lastFrame+1)/(self.createMax+2)
            self.part *= 4
            self.tempImg = pygame.transform.rotozoom(self.createImg, 0, self.part)
            self.tempImg.set_alpha(200/self.part)
            functions.drawImage(self.tempImg, self.rect.center, 270, screen)
        if self.lastFrame >= self.createMax:
            drawBullet(self.hitbox,self.image,self.rect.center,self.dAngle,screen)

    def checkValid(self,bullets):
        if self.rect.top<=0 or self.rect.bottom>=896/2*1.5:#vertical
            self.Explode(bullets)
            self.kill()
        if self.rect.left<=0 or self.rect.right>=576:#horizontal
            self.Explode(bullets)
            self.kill()
    def Explode(self, bullets):
        for i in range(0,5):
            new_bullet = Satsu_Bullet()
            new_bullet.initial(self.rect.centerx,self.rect.centery)
            new_bullet.setSpeed(i*72+self.exAngle, 5)
            new_bullet.loadColor('blue')
            bullets.add(new_bullet)
        #self.kill()
 
        
class Rain_Rice_Bullet(Rice_Bullet):
    def __init__(self):
        super().__init__()
        self.rainFrame=0
        self.stFrame=0
        self.orgAngle=0
        self.orgSpeed=0
        
    def checkValid(self):
        if self.lastFrame < self.stFrame+self.rainFrame+60:
            return
        super().checkValid()
    
    def movement(self):
        if self.lastFrame >= self.stFrame and self.lastFrame < self.stFrame+self.rainFrame//2:
            if self.angle > 270:
                angle = self.angle+((360-self.orgAngle)/(self.rainFrame/2))
            else:
                angle = self.angle-((self.orgAngle-180)/(self.rainFrame/2))
            speed = self.speed-(self.orgSpeed/(self.rainFrame/2))
            self.setSpeed(angle, speed)
        elif self.lastFrame == self.stFrame+self.rainFrame//2:
            if self.orgAngle>270:
                self.setSpeed(0,self.speed)
                self.orgAngle=0
            else:
                self.setSpeed(180,self.speed)
                self.orgAngle=180
        elif self.lastFrame > self.stFrame+self.rainFrame//2 and self.lastFrame <= self.stFrame+self.rainFrame:
            if self.orgAngle == 0:
                angle = self.angle+(90/(self.rainFrame/2))
            else:
                angle = self.angle-(90/(self.rainFrame/2))
            speed = self.speed+(self.orgSpeed/(self.rainFrame/2))
            self.setSpeed(angle, speed)
        if self.lastFrame >= self.createMax:
            self.tx += self.speedx
            self.ty += self.speedy
        self.truePos()
        self.countAngle()


class DNA_Orb_Bullet(Orb_Bullet):
    def __init__(self):
        super().__init__()

    def initial(self,tx,ty,angle,speed):
        self.tx=tx
        self.ty=ty
        self.angle=angle
        self.speed=speed
        self.intAngle=angle
        self.truePos()
        self.setSpeed(angle,speed)
        
    def movement(self):
        if self.lastFrame == 1:
            angle = self.angle+45
            self.setSpeed(angle,self.speed)
        elif self.lastFrame >=10 and self.lastFrame<=20:
            angle = self.angle-90/10
            self.setSpeed(angle,self.speed)
        elif self.lastFrame >= 30 and self.lastFrame<=40:
            angle = self.angle+90/10
            self.setSpeed(angle,self.speed)
        elif self.lastFrame == 50:
            self.lastFrame = 9
        self.tx+=self.speedx
        self.ty+=self.speedy
        self.truePos()
        self.countAngle()

     
class Lasers(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.hitbox=pygame.Surface((24,24)).convert_alpha()
        self.rect=self.hitbox.get_rect()
        self.colorDict={'grey':0,'red':1,'lightRed':2,'purple':3,'pink':4,'blue':5,'seaBlue':6,'skyBlue':7,'lightBlue':8,'lakeBlue':8,'darkGreen':9,'green':10,'lightGreen':11,'yellow':12,'lemonYellow':13,'orange':14,'white':15}
        self.tx=0.0
        self.ty=0.0
        self.angle=0.0
        self.length=0.0
        self.maxLength=0.0
        self.lastFrame=0
        self.maxFrame=100
        self.valid=True
        self.edit=False
        self.main=False
        self.createMax=0
        self.graze=True
        
    def initial(self,tx,ty,angle):
        self.tx=tx
        self.ty=ty
        self.angle=angle
        self.w, self.h = self.hitbox.get_size()
        
    def loadColor(self,color):
        self.color=color
        index=self.colorDict[color]
        self.img=get_value('laser')[index]
        
    def truePos(self):
        self.rect.centerx=round(self.tx)
        self.rect.centery=round(self.ty)
        self.checkDistance()
        
    def checkDistance(self):
        if get_value('edit_mode'):
            return
        px,py = get_value('player_cx'), get_value('player_cy')
        self.distance = Vector2(px,py).distance_to(Vector2(self.tx,self.ty))
        if self.graze and (self.distance - self.w/2 <= 18*magnitude or self.distance - self.h/2 <= 18*magnitude):
            self.graze = False
            if not get_value('grazing'):
                get_value('graze_sound').play()
                set_value('grazing',True)
            grazeNum=get_value('grazeNum')+1
            set_value('grazeNum',grazeNum)
            
        if (self.distance - self.w/2 <= 0 or self.distance-self.h/2 <= 0) and not (get_value('immune') or get_value('gethit')):
            get_value('miss_sound').play()
            set_value('gethit', True)
            self.kill()
            
    def countAngle(self):
        angle=Vector2(0,0).angle_to(Vector2(self.speedx,self.speedy))
        self.angle=360+angle if angle<0 else angle

    def setSpeed(self,angle,speed):
        s=sin(radians(angle))
        c=cos(radians(angle))
        self.speedy=s*speed
        self.speedx=c*speed
        self.speed=speed
        self.countAngle()

    def checkValid(self):
        if self.valid:
            return
        if self.edit:
            if self.rect.bottom<=0-24 or self.rect.top>=960+24:#vertical
                self.kill()
            if self.rect.right<=0-24 or self.rect.left>=1280+24:#horizontal
                self.kill()
        else:
            if self.rect.bottom<=-6*magnitude or self.rect.top>=(448+6)*magnitude:#vertical
                self.kill()
            if self.rect.right<=-6*magnitude or self.rect.left>=(384+6)*magnitude:#horizontal
                self.kill()
                
    def Linear_Movement(self):
        if self.lastFrame >= self.createMax:
            self.tx+=self.speedx
            self.ty+=self.speedy
        self.truePos()
        self.countAngle()
        
    def update(self,screen,lasers):
        self.lastFrame+=1
        #self.length+=1
        if self.lastFrame>self.maxFrame:
            self.kill()
        if self.main:
            new_laser = Lasers()
            new_laser.initial(self.tx,self.ty,self.angle)
            new_laser.loadColor(self.color)
            new_laser.setSpeed(self.angle,self.speed)
            lasers.add(new_laser)
            
        else:
            self.Linear_Movement()
            angle=self.angle+15*sin(radians(self.lastFrame*10))
            self.setSpeed(angle,self.speed)
            self.checkDistance()
        functions.drawImage(self.img,(self.tx,self.ty),self.angle,screen)
        #self.collision()
        #self.drawLaser(screen)
        
    def collision(self,player):
        self.hit=False
        enemy_hit = pygame.sprite.spritecollide(self,player, 0, collided = pygame.sprite.collide_mask)
        for sp in enemy_hit:
            sp.health -= self.damage
            dx = self.tx - sp.rect.centerx
            dy = self.ty - sp.rect.centery
            dist = sqrt(dx**2+dy**2)
            self.maxlength = min(self.maxlength, int(dist))
            self.hit=True
        
    def drawLaser(self,screen):
        if self.length != self.rect.h:
            self.image = pygame.transform.smoothscale(self.img,(24,self.length))
            self.image = pygame.transform.rotate(self.image,-self.angle-90).convert_alpha()
            self.rect=self.image.get_rect()
            self.rect.midtop=(self.tx,self.ty)
        screen.blit(self.image,self.rect)
    