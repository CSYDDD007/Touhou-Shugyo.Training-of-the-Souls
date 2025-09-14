import pygame
import functions
import ImageManager
from global_var import *

class OBJ(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.lastFrame = 0
        self.x = 0
        self.y = 0
        self.type = 'Enemy'
        self.image = pygame.Surface((24,24)).convert_alpha()
        self.image.fill((255,255,255))
        self.img_idx = 0
        self.speed = 0
        self.angle = 0
        self.speedx = 0
        self.speedy = 0
        self.rect = pygame.Rect(0, 0, 16, 16)
        self.rot = 0
        self.omiga = 0
        self.damage = 0
        self.hp = 0
        self.maxHp = 0
        self.dp = 0.0
        self.hscale = 1.0
        self.vscale = 1.0
        self.maxFrame = -1 
        self.immune = False
        self.navi = False
        self.destroyable = False
        self.out_of_wall = True
        self.boss = False
        self.invincible = False
        self.tweening_nodes = []
        self.var = {}
        self.nodes = []
        
    def setSpeed(self, speed, angle):
        self.speed = speed
        self.angle = angle
        self.speedx, self.speedy = functions.get_speed_in_angle(speed, angle)

    def checkValid(self):
        if self.out_of_wall:
            return
        if self.rect.top > 448 or self.rect.bottom < 0:
            self.kill()
            return
        if self.rect.left > 384 or self.rect.right < 0:
            self.kill()
            return
    
    def checkDistance(self):
        dist = functions.dist((get_value('player').x, get_value('player').y), (self.x, self.y))
        miniDist = get_value('enemypos')[2]
        if self.x <= 384 and self.x >= 0 and self.y <= 448 and self.y>=0 and dist<miniDist:
            set_value('enemypos',(self.x,self.y,dist))
        
    def movement(self):
        self.x += self.speedx
        self.y += self.speedy
        self.angle = functions.get_target_angle((0,0), (self.speedx, self.speedy))
        self.truePos()
        
    def truePos(self):
        self.rect.center = (self.x, self.y)
        
    def countRot(self):
        if self.navi:
            self.rot = -functions.get_target_angle((0, 0), (self.speedx, self.speedy))-90
        else:
            self.rot += self.omiga

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
            
    def update(self, screen, *args):
        self.lastFrame += 1
        self.checkValid()
        if self.maxFrame != -1 and self.lastFrame > self.maxFrame:
            self.kill()
            return
        if self.hp <= 0:
            self.kill()
            return
        if self.nodes:
            self.var['self'] = self
            self.nodes['update'].update(self.var)
        self.movement()
        self.checkDistance()
        self.countRot()
        self.truePos()
        img = pygame.transform.smoothscale(self.image, (self.image.get_size()[0]*self.hscale,self.image.get_size()[1]*self.vscale))
        functions.drawImage(img, (self.x,self.y),self.rot,screen)
    
    def kill(self, type=None):
        if len(self.nodes) == 2:
            self.var['self'] = self
            self.nodes['kill'].update(self.var)
        super().kill()
    
    def DrawHealthbar(self, screen):
        healthbar = pygame.Surface((50, 8)).convert_alpha()
        healthbar.fill((0,0,0))
        health = max(self.hp,0)/self.maxHp
        health = pygame.Surface((health*50, 8)).convert_alpha()
        health.fill((128,255,128))
        healthbar.blit(health,(0,0))
        screen.blit(healthbar,(self.x-25,self.rect.y-10))
        pygame.draw.rect(screen,(255,255,255),pygame.Rect(self.x-25,self.rect.y-10,50,8),2)
        
    def ShowHealthValue(self, screen):
        if self.lastHp != self.hp:
            self.lastHp = self.hp
            self.health_text = ImageManager.stot("Regular_font", 12, f"{int(max(0,self.hp))}/{self.maxHp}", (255,255,255), (0,0,0), 1)
        health_text_rect = self.health_text.get_rect(center=(self.x,self.rect.y-15))
        screen.blit(self.health_text,health_text_rect)
        if self.type != 'Enemy':
            return
        if get_value('enemy_draw_healthbar'):
            self.DrawHealthbar(screen)
        if get_value('enemy_show_health_value'):
            self.ShowHealthValue(screen)
        
        
        