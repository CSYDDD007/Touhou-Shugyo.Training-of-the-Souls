import pygame
import bullet
import effect
import functions
import item


from pygame.math import Vector2
from const import *
from math import *
from random import *
from global_var import *
import SoundEffect as SE
magnitude=1.5

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 0, 32, 32)
        self.tx = 0.0 #x-coordinate
        self.ty = 0.0 #y-coordinate
        self.health = 0 #health point
        self.speed = 0.0 #velocity
        self.speedx = 0.0 #horizontal speed
        self.speedy = 0.0 #vertical speed
        self.angle = 0.0 #direction of velocity
        self.lastFrame = 0 #current frame
        self.maxFrame = 0 #maximum exist frame
        self.color='red' #color of enemy
        self.gethit=False #if enemy get hit, play hit animation frame
        self.gethitNum=0 #hit animation frame
        self.edit=False
        self.moving_lists=[] #stFrame,lastFrame,angle,direction,speed
        self.attacking_lists=[] #stFrame,lastFrame,bullet_type,angle,speed,movingtype
        self.danmaku_lists=[]
        
    def initial(self, tx, ty):
        self.tx = tx
        self.ty = ty
        self.truePos()
        
    def truePos(self):
        self.rect.centerx = round(self.tx)
        self.rect.centery = round(self.ty)
        self.checkDistance()

    def checkValid(self):
        if self.edit:
            if self.rect.bottom < 0 or self.rect.top > 960:#vertical
                self.kill()
            if self.rect.right < 0 or self.rect.left > 1280:#horizontal
                self.kill()
        else:
            if self.rect.bottom < 0 or self.rect.top > 448*magnitude:#vertical
                self.kill()
            if self.rect.right < 0 or self.rect.left > 384*magnitude:#horizontal
                self.kill()

    def Target(self, tx, ty, speed):
        mx = self.tx
        my = self.ty
        dx = tx-mx
        dy = ty-my
        dist = sqrt(dx**2 + dy**2)
        times = dist/speed
        self.speedx= dx/times
        self.speedy = dy/times

    def countTargetAngle(self,tx,ty):
        mycx=self.tx
        mycy=self.ty
        dif=sqrt(pow(tx-mycx,2)+pow(ty-mycy,2))
        dx=(tx-mycx)/dif
        dy=(ty-mycy)/dif
        if dx != 0:
            t = dy/dx
            deg = atan(t)*180/pi
            if dx<0: #leftdown
                deg+=180
            elif dy<0 and deg<0: #rightup
                deg+=360
        else: #speedx == 0
            if dy >= 0: #downwards
                deg = 90
            else: #upwards
                deg = 270
        return deg

    def setSpeed(self, angle, speed):
        s = sin(radians(angle))
        c = cos(radians(angle))
        self.speedx = c*speed
        self.speedy = s*speed
        self.speed = speed
        self.countAngle()

    def countAngle(self):
        angle=Vector2(0,0).angle_to(Vector2(self.speedx,self.speedy))
        self.angle=360+angle if angle<0 else angle
        
    def checkDistance(self):
        px = get_value('player_cx')
        py = get_value('player_cy')
        dx = px-self.tx
        dy = py-self.ty
        dist = sqrt(dx**2+dy**2)
        miniDist = get_value('enemypos')[2]
        if self.tx<=768 and self.tx>=0 and self.ty<=896 and self.ty>=0 and dist<miniDist:
            set_value('enemypos',(self.tx,self.ty,dist))

    def update(self, screen, bullets, lasers, items, effects, backgrounds):
        self.lastFrame += 1
        if self.health <= 0:
            self.killEffect(effects)
            self.doKill(items,bullets)
        if self.lastFrame >= 100:
            self.checkValid()
        self.movement()
        self.fire(bullets)
        self.laser(lasers)
        self.draw(screen)
            
    def movement(self):
        #self.moving_lists=[] #stFrame,lastFrame,angle,direction,speed
        if self.moving_lists:#has command
            command=self.moving_lists[0]
            if self.lastFrame<command[0]:
                self.tx += self.speedx
                self.ty += self.speedy
                self.truePos()
                self.countAngle()
                return
            elif self.lastFrame==command[0]:
                self.command_start=command[0]
                self.command_last=command[1]
                self.command_end=command[0]+command[1]
                self.command_angle=command[2]
                self.original_speed=self.speed
                self.command_speed=command[3]
            elif self.lastFrame>=self.command_start and self.lastFrame<=self.command_end:
                angle=self.angle+self.command_angle/self.command_last
                if self.command_speed==0:
                    speed=self.speed
                else:
                    speed=self.speed+((self.command_speed-self.original_speed)/self.command_last)
                self.setSpeed(angle,speed)
            if self.lastFrame==self.command_end:
                self.moving_lists.pop(0)
            self.tx += self.speedx
            self.ty += self.speedy
            self.truePos()
            self.countAngle()
        else:#line movement without command
            self.tx += self.speedx
            self.ty += self.speedy
            self.truePos()
            self.countAngle()

    def fire(self, bullets):
        for i in range(len(self.danmaku_lists)):
            if self.lastFrame >= self.danmaku_lists[i][11]:
                self.fire_check(i, bullets)
                
    def laser(self, lasers):
        pass
                    
    def fire_check(self, idx, bullets):
        if self.danmaku_lists[idx][15]!=self.danmaku_lists[idx][7] and self.danmaku_lists[idx][17]!=self.danmaku_lists[idx][9] and self.danmaku_lists[idx][18]==self.danmaku_lists[idx][10]:
            if self.danmaku_lists[idx][16]==self.danmaku_lists[idx][8]:
                self.danmaku_lists[idx][16]=0
                self.danmaku_lists[idx][15]+=1
                #print(self.danmaku_lists[idx][0])
                if self.danmaku_lists[idx][0]==0:
                    self.armed_fire(idx, bullets)
                elif self.danmaku_lists[idx][0]==1:
                    self.circle_fire(idx, bullets)
            else:
                self.danmaku_lists[idx][16]+=1
        elif self.danmaku_lists[idx][15]==self.danmaku_lists[idx][7]:
            self.danmaku_lists[idx][15]=0
            self.danmaku_lists[idx][17]+=1
            self.danmaku_lists[idx][18]=0
        elif self.danmaku_lists[idx][18]!=self.danmaku_lists[idx][10]:
            self.danmaku_lists[idx][18]+=1
    
    def returnTargetAngle(self, cx,cy):
        target = Vector2(cx,cy)
        me = Vector2(self.tx, self.ty)
        diff = target-me
        angle = Vector2(0,0).angle_to(diff)
        return angle
    
    def armed_fire(self, idx, bullets):
        target_angle = self.returnTargetAngle(get_value('player_cx'),get_value('player_cy')) if self.danmaku_lists[idx][1]==-1 else self.danmaku_lists[idx][1]
        if self.danmaku_lists[idx][6]%2!=0:
            #print(self.danmaku_lists[idx][6]//2)
            for i in range(-self.danmaku_lists[idx][6]//2+1,self.danmaku_lists[idx][6]//2+1):
                angle = target_angle+self.danmaku_lists[idx][12]*i
                #print(angle, i)
                speed = 5
                new_bullet = bullet.Scale_Bullet()
                if self.danmaku_lists[idx][3]:
                    bx = self.tx+self.danmaku_lists[idx][2]
                else:
                    bx = self.danmaku_lists[idx][2]
                if self.danmaku_lists[idx][5]:
                    by = self.ty+self.danmaku_lists[idx][4]
                else:
                    by = self.danmaku_lists[idx][4]
                new_bullet.initial(bx, by)
                #print(by)
                new_bullet.setSpeed(angle, speed)
                new_bullet.loadColor('red')
                new_bullet.edit=True
                bullets.add(new_bullet)
        else:
            for i in range(-self.danmaku_lists[idx][6]//2,self.danmaku_lists[idx][6]//2+1):
                if i==0:
                    continue
                elif i==-1 or i==1:
                    angle = target_angle+self.danmaku_lists[idx][12]*(i/2)
                else:
                    angle = target_angle+self.danmaku_lists[idx][12]*i-self.danmaku_lists[idx][12]*(0.5 if i>0 else -0.5)
                #print(angle,i)
                speed = 5
                new_bullet = bullet.Scale_Bullet()
                if self.danmaku_lists[idx][3]:
                    bx = self.tx+self.danmaku_lists[idx][2]
                else:
                    bx = self.danmaku_lists[idx][2]
                if self.danmaku_lists[idx][5]:
                    by = self.ty+self.danmaku_lists[idx][4]
                else:
                    by = self.danmaku_lists[idx][4]
                new_bullet.initial(bx, by)
                new_bullet.setSpeed(angle, speed)
                new_bullet.loadColor('red')
                new_bullet.edit=True
                bullets.add(new_bullet)
                
    def circle_fire(self, idx, bullets):
        #print('fire')
        target_angle = self.returnTargetAngle(get_value('player_cx'),get_value('player_cy')) if self.danmaku_lists[idx][1]==-1 else self.danmaku_lists[idx][1]
        for i in range(self.danmaku_lists[idx][6]):
            angle = target_angle+360/self.danmaku_lists[idx][6]*i
            speed = 5
            new_bullet = bullet.Scale_Bullet()
            new_bullet.initial(self.tx, self.ty)
            new_bullet.setSpeed(angle, speed)
            new_bullet.loadColor('red')
            new_bullet.edit=True
            bullets.add(new_bullet)
            
                

    def draw(self, screen):
        pass

    def createItem(self,items,Type,num):
        for i in range(0,num):
            dx=random()*120-60
            dy=random()*-120
            new_item = item.item()
            new_item.type=Type
            x_now=self.tx+dx
            y_now=self.ty+dy
            if x_now<0:
                x_now=0
            if x_now>768:
                x_now=768
            new_item.initial(x_now,y_now)
            items.add(new_item)
            
    def dropItem(self, items):
        pass

    def doKill(self,items,bullets):
        self.kill()
    
    def killEffect(self, effects):
        SE.play('enemyDead_sound',0.1)
        new_effect = effect.enemyDeath()
        new_effect.initial(self.rect.center,self.color)
        effects.add(new_effect)

class Fairy(Enemy):
    def __init__(self):
        super().__init__()
        self.hitbox=pygame.Surface((32*magnitude,32*magnitude)).convert_alpha()
        self.rect=self.hitbox.get_rect()
        self.health = 1500
        self.frame = 0
        self.colorNum = randint(0, 3)
        self.direction = 0
        self.angleNum = 0
        self.interval = 5
        self.part = 0
        self.lockNum = 0
        self.lock = False
        self.colorDict = {'blue':0, 'red':1, 'green':2, 'yellow':3}
        self.nimbusAngle = 0
        self.corrode = False
        
        
    def initial(self,tx,ty,color):
        self.tx=tx
        self.ty=ty
        self.colorNum=self.colorDict.get(color)
        self.color=color
        self.getHit_effect = pygame.Surface((32*magnitude,32*magnitude)).convert_alpha()
        self.getHit_effect.fill((255, 0, 0))
        self.truePos()
        
    def draw(self, screen):
        '''
        nimbusImage=pygame.Surface((48, 48))
        nimbusImage=nimbusImage.convert_alpha()
        nimbusImage.fill((0, 0, 0, 0))
        nimbusImage.blit(get_value('nimbus'),(0, 0),(48*self.colorDict[self.colorNum], 0, 48,48))
        #nimbusImage = pygame.transform.smoothscale(nimbusImage,(64+sizeAdj, 64+sizeAdj))
        #functions.drawImage(nimbusImage,(self.rect.centerx, self.rect.centery), self.nimbusAngle, screen)
        self.nimbusAngle+=6
        '''
        self.frame += 1
        if self.frame >= self.interval:
            self.frame = 0
            self.part = (self.part+1)%4
        if self.angle>=50 and self.angle<=130 or self.angle<=310 and self.angle>=220:
            self.angleNum=0
        elif self.angle>=45 and self.angle<=135:
            self.angleNum=6
        elif self.angle>=40 and self.angle<=140:
            self.angleNum=7
        else:
            self.angleNum=8
        if self.gethit:
            self.gethitNum=48
            self.gethit=False
        else:
            self.gethitNum=0
        if self.corrode:
            if self.lock:
                self.image=get_value('corroded_fairy')[5+self.colorNum*12+self.gethitNum]
            else:
                self.image=get_value('corroded_fairy')[self.angleNum+self.part+self.colorNum*12+self.gethitNum]
        else:
            if self.lock:
                self.image=get_value('fairy')[5+self.colorNum*12+self.gethitNum]
            else:
                self.image=get_value('fairy')[self.angleNum+self.part+self.colorNum*12+self.gethitNum]
        if self.angle>130 and self.angle < 220:
            self.image=pygame.transform.flip(self.image,True,False)
        functions.drawImage(self.image, self.rect.center, 270, screen)
        
class Sp_Fairy(Enemy):
    def __init__(self):
        super().__init__()
        self.hitbox = pygame.Surface((48*magnitude,32*magnitude)).convert_alpha()
        self.rect = self.hitbox.get_rect()
        self.health = 1500
        self.frame = 0
        self.colorNum = randint(0, 1)
        self.direction = 0
        self.angleNum = 0
        self.interval = 5
        self.part = 0
        self.lockNum = 0
        self.lock = False
        self.colorDict = {'blue':0, 'red':1}
        self.nimbusAngle = 0

    def initial(self,tx,ty,color):
        self.tx=tx
        self.ty=ty
        self.colorNum=self.colorDict.get(color)
        self.color=color
        self.truePos()
        
    def draw(self, screen):
        self.frame += 1
        if self.frame >= self.interval:
            self.frame = 0
            self.part = (self.part+1)%4
        if self.angle>=50 and self.angle<=130 or self.angle<=310 and self.angle>=220:
            self.angleNum=0
        elif self.angle>=45 and self.angle<=135:
            self.angleNum=6
        elif self.angle>=40 and self.angle<=140:
            self.angleNum=7
        else:
            self.angleNum=8
        if self.gethit:
            self.gethitNum=24
            self.gethit=False
        else:
            self.gethitNum=0
        if self.lock:
            self.image=get_value('sp_fairy')[5+self.colorNum*12+self.gethitNum]
        else:
            self.image=get_value('sp_fairy')[self.angleNum+self.part+self.colorNum*12+self.gethitNum]
        if self.angle>130 and self.angle < 220:
            self.image=pygame.transform.flip(self.image,True,False)
        functions.drawImage(self.image, self.rect.center, 270, screen)
        
class Mid_Fairy(Enemy):
    def __init__(self):
        super().__init__()
        self.hitbox = pygame.Surface((48*magnitude,48*magnitude)).convert_alpha()
        self.rect = self.hitbox.get_rect()
        self.health = 1500
        self.frame = 0
        self.colorNum = randint(0, 1)
        self.direction = 0
        self.angleNum = 0
        self.interval = 5
        self.part = 0
        self.lockNum = 0
        self.lock = False
        self.colorDict = {'red':0, 'blue':1}
        self.nimbusAngle = 0

    def initial(self,tx,ty,color):
        self.tx=tx
        self.ty=ty
        self.colorNum=self.colorDict.get(color)
        self.color=color
        self.truePos()
        
    def draw(self, screen):
        self.frame += 1
        if self.frame >= self.interval:
            self.frame = 0
            self.part = (self.part+1)%4
        if self.angle>=50 and self.angle<=130 or self.angle<=310 and self.angle>=220:
            self.angleNum=0
        elif self.angle>=45 and self.angle<=135:
            self.angleNum=6
        elif self.angle>=40 and self.angle<=140:
            self.angleNum=7
        else:
            self.angleNum=8
        if self.gethit:
            self.gethitNum=24
            self.gethit=False
        else:
            self.gethitNum=0
        if self.lock:
            self.image=get_value('mid_fairy')[5+self.colorNum*12+self.gethitNum]
        else:
            self.image=get_value('mid_fairy')[self.angleNum+self.part+self.colorNum*12+self.gethitNum]
        if self.angle>130 and self.angle < 220:
            self.image=pygame.transform.flip(self.image,True,False)
        functions.drawImage(self.image, self.rect.center, 270, screen)

class Flower_Fairy(Enemy):
    def __init__(self):
        super().__init__()
        self.hitbox = pygame.Surface((64*magnitude,64*magnitude)).convert_alpha()
        self.rect = self.hitbox.get_rect()
        self.health = 1500
        self.frame = 0
        self.colorNum = randint(0, 3)
        self.direction = 0
        self.angleNum = 0
        self.interval = 5
        self.part = 0
        self.lockNum = 0
        self.lock = False
        self.colorDict = (2,0,1,0)
        self.nimbusAngle = 0
        self.corrode = False
        self.pale = False

    def draw(self, screen):
        sizeAdj = round(4*sin(self.lastFrame*3/180*pi))
        nimbusImage=pygame.Surface((48, 48))
        nimbusImage=nimbusImage.convert_alpha()
        nimbusImage.fill((0, 0, 0, 0))
        nimbusImage.blit(get_value('nimbus'),(0, 0),(48*self.colorDict[self.colorNum], 0, 48, 48))
        nimbusImage = pygame.transform.smoothscale(nimbusImage,(64+sizeAdj, 64+sizeAdj))
        #functions.drawImage(nimbusImage,(self.rect.centerx, self.rect.centery), self.nimbusAngle, screen)
        self.nimbusAngle+=6
        self.frame += 1
        if self.frame >= self.interval:
            self.frame = 0
            self.part = (self.part+1)%4
        if self.angle>=50 and self.angle<=130 or self.angle>=310 and self.angle<=220:
            self.angleNum=0
        elif self.angle>=40 and self.angle<=140:
            self.angleNum=6
        elif self.angle>=15 and self.angle<=165:
            self.angleNum=7
        else:
            self.angleNum=8
        if self.gethit:
            self.gethitNum=12
            self.gethit=False
        else:
            self.gethitNum=0
        if self.corrode:
            self.image=get_value('corrodedflower_fairy')[self.angleNum+self.part+self.gethitNum]
        elif self.pale:
            self.image=get_value('paleflower_fairy')[self.angleNum+self.part+self.gethitNum]
        else:
            self.image=get_value('sunflower_fairy')[self.angleNum+self.part+self.gethitNum]
        
        if self.angle>130 and self.angle < 220:
            self.image=pygame.transform.flip(self.image,True,False)
        functions.drawImage(self.image, self.rect.center, 270, screen)

class Ghost(Enemy):
    def __init__(self):
        super().__init__()
        self.hitbox=pygame.Surface((32*magnitude,32*magnitude)).convert_alpha()
        self.rect=self.hitbox.get_rect()
        self.health = 1000
        self.frame = 0
        self.colorNum = randint(0, 3)
        self.direction = 0
        self.angleNum = 0
        self.interval = 5
        self.part = 0
        self.lockNum = 0
        self.lock = False
        self.colorDict = {'red':0, 'green':1, 'blue':2, 'yellow':3}
        self.nimbusAngle = 0
        
    def initial(self,tx,ty,color):
        self.tx=tx
        self.ty=ty
        self.colorNum=self.colorDict.get(color)
        self.color=color
        self.truePos()
        
    def update(self, screen, bullets, lasers, items, effects, backgrounds):
        super(Ghost, self).update(screen, bullets, lasers, items, effects, backgrounds)
        if self.lastFrame%5==0:
            self.flameEffect(effects)
        
    def flameEffect(self, effects):
        new_effect = effect.Ghost_flame_effect()
        new_effect.initial(self.tx, self.ty, self.colorNum)
        effects.add(new_effect)
    
    def draw(self,screen):
        '''
        sizeAdj = round(4*sin(self.lastFrame*3/180*pi))
        nimbusImage=pygame.Surface((48,48))
        nimbusImage=nimbusImage.convert_alpha()
        nimbusImage.fill((0, 0, 0, 0))
        nimbusImage.blit(get_value('nimbus'),(0, 0),(32*self.colorDict[self.colorNum], 0, 48,48))
        #nimbusImage = pygame.transform.smoothscale(nimbusImage,(64+sizeAdj, 64+sizeAdj))
        #functions.drawImage(nimbusImage,(self.rect.centerx, self.rect.centery), self.nimbusAngle, screen)
        self.nimbusAngle+=6
        '''
        self.frame += 1
        if self.frame >= self.interval:
            self.frame = 0
            self.part = (self.part+1)%8
        if self.gethit:
            self.gethitNum=32
            self.gethit=False
        else:
            self.gethitNum=0
        self.image=get_value('ghost')[self.part+self.colorNum*8+self.gethitNum]
        functions.drawImage(self.image, self.rect.center, 0, screen)

class Kedama(Enemy):
    def __init__(self):
        super().__init__()
        self.hitbox=pygame.Surface((32*magnitude,32*magnitude)).convert_alpha()
        self.rect=self.hitbox.get_rect()
        self.health = 1000
        self.frame = 0
        self.colorNum = randint(0, 3)
        self.direction = 0
        self.angleNum = 0
        self.interval = 5
        self.part = 0
        self.colorDict={'blue':0,'red':1,'green':2,'yellow':3}
    def initial(self,tx,ty,color):
        self.tx=tx
        self.ty=ty
        self.colorNum=self.colorDict.get(color)
        self.color=color
        self.truePos()
    def draw(self, screen):
        self.frame += 1
        if self.gethit:
            self.gethitNum=4
            self.gethit=False
        else:
            self.gethitNum=0
        if self.frame >= self.interval:
            self.frame = 0
        self.angleNum += 15
        self.image=get_value('kedama')[self.colorNum+self.gethitNum]
        functions.drawImage(self.image, self.rect.center, self.angleNum, screen)

class YinYangYu(Enemy):
    def __init__(self):
        super().__init__()
        self.hitbox=pygame.Surface((32*magnitude,32*magnitude)).convert_alpha()
        self.rect=self.hitbox.get_rect()
        self.health = 1000
        self.frame = 0
        self.colorNum = randint(0, 3)
        self.direction = 0
        self.angleNum = 0
        self.interval = 5
        self.part = 0
        self.colorDict={'red':0,'green':1,'blue':2,'purple':3}
    def initial(self,tx,ty,color):
        self.tx=tx
        self.ty=ty
        self.colorNum=self.colorDict.get(color)
        self.color=color
        self.truePos()
    def draw(self, screen):
        self.frame += 1
        if self.frame >= self.interval:
            self.frame = 0
        self.angleNum += 15
        if self.gethit:
            self.gethitNum=4
            self.gethit=False
        else:
            self.gethitNum=0
        self.image=get_value('yinyangyu')[self.colorNum+self.gethitNum]
        nimbus=get_value('yinyangyu')[self.colorNum+4+self.gethitNum]
        functions.drawImage(nimbus, self.rect.center, self.angleNum, screen)
        functions.drawImage(self.image, self.rect.center, self.angleNum, screen)

class Small_YinYangYu(Enemy):
    def __init__(self):
        super().__init__()
        self.hitbox=pygame.Surface((32*magnitude,32*magnitude)).convert_alpha()
        self.rect=self.hitbox.get_rect()
        self.health = 1000
        self.frame = 0
        self.colorNum = randint(0, 3)
        self.direction = 0
        self.angleNum = 0
        self.dAngleNum = 0
        self.interval = 5
        self.part = 0
        self.colorDict={'red':0,'green':1,'blue':2,'purple':3}
    def initial(self,tx,ty,color):
        self.tx=tx
        self.ty=ty
        self.colorNum=self.colorDict.get(color)
        self.color=color
        self.truePos()
    def draw(self, screen):
        self.frame += 1
        if self.frame >= self.interval:
            self.frame = 0
        self.angleNum += 15
        self.dAngleNum -= 15
        if self.gethit:
            self.gethitNum=4
            self.gethit=False
        else:
            self.gethitNum=0
        self.image=get_value('small_yinyangyu')[self.colorNum+self.gethitNum]
        nimbus=get_value('small_yinyangyu')[self.colorNum+4+self.gethitNum]
        functions.drawImage(nimbus, self.rect.center, self.dAngleNum, screen)
        functions.drawImage(self.image, self.rect.center, self.angleNum, screen)

#Stage 1 Beginning
class Small_YinYangYu_Begin_Stage_1(Small_YinYangYu):
    def __init__(self):
        super().__init__()
        self.health = 1000
        self.colorNum = 0
        
    def fire(self,bullets):
        if self.lastFrame==55:
            SE.play('enemyShoot_sound1',0.1)
            for i in range(6):
                new_bullet = bullet.Orb_Bullet()
                new_bullet.initial(self.tx,self.ty)
                new_bullet.selfTarget(get_value('player_cx'),get_value('player_cy'),5)
                if i == 0:
                    angle = new_bullet.angle
                else:
                    new_bullet.setSpeed(angle+i*60, 5)
                new_bullet.loadColor(self.color)
                bullets.add(new_bullet)

    def movement(self):
        if self.lastFrame<=50:
            speed = 10-10*(self.lastFrame/50)
            self.setSpeed(self.angle, speed)
        elif self.lastFrame == 60:
            angle = 45 if self.angle==0 else 135
            self.setSpeed(angle, 5)
        self.tx+=self.speedx
        self.ty+=self.speedy
        self.truePos()
        
    def doKill(self,items,bullets):
        self.createItem(items,1,2)
        self.createItem(items,0,2)
        new_bullet = bullet.Orb_Bullet()
        new_bullet.initial(self.tx,self.ty)
        new_bullet.selfTarget(get_value('player_cx'),get_value('player_cy'),10)
        new_bullet.loadColor('green')
        bullets.add(new_bullet)
        self.kill()

        
#Stage 1 Wave 1
class Fairy_Wave1_Stage_1(Fairy):
    def __init__(self):
        super().__init__()
        self.health=500
        
    def fire(self, bullets):
        if self.lastFrame==30:
            SE.play('enemyShoot_sound1',0.1)
            for i in range(1,6):
                new_bullet = bullet.Rice_Bullet()
                new_bullet.initial(self.rect.centerx,self.rect.centery)
                new_bullet.selfTarget(get_value('player_cx'),get_value('player_cy'),i*4)
                new_bullet.loadColor(list(small_bullet_colorDict.keys())[i+1])
                bullets.add(new_bullet)
    
    def movement(self):
        if self.lastFrame < 30:
            self.setSpeed(90,self.speed-(self.speed/30))
        elif self.lastFrame == 30:
            self.setSpeed(90, 0)
        elif self.lastFrame >=31 and self.speed<8:
            self.setSpeed(90,self.speed+8/30)
        self.tx += self.speedx
        self.ty += self.speedy
        self.truePos()
        self.countAngle()
        
    def doKill(self,items,bullets):
        self.createItem(items,1,2)
        self.createItem(items,0,2)
        for i in range(-1,2):
            new_bullet = bullet.Scale_Bullet()
            new_bullet.initial(self.tx,self.ty)
            new_bullet.selfTarget(get_value('player_cx'),get_value('player_cy'),10)
            new_bullet.setSpeed(new_bullet.angle+i*10, 10)
            new_bullet.loadColor('blue')
            bullets.add(new_bullet)
        self.kill()
        
class Flower_Fairy_Wave1_Stage_1(Flower_Fairy):
    def __init__(self):
        super().__init__()
        self.health = 10000
        
    def movement(self):
        if self.lastFrame%3==0 and self.speedy>0:
            self.speedy -= 1
        if self.lastFrame >= 300 and self.speedy<4 and self.lastFrame%2==0:
            self.speedy += 1
        #print(self.speedx)
        self.tx+=self.speedx
        self.ty+=self.speedy
        self.truePos()
    
    def fire(self,bullets):
        if self.lastFrame%30!=0 or self.speedy !=0 or self.lastFrame >= 300:
            return
        SE.play('enemyShoot_sound1',0.1)
        for i in range(0,36):
            new_bullet=bullet.Mid_Bullet()
            new_bullet.Accelerate_initial(self.tx,self.ty,60,0,60,20,10)
            if i == 0:
                new_bullet.selfTarget(get_value('player_cx'), get_value('player_cy'), 15)
                self.fangle=new_bullet.angle
            else:
                new_bullet.setSpeed((self.fangle+i*10)%360,15)
            new_bullet.loadColor(list(small_bullet_colorDict.keys())[12])
            bullets.add(new_bullet)
    
    def doKill(self,items,bullets):
        self.createItem(items,1,2)
        if get_value('player_firelevel') == 4:
            self.createItem(items,1,5)
        else:
            self.createItem(items,0,5)
        self.kill()
            
#Stage 1 Wave 2
class Small_YinYangYu_Left_Wave2_Stage_1(Small_YinYangYu):
    def __init__(self):
        super().__init__()
        self.health = 500
        self.fireframe = randint(0,25)
        
    def fire(self, bullets):
        self.fireframe += 1
        if self.fireframe % 50 == 0:
            new_bullet = bullet.Pin_Bullet()
            new_bullet.initial(self.rect.centerx,self.rect.centery)
            new_bullet.selfTarget(get_value('player_cx'), get_value('player_cy'), 6)
            new_bullet.loadColor(self.color)
            SE.play('enemyShoot_sound1',0.1)
            bullets.add(new_bullet)
            
    def movement(self):
        if self.lastFrame > 60 and self.lastFrame <= 75:
            self.setSpeed((self.lastFrame-60)*(90//15), 7)
        if self.lastFrame == 75:
            self.setSpeed(90, 7)
        elif self.lastFrame > 100 and self.lastFrame%3==0 and self.lastFrame < 400:
            angle = (self.angle+6)%360
            self.setSpeed(angle, 7)
        self.tx += self.speedx
        self.ty += self.speedy
        self.truePos()

    def doKill(self, items, bullets):
        self.createItem(items,1,2)
        if get_value('player_firelevel') == 4:
            self.createItem(items,1,1)
        else:
            self.createItem(items,0,1)
        self.kill()

class Small_YinYangYu_Right_Wave2_Stage_1(Small_YinYangYu):
    def __init__(self):
        super().__init__()
        self.health = 500
        self.fireframe = randint(0,25)

    def fire(self, bullets):
        self.fireframe += 1
        if self.fireframe % 50 == 0:
            new_bullet = bullet.Chain_Bullet()
            new_bullet.initial(self.rect.centerx,self.rect.centery)
            new_bullet.selfTarget(get_value('player_cx'), get_value('player_cy'), 6)
            new_bullet.loadColor(self.color)
            SE.play('enemyShoot_sound1',0.1)
            bullets.add(new_bullet)
            
    def movement(self):
        if self.lastFrame > 60 and self.lastFrame <= 75:
            self.setSpeed(180-(self.lastFrame-60)*(90//15), 7)
        if self.lastFrame == 75:
            self.setSpeed(90, 7)
        elif self.lastFrame > 100 and self.lastFrame%3==0 and self.lastFrame < 400:
            angle = (self.angle-6)%360
            self.setSpeed(angle, 7)
        self.tx += self.speedx
        self.ty += self.speedy
        self.truePos()

    def doKill(self, items, bullets):
        self.createItem(items,1,2)
        if get_value('player_firelevel') == 4:
            self.createItem(items,1,1)
        else:
            self.createItem(items,0,1)
        self.kill()
        
#Stage 1 Wave 3
class Ghost_Wave3_Stage_1(Ghost):
    def __init__(self):
        super().__init__()
        self.health=300
        
    def initial(self,tx,ty,color,item_type):
        self.tx=tx
        self.ty=ty
        self.colorNum = self.colorDict.get(color)
        self.color=color
        self.item_type=item_type
        self.truePos()
        
    def movement(self):
        self.tx += uniform(-5,5)
        self.ty += 3
        self.truePos()
        
    def fire(self,bullets):
        if self.lastFrame%10==0 and self.lastFrame <= 50:
            for i in range(0, 3):
                SE.play('enemyShoot_sound1',0.1)
                new_bullet = bullet.Satsu_Bullet()
                new_bullet.initial(self.rect.centerx,self.rect.centery)
                if i == 0:
                    new_bullet.selfTarget(get_value('player_cx'), get_value('player_cy'), 3)
                    angle = new_bullet.angle
                new_bullet.setSpeed(angle+(i-1)*15, 15)
                new_bullet.loadColor(self.color)
                bullets.add(new_bullet)
        
    def doKill(self,items, bullets):
        self.createItem(items,self.item_type,2)
        self.kill()
        
#Stage 1 Wave 4
class fairy_test_Stage_1(Fairy):
    def __init__(self):
        super().__init__()
        self.health = 600
        
    def fire(self,bullets):
        if self.lastFrame == 70:
            SE.play('enemyShoot_sound2',0.1)
            basicAngle=random()*360
            for j in range(0,3):
                angle=basicAngle-j*8
                for i in range(0,10):
                    new_bullet=bullet.Mid_Bullet()
                    new_bullet.Accelerate_initial(self.rect.centerx,self.rect.centery,10,0,0,15,20)
                    new_bullet.setSpeed(angle+i*36,15)
                    new_bullet.loadColor(list(small_bullet_colorDict.keys())[5])
                    bullets.add(new_bullet)
                    
    def movement(self):
        if self.lastFrame == 59:
            self.angleFixed = self.angle
        if self.lastFrame >= 60 and self.lastFrame <= 100:
            if self.angleFixed < 90:
                self.setSpeed(self.angleFixed+self.lastFrame/2, 2)
            else:
                self.setSpeed(self.angleFixed-self.lastFrame/2, 2)
        self.tx += self.speedx
        self.ty += self.speedy
        self.truePos()
        #print(self.angle, self.angleNum)
    
    def doKill(self,items,bullets):
        self.createItem(items,1,2)
        if get_value('player_firelevel') == 4:
            self.createItem(items,1,5)
        else:
            self.createItem(items,0,5)
        self.kill()
        
class flower_fairy_test_Stage_1(Flower_Fairy):
    def __init__(self):
        super().__init__()
        self.health = 3000
        self.fireangle = -60
        self.change = False

    def fire(self,bullets):
        angle = uniform(-3,3)
        if self.lastFrame >= 30 and self.lastFrame <= 110 and self.lastFrame%30==0:
            SE.play('enemyShoot_sound1',0.1)
            for i in range(-10, 11):
                new_bullet=bullet.Gun_Bullet()
                new_bullet.Accelerate_initial(self.rect.centerx,self.rect.centery,10,0,30,15,20)
                new_bullet.setSpeed(90+i*6+angle,15)
                new_bullet.loadColor(list(small_bullet_colorDict.keys())[1])
                bullets.add(new_bullet)

    def movement(self):
        self.speedx = 0
        if self.lastFrame <= 30 and self.lastFrame % 7 == 0:
            self.speedy -= 1
        elif self.lastFrame > 110 and self.speedy < 7 and self.lastFrame % 3 == 0:
            self.speedy += 1
        #print(self.speedy)
        self.tx += self.speedx
        self.ty += self.speedy
        self.truePos()

    def doKill(self,items,bullets):
        self.createItem(items,1,2)
        if get_value('player_firelevel') == 4:
            self.createItem(items,1,5)
        else:
            self.createItem(items,0,5)
        self.kill()

#Stage 1 Wave 5
class YinYangYu_Wave5_Stage_1(YinYangYu):
    def __init__(self):
        super().__init__()
        self.health = 500
        self.fireFrame=-1
        self.fireAngle=0
        
    def fire(self,bullets):
        self.fireFrame+=1
        if self.fireFrame%100!=0 and self.fireFrame%100!= 15 and self.fireFrame%100 != 30 and self.fireFrame%100 != 45:
            return
        SE.play('enemyShoot_sound1',0.1)
        self.fireAngle=randint(0,60)
        for i in range(0,6):
            new_bullet=bullet.Knife_Bullet()
            new_bullet.initial(self.rect.centerx,self.rect.centery)
            new_bullet.setSpeed(self.fireAngle+i*60,15)
            new_bullet.loadColor(list(mid_bullet_colorDict.keys())[randint(0,7)])
            bullets.add(new_bullet)
        
    def doKill(self, items, bullets):
        self.createItem(items,1,2)
        if get_value('player_firelevel') == 4:
            self.createItem(items,1,1)
        else:
            self.createItem(items,0,1)
        self.kill()

#Stage 1 Wave 6
class Kedama_Wave6_Stage_1(Kedama):
    def __init__(self):
        super().__init__()
        self.health = 1000
        self.fireFrame = -1
        
    def fire(self,bullets):
        self.fireFrame += 1
        if self.fireFrame % 23 != 0:
            return
        SE.play('enemyShoot_sound1',0.1)
        for i in range(-1, 2):
            if not i:
                continue
            new_bullet=bullet.Satsu_Bullet()
            new_bullet.Locus_initial(self.rect.centerx,self.rect.centery,i*2,10,60)
            new_bullet.loadColor(list(small_bullet_colorDict.keys())[randint(0,15)])
            new_bullet.setSpeed(self.angle+i*30,7)
            bullets.add(new_bullet)
        
    def doKill(self, items, bullets):
        self.createItem(items,1,2)
        if get_value('player_firelevel') == 4:
            self.createItem(items,1,1)
        else:
            self.createItem(items,0,1)
        self.kill()
        angle = randint(0,45)
        for i in range(0,9):
            new_bullet=bullet.Satsu_Bullet()
            new_bullet.initial(self.rect.centerx,self.rect.centery)
            new_bullet.setSpeed(i*45+angle,7)
            new_bullet.loadColor(list(small_bullet_colorDict.keys())[randint(0,15)])
            bullets.add(new_bullet)

#Stage 1 Wave 7
class Sp_Fairy_Wave7_Stage_1(Sp_Fairy):
    def __init__(self):
        super().__init__()
        self.health = 500
        self.fireFrame = -1
        
    def fire(self,bullets):
        self.fireFrame += 1
        if self.fireFrame % 30 != 0:
            return
        SE.play('enemyShoot_sound2',0.1)
        angle = self.countTargetAngle(get_value('player_cx'),get_value('player_cy'))
        for i in range(-1, 2):
            new_bullet=bullet.Bact_Bullet()
            new_bullet.Accelerate_initial(self.rect.centerx,self.rect.centery,10,0,30,15,20)
            new_bullet.setSpeed(angle+i*15,15)
            new_bullet.loadColor(list(small_bullet_colorDict.keys())[randint(0,15)])
            bullets.add(new_bullet)
        
    def doKill(self, items, bullets):
        self.createItem(items,1,2)
        if get_value('player_firelevel') == 4:
            self.createItem(items,1,5)
        else:
            self.createItem(items,0,5)  
        self.kill()

class Mid_Fairy_Wave7_Stage_1(Mid_Fairy):
    def __init__(self):
        super().__init__()
        self.health = 1500
        self.fireFrame = -1

    def movement(self):
        if self.lastFrame <= 30:
            speed = 10*cos(radians(self.lastFrame*2.5))
            self.setSpeed(self.angle,speed)
        elif self.lastFrame > 60 and self.lastFrame <= 120:
            speed = 6*sin(radians(self.lastFrame-60))
            self.setSpeed(self.angle,speed)
        self.tx += self.speedx
        self.ty += self.speedy
        self.truePos()
        self.countAngle()
        
    
    def fire(self,bullets):
        self.fireFrame += 1
        if self.fireFrame != 40 and self.fireFrame != 60:
            return
        SE.play('enemyShoot_sound1',0.25,1)
        #angle = self.countTargetAngle(get_value('player_cx'),get_value('player_cy'))
        radius=10
        sides=4
        per_bullet=2
        for i in range(sides):
            angle1 = (2 * pi / sides) * i
            angle2 = (2 * pi / sides) * (i + 1)
        
            # Calculate the vertex positions
            x1 = self.tx + radius * cos(angle1)
            y1 = self.ty + radius * sin(angle1)
            x2 = self.tx + radius * cos(angle2)
            y2 = self.ty + radius * sin(angle2)
            
            # Draw bullets along the line segment (side) between vertices
            for j in range(per_bullet + 1):  # +1 to include the vertex
                # Interpolate position along the side
                bullet_x = x1 + (x2 - x1) * (j / per_bullet)
                bullet_y = y1 + (y2 - y1) * (j / per_bullet)
                new_bullet = bullet.Orb_Bullet()
                part = abs(j-per_bullet/2+1)/(per_bullet)
                new_bullet.Accelerate_initial(bullet_x,bullet_y,20,0,20,10,5)
                angle = new_bullet.returnTargetAngle(self.tx,self.ty)-180
                new_bullet.setSpeed(angle,10)
                new_bullet.loadColor('red')
                bullets.add(new_bullet)
                
    
    # def laser(self,lasers):
    #     if self.lastFrame==20:
    #         new_laser = bullet.Lasers()
    #         new_laser.main=True
    #         new_laser.initial(self.tx,self.ty,90)
    #         new_laser.loadColor('red')
    #         new_laser.setSpeed(90,10)
    #         lasers.add(new_laser)
        
    def doKill(self, items, bullets):
        self.createItem(items,1,2)
        if get_value('player_firelevel') == 4:
            self.createItem(items,1,5)
        else:
            self.createItem(items,0,5)  
        self.kill()


#Stage 2 Begginning
class Fairy_Begin_Left_Stage_1(Fairy):
    def __init__(self):
        super().__init__()
        self.health = 150
        self.colorNum = 1
        self.r = randint(-10,50)
        
    def fire(self,bullets):
        if self.lastFrame==100+self.r:
            SE.play('enemyShoot_sound1',0.1)
            new_bullet = bullet.Orb_Bullet()
            new_bullet.initial(self.tx,self.ty)
            new_bullet.selfTarget(get_value('player_cx'),get_value('player_cy'),5)
            new_bullet.loadColor('orange')
            bullets.add(new_bullet)
        
    def movement(self):
        if self.lastFrame<=90+self.r:
            angle = self.angle-60/(90+self.r)
            if angle < 0:
                angle=0
            self.setSpeed(angle,abs(cos(radians(self.lastFrame-self.r+10))*4))
        elif self.lastFrame > 90+self.r and self.lastFrame <= 95+self.r:
            angle = self.angle+90/5
            self.setSpeed(angle, 0)
            if self.angle >= 20 and self.angle <= 50:
                self.lock=True
            else:
                self.lock=False
        else:
            angle = 360-10*(self.lastFrame-95-self.r)
            if angle < 340:
                angle=340
            self.setSpeed(angle, 3)
            if self.angle >= 20 and self.angle <= 50:
                self.lock=True
            else:
                self.lock=False
        self.tx += self.speedx
        self.ty += self.speedy
        self.truePos()
        
    def doKill(self,items,bullets):
        self.createItem(items,1,2)
        self.createItem(items,0,2)
        new_bullet = bullet.Orb_Bullet()
        new_bullet.initial(self.tx,self.ty)
        new_bullet.selfTarget(get_value('player_cx'),get_value('player_cy'),10)
        new_bullet.loadColor('red')
        bullets.add(new_bullet)
        self.kill()

class Fairy_Begin_Right_Stage_1(Fairy):
    def __init__(self):
        super().__init__()
        self.health = 150
        self.colorNum = 0
        self.r = randint(-10,50)
        
    def fire(self,bullets):
        if self.lastFrame==100+self.r:
            SE.play('enemyShoot_sound1',0.1)
            new_bullet = bullet.Orb_Bullet()
            new_bullet.initial(self.tx,self.ty)
            new_bullet.selfTarget(get_value('player_cx'),get_value('player_cy'),5)
            new_bullet.loadColor('lightBlue')
            bullets.add(new_bullet)
        
    def movement(self):
        if self.lastFrame<=90+self.r:
            angle = self.angle+60/(90+self.r)
            if angle > 180:
                angle=180
            self.setSpeed(angle,abs(cos(radians(self.lastFrame-self.r+10))*4))
        elif self.lastFrame > 90+self.r and self.lastFrame <= 95+self.r:
            angle = self.angle-90/5
            self.setSpeed(angle, 0)
            if self.angle >= 130 and self.angle <= 160:
                self.lock=True
            else:
                self.lock=False
        elif self.lastFrame > 95+self.r:
            angle = 90+10*(self.lastFrame-95-self.r)
            if angle > 200:
                angle=200
            self.setSpeed(angle, 3)
            if self.angle >= 130 and self.angle <= 160:
                self.lock=True
            else:
                self.lock=False
        self.tx += self.speedx
        self.ty += self.speedy
        self.truePos()
        
    def doKill(self,items,bullets):
        self.createItem(items,1,2)
        self.createItem(items,0,2)
        new_bullet = bullet.Orb_Bullet()
        new_bullet.initial(self.tx,self.ty)
        new_bullet.selfTarget(get_value('player_cx'),get_value('player_cy'),10)
        new_bullet.loadColor('blue')
        bullets.add(new_bullet)
        self.kill()
        
#Stage 2 Wave 1