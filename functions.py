import pygame
import background
import effect
import item

from const import *
from math import *
from random import *
from global_var import *
import SoundEffect

def returnScoreFormat(score):
    string = str(score)
    scoreFinal=''
    cnt=0
    for i in range(len(string)-1, -1, -1):
        scoreFinal = string[i] + scoreFinal
        cnt+=1
        if cnt%3==0 and i != 0:
            scoreFinal= ',' + scoreFinal
    return scoreFinal

def drawImage(image,pos,angle,screen):
    image = pygame.transform.rotate(image, -angle-90).convert_alpha()
    rect = image.get_rect(center=pos)
    screen.blit(image, rect)
    
def get_rainbow_color(angle):
    r = int((sin(angle) + 1) * 127.5)
    g = int((sin(angle + 2) + 1) * 127.5)
    b = int((sin(angle + 4) + 1) * 127.5)
    return (r, g, b)

def initialize():
    set_value('player_HP', 4)
    set_value('player_Boom', 2)
    set_value('shift_down', False)
    set_value('player_attack', False)
    set_value('score', 0)
    set_value('immune', False)
    set_value('immune_time', 0)
    set_value('select', 1)
    set_value('show_dialogue', False)
    set_value('pause', False)
    set_value('player_firelevel', 1)
    set_value('player_alive', True)
    set_value('enemypos', (0, 0, 10000))
    set_value('waveNum', 0)
    set_value('frame', -100)
    set_value('fps', 60.0)
    set_value('maximum_score', 10000)
    set_value('score', 0)
    set_value('hi_score', 1000000)
    set_value('score_item_count', 0)
    set_value('score_item_bound', 10)

def RESET(player):
    player.life = 4
    player.power = 400
    player.boom = 2
    player.score = 0
    set_value('player_Boom', 2)
    set_value('shift_down', False)
    set_value('player_attack', False)
    set_value('player_alive', True)
    set_value('pause', False)
    set_value('maximum_score', 10000)
    set_value('score', 0)
    set_value('score_item_count', 0)
    set_value('score_item_bound', 10)
    
def EXIT(player_bullets, player_lasers, enemy_bullets, enemy_lasers, enemies, floatguns, items, background, effects, wave, STAGE, screen, plot):
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
    set_value('plot',False)
    set_value('finish',0)
    STAGE.fill((0,0,0,0))
    screen.blit(STAGE, (30, 30))

magnitude=1.5
    
def clearBullets(bullets,effects):
    for b in bullets:
        new_vanish = effect.bulletVanish()
        new_vanish.initial(b.image, b.rect.center, b.angle)
        effects.add(new_vanish)
        b.kill()

from pygame.math import Vector2
#自机受击
def missDetect(player, lasers, enemy, enemy_bullet, effects, wave, items):
    px,py = player.tx, player.ty
    gethit = False
    for bullet in enemy_bullet:
        distance = Vector2(px,py).distance_to(Vector2(bullet.tx,bullet.ty))
        if bullet.graze and (distance - bullet.w/2 <= 12*magnitude or distance - bullet.h/2 <= 12*magnitude):
            bullet.graze = False
            if not get_value('grazing'):
                SoundEffect.play('graze_sound',0.5,True)
                set_value('grazing',True)
                new_effect = effect.Particle((230,230,230,200),(player.tx,player.ty),4)
                effects.add(new_effect)
            grazeNum=get_value('grazeNum')+1
            set_value('grazeNum',grazeNum)
        if (distance - bullet.w/2 <= 1 or distance-bullet.h/2 <= 1):
            if not player.immuneFrame:
                player.immuneFrame = 200
                SoundEffect.play('miss_sound',0.5,True)
                gethit = True
            bullet.kill()
    if gethit:
        player.BACK()
        player.life -= 1
        player.gethit = True
        #set_value('pl_gethit',1)
        if player.__class__.__name__ == 'REIMU':
            player.power -= 100
        elif player.__class__.__name__ == 'MARISA':
            player.power -= 100
            lasers.empty()
            #print(len(lasers))
        new_wave=effect.wave()
        new_wave.initial([player.tx,player.ty], enemy_bullet)
        wave.add(new_wave)
        for i in range(-2,3):
            new_item = item.item()
            new_item.type = 0
            new_item.initial((192+i*25)*magnitude, (325+abs(i*10))*magnitude)
            items.add(new_item)
        

