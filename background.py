import pygame
import functions
import ImageManager
import obj

from pygame.locals import *
from const import *
from math import *
from random import *
from global_var import *

class Layer(obj.OBJ):
    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0
        self.vars = {}
        self.nodes = []
        self.updateIdx = 0
        self.sx = 0
        self.sy = 0
        
    def initial(self, img, istile, pos, velociy):
        self.image = ImageManager.getImage("Mods", img)
        self.istile = istile
        if istile:
            tmp = ImageManager.getImage("Mods", img)
            w, h = tmp.get_size()
            self.image = pygame.Surface((max(384, w*(384//w+(384/w!=0))), max(448, h*(448//h+(448/h!=0))))).convert_alpha()
            self.image.fill((0,0,0,0))
            self.w, self.h = self.image.get_size()
            for c in range(0, self.w+1, w):
                for r in range(0, self.h+1, h):
                    self.image.blit(tmp, (r, c))
        self.x, self.y = pos
        self.speedx = velociy[0]
        self.speedy = velociy[1]
        
    def update(self, screen):
        self.x += self.speedx
        self.y += self.speedy
        if get_value('screen_shaking'):
            self.sx = randint(-4, 4)
            self.sy = randint(-4, 4)
            set_value('screen_shaking', get_value('screen_shaking')-1)
        else:
            self.sx = self.sy = 0
        self.img = self.image.copy()
        self.vars['self'] = self
        while self.updateIdx < len(self.nodes):
            self.nodes[self.updateIdx].update(self.vars)
            if self.nodes[self.updateIdx].state in ("repeating", 'doing'):
                break
            self.updateIdx += 1
        if self.istile:
            self.x %= self.w
            self.y %= self.h
            screen.blit(self.img, (self.w+self.x+self.sx if self.x <= 0 else self.x-self.w+self.sx, self.h+self.y+self.sy if self.y <= 0 else self.y-self.h+self.sy))
            screen.blit(self.img, (self.w+self.x+self.sx if self.x <= 0 else self.x-self.w+self.sx, self.y+self.sy))
            screen.blit(self.img, (self.x+self.sx, self.h+self.y if self.y <= 0 else self.y-self.h+self.sy))
            screen.blit(self.img, (self.x+self.sx, self.y+self.sy))
        else:
            screen.blit(self.img, (self.x+self.sx, self.y+self.sy))
            

class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.layers = []
        self.lastFrame = 0
        self.maxFrame = -1
        
    def update(self, screen):
        self.lastFrame += 1
        if self.maxFrame != -1 and self.lastFrame > self.maxFrame:
            self.kill()
            return
        for i in self.layers:
            i.update(screen)

class SpellCardAttack(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((500, 400)).convert_alpha()
        self.img = ImageManager.getImage("BattleUI","SpellCardAttack")
        self.lastFrame = 0
        
    def update(self, screen):
        self.lastFrame += 1
        if self.lastFrame >= 91:
            self.kill()
        self.surf.fill((0,0,0,0))
        for i in range(-200, 700, 128):
            for j in range(0, 300, 64):
                self.surf.blit(self.img, (i+self.lastFrame*(1 if j%128==0 else -1)*3, j))
        surf = pygame.transform.rotate(self.surf, 30)
        if self.lastFrame <= 30:
            surf.set_alpha(functions.linear(0, 255, self.lastFrame, 30))
        elif self.lastFrame >= 60:
            surf.set_alpha(functions.linear(255, 0, self.lastFrame-60, 30))
        elif self.lastFrame == 31:
            surf.set_alpha(255)
        screen.blit(surf, (-70,-70))