import pygame
import background
import effect
import item
import math
import pytweening

from const import *
from random import *
from global_var import *
import SoundManager

def drawImage(image :pygame.Surface ,pos :list ,angle :float ,screen :pygame.Surface):
    image = pygame.transform.rotate(image, angle).convert_alpha()
    rect = image.get_rect(center=pos)
    screen.blit(image, rect)
    
def sin(angle :float) -> float:
    return math.sin(math.radians(angle))

def cos(angle :float) -> float:
    return math.cos(math.radians(angle))

def sqrt(n :float) -> float:
    return math.sqrt(n)

def dist(p: list, q: list) -> float:
    return math.sqrt((p[0]-q[0])**2+(p[1]-q[1])**2)

def get_target_angle(p :list, q :list) -> float:
    dx = q[0] - p[0]
    dy = q[1] - p[1]
    angle = math.degrees(math.atan2(dy, dx))
    return angle

def get_speed_in_angle(speed :float, angle :float) -> tuple:
    speedx = cos(angle)*speed
    speedy = sin(angle)*speed
    return (round(speedx, 10), round(speedy, 10))

def get_speed_from_components(speedx :float, speedy :float) -> float:
    return sqrt(speedx*speedx+speedy*speedy)

def get_quadrant_in_angle(angle :float) -> int:
    if angle >= 0 and angle <= 90:
        return 1
    if angle >= 90 and angle <= 180:
        return 2
    if angle >= -180 and angle <= -90:
        return 3
    if angle >= -90 and angle <= 0:
        return 4

def acc(start :float, end :float, t :float, max_t :float) -> float:
    return start+(end-start)*pytweening.easeInQuad(t/max_t)

def dcc(start :float, end :float, t :float, max_t :float) -> float:
    return start+(end-start)*pytweening.easeOutQuad(t/max_t)

def acc_dcc(start :float, end :float, t :float, max_t :float) -> float:
    return start+(end-start)*pytweening.easeInOutQuad(t/max_t)

def linear(start :float, end :float, t :float, max_t :float) -> float:
    return start+(end-start)*(t/max_t)

def bezier_equation(t :float, start :float, points :list, end :float) -> float:
    pow = len(points)+1
    ans = (1-t)**pow * start + t**pow * end
    for i in range(len(points)):
        ans += (1-t)*t*points[i]
    return ans
    
def get_rainbow_color(angle :float) -> tuple:
    r = int((math.sin(angle) + 1) * 127.5)
    g = int((math.sin(angle + 2) + 1) * 127.5)
    b = int((math.sin(angle + 4) + 1) * 127.5)
    return (r, g, b)

def lerp_color(c1 :tuple, c2 :tuple, t :float) -> tuple:
    return (c1[0]+(c2[0]-c1[0])*t, c1[1]+(c2[1]-c1[1])*t, c1[2]+(c2[2]-c1[2])*t)

def dropItem(cx, cy, type, num):
    for _ in range(num):
        dx=random()*120-60
        dy=random()*-120
        x=cx+dx
        y=cy+dy
        if x<8:
            x=8
        if x>440:
            x=440
        new_item = item.item(type,x,y)
        get_value('items').add(new_item)

def initialize():
    set_value('score', 0)
    set_value('enemypos', (0, 0, 10000))
    set_value('waveNum', 0)
    set_value('grazeNum', 0)
    set_value('frame', -100)
    set_value('maximum_score', 10000)
    set_value('score', 0)
    set_value('hi_score', 0)
    set_value('fps', 60.0)
    set_value('score_item_count', 0)
    set_value('score_item_bound', 10)

def RESET(player):
    player.life = 40
    player.power = 400
    player.boom = 20
    player.score = 0
    player.isAlive = True
    set_value('maximum_score', 10000)
    set_value('score', 0)
    set_value('score_item_count', 0)
    set_value('score_item_bound', 10)
    
def EXIT(player_bullets, player_lasers, enemy_bullets, enemy_lasers, enemies, floatguns, items, background, effects, wave, STAGE, screen):
    player_bullets.empty()
    player_lasers.empty()
    enemy_bullets.empty()
    enemy_lasers.empty()
    enemies.empty()
    floatguns.empty()
    items.empty()
    background.empty()
    effects.empty()
    wave.empty()
    get_value('boss_effect').empty()
    set_value('boss_alive',False)
    set_value('show_health',False)
    set_value('screen_shaking',False)
    set_value('booming',False)
    set_value('finish',0)
    STAGE.fill((0,0,0,0))
    screen.blit(STAGE, (30, 30))

magnitude=1.5

#自機判定
def missDetect(player, lasers, enemies, enemy_bullet, effects, wave, items):
    px,py = player.x, player.y
    gethit = False
    for bullet in enemy_bullet:
        distance = dist((px, py), (bullet.x, bullet.y))
        if bullet.graze and (distance - bullet.rect.w/2 <= 12*magnitude or distance - bullet.rect.h/2 <= 12*magnitude):
            bullet.graze = False
            if not get_value('grazing'):
                SoundManager.play('graze_sound',0.5,True)
                set_value('grazing',True)
                new_effect = effect.Particle((230,230,230,200),(player.x,player.y),4)
                effects.add(new_effect)
            grazeNum=get_value('grazeNum')+1
            set_value('grazeNum',grazeNum)
        if (distance - bullet.w/2 <= 1 or distance-bullet.h/2 <= 1):
            if not player.immuneFrame and not get_value('Debug'):
                player.immuneFrame = 200
                SoundManager.play('miss_sound',0.5,True)
                gethit = True
            if bullet.destroyable:
                bullet.kill()
    if not player.immuneFrame and not get_value('Debug'):
        for enemy in enemies:
            distance = dist((px, py), (enemy.x, enemy.y))
            if (distance - enemy.rect.w/2 <= 1 or distance-enemy.rect.h/2 <= 1):
                player.immuneFrame = 200
                SoundManager.play('miss_sound',0.5,True)
                gethit = True
                break
    if gethit:
        for i in get_value('boss_effect'):
            if i.__class__.__name__ == 'SpellCardBonus':
                i.failed = True
                break
        player.IDLE()
        player.life -= 10
        player.gethit = True
        if player.__class__.__name__ == 'REIMU':
            player.power -= 100
        elif player.__class__.__name__ == 'MARISA':
            player.power -= 50
            lasers.empty()
        new_wave=effect.wave(player.x, player.y, 600)
        wave.add(new_wave)
        for i in range(-2,3):
            new_item = item.item(0, 192+i*25, 325+abs(i*10))
            items.add(new_item)
        

