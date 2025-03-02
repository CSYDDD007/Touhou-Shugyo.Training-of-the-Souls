import pygame
import bullet
import functions
import item
import effect
import background


from const import *
from math import *
from random import *
from global_var import *
import SoundEffect


class BOSS(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.hitbox = pygame.Surface((100, 160))
        self.hitbox.fill( WHITE )
        self.rect = self.hitbox.get_rect()
        self.tx = 1000.0
        self.ty = -600.0
        self.speedx = 0.0
        self.speedy = 0.0
        self.movingFrame = 0
        self.maxMovingFrame = 0
        self.lastFrame = 0
        self.maxhealth = 100000
        self.health = 100000
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
        self.nimbus = get_value('boss_magic')

    def speedAlter(self, speedx, speedy):
        self.speedx = speedx
        self.speedy = speedy

    def selfTarget(self, speed):
        px = get_value('player_cx')
        py = get_value('player_cy')
        mx = self.tx
        my = self.ty
        dx = px-mx
        dy = py-my
        dist = sqrt(dx**2 + dy**2)
        times = dist/speed
        speedx = dx/times
        speedy = dy/times
        self.speedAlter(speedx, speedy)

    def setSpeed(self, angle, speed):
        s = sin(radians(angle))
        c = cos(radians(angle))
        self.speedx = c*speed
        self.speedy = s*speed

    def initial(self, posx, posy):
        self.tx = posx
        self.ty = posy
        self.truePos()

    def truePos(self):
        self.rect.centerx = round(self.tx)
        self.rect.centery = round(self.ty)

    def countAngle(self, dx, dy):
        if dx != 0:
            t = dy/dx
            deg = atan(t)*180/pi
        else: #speedx == 0
            if dy >= 0: #downwards
                deg = 90
            elif dy < 0: #upwards
                deg = 270
        if dx<0:
            deg+=180
        elif dy<0 and deg<0:
            deg+=360
        self.angle = deg

    def checkDistance(self):
        px = get_value('player_cx')
        py = get_value('player_cy')
        mx = self.tx
        my = self.ty
        dx = px-mx
        dy = py-my
        dist = sqrt(dx**2+dy**2)
        miniDist = get_value('enemypos')[2]
        if self.tx<820 and self.tx>60 and self.ty<900 and self.ty>30 and dist<miniDist:
            set_value('enemypos',(self.tx,self.ty,dist))

    def gotoPosition(self,x,y,inFrame):
        dx=x-self.tx
        dy=y-self.ty
        distance=sqrt(pow(dx,2)+pow(dy,2))
        speed=distance/inFrame
        self.movingFrame=inFrame
        self.maxMovingFrame=inFrame
        self.countAngle(dx,dy)
        self.setSpeed(self.angle,speed)
        self.tempx=0
        self.tempy=0

    def movement(self):
        self.movingFrame-=1
        if self.maxMovingFrame!=0:
            self.moving = True
            if self.movingFrame<self.maxMovingFrame/2:
                self.tempx-=self.speedx/self.maxMovingFrame*4
                self.tempy-=self.speedy/self.maxMovingFrame*4
            else:
                self.tempx+=self.speedx/self.maxMovingFrame*4
                self.tempy+=self.speedy/self.maxMovingFrame*4
            #print(self.tx, self.ty)
        
        self.tx+=self.tempx
        self.ty+=self.tempy
        self.truePos()
        if self.movingFrame<=0:
            self.tempx=0
            self.tempy=0
            self.speedx=0
            self.speedy=0
            self.movingFrame=0
            self.moving = False
            
    def recover(self):
        set_value('show_health', True)
        if self.health<self.maxhealth:
            self.health+=1000
        else:
            self.recovering = False
            
    def createItem(self,items,Type,num):
        for i in range(0,num):
            dx=random()*240-120
            dy=random()*100*-1
            new_item = item.item()
            new_item.type=Type
            x_now=self.tx+dx
            y_now=self.ty+dy
            if x_now<0+16:
                x_now=16
            if x_now>768-16:
                x_now=768-16
            new_item.initial(x_now,y_now)
            items.add(new_item)

    def dropItem(self, items):
        self.createItem(items,0,30)
        self.createItem(items,1,30)

    def doKill(self,items,bullets,effects):
        for b in bullets:
            new_item=bullet.createItem(b.rect.centerx,b.rect.centery,items)
            new_vanish = effect.bulletVanish()
            new_vanish.initial(b.image, b.rect.center, b.angle)
            effects.add(new_vanish)
            b.kill()
        #self.dropItem(items)

    def drawSpellCardAttack(self,backgrounds,name):
        '''
        for i in range(0,12):
            for j in range(-1,5):
                new_back = background.Spell_Attack()
                if i%2 == 0:#move right 237 155
                    if j == -1:
                        sy =i*70+460
                    new_back.initial(237*j+50, i*70-(j+1)*130+320,sy,1)
                    new_back.setSpeed(330, 6)
                    new_back.moveFrame = (3-j+1)*40+20
                else:
                    if j == -1:
                        sy = i*70-300
                    new_back.initial(237*j, i*70-(j+1)*130+350,sy, 0)
                    new_back.setSpeed(150, 6)
                    new_back.moveFrame = (j+1)*40+20
                backgrounds.add(new_back)
        '''
        new_back = background.Spell_NPC()
        new_back.initial(540,-400,name)
        new_back.setSpeed(130,30)
        backgrounds.add(new_back)
        new_back = background.spellAttackImage()
        backgrounds.add(new_back)
        
    '''
    def drawArc(self, surface, x, y, r, th, start, stop, color):
        points_outer = []
        points_inner = []
        n = round(r*abs(stop-start)/20)
        if n<2:
            n = 2
        for i in range(n):
            delta = i/(n-1)
            phi0 = start + (stop-start)*delta
            x0 = round(x+r*cos(phi0))
            y0 = round(y+r*sin(phi0))
            points_outer.append([x0,y0])
            phi1 = stop + (start-stop)*delta
            x1 = round(x+(r-th)*cos(phi1))
            y1 = round(y+(r-th)*sin(phi1))
            points_inner.append([x1,y1])
        points = points_outer + points_inner        
        pygame.gfxdraw.aapolygon(surface, points, color)
        pygame.gfxdraw.filled_polygon(surface, points, color)
    '''
        
class Reitsu(BOSS):
    def __init__(self):
        super().__init__()
        self.img = get_value('cat_boss')
        self.index = 0
        self.health = 100000
        self.maxhealth = 100000
        self.tospellhealth = 20000
        self.wait=0
        self.fireangle = 60
        self.fireangle1 = 25
        self.fireangle2 = 60
        self.change = False
        self.nimbusAngle=0
        self.nimbusSize=0
        self.entering=True
        self.idxFrame=0
        self.spellName = ['列符「札卡小队」','齐心「团队合作」','列符「札卡方阵」','无畏「札卡冲锋」','努力「一开始就要坚持到底」']
        self.cardNum=1
        self.times_lists = [30,60,60,60,30,60]
        self.a = 0

    def draw(self, screen):
        self.idxFrame+=1
        if self.idxFrame % 6 == 0:
            if not self.moving or self.moving and self.tempx == 0:
                if self.index < 0 and self.index > 3:
                    self.index = 0
                self.index = (self.index+1)%4
            else:
                if self.tempx > 0:
                    if self.index < 4 or self.index > 7:
                        self.index = 4
                    if self.index < 7:
                        self.index += 1
                elif self.tempx < 0:
                    if self.index < 8 or self.index > 11:
                        self.index = 8
                    if self.index < 11:
                        self.index += 1
                #print(self.tempx)
                #print(self.index)
        self.nimbusAngle = (self.nimbusAngle+1)%360
        nimbus = pygame.transform.smoothscale(self.nimbus, (384+sin(radians(self.nimbusAngle))*70, 384-sin(radians(self.nimbusAngle))*70))
        self.image=self.img
        functions.drawImage(nimbus, self.rect.center, self.nimbusAngle, screen)
        functions.drawImage(self.image, (self.rect.centerx, self.rect.centery+sin(radians(self.lastFrame))*30), 270, screen)
        
    def update(self, screen, bullets, lasers, items, effects, backgrounds):
        set_value('boss_health',self.health)
        set_value('boss_maxhealth',self.maxhealth)
        set_value('boss_spellhealth',self.tospellhealth)
        if self.wait:
            self.wait-=1
        if not get_value('plot') and not self.wait:
            self.lastFrame += 1
        if self.recovering and not self.wait:
            if self.recovering == 2:
                self.health = 10
                new_effect = effect.Health_Bar()
                new_effect.initial(self.maxhealth)
                get_value('boss_effect').add(new_effect)
                set_value('boss_health',self.health)
                self.recovering = True
            elif self.recovering > 1:
                self.recovering -= 1
            else:
                self.recover()
        if get_value('plot'):
            self.entering=False
        self.Change_Stage(items,bullets,backgrounds,effects)
        self.movement()
        set_value('boss_pos',self.rect.center)
        self.checkDistance()
        self.draw(screen)
        self.Attack(bullets,effects)
        
        
    def Change_Stage(self,items,bullets,backgrounds,effects):
        if (self.health <= self.tospellhealth and not self.recovering or self.times_lists[(self.cardNum-1)*2+self.ifSpell]-self.lastFrame/60<=0)and not self.ifSpell:
            for i in get_value('boss_effect'):
                if i.__class__.__name__ in ('Timer', 'SpellCard_Bonus'):
                    i.times = self.times_lists[(self.cardNum-1)*2+self.ifSpell]*60
            functions.showBackground(backgrounds, 'STAGE_2')
            SoundEffect.play('spell_sound',0.5)
            self.spellFrame=-1
            self.ifSpell = True
            new_effect = effect.Spell_Name()
            new_effect.initial(self.spellName[self.cardNum-1])
            get_value('boss_effect').add(new_effect)
            set_value('ifSpell',True)
            self.gotoPosition(384*1.5/2,200,30)
            self.doKill(items,bullets,effects)
            self.drawSpellCardAttack(backgrounds,'reitsu')
            self.lastFrame=1
        elif (self.health <= 0 or self.times_lists[(self.cardNum-1)*2+self.ifSpell]-self.lastFrame/60 <= 0) and self.ifSpell:
            for i in get_value('boss_effect'):
                if i.__class__.__name__ in ('Timer', 'SpellCard_Bonus'):
                    i.times = self.times_lists[(self.cardNum-1)*2+self.ifSpell]*60
            if self.cardNum == 3:
                set_value('waveNum',11)
                set_value('frame', 0)
                set_value('boss_alive',False)
                self.kill()
            functions.showBackground(backgrounds, 'STAGE_1')
            SoundEffect.play('spellEnd_sound',0.5)
            self.doKill(items,bullets,effects)
            self.dropItem(items)
            self.cardNum += 1
            if self.cardNum==4:
                self.cardNum=1
            if self.cardNum == 2:
                self.gotoPosition(384*1.5/2,200,10)
            self.health = 10
            self.recovering=15
            set_value('show_health', False)
            self.maxhealth = 100000
            self.ifSpell = False
            set_value('ifSpell',False)
            self.lastFrame=1
            self.wait=60
            
        
    def Attack(self, bullets,effects):
        if get_value('plot') or self.entering:
            return
        if self.cardNum== 1:
            if not self.ifSpell:
                if len(get_value('boss_effect'))==1:
                    new_effect = effect.Timer()
                    new_effect.times = 30*60
                    get_value('boss_effect').add(new_effect)
                    new_effect = effect.SpellCard_Bonus()
                    get_value('boss_effect').add(new_effect)
                    self.recovering = 3
                    new_effect1 = effect.Boss_Attack_Effect()
                    effects.add(new_effect1)
                self.non_spell_test_5(bullets)
                if self.lastFrame % 150 == 0:
                    self.gotoPosition(randint(50, 576-50), randint(120, 240), 100)
                if self.moving and not self.entering:
                    if self.lastFrame%3==0:
                        self.non_spell_test(bullets)
            else:
                self.Spell_1(bullets,effects)
        elif self.cardNum== 2:
            if not self.ifSpell:
                self.non_spell_test_4(bullets)
            elif self.ifSpell and self.lastFrame > 100:
                self.Spell_2(bullets)
            elif self.ifSpell and self.lastFrame == 30:
                new_effect1 = effect.Boss_Attack_Effect()
                effects.add(new_effect1)
        elif self.cardNum == 3:
            if not self.ifSpell:
                if self.lastFrame % 150 == 0:
                    self.gotoPosition(randint(50, 576-50), randint(120, 240), 100)
                if not self.moving:
                    self.non_spell_test_6(bullets)
            else:
                if self.lastFrame % 100 == 0:
                    if self.rect.centerx < 288:
                        self.gotoPosition(self.rect.centerx+randint(50,100), randint(120, 240), 70)
                    else:
                        self.gotoPosition(self.rect.centerx-randint(50,100), randint(120, 240), 70)
                self.Spell_3(bullets)

    def Spell_1(self, bullets, effects):
        if self.lastFrame % 220 == 0:
            self.gotoPosition(randint(50, 576-50), randint(120, 240), 70)
        if not self.moving:
            if self.lastFrame % 100 == 30:
                new_effect1 = effect.Boss_Attack_Effect()
                effects.add(new_effect1)
            if self.lastFrame % 100 == 0:
                self.non_spell_test_2(bullets)
            if self.lastFrame % 8 == 0:
                self.non_spell_test_1(bullets)

    def Spell_2(self, bullets):
        #SoundEffect.play('kira_sound',0.2,0)
        self.a = (self.a+12*sin(radians(self.lastFrame)))%360
        new_bullet=bullet.Satsu_Bullet()
        new_bullet.initial(self.rect.centerx-100,self.rect.centery)
        new_bullet.loadColor('skyBlue')
        new_bullet.setSpeed(self.a+uniform(-1,1),7)
        bullets.add(new_bullet)
        new_bullet=bullet.Satsu_Bullet()
        new_bullet.initial(self.rect.centerx+100,self.rect.centery)
        new_bullet.loadColor('skyBlue')
        new_bullet.setSpeed(-self.a+uniform(-1,1)+180,7)
        bullets.add(new_bullet)
        if self.lastFrame % 100 in(0,20,40):
            SoundEffect.play('enemyShoot_sound1',0.35,True)
            new_bullet=bullet.Mid_Bullet()
            new_bullet.initial(self.rect.centerx+100,self.rect.centery)
            new_bullet.loadColor('blue')
            new_bullet.selfTarget(get_value('player_cx'), get_value('player_cy'), 3)
            bullets.add(new_bullet)
            new_bullet=bullet.Mid_Bullet()
            new_bullet.initial(self.rect.centerx-100,self.rect.centery)
            new_bullet.loadColor('blue')
            new_bullet.selfTarget(get_value('player_cx'), get_value('player_cy'), 3)
            bullets.add(new_bullet)
            

    def Spell_3(self, bullets):
        if not self.moving:
            if self.lastFrame % 20==0:
                new_bullet=bullet.Explode_Big_Star_Bullet()
                new_bullet.initial(self.rect.centerx,self.rect.centery)
                new_bullet.explodeFrame=100
                new_bullet.loadColor('blue')
                new_bullet.selfTarget(get_value('player_cx'), get_value('player_cy'), 7)
                angle = new_bullet.angle
                bullets.add(new_bullet)
                for i in range(-3,4):
                    if i == 0:
                        continue
                    new_bullet=bullet.Explode_Big_Star_Bullet()
                    new_bullet.initial(self.rect.centerx,self.rect.centery)
                    new_bullet.explodeFrame=1000
                    new_bullet.loadColor('blue')
                    new_bullet.setSpeed(angle+i*10, 7)
                    bullets.add(new_bullet)


    def non_spell_test(self,bullets):
        angle = 90+uniform(-5,5)*12
        for i in range(-2,3):
            new_bullet=bullet.Satsu_Bullet()
            new_bullet.initial(self.rect.centerx,self.rect.centery)
            new_bullet.setSpeed(angle+i*15,5+uniform(2,7))
            new_bullet.loadColor('skyBlue')
            bullets.add(new_bullet)

    def non_spell_test_1(self,bullets):
        self.fireangle1 += 10
        new_bullet=bullet.Explode_Big_Star_Bullet()
        new_bullet.initial(self.rect.centerx,self.rect.centery)
        new_bullet.explodeFrame=100
        new_bullet.setSpeed(90+self.fireangle1,10)
        new_bullet.loadColor('blue')
        bullets.add(new_bullet)

    def non_spell_test_2(self,bullets):
        for i in range(-30, 31):
            new_bullet=bullet.Satsu_Bullet()
            new_bullet.Locus_initial(self.rect.centerx,self.rect.centery,randint(-2,2),10,60)
            new_bullet.setSpeed(90+i*6+uniform(-1,1),5)
            new_bullet.loadColor('skyBlue')
            bullets.add(new_bullet)
            
    def non_spell_test_3(self,bullets):
        if self.lastFrame%2==0:
            new_bullet=bullet.Rain_Rice_Bullet()
            new_bullet.initial(randint(30,768-30),randint(100,520))
            new_bullet.stFrame=15
            new_bullet.rainFrame=60
            angle = randint(260,280)
            speed=randint(3,6)
            new_bullet.setSpeed(angle,speed)
            new_bullet.orgAngle=angle
            new_bullet.orgSpeed=speed
            new_bullet.loadColor('skyBlue')
            bullets.add(new_bullet)

    def non_spell_test_4(self,bullets):
        if self.lastFrame%4==0:
            new_bullet=bullet.Mid_Bullet()
            new_bullet.Bounce_initial(self.rect.centerx,self.rect.centery,2,1800)
            new_bullet.setSpeed(randint(60,120),7)
            new_bullet.loadColor('blue')
            bullets.add(new_bullet)

    def non_spell_test_5(self,bullets):
        if self.lastFrame%10==0:
            a=randint(0,30)
            x=randint(-20,20)
            y=randint(-20,20)
            for i in range(0,12):
                color = list(small_bullet_colorDict.keys())[choice([1,15])]
                angle=30*i+a
                for j in range(-2,3):
                    new_bullet = bullet.Satsu_Bullet()
                    new_bullet.initial(self.rect.centerx+x,self.rect.centery+y)
                    new_bullet.setSpeed(angle+j*3,5)
                    new_bullet.loadColor(color)
                    bullets.add(new_bullet)
                    
    def non_spell_test_6(self,bullets):
        if self.lastFrame%10==0:
            SoundEffect.play('enemyShoot_sound1',0.35,True)
            a=randint(0,45)
            for i in range(0,8):
                color = list(small_bullet_colorDict.keys())[4]
                angle=45*i+a
                for j in range(0,8):
                    new_bullet=bullet.Satsu_Bullet()
                    new_bullet.Circular_initial(self.rect.centerx,self.rect.centery,self.rect.centerx,self.rect.centery,40,j*45)
                    new_bullet.setSpeed(angle,5)
                    new_bullet.loadColor(color)
                    bullets.add(new_bullet)

    
class Cirno(BOSS):
    def __init__(self):
        super().__init__()
        self.img = get_value('cirno_boss')
        self.index = 0
        self.health = 100000
        self.maxhealth = 100000
        self.tospellhealth = 20000
        self.wait=0
        self.fireangle = 60
        self.fireangle1 = 25
        self.fireangle2 = 60
        self.change = False
        self.nimbusAngle=0
        self.nimbusSize=0
        self.entering=True
        self.idxFrame=0
        self.spellName = ['雪怒「Ice Age」','雪怒「Snowstorm」','雪怒「Frostbite」','雪怒「Blizzard」','雪怒「Hailstorm」','雪怒「Thunderstorm」']
        self.cardNum=1
        self.times_lists = [30,60,60,60,30,60]
        self.a = 0
        set_value('ifSpell',False)

    def draw(self, screen):
        self.idxFrame+=1
        if self.idxFrame % 6 == 0:
            if not self.moving or self.moving and self.tempx == 0:
                if self.index < 0 and self.index > 3:
                    self.index = 0
                self.index = (self.index+1)%4
            else:
                if self.tempx > 0:
                    if self.index < 4 or self.index > 7:
                        self.index = 4
                    if self.index < 7:
                        self.index += 1
                elif self.tempx < 0:
                    if self.index < 8 or self.index > 11:
                        self.index = 8
                    if self.index < 11:
                        self.index += 1
                #print(self.tempx)
                #print(self.index)
        self.nimbusAngle = (self.nimbusAngle+1)%360
        nimbus = pygame.transform.smoothscale(self.nimbus, (384+sin(radians(self.nimbusAngle))*70, 384-sin(radians(self.nimbusAngle))*70))
        self.image=self.img[self.index]
        functions.drawImage(nimbus, self.rect.center, self.nimbusAngle, screen)
        functions.drawImage(self.image, self.rect.center, 270, screen)
        
    def update(self, screen, bullets, lasers, items, effects, backgrounds):
        set_value('boss_health',self.health)
        set_value('boss_maxhealth',self.maxhealth)
        set_value('boss_spellhealth',self.tospellhealth)
        #print(self.health/self.maxhealth)
        if self.wait:
            self.wait-=1
        if not get_value('plot') and not self.wait:
            self.lastFrame += 1
        if self.recovering and not self.wait:
            if self.recovering == 2:
                self.health = 10
                new_effect = effect.Health_Bar()
                new_effect.initial(self.maxhealth)
                get_value('boss_effect').add(new_effect)
                set_value('boss_health',self.health)
                self.recovering = True
            elif self.recovering > 1:
                self.recovering -= 1
            else:
                self.recover()
        if get_value('plot'):
            self.entering=False
        self.Change_Stage(items,bullets,backgrounds,effects)
        self.movement()
        set_value('boss_pos',self.rect.center)
        self.checkDistance()
        self.draw(screen)
        self.Attack(bullets,effects)
        
        
    def Change_Stage(self,items,bullets,backgrounds,effects):
        if (self.health <= self.tospellhealth and not self.recovering or self.times_lists[(self.cardNum-1)*2+self.ifSpell]-self.lastFrame/60<=0)and not self.ifSpell:
            for i in get_value('boss_effect'):
                if i.__class__.__name__ in ('Timer', 'SpellCard_Bonus'):
                    i.times = self.times_lists[(self.cardNum-1)*2+self.ifSpell]*60
            functions.showBackground(backgrounds, 'cirno')
            SoundEffect.play('spell_sound',0.5)
            self.spellFrame=-1
            self.ifSpell = True
            new_effect = effect.Spell_Name()
            new_effect.initial(self.spellName[self.cardNum-1])
            get_value('boss_effect').add(new_effect)
            set_value('ifSpell',True)
            self.gotoPosition(384*1.5/2,200,30)
            self.doKill(items,bullets,effects)
            self.drawSpellCardAttack(backgrounds,'cirno')
            self.lastFrame=1
        elif (self.health <= 0 or self.times_lists[(self.cardNum-1)*2+self.ifSpell]-self.lastFrame/60 <= 0) and self.ifSpell:
            for i in get_value('boss_effect'):
                if i.__class__.__name__ in ('Timer', 'SpellCard_Bonus'):
                    i.times = self.times_lists[(self.cardNum-1)*2+self.ifSpell]*60
            if self.cardNum == 3:
                set_value('waveNum',11)
                set_value('frame', 0)
                set_value('boss_alive',False)
                set_value('finish',True)
                self.kill()
            functions.showBackground(backgrounds, 'STAGE_2')
            SoundEffect.play('spellEnd_sound',0.5)
            self.doKill(items,bullets,effects)
            self.dropItem(items)
            self.cardNum += 1
            if self.cardNum==4:
                self.cardNum=1
            if self.cardNum == 2:
                self.gotoPosition(384*1.5/2,200,10)
            self.health = 10
            self.recovering=15
            set_value('show_health', False)
            self.maxhealth = 100000
            self.ifSpell = False
            set_value('ifSpell',False)
            self.lastFrame=1
            self.wait=60
            
        
    def Attack(self, bullets,effects):
        if get_value('plot') or self.entering:
            return
        if self.cardNum == 1:
            if not self.ifSpell:
                if len(get_value('boss_effect'))==1:
                    new_effect = effect.Timer()
                    new_effect.times = 30*60
                    get_value('boss_effect').add(new_effect)
                    new_effect = effect.SpellCard_Bonus()
                    get_value('boss_effect').add(new_effect)
                    self.recovering = 3
                    new_effect1 = effect.Boss_Attack_Effect()
                    effects.add(new_effect1)
                self.non_spell_test_5(bullets)
                if self.lastFrame % 150 == 0:
                    self.gotoPosition(randint(50, 576-50), randint(120, 240), 100)
                if self.moving and not self.entering:
                    if self.lastFrame%3==0:
                        self.non_spell_test(bullets)
            else:
                self.Spell_1(bullets,effects)
        elif self.cardNum == 2:
            if not self.ifSpell:
                self.non_spell_test_4(bullets)
            elif self.ifSpell and self.lastFrame > 100:
                self.Spell_2(bullets)
            elif self.ifSpell and self.lastFrame == 30:
                new_effect1 = effect.Boss_Attack_Effect()
                effects.add(new_effect1)
        elif self.cardNum == 3:
            if not self.ifSpell:
                if self.lastFrame % 150 == 0:
                    self.gotoPosition(randint(50, 576-50), randint(120, 240), 100)
                if not self.moving:
                    self.non_spell_test_6(bullets)
            else:
                if self.lastFrame % 100 == 0:
                    if self.rect.centerx < 288:
                        self.gotoPosition(self.rect.centerx+randint(50,100), randint(120, 240), 70)
                    else:
                        self.gotoPosition(self.rect.centerx-randint(50,100), randint(120, 240), 70)
                self.Spell_3(bullets)

    def Spell_1(self, bullets, effects):
        if self.lastFrame % 220 == 0:
            self.gotoPosition(randint(50, 576-50), randint(120, 240), 70)
        if not self.moving:
            if self.lastFrame % 100 == 30:
                new_effect1 = effect.Boss_Attack_Effect()
                effects.add(new_effect1)
            if self.lastFrame % 100 == 0:
                self.non_spell_test_2(bullets)
            if self.lastFrame % 8 == 0:
                self.non_spell_test_1(bullets)

    def Spell_2(self, bullets):
        #SoundEffect.play('kira_sound',0.2,0)
        self.a = (self.a+12*sin(radians(self.lastFrame)))%360
        new_bullet=bullet.Satsu_Bullet()
        new_bullet.initial(self.rect.centerx-100,self.rect.centery)
        new_bullet.loadColor('skyBlue')
        new_bullet.setSpeed(self.a+uniform(-1,1),7)
        bullets.add(new_bullet)
        new_bullet=bullet.Satsu_Bullet()
        new_bullet.initial(self.rect.centerx+100,self.rect.centery)
        new_bullet.loadColor('skyBlue')
        new_bullet.setSpeed(-self.a+uniform(-1,1)+180,7)
        bullets.add(new_bullet)
        if self.lastFrame % 100 in(0,20,40):
            SoundEffect.play('enemyShoot_sound1',0.35,True)
            new_bullet=bullet.Mid_Bullet()
            new_bullet.initial(self.rect.centerx+100,self.rect.centery)
            new_bullet.loadColor('blue')
            new_bullet.selfTarget(get_value('player_cx'), get_value('player_cy'), 3)
            bullets.add(new_bullet)
            new_bullet=bullet.Mid_Bullet()
            new_bullet.initial(self.rect.centerx-100,self.rect.centery)
            new_bullet.loadColor('blue')
            new_bullet.selfTarget(get_value('player_cx'), get_value('player_cy'), 3)
            bullets.add(new_bullet)
            

    def Spell_3(self, bullets):
        if not self.moving:
            if self.lastFrame % 20==0:
                new_bullet=bullet.Explode_Big_Star_Bullet()
                new_bullet.initial(self.rect.centerx,self.rect.centery)
                new_bullet.explodeFrame=100
                new_bullet.loadColor('blue')
                new_bullet.selfTarget(get_value('player_cx'), get_value('player_cy'), 7)
                angle = new_bullet.angle
                bullets.add(new_bullet)
                for i in range(-3,4):
                    if i == 0:
                        continue
                    new_bullet=bullet.Explode_Big_Star_Bullet()
                    new_bullet.initial(self.rect.centerx,self.rect.centery)
                    new_bullet.explodeFrame=1000
                    new_bullet.loadColor('blue')
                    new_bullet.setSpeed(angle+i*10, 7)
                    bullets.add(new_bullet)


    def non_spell_test(self,bullets):
        angle = 90+uniform(-5,5)*12
        for i in range(-2,3):
            new_bullet=bullet.Satsu_Bullet()
            new_bullet.initial(self.rect.centerx,self.rect.centery)
            new_bullet.setSpeed(angle+i*15,5+uniform(2,7))
            new_bullet.loadColor('skyBlue')
            bullets.add(new_bullet)

    def non_spell_test_1(self,bullets):
        self.fireangle1 += 10
        new_bullet=bullet.Explode_Big_Star_Bullet()
        new_bullet.initial(self.rect.centerx,self.rect.centery)
        new_bullet.explodeFrame=100
        new_bullet.setSpeed(90+self.fireangle1,10)
        new_bullet.loadColor('blue')
        bullets.add(new_bullet)

    def non_spell_test_2(self,bullets):
        for i in range(-30, 31):
            new_bullet=bullet.Satsu_Bullet()
            new_bullet.Locus_initial(self.rect.centerx,self.rect.centery,randint(-2,2),10,60)
            new_bullet.setSpeed(90+i*6+uniform(-1,1),5)
            new_bullet.loadColor('skyBlue')
            bullets.add(new_bullet)
            
    def non_spell_test_3(self,bullets):
        if self.lastFrame%2==0:
            new_bullet=bullet.Rain_Rice_Bullet()
            new_bullet.initial(randint(30,768-30),randint(100,520))
            new_bullet.stFrame=15
            new_bullet.rainFrame=60
            angle = randint(260,280)
            speed=randint(3,6)
            new_bullet.setSpeed(angle,speed)
            new_bullet.orgAngle=angle
            new_bullet.orgSpeed=speed
            new_bullet.loadColor('skyBlue')
            bullets.add(new_bullet)

    def non_spell_test_4(self,bullets):
        if self.lastFrame%4==0:
            new_bullet=bullet.Mid_Bullet()
            new_bullet.Bounce_initial(self.rect.centerx,self.rect.centery,2,1800)
            new_bullet.setSpeed(randint(60,120),7)
            new_bullet.loadColor('blue')
            bullets.add(new_bullet)

    def non_spell_test_5(self,bullets):
        if self.lastFrame%10==0:
            a=randint(0,30)
            x=randint(-20,20)
            y=randint(-20,20)
            for i in range(0,12):
                color = list(small_bullet_colorDict.keys())[choice([1,15])]
                angle=30*i+a
                for j in range(-2,3):
                    new_bullet = bullet.Satsu_Bullet()
                    new_bullet.initial(self.rect.centerx+x,self.rect.centery+y)
                    new_bullet.setSpeed(angle+j*3,5)
                    new_bullet.loadColor(color)
                    bullets.add(new_bullet)
                    
    def non_spell_test_6(self,bullets):
        if self.lastFrame%10==0:
            SoundEffect.play('enemyShoot_sound1',0.35,True)
            a=randint(0,45)
            for i in range(0,8):
                color = list(small_bullet_colorDict.keys())[4]
                angle=45*i+a
                for j in range(0,8):
                    new_bullet=bullet.Satsu_Bullet()
                    new_bullet.Circular_initial(self.rect.centerx,self.rect.centery,self.rect.centerx,self.rect.centery,40,j*45)
                    new_bullet.setSpeed(angle,5)
                    new_bullet.loadColor(color)
                    bullets.add(new_bullet)

        