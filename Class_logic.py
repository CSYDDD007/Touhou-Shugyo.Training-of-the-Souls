import pygame
import boss
import enemy
import functions
import effect
import bullet

from const import *
from math import *
from random import *
from global_var import *

enemy_color=['red','yellow','green','blue']
class enemy_begin_stage_1():
    def __init__(self):
        self.time=-1
    
    def update(self,enemies):
        self.time+=1
        self.Small_YinYangYu(enemies)
    
    def Small_YinYangYu(self, enemies):
        if self.time % 14 == 0 and self.time < 280-14*3:
            new_enemy = enemy.Small_YinYangYu_Begin_Stage_1()
            new_enemy.initial((384+20)*1.5+randint(0,120), 20+self.time*2,'red')
            new_enemy.setSpeed(180, 10)
            enemies.add(new_enemy)
        elif self.time % 14 == 0 and self.time >= 280-14*3:
            new_enemy = enemy.Small_YinYangYu_Begin_Stage_1()
            new_enemy.initial(-20*1.5-randint(0,120), 20+(self.time-280)*2,'blue')
            new_enemy.setSpeed(0, 10)
            enemies.add(new_enemy)

class enemy_wave_1_stage_1():
    def __init__(self):
        self.time=-1
        
    def update(self,enemies):
        self.time += 1
        self.Fairy(enemies)
        self.Sunflower_Fairy(enemies)
        
    def Sunflower_Fairy(self,enemies):
        if self.time==1:
            new_enemy = enemy.Flower_Fairy_Wave1_Stage_1()
            new_enemy.initial(384*1.5/2, -50)
            new_enemy.setSpeed(90,10)
            enemies.add(new_enemy)
            
    def Fairy(self,enemies):
        if self.time%15==0 and self.time > 50 and self.time < 450:
            new_enemy = enemy.Fairy_Wave1_Stage_1()
            new_enemy.initial(uniform(50*1.5,(384-50)*1.5), -30,'yellow')
            new_enemy.setSpeed(90,8)
            new_enemy.colorNum=randint(0,3)
            enemies.add(new_enemy)

class enemy_wave_2_stage_1():
    def __init__(self):
        self.time=-1
        
    def Small_YinYangYu(self, enemies):
        self.time+=1
        if self.time % 28 == 0:
            new_enemy = enemy.Small_YinYangYu_Right_Wave2_Stage_1()
            new_enemy.initial((384+10)*1.5, 30,'red')
            new_enemy.setSpeed(180, 7)
            enemies.add(new_enemy)
        elif self.time % 28 == 14:
            new_enemy = enemy.Small_YinYangYu_Left_Wave2_Stage_1()
            new_enemy.initial(-10*1.5, 30,'blue')
            new_enemy.setSpeed(0, 7)
            enemies.add(new_enemy)

class enemy_wave_3_stage_1():
    def __init__(self):
        self.time=-1
        
    def Ghost(self, enemies):
        self.time+=1
        if self.time % 10 == 0:
            new_enemy = enemy.Ghost_Wave3_Stage_1()
            new_enemy.initial(randint(22,553), -10, 'blue', 1)
            new_enemy.setSpeed(90, 3)
            enemies.add(new_enemy)
        elif self.time % 10 == 5:
            new_enemy = enemy.Ghost_Wave3_Stage_1()
            new_enemy.initial(randint(22,553), -10, 'red', 0)
            new_enemy.setSpeed(90, 3)
            enemies.add(new_enemy)

class enemy_wave_4_stage_1():
    def __init__(self):
        self.time=-1
        
    def update(self,enemies):
        self.time += 1
        self.sunflower_fairy(enemies) 
        self.fairy(enemies)
        
    def sunflower_fairy(self, enemies):
        if self.time % 100 == 0:
            p = randint(96, 288)
            new_enemy = enemy.flower_fairy_test_Stage_1()
            new_enemy.initial(p, -20)
            new_enemy.setSpeed(90, 5)
            #new_enemy.pale = True
            enemies.add(new_enemy)
            new_enemy = enemy.flower_fairy_test_Stage_1()
            new_enemy.initial(384*1.5-p, -20)
            new_enemy.setSpeed(90, 5)
            new_enemy.pale = True
            enemies.add(new_enemy)
            
    def fairy(self, enemies):
        if self.time % 100 == 0:
            new_enemy=enemy.fairy_test_Stage_1()
            new_enemy.initial(-10*1.5,30,'yellow')
            new_enemy.setSpeed(10, 3)
            enemies.add(new_enemy)
            new_enemy=enemy.fairy_test_Stage_1()
            new_enemy.initial((384+10)*1.5,30,'green')
            new_enemy.setSpeed(170, 3)
            enemies.add(new_enemy)