def hitEnemy(enemy, player, player_bullets, effects):
    enemy_hit = pygame.sprite.groupcollide(enemy, player_bullets, 0, 0)
    bullet_hit = pygame.sprite.groupcollide(player_bullets, enemy, 0, 0)
    if bullet_hit:
        SoundManager.play('hit_sound1',0.2,True)
    for sp in enemy_hit:
        single_hit = pygame.sprite.spritecollide(sp, bullet_hit, False)
        sp.gethit = True
        if sp.dp==1:
            continue
        for bullet in single_hit:
            if sp.invincible:
                continue
            if bullet.__class__.__name__ == 'Dream_Seal' and bullet.cancelable:
                sp.hp -= 1000*(1-sp.dp)
            else:
                sp.hp -= bullet.damage*(1-sp.dp)
            if sp.hp:
                new_effect = effect.Damage_Show_Text(bullet.damage, (bullet.x,bullet.y))
                effects.add(new_effect)
            if bullet.__class__.__name__ != 'Dream_Seal' and bullet.__class__.__name__ != 'Master_Spark':
                break

    for bullet in bullet_hit:
        if player.__class__.__name__ == 'REIMU':
            if bullet.__class__.__name__ == 'reimuMainSatsu':
                new_effect = effect.Reimu_main_fire_effect(bullet.x, bullet.y)
                effects.add(new_effect)
            elif bullet.__class__.__name__ == 'reimuTargetSatsu':
                new_effect = effect.Reimu_target_fire_effect(bullet.x, bullet.y, bullet.rot)
                effects.add(new_effect)
            elif bullet.__class__.__name__ == 'reimuShiftSatsu':
                new_effect = effect.Reimu_shift_fire_effect(bullet.x, bullet.y)
                effects.add(new_effect)
            elif bullet.__class__.__name__ == 'Dream_Seal' and bullet.cancelable:
                bullet.doKill()
                
        elif player.__class__.__name__ == 'MARISA':
            if bullet.__class__.__name__ == 'marisaMainBullet':
                new_effect = effect.Marisa_main_fire_effect(bullet.x, bullet.y)
                effects.add(new_effect)
            elif bullet.__class__.__name__ == 'marisaMissile':
                new_effect = effect.Marisa_missile_effect(bullet.x, bullet.y)
                effects.add(new_effect)
        
        player.score+=10
        if bullet.__class__.__name__ not in ('Master_Spark', 'Dream_Seal'):
            bullet.kill()
            
def laser_collision(enemy, player, lasers, effects):
    for self in lasers:
        self.hit=False
        height=256*3
        sp=None
        for i in enemy:
            #terrible equation :)
            x=self.x+(i.x-self.x)*cos(-10*self.index)-(i.y-self.y)*sin(-10*self.index)
            y=self.y+(i.x-self.x)*sin(-10*self.index)+(i.y-self.y)*cos(-10*self.index)
            if y-i.rect.height//2>self.y or y+i.rect.height//2<self.y-self.length:
                continue
            if x-i.rect.width//2>self.x+12 or x+i.rect.width//2<self.x-12:
                continue
            if self.y-y<height:
                sp=i
                height=max(0,self.y-y)
            self.hit=True
            
        if sp is not None and not sp.invincible:
            sp.gethit=True
            player.score += 5
            sp.hp -= self.damage*sp.dp
            new_effect = effect.Particle((randint(100,205),randint(100,205),randint(100,205)),(sp.x,sp.y),randint(2,3))
            effects.add(new_effect)
            if sp.dp!=0:
                new_effect = effect.Damage_Show_Text(self.damage, (sp.x,sp.y))
                effects.add(new_effect)
        self.maxlength = height
        

def showBackground(backgrounds, type, screen):
    backgrounds.empty()
    if type == 'STAGE_1':
        for i in range(-2, 3):
            for j in range(0, 3):
                back = background.Background()
                back.initialize(360*j-240, 0+i*360)
                backgrounds.add(back)
    elif type == 'reitsu':
        for i in range(-1, 4):
            for j in range(0, 5):
                back = background.Stage_1_SP_BG(225*j, i*225)
                backgrounds.add(back)
        back = background.DarkMask(screen, 100)
        backgrounds.add(back)
        back = background.DarkMask(screen, -100)
        backgrounds.add(back)
    elif type == 'STAGE_2':
        back=background.Lake_Background()
        backgrounds.add(back)
    elif type == 'cirno':
        a = [-2,2,-2]
        for i in range(0, 3):
            for j in range(-2, 3):
                back = background.Cirno_Background(j*260, i*260, a[i])
                backgrounds.add(back)
        back = background.DarkMask(screen, 100)
        backgrounds.add(back)
    
