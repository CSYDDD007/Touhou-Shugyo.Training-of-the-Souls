from global_var import *
from const import *

import effect

class Stage_1():
    def __init__(self, player):
        self.image=get_value('textbox')
        self.image_1=pygame.transform.flip(self.image,True,False).convert_alpha()
        self.times = 0
        self.plot = get_value('plot_1_Reimu') if player=='REIMU' else get_value('plot_1_Marisa')
        self.line = self.plot[0]
        self.text = engtextfont.render(self.line,True,(0,0,0))
        self.player = pygame.transform.flip(get_value('Reimu_pos')[0] if player=='REIMU' else get_value("Marisa_pos")[0], True if player=='REIMU' else 0, False).convert_alpha()
        self.pos = 0 if player=='REIMU' else 100
        self.enemy = get_value('cat_boss_plot')
        
    def update(self):
        self.times+=1
        if self.times>len(self.plot):
            set_value('plot',False)
            set_value('waveNum', get_value('waveNum')+1)
            set_value('frame', 0)
            return
        self.line = self.plot[self.times]
        self.text = engtextfont.render(self.line,True,(0,0,0))
        
    def draw(self,screen):
        if self.times%2==0 and self.times<=6 or self.times%2==1 and self.times>=9:
            img = self.image.copy()
            img.blit(self.text,(80,220))
            screen.blit(img,(100,100))
            screen.blit(self.player,(-150+self.pos,300))
        else:
            img = self.image_1.copy()
            img.blit(self.text,(100,220))
            screen.blit(img,(200,100))
            screen.blit(self.enemy,(600,400))
            

class Stage_2():
    def __init__(self, player):
        self.image=get_value('textbox')
        self.image_1=pygame.transform.flip(self.image,True,False).convert_alpha()
        self.times = 0
        self.plot = get_value('plot_2_Reimu') if player=='REIMU' else get_value('plot_2_Marisa')
        self.talk = 0
        self.line = self.plot[0]
        if self.line[0:3]=='P: ':
            self.line = self.line.replace('P: ','')
            self.talk = 0
        else:
            self.line = self.line.replace("C: ",'')
            self.talk = 1
        self.text = engtextfont.render(self.line,True,(0,0,0))
        self.player = pygame.transform.flip(get_value('Reimu_pos')[0] if player=='REIMU' else get_value("Marisa_pos")[0], True if player=='REIMU' else 0, False).convert_alpha()
        self.pos = 0 if player=='REIMU' else 100
        self.enemy = get_value('Cirno_pos')[0]
        
    def update(self):
        self.times+=1
        if self.times==7 and not get_value('boss_effect'):
            get_value('boss_effect').add(effect.Boss_Name('Cirno'))
        if self.times>=len(self.plot):
            set_value('plot',False)
            set_value('waveNum', get_value('waveNum')+1)
            set_value('frame', 0)
            return
        self.line = self.plot[self.times]
        if self.line[0:3]=='P: ':
            self.line = self.line.replace('P: ','')
            self.talk = 0
        else:
            self.line = self.line.replace("C: ",'')
            self.talk = 1
        self.text = engtextfont.render(self.line,True,(0,0,0))
        
    def draw(self,screen):
        if self.talk==0:
            img = self.image.copy()
            img.blit(self.text,(80,220))
            screen.blit(img,(100,100))
            screen.blit(self.player,(-150+self.pos,300))
        else:
            img = self.image_1.copy()
            img.blit(self.text,(100,220))
            screen.blit(img,(200,100))
            screen.blit(self.enemy,(600,300))
            
        