class enemy_wave_5_stage_1():
    def __init__(self):
        self.time=-1
        
    def yinyangyu(self,enemies):
        self.time+=1
        if self.time%50==0:
            new_enemy = enemy.YinYangYu_Wave5_Stage_1()
            new_enemy.initial(-10*1.5, randint(0,30),'red')
            new_enemy.setSpeed(45,5)
            enemies.add(new_enemy)
        elif self.time%50==25:
            new_enemy = enemy.YinYangYu_Wave5_Stage_1()
            new_enemy.initial((384+10)*1.5, randint(0,30),'blue')
            new_enemy.setSpeed(135,5)
            enemies.add(new_enemy)

class enemy_wave_6_stage_1():
    def __init__(self):
        self.time=-1
        
    def kedama(self,enemies):
        self.time+=1
        if self.time%13==0:
            new_enemy=enemy.Kedama_Wave6_Stage_1()
            new_enemy.initial(randint(37,538),0,enemy_color[randint(0,3)])
            new_enemy.setSpeed(randint(80,100),randint(5,7))
            enemies.add(new_enemy)

class enemy_wave_7_stage_1():
    def __init__(self):
        self.time=-1

    def update(self,enemies):
        self.time+=1
        self.mid_fairy(enemies)
        self.sp_fairy(enemies)

    def sp_fairy(self,enemies):
        if self.time%25==0:
            new_enemy=enemy.Sp_Fairy_Wave7_Stage_1()
            new_enemy.initial(randint(37,538),0,'red')
            new_enemy.setSpeed(90,10)
            enemies.add(new_enemy)

    def mid_fairy(self,enemies):
        if self.time%200==0:
            for i in range(-2,3):
                new_enemy=enemy.Mid_Fairy_Wave7_Stage_1()
                new_enemy.initial(i*100+384*1.5/2,-20,'red')
                new_enemy.setSpeed(90,10)
                enemies.add(new_enemy)

class BOSS_stage_1():
    def __init__(self):
        self.time=1
    def boss_reitsu(self,enemies):
        new_enemy = boss.Reitsu()
        new_enemy.initial(1000, -600)
        new_enemy.gotoPosition(384, 150, 180)
        new_enemy.wait=180
        enemies.add(new_enemy)

class stagecontroller_stage_1():
    def __init__(self,node_lists=[]):
        self.E_Begin = enemy_begin_stage_1()
        self.Wave_1 = enemy_wave_1_stage_1()
        self.Wave_2 = enemy_wave_2_stage_1()
        self.Wave_3 = enemy_wave_3_stage_1()
        self.Wave_4 = enemy_wave_4_stage_1()
        self.Wave_5 = enemy_wave_5_stage_1()
        self.Wave_6 = enemy_wave_6_stage_1()
        self.Wave_7 = enemy_wave_7_stage_1()
        self.BOSS = BOSS_stage_1()

    def update(self, enemies, bullets, effects, backgrounds, frame):
        waveNum = get_value('waveNum')
        if waveNum==0:
            if frame == -99:
                functions.showBackground(backgrounds, 'STAGE_1')
                pygame.mixer.music.stop()
                pygame.mixer.music.load("resource/BGM/As the Normal Days.mp3")
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.7)
                set_value('waveNum',8)
            elif frame>=1 and frame<=560-14*6:
                self.E_Begin.update(enemies)
            elif frame>560-14*6 and len(enemies)==0:
                set_value('waveNum', waveNum+0.5)
                set_value('frame', 0)
                functions.clearBullets(bullets, effects)
        elif waveNum==0.5:
            if frame == 1:
                new_effect=effect.Stage_Begin_Surface()
                new_effect.initial(1)
                get_value('boss_effect').add(new_effect)
            elif frame>280:
                set_value('waveNum', 1)
                set_value('frame', 0)
        elif waveNum==1:
            if frame >= 1 and frame <= 500:
                self.Wave_1.update(enemies)
            elif frame > 550 and len(enemies)==0:
                set_value('waveNum', waveNum+1)
                set_value('frame', 0)
                functions.clearBullets(bullets, effects)
        elif waveNum==2:
            if frame >= 1 and frame <= 500:
                self.Wave_2.Small_YinYangYu(enemies)
            elif frame > 550 and len(enemies)==0:
                set_value('waveNum', waveNum+1)
                set_value('frame', 0)
                functions.clearBullets(bullets, effects)
        elif waveNum==3:
            if frame%200 >= 1 and frame%200 <= 100:
                self.Wave_3.Ghost(enemies)
            elif frame > 550 and len(enemies)==0:
                set_value('waveNum', waveNum+1)
                set_value('frame', 0)
                functions.clearBullets(bullets, effects)
        elif waveNum==4:
            if frame >= 1 and frame <= 500:
                self.Wave_4.update(enemies)
            elif frame > 550 and len(enemies)==0:
                set_value('waveNum', waveNum+1)
                set_value('frame', 0)
                functions.clearBullets(bullets, effects)
        elif waveNum==5:
            if frame >= 1 and frame <= 500:
                self.Wave_5.yinyangyu(enemies)
            elif frame > 550 and len(enemies)==0:
                set_value('waveNum', waveNum+1)
                set_value('frame', 0)
                functions.clearBullets(bullets, effects)
        elif waveNum==6:
            if frame >= 1 and frame <= 500:
                self.Wave_6.kedama(enemies)
            elif frame > 550 and len(enemies)==0:
                set_value('waveNum', waveNum+1)
                set_value('frame', 0)
                functions.clearBullets(bullets, effects)
        elif waveNum==7:
            if frame >= 1 and frame <= 500:
                self.Wave_7.update(enemies)
            elif frame > 550 and len(enemies)==0:
                set_value('waveNum', waveNum+1)
                set_value('frame', 0)
                functions.clearBullets(bullets, effects)
        elif waveNum==8:
            if frame == 1:
                set_value('boss_alive',True)
                self.BOSS.boss_reitsu(enemies)
            elif frame==180:
                set_value('waveNum', waveNum+1)
                set_value('frame', 0)
        elif waveNum==9:
            if frame == 1:
                #set_value('waveNum', waveNum+1)
                #set_value('frame', 0)
                set_value('plot',True)
        elif waveNum==10:
            if frame == 1:
                pygame.mixer.music.stop()
                pygame.mixer.music.load("resource/BGM/04. Tomboyish Girl in Love.mp3")
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(1)
        elif waveNum==11:
            if frame == 360:
                set_value('stage_Num',2)
                set_value('change',True)