def hitEnemy(enemy, player, player_bullets, effects):
    enemy_hit = pygame.sprite.groupcollide(enemy, player_bullets, 0, 0)
    bullet_hit = pygame.sprite.groupcollide(player_bullets, enemy, 0, 0)
    if bullet_hit:
        SoundEffect.play('hit_sound1',0.2,True)
    for sp in enemy_hit:
        single_hit = pygame.sprite.spritecollide(sp, bullet_hit, False)
        sp.gethit=True
        for bullet in single_hit:
            if (sp.__class__.__name__ == 'Cirno' or sp.__class__.__name__ == 'Reitsu') and (sp.wait or sp.recovering):
                break
            if bullet.__class__.__name__ == 'Dream_Seal' and bullet.cancelable:
                if (sp.__class__.__name__ == 'Cirno' or sp.__class__.__name__ == 'Reitsu') and sp.ifSpell:
                    sp.health -= 5000/7
                elif (sp.__class__.__name__ == 'Cirno' or sp.__class__.__name__ == 'Reitsu'):
                    sp.health = max(sp.health-5000,sp.tospellhealth)
                else:
                    sp.health -= 5000
                bullet.doKill()
            else:
                if (sp.__class__.__name__ == 'Cirno' or sp.__class__.__name__ == 'Reitsu') and sp.ifSpell:
                    sp.health -= bullet.damage/7
                else:
                    sp.health -= bullet.damage

    for bullet in bullet_hit:
        if player.__class__.__name__ == 'REIMU':
            if bullet.__class__.__name__ == 'reimuMainSatsu':
                new_effect = effect.Reimu_main_fire_effect()
                new_effect.initial(bullet.rect.centerx,bullet.rect.centery)
                effects.add(new_effect)
            elif bullet.__class__.__name__ == 'reimuTargetSatsu':
                new_effect = effect.Reimu_target_fire_effect()
                new_effect.initial(bullet.rect.centerx,bullet.rect.centery)
                effects.add(new_effect)
            elif bullet.__class__.__name__ == 'reimuShiftSatsu':
                new_effect = effect.Reimu_shift_fire_effect()
                new_effect.initial(bullet.rect.centerx,bullet.rect.centery)
                effects.add(new_effect)
            elif bullet.__class__.__name__ == 'Dream_Seal' and bullet.cancelable:
                bullet.doKill()
                
        elif player.__class__.__name__ == 'MARISA':
            if bullet.__class__.__name__ == 'marisaMainBullet':
                new_effect = effect.Marisa_main_fire_effect()
                new_effect.initial(bullet.rect.center)
                effects.add(new_effect)
            elif bullet.__class__.__name__ == 'marisaMissile':
                new_effect = effect.Marisa_missile_effect()
                new_effect.initial(bullet.rect.center)
                effects.add(new_effect)
        player.score+=10
        if bullet.__class__.__name__ != 'Master_Spark' and bullet.__class__.__name__ != 'Dream_Seal' and bullet.__class__.__name__ != 'marisaLaser':
            bullet.kill()
            
def laser_collision(enemy, lasers, effects):
    for self in lasers:
        self.hit=False
        height=384*3
        sp=None
        for i in enemy:
            #terrible equation :)
            x=self.tx+(i.rect.centerx-self.tx)*cos(radians(-10*self.index))-(i.rect.centery-self.ty)*sin(radians(-10*self.index))
            y=self.ty+(i.rect.centerx-self.tx)*sin(radians(-10*self.index))+(i.rect.centery-self.ty)*cos(radians(-10*self.index))
            #print(x,i.rect.centerx,y,i.rect.centery,self.tx,self.ty)
            if y-i.rect.height//2>self.ty or y+i.rect.height//2<self.ty-self.length:
                continue
            if x-i.rect.width//2>self.tx+12 or x+i.rect.width//2<self.tx-12:
                continue
            if self.ty-y<height:
                sp=i
                height=max(0,self.ty-y)
            self.hit=True
            
        if sp is not None:
            sp.gethit=True
            if (sp.__class__.__name__ == 'Cirno' or sp.__class__.__name__ == 'Reitsu') and sp.ifSpell:
                sp.health -= self.damage/7
            else:
                sp.health -= self.damage
            for i in range(0,3):
                new_effect = effect.Particle((randint(100,205),randint(100,205),randint(100,205),200),(sp.tx,sp.ty),randint(3,6))
                effects.add(new_effect)
        self.maxlength = height
        

def showBackground(backgrounds, type):
    backgrounds.empty()
    if type == 'STAGE_1':
        for i in range(-2, 3):
            for j in range(0, 3):
                back = background.Background()
                back.initialize(360*j-240, 0+i*360)
                backgrounds.add(back)
    elif type == 'reitsu':
        return
    elif type == 'STAGE_2':
        back=background.Lake_Background()
        backgrounds.add(back)
    elif type == 'cirno':
        for i in range(-1, 5):
            for j in range(0, 3):
                back = background.Cirno_Background()
                back.initialize(0+j*260, 0+i*260)
                backgrounds.add(back)
    
