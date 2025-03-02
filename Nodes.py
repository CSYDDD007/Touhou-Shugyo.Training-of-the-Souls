import bullet
import enemy
import SoundEffect

from random import *
from math import *
from global_var import *

import json

#filename = 'hello'
def load(filename):
    if filename:
        filename = 'mods/'+filename+'.sba_dat'
        with open(filename, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
            except:
                set_value('running',False)
                return
            final_nodes = []
        final_nodes.append(loading(data['0']))
        print(final_nodes)
        return final_nodes
        

def loading(data):
    length = len(data)-1
    new_node = Node('None',[],[])
    if data['message']['tags'][0]=='Folder':
        new_node = FolderNode([], data['message']['text'])
    elif data['message']['tags'][0]=='StageGroup':
        new_node = StageGroupNode([], data['message']['values'])
    elif data['message']['tags'][0]=='Stage':
        new_node = StageNode([], data['message']['values'])
    elif data['message']['tags'][0]=='Action':
        new_node = ActionNode([], data['message']['values'])
    elif data['message']['tags'][0]=='Wait':
        new_node = WaitNode([], data['message']['values'])
    elif data['message']['tags'][0]=='Repeat':
        new_node = RepeatNode([], data['message']['values'])
    elif data['message']['tags'][0]=='Bullet':
        new_node = BulletNode([], data['message']['values'])
    elif data['message']['tags'][0]=='Condition':
        new_node = ConditionNode([], data['message']['values'])
    elif data['message']['tags'][0]=='Break':
        new_node = BreakNode([], data['message']['values'])
    elif data['message']['tags'][0]=='Sound':
        new_node = SoundNode([], data['message']['values'])
    print(new_node.type)
    for i in range(0,length):
        keys = str(i)
        new_node.children.append(loading(data[keys]))
    return new_node

class Node:
    def __init__(self, type, children, data):
        self.type = type
        self.children = children
        self.data = data
        self.state = 'wait_to_do' #wait_to_do, doing, done
    
    def get_var(self, var_name):
        pass
    
    def set_var(self, var_name, value):
        pass
    
class FolderNode(Node):
    def __init__(self, children, data):
        super().__init__('Folder', children, data)
        self.name = data
        self.idx = 0
        self.done = True
        
    def update(self, enemies, bullets, effects, backgrounds, frame, var):
        #self.done = True
        for i in range(self.idx, len(self.children)):
            self.children[i].update(enemies, bullets, effects, backgrounds, frame, var)
            self.idx = i
            break
        return None
        
class StageGroupNode(Node):
    def __init__(self, children, data):
        super().__init__('StageGroup', children, data)
        self.rank = data[0]
        self.idx = 0
        
    def update(self, enemies, bullets, effects, backgrounds, frame):
        for i in range(self.idx, len(self.children)):
            self.children[i].update(enemies, bullets, effects, backgrounds, frame)
            self.idx = i
        return None

class StageNode(Node):
    def __init__(self, children, data):
        super().__init__('Stage', children, data)
        self.frame = -1
        self.idx = 0
        self.var = {}
        
    def update(self, enemies, bullets, effects, backgrounds, frame):
        self.frame += 1
        for i in range(self.idx, len(self.children)):
            self.children[i].update(enemies, bullets, effects, backgrounds, self.frame, self.var)
            self.idx = i
            #print(self.idx)
            #if self.children[i].state == 'doing':
            #    return

class WaitNode(Node):
    def __init__(self, children, data):
        super().__init__('Wait', children, data)
        self.frame = data[0]

    def update(self, enemies, bullets, effects, backgrounds, frame, var):
        if self.state == 'wait_to_do':
            self.state = 'doing'
            self.frame = self.data[0]
        if not self.frame:
            self.state = 'wait_to_do'
            return
        self.frame -= 1

class ActionNode(Node):
    def __init__(self, children, data):
        super().__init__('Action', children, data)
        self.idx = 0
        self.frame = -1

    def update(self, enemies, bullets, effects, backgrounds, frame, var):
        if self.state == 'wait_to_do':
            self.state = 'doing'
            self.frame = -1
        self.frame += 1
        while self.idx<len(self.children):
            self.children[self.idx].update(enemies, bullets, effects, backgrounds, self.frame, var)
            if self.children[self.idx].state in ('doing','repeating'):
                return
            self.idx += 1
        self.state = 'wait_to_do'

class BulletNode(Node):
    def __init__(self, children, data):
        super().__init__('Bullet', children, data)
        
    def update(self, enemies, bullets, effects, backgrounds, frame, var):
        if self.data[0] == "Scale":
            new_bullet = bullet.Scale_Bullet()
        elif self.data[0] == "Orb":
            new_bullet = bullet.Orb_Bullet()
        elif self.data[0] == "Small":
            new_bullet = bullet.Small_Bullet()
        elif self.data[0] == "Rice":
            new_bullet = bullet.Rice_Bullet()
        elif self.data[0] == "Chain":
            new_bullet = bullet.Chain_Bullet()
        elif self.data[0] == 'Pin':
            new_bullet = bullet.Pin_Bullet()
        elif self.data[0] == 'Satsu':
            new_bullet = bullet.Satsu_Bullet()
        elif self.data[0] == 'Gun':
            new_bullet = bullet.Gun_Bullet()
        elif self.data[0] == 'Bact':
            new_bullet = bullet.Bact_Bullet()
        elif self.data[0] == 'Star':
            new_bullet = bullet.Star_Bullet()
        elif self.data[0] == 'Grape':
            new_bullet = bullet.Grape_Bullet()
        elif self.data[0] == 'Dot':
            new_bullet = bullet.Dot_Bullet()
        new_bullet.loadColor(self.data[1])
        code = 'result = '
        command = 'randint(100,500)'
        #local_vars = {'a':10}
        exec(code+command, globals(), var)
        result = var['result']
        #print(var)
        new_bullet.initial(300,300)
        exec('result=a[0]', globals(), var)
        result = var['result'] 
        new_bullet.setSpeed(result,4)
        bullets.add(new_bullet)
        self.state = 'wait_to_do'

class SoundNode(Node):
    def __init__(self, children, data):
        super().__init__('Sound', children, data)
        
    def update(self, enemies, bullets, effects, backgrounds, frame, var):
        SoundEffect.play(self.data[0], self.data[1]/100, 0)

class ConditionNode(Node):
    def __init__(self, children, data):
        super().__init__('Condition', children, data)

class RepeatNode(Node):
    def __init__(self, children, data):
        super().__init__('Repeat', children, data)
        self.idx = 0
        self.times = data[0]
        self.interval = 1
        self.var = {'a':[0,0,10]}
        
    def update(self, enemies, bullets, effects, backgrounds, frame, var):
        if self.state == 'wait_to_do':
            self.times = self.data[0]
            self.state = 'doing'
        if self.times == 0:
            return
        if self.data[1] == 0:
            #print(self.times)
            for k in range(self.times):
                while self.idx < len(self.children):
                    self.children[self.idx].update(enemies, bullets, effects, backgrounds, frame, self.var)
                    if self.children[self.idx].state == 'doing':
                        return
                    self.idx += 1
                self.var['a'][0]+=self.var['a'][2]
                self.idx = 0
            self.var['a'][0]=self.var['a'][1]
            self.state = 'wait_to_do'
            
        elif self.interval == self.data[1] or self.state == 'repeating':
            self.state = 'repeating'
            while self.idx < len(self.children):
                self.children[self.idx].update(enemies, bullets, effects, backgrounds, frame, self.var)
                if self.children[self.idx].state in ('doing','repeating'):
                    return
                self.idx += 1
            self.times -= 1
            self.state = 'wait_to_do'
            self.idx = 0
            self.interval = 0
            if self.data[0]==-1:
                self.state = 'doing'
        self.interval += 1
        if self.times == 0:
            self.state = 'wait_to_do'
            self.idx = 0

class BreakNode(Node):
    pass


'''
repeat 60 -1
    repeat 0 10
        create bullet
'''
a={'a':[0,3]}
exec("result=a[0]",globals(),a)
print(a['result'])
exec("result=a[1]",globals(),a)
print(a['result'])
if 100%5 in (0,10,20):
    print("Yes")