class enemy_begin_stage_2():
    def __init__(self):
        self.time=-1
        
    def Fairy(self, enemies):
        self.time +=1
        if self.time % 30 == 0 and self.time < 360:
            new_enemy=enemy.Fairy_Begin_Right_Stage_1()
            new_enemy.initial(576+48,60+randint(-50,50),'blue')
            new_enemy.setSpeed(120, 4)
            enemies.add(new_enemy)
        if self.time % 30 == 15 and self.time < 360:
            new_enemy=enemy.Fairy_Begin_Left_Stage_1()
            new_enemy.initial(-48,60+randint(-50,50),'red')
            new_enemy.setSpeed(60, 4)
            enemies.add(new_enemy)
        if self.time % 30 == 0 and self.time >= 360:
            new_enemy=enemy.Fairy_Begin_Right_Stage_1()
            new_enemy.initial(576+48,60+randint(-50,50),'yellow')
            new_enemy.setSpeed(120, 4)
            enemies.add(new_enemy)
        if self.time % 30 == 15 and self.time >= 360:
            new_enemy=enemy.Fairy_Begin_Left_Stage_1()
            new_enemy.initial(-48,60+randint(-50,50),'green')
            new_enemy.setSpeed(60, 4)
            enemies.add(new_enemy)

class enemy_wave_1_stage_2():
    def __init__(self):
        self.time=-1
        
    def update(self,enemies):
        self.time += 1
        self.Fairy(enemies)
        self.Sunflower_Fairy(enemies)
        
    def Sunflower_Fairy(self,enemies):
        if self.time==1:
            new_enemy = enemy.Flower_Fairy_Wave1_Stage_1()
            new_enemy.initial(384, -50)
            new_enemy.setSpeed(90,10)
            enemies.add(new_enemy)
            
    def Fairy(self,enemies):
        if self.time%15==0 and self.time > 50 and self.time < 450:
            new_enemy = enemy.Fairy_Wave1_Stage_1()
            new_enemy.initial(randint(50,718), -30,'yellow')
            new_enemy.setSpeed(90,8)
            new_enemy.colorNum=randint(0,3)
            enemies.add(new_enemy)

class enemy_wave_2_stage_2():
    def __init__(self):
        self.time=-1

class enemy_wave_3_stage_2():
    def __init__(self):
        self.time=-1

class enemy_wave_4_stage_2():
    def __init__(self):
        self.time=-1

class enemy_wave_5_stage_2():
    def __init__(self):
        self.time=-1

class enemy_wave_6_stage_2():
    def __init__(self):
        self.time=-1

class BOSS_stage_2():
    def __init__(self):
        self.time=1
    def boss_cirno(self, enemies):
        new_enemy = boss.Cirno()
        new_enemy.initial(1000, -600)
        new_enemy.gotoPosition(288, 150, 180)
        new_enemy.wait=180
        enemies.add(new_enemy)

class stagecontroller_stage_2():
    def __init__(self,node_lists=[]):
        self.E_Begin = enemy_begin_stage_2()
        self.Wave_1 = enemy_wave_1_stage_1()
        self.Wave_2 = enemy_wave_2_stage_1()
        self.Wave_3 = enemy_wave_3_stage_1()
        self.Wave_4 = enemy_wave_4_stage_1()
        self.Wave_5 = enemy_wave_5_stage_1()
        self.Wave_6 = enemy_wave_6_stage_1()
        self.Wave_7 = enemy_wave_7_stage_1()
        self.BOSS = BOSS_stage_2()

    def update(self, enemies, bullets, effects, backgrounds, frame):
        waveNum = get_value('waveNum')
        if waveNum==0:
            if frame == -99:
                functions.showBackground(backgrounds, 'STAGE_2')
                pygame.mixer.music.stop()
                pygame.mixer.music.load("resource/BGM/04. Lunate Elf.mp3")
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.7)
                set_value('waveNum', 8)
            elif frame>=1 and frame<=720:
                self.E_Begin.Fairy(enemies)
            elif frame>720 and len(enemies)==0:
                set_value('waveNum', waveNum+0.5)
                set_value('frame', 0)
                functions.clearBullets(bullets, effects)
        elif waveNum==0.5:
            if frame == 1:
                new_effect=effect.Stage_Begin_Surface()
                new_effect.initial(2)
                effects.add(new_effect)
            elif frame>280:
                set_value('waveNum', waveNum+0.5)
                set_value('frame', 0)
        elif waveNum==1:
            if frame >= 1 and frame <= 500:
                self.Wave_1.update(enemies)
            elif frame > 550 and len(enemies)==0:
                set_value('waveNum', waveNum+1)
                set_value('frame', 0)
                functions.clearBullets(bullets, effects)
        elif waveNum==2:
            if frame >= 1 and frame <= 500:
                self.Wave_2.Small_YinYangYu(enemies)
            elif frame > 550 and len(enemies)==0:
                set_value('waveNum', waveNum+1)
                set_value('frame', 0)
                functions.clearBullets(bullets, effects)
        elif waveNum==3:
            if frame >= 1 and frame <= 100 or frame >= 300 and frame <= 400:
                self.Wave_3.Ghost(enemies)
            elif frame > 550 and len(enemies)==0:
                set_value('waveNum', waveNum+1)
                set_value('frame', 0)
                functions.clearBullets(bullets, effects)
        elif waveNum==4:
            if frame >= 1 and frame <= 500:
                self.Wave_4.update(enemies)
            elif frame > 550 and len(enemies)==0:
                set_value('waveNum', waveNum+1)
                set_value('frame', 0)
                functions.clearBullets(bullets, effects)
        elif waveNum==5:
            if frame >= 1 and frame <= 500:
                self.Wave_5.yinyangyu(enemies)
            elif frame > 550 and len(enemies)==0:
                set_value('waveNum', waveNum+1)
                set_value('frame', 0)
                functions.clearBullets(bullets, effects)
        elif waveNum==6:
            if frame >= 1 and frame <= 500:
                self.Wave_6.kedama(enemies)
            elif frame > 550 and len(enemies)==0:
                set_value('waveNum', waveNum+1)
                set_value('frame', 0)
                functions.clearBullets(bullets, effects)
        elif waveNum==7:
            if frame >= 1 and frame <= 500:
                self.Wave_7.update(enemies)
            elif frame > 550 and len(enemies)==0:
                set_value('waveNum', waveNum+1)
                set_value('frame', 0)
                functions.clearBullets(bullets, effects)
        elif waveNum==8:
            if frame == 1:
                set_value('boss_alive',True)
                self.BOSS.boss_cirno(enemies)
            elif frame==180:
                set_value('waveNum', waveNum+1)
                set_value('frame', 0)
        elif waveNum==9:
            if frame == 1:
                set_value('plot',True)
        elif waveNum==10:
            if frame == 1:
                pygame.mixer.music.stop()
                pygame.mixer.music.load("resource/BGM/04. Tomboyish Girl in Love.mp3")
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(1)
        elif waveNum==11:
            if frame == 400:
                set_value('pause',True)
                set_value('deadpause',1)



class stagecontroller_stage_editor():
    def __init__(self,node_lists=[]):
        self.frame = -1
        self.node_lists = node_lists
        self.idx = 0

    def update(self, enemies, bullets, effects, backgrounds, frame):
        self.frame += 1
        if self.frame == 0:
            functions.showBackground(backgrounds, 'STAGE_2')
            pygame.mixer.music.stop()
            pygame.mixer.music.load("resource/BGM/04. Lunate Elf.mp3")
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.7)
        self.node_lists[self.idx].update(enemies, bullets, effects, backgrounds, frame)

#a = stagecontroller_stage_editor()
#a.load()
                
                
                