import obj
import bullet
import enemy
import boss
import SoundManager
import ImageManager
import pygame

from random import *
from global_var import *
from functions import *

import json
import sys
#filename = 'hello'


def return_value(statement, vars):
    exec('result={}'.format(statement), globals(), vars)
    return vars['result']

function_lists = {}
enemy_lists = {}
bullet_lists = {}
boss_lists = {}
background_lists = {}
object_lists = {}
def load(filename):
    global function_lists, enemy_lists, bullet_lists, boss_lists, background_lists, object_lists
    function_lists = {}
    enemy_lists = {}
    bullet_lists = {}
    boss_lists = {}
    background_lists = {}
    object_lists = {}
    if filename:
        filename = 'mods/'+filename+'.sba_dat'
        with open(filename, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
            except:
                set_value('running',False)
                return
            final_nodes = []
        final_nodes.append(loading(data['0'], None))
        return final_nodes
        
def INIT(v):
    set_value('Reimu_Main_Bullet', int(v[0]))
    set_value('Reimu_Satsu', int(v[1]))
    set_value('Reimu_Pin', int(v[2]))
    set_value('Dream Seal', int(v[3]))
    set_value('Marisa_Main_Bullet', int(v[4]))
    set_value('Marisa_Laser', int(v[5]))
    set_value('Marisa_Missile', int(v[6]))
    set_value('Master_Spark', int(v[7]))
    set_value('Debug', 0 if v[8]=="False" else 1)

def loading(data, father):
    global function_lists, enemy_lists, bullet_lists, boss_lists
    length = len(data)-1
    type = data['message']['tags'][0]
    value = data['message']['values']
    new_node = Node('None',father,[],value)
    if type=='Setting':
        INIT(value)
    elif type=='Folder':
        new_node = FolderNode(father, [], data['message']['text'])
    elif type=='Rank':
        new_node = RankNode(father, [], value)
    elif type=='Stage':
        new_node = StageNode(father, [], value)
    elif type=='Stage_Title':
        new_node = StageTitleNode(father, [], value)
    elif type=='Thread':
        new_node = ThreadNode(father, [], value)
    elif type=='Wait':
        new_node = WaitNode(father, [], value)
    elif type=='Repeat':
        new_node = RepeatNode(father, [], value)
    elif type=='Bullet':
        new_node = BulletNode(father, [], value)
    elif type=='Enemy':
        new_node = EnemyNode(father, [], value)
    elif type=="If":
        new_node = IfNode(father, [], value)
    elif type in ('True','False'):
        new_node = TrueFalseNode(father, [], value)
    elif type=='Break':
        new_node = BreakNode(father, [], value)
    elif type=='Continue':
        new_node = ContinueNode(father, [], value)
    elif type=='Sound':
        new_node = SoundNode(father, [], value)
    elif type=='Music':
        new_node = MusicNode(father, [], value)
    elif type=='Var':
        new_node = VarNode(father, [], value)
    elif type=='Code':
        new_node = CodeNode(father, [], value)
    elif type=='Create_Object':
        new_node = CreateObjectNode(father, [], value)
    elif type=='Object_Class':
        new_node = ObjectClassNode(father, [], value)
    elif type=='Create_Enemy':
        new_node = CreateEnemyNode(father, [], value)
    elif type=='Clear_Enemy':
        new_node = ClearEnemyNode(father, [], value)
    elif type=='Enemy_Class':
        new_node = EnemyClassNode(father, [], value)
    elif type=='Create_Bullet':
        new_node = CreateBulletNode(father, [], value)
    elif type=='Clear_Bullet':
        new_node = ClearBulletNode(father, [], value)
    elif type=='Bullet_Class':
        new_node = BulletClassNode(father, [], value)
    elif type=='Boss_Class':
        new_node = BossClassNode(father, [], value)
    elif type=='Create_Boss':
        new_node = CallBossNode(father, [], value)
    elif type=='Background_Class':
        new_node = BackgroundClassNode(father, [], value)
    elif type=='Create_Background':
        new_node = CallBackgroundNode(father, [], value)
    elif type=='Clear_Background':
        new_node = ClearBackgroundNode(father, [], value)
    elif type=='Movement':
        new_node = MoveToNode(father, [], value)
    elif type=='Boss_Spell':
        new_node = BossSpellNode(father, [], value)
    elif type=='Boss_Explosion':
        new_node = BossExplosionNode(father, [], value)
    elif type=='Dialogue':
        new_node = DialogueNode(father, [], value)
    elif type=='Sentence':
        new_node = SentenceNode(father, [], value)
    elif type=='SpellCard':
        new_node = SpellCardNode(father, [], value)
    elif type=='Function':
        new_node = FunctionNode(father, [], value)
    elif type=='Velocity':
        new_node = VelocityNode(father, [], value)
    elif type=='Tweening':
        new_node = TweeningNode(father, [], value)
    elif type=='Image_Resource':
        new_node = ImageResourceNode(father, [], value)
        new_node.update({})
    elif type=='Sound_Resource':
        new_node = SoundResourceNode(father, [], value)
        new_node.update({})
    elif type=='Music_Resource':
        new_node = MusicResourceNode(father, [], value)
        new_node.update({})
    elif type=='Item':
        new_node = ItemNode(father, [], value)
    elif type=='Delete':
        new_node = DeleteNode(father, [], value)
    for i in range(0,length):
        keys = str(i)
        new_node.children.append(loading(data[keys], new_node))
    if new_node.type == 'Function':
        function_lists[new_node.name] = new_node
    elif new_node.type == 'Enemy_Class':
        enemy_lists[new_node.name] = new_node
    elif new_node.type == 'Bullet_Class':
        bullet_lists[new_node.name] = new_node
    elif new_node.type == 'Boss_Class':
        boss_lists[new_node.name] = new_node
    elif new_node.type == 'Background_Class':
        background_lists[new_node.name] = new_node
    elif new_node.type == 'Object_Class':
        object_lists[new_node.name] = new_node
    elif new_node.type == 'Rank':
        get_value('ranks').append(new_node)
    elif new_node.type == 'Stage':
        get_value('stages').append(new_node)
    return new_node

def replace_nodes(target_node, father):
    new_node = Node('None', father, [], target_node.data)
    if target_node.type == 'Folder':
        new_node = FolderNode(father, [], target_node.data)
    elif target_node.type == 'Rank':
        new_node = RankNode(father, [], target_node.data)
    elif target_node.type == 'Stage':
        new_node = StageNode(father, [], target_node.data)
    elif target_node.type == 'Thread':
        new_node = ThreadNode(father, [], target_node.data)
    elif target_node.type == 'Wait':
        new_node = WaitNode(father, [], target_node.data)
    elif target_node.type == 'Repeat':
        new_node = RepeatNode(father, [], target_node.data)
    elif target_node.type == 'Bullet':
        new_node = BulletNode(father, [], target_node.data)
    elif target_node.type=='Create_Bullet':
        new_node = CreateBulletNode(father, [], target_node.data)
    elif target_node.type == 'Enemy':
        new_node = EnemyNode(father, [], target_node.data)
    elif target_node.type=='Clear_Bullet':
        new_node = ClearBulletNode(father, [], target_node.data)
    elif target_node.type=='Clear_Enemy':
        new_node = ClearEnemyNode(father, [], target_node.data)
    elif target_node.type == 'Break':
        new_node = BreakNode(father, [], target_node.data)
    elif target_node.type == 'Sound':
        new_node = SoundNode(father, [], target_node.data)
    elif target_node.type == 'Music':
        new_node = MusicNode(father, [], target_node.data)
    elif target_node.type == 'Var':
        new_node = VarNode(father, [], target_node.data)
    elif target_node.type == 'Enemy_Class':
        new_node = EnemyClassNode(father, [], target_node.data)
    elif target_node.type == 'Bullet_Class':
        new_node = BulletClassNode(father, [], target_node.data)
    elif target_node.type == 'Boss_Class':
        new_node = BossClassNode(father, [], target_node.data)
    elif target_node.type == 'Background_Class':
        new_node = BackgroundClassNode(father, [], target_node.data)
    elif target_node.type == 'Object_Class':
        new_node = ObjectClassNode(father, [], target_node.data)
    elif target_node.type == 'MoveTo':
        new_node = MoveToNode(father, [], target_node.data)
    elif target_node.type == 'Boss_Spell':
        new_node = BossSpellNode(father, [], target_node.data)
    elif target_node.type == 'Boss_Explosion':
        new_node = BossExplosionNode(father, [], target_node.data)
    elif target_node.type == 'Dialogue':
        new_node = DialogueNode(father, [], target_node.data)
    elif target_node.type == 'Sentence':
        new_node = SentenceNode(father, [], target_node.data)
    elif target_node.type == 'SpellCard':
        new_node = SpellCardNode(father, [], target_node.data)
    elif target_node.type == 'Function':
        new_node = FunctionNode(father, [], target_node.data)
    elif target_node.type == 'Code':
        new_node = CodeNode(father, [], target_node.data)
    elif target_node.type=='Velocity':
        new_node = VelocityNode(father, [], target_node.data)
    elif target_node.type == 'Tweening':
        new_node = TweeningNode(father, [], target_node.data)
    elif target_node.type == 'Delete':
        new_node = DeleteNode(father, [], target_node.data)
    elif target_node.type == 'If':
        new_node = IfNode(father, [], target_node.data)
    elif target_node.type == 'TrueFalse':
        new_node = TrueFalseNode(father, [], target_node.data)
    elif target_node.type=='Delete':
        new_node = DeleteNode(father, [], target_node.data)
    elif target_node.type=='Item':
        new_node = ItemNode(father, [], target_node.data)
    for i in target_node.children:
        new_node.children.append(replace_nodes(i, new_node))
    return new_node
'''
Types of Nodes:
FolderNode: A node that contains other nodes.
FuntionNode: A node that defines a function.
EnemyNodes: A node that defines an enemy.
BulletNodes: A node that defines a bullet.
RankNode: A node that defines a rank {Easy, Normal, Hard, Lunatic, Extra}.
StageNode: A node that defines a stage {1, 2, 3, 4, 5, 6, ?}.
ThreadNode: A node that defines a thread (Independent times) (Once created, it will last until it is finished or breaked or jumped).
WaitNode: A node that pauses the program for a while.
RepeatNode: A node that repeats for n times. {n: times, t: interval frame(s), vars: increment(s)}.
SimpleBulletNode: A node that creates a simple bullet.
CreateEnemyNode: A node that calls an enemy which is defined.
CallBulletNode: A node that calls a bullet which is defined.
VarNode: A node that defines a variable.
SoundNode: A node that plays a sound {SE type, volume}.
'''
#thread_lists = []

class Node:
    def __init__(self, type, father = None, children = None, data = None):
        self.type = type
        self.father = father
        self.children = children
        self.data = data
        self.var = {}
        self.state = 'wait_to_do' #wait_to_do, doing, done
        
    def update(self, var):
        pass
    
    def set_var(self, var_name, value, var):
        cmd = 'result = ' + str(value)
        exec(cmd, globals(), var)
        self.var[var_name] = var['result']
        if self.father is not None and self.father.var.get(var_name) is not None:
            self.father.set_var(var_name, value, var)
            
    def break_repeat(self):
        if self.type == 'Repeat':
            self.times = 0
        else:
            self.father.break_repeat()
            
    def continue_repeat(self):
        if self.type == 'Repeat':
            self.idx = len(self.children)
        else:
            self.father.continue_repeat()
    
class FolderNode(Node):
    def __init__(self, father, children, data):
        super().__init__('Folder', father, children, data)
        self.name = data
        self.idx = 0
        self.done = True
        
    def update(self, var):
        for i in range(self.idx, len(self.children)):
            self.children[i].update(var)
            self.idx = i
            break
        return None
    
class FunctionNode(Node):
    def __init__(self, father, children, data):
        super().__init__('Function', father, children, data)
        self.name = data[0]
        self.idx = 0
        self.thread = []
        self.state = 'wait_to_do'

    def update(self, var):
        for i in self.thread:
            i.update(var)
            if i.state == 'wait_to_do':
                self.thread.remove(i)
        if self.thread:
            self.state = 'threading'
        while self.idx<len(self.children):
            self.children[self.idx].update(var)
            if self.children[self.idx].type == 'Thread':
                self.thread.append(self.children[self.idx])
                self.idx += 1
                continue
            if self.children[self.idx].state in ('doing','repeating'):
                return
            self.idx += 1
        self.state = 'wait_to_do'
        
class ImageResourceNode(Node):
    def __init__(self, father, children, data):
        super().__init__('Image_Resource', father, children, data)
        
    def update(self, var):
        new_image = pygame.image.load(self.data[0]).convert_alpha()
        self.vars={'new_image':new_image}
        if self.data[2] == '':
            size = new_image.get_size()
        else:
            exec('result={}'.format(self.data[2]),globals(),self.vars)
            size = self.vars['result']
        exec('result={}'.format(self.data[3]),globals(),self.vars)
        zoom = self.vars['result']
        exec('result={}'.format(self.data[4]),globals(),self.vars)
        alpha = self.vars['result']
        exec('result={}'.format(self.data[5]),globals(),self.vars)
        rotation = self.vars['result']
        exec('result=({})'.format(self.data[6]),globals(),self.vars)
        flip = self.vars['result']
        new_image = ImageManager.CropImage(new_image, (size[-2], size[-1]), size if self.data[2]!='' else (0,0,size[0],size[1]), zoom=zoom, alpha=alpha, rotation=rotation, flip=flip)
        ImageManager.addImage(self.data[1], new_image)

class SoundResourceNode(Node):
    def __init__(self, father, children, data):
        super().__init__('Sound_Resource', father, children, data)

    def update(self):
        SoundManager.addSound(self.data[1], self.data[0])

class MusicResourceNode(Node):
    def __init__(self, father, children, data):
        super().__init__('MusicResource', father, children, data)

    def update(self):
        SoundManager.addBGM(self.data[1], self.data[0])

class ObjectClassNode(Node):
    def __init__(self, father, children, data):
        super().__init__('Object_Class', father, children, data)
        self.name = data[0]
        self.func_dicts = {}
        self.idx = 0
        self.vars = {}
        
    def update(self, var):
        new_obj = obj.OBJ()
        new_obj.var = self.vars
        for i in self.children:
            self.func_dicts[i.name] = replace_nodes(i, new_obj)
        new_obj.type = self.data[1]
        new_obj.image = ImageManager.getImage('Mods', self.data[2])
        new_obj.x, new_obj.y = return_value(self.data[5], self.vars)
        size = return_value(self.data[3], self.vars)
        new_obj.rect = pygame.Rect(new_obj.x, new_obj.y, size[0], size[1])
        new_obj.hp = new_obj.maxHp = new_obj.damage = return_value(self.data[4], self.vars)
        new_obj.setSpeed(return_value(self.data[6], self.vars), return_value(self.data[7], self.vars))
        new_obj.rot = return_value(self.data[8], self.vars)
        new_obj.omiga = return_value(self.data[9], self.vars)
        new_obj.out_of_wall = return_value(self.data[10], self.vars)
        new_obj.hscale = return_value(self.data[11], self.vars)
        new_obj.vscale = return_value(self.data[12], self.vars)
        new_obj.maxFrame = return_value(self.data[13], self.vars)
        new_obj.nodes = self.func_dicts.copy()
        var['last'] = new_obj
        if new_obj.type=="Enemy":
            get_value('enemies').add(new_obj)
        elif new_obj.type=='Enemy_Bullet':
            get_value('bullets').add(new_obj)
        elif new_obj.type=='Effect':
            get_value('effects').add(new_obj)
        else:
            get_value('player_bullets').add(new_obj)

class CreateObjectNode(Node):
    def __init__(self, father, children, data):
        super().__init__('Create_Object', father, children, data)
        self.name = data[0]
        self.nodes = replace_nodes(object_lists[self.name], self)
        self.parameter=data[1:]
    def update(self, var):
        for i in range(0, len(self.parameter), 2):
            if len(self.parameter)==1:
                break
            exec("result={}".format(self.parameter[i+1]), globals(), var)
            self.nodes.vars[self.parameter[i]]=var['result']
        self.nodes.update(var)
        
        
class EnemyClassNode(Node):
    def __init__(self, father, children, data):
        super().__init__('Enemy_Class', father, children, data)
        self.name = data[0]
        self.func_dicts = {}
        self.idx = 0
        self.vars = {}
        
    def update(self, var):
        new_enemy = enemy.Enemy()
        new_enemy.var = self.vars
        for i in self.children:
            self.func_dicts[i.name] = replace_nodes(i, new_enemy)
        type = return_value(self.data[1], self.vars)
        pos = return_value(self.data[2], self.vars)
        angle = return_value(self.data[3], self.vars)
        speed = return_value(self.data[4], self.vars)
        hp = return_value(self.data[5], self.vars)
        new_enemy.power_num = return_value(self.data[6], self.vars)
        new_enemy.point_num = return_value(self.data[7], self.vars)
        new_enemy.initial(pos[0], pos[1], type, hp)
        new_enemy.setSpeed(speed, angle)
        new_enemy.nodes = self.func_dicts.copy()
        var['last'] = new_enemy
        get_value('enemies').add(new_enemy)
        
class BulletClassNode(Node):
    def __init__(self, father, children, data):
        super().__init__('Bullet_Class', father, children, data)
        self.name = data[0]
        self.func_dicts = {}
        self.idx = 0
        self.vars = {}
        
    def update(self, var):
        new_bullet = bullet.Bullet()
        new_bullet.var = self.vars
        for i in self.children:
            self.func_dicts[i.name] = replace_nodes(i, new_bullet)
        type :str = self.data[1]
        new_bullet.loadType(type.lower())
        new_bullet.loadColor(self.data[2])
        pos = return_value(self.data[3], self.vars)
        speed = return_value(self.data[4], self.vars)
        angle = return_value(self.data[5], self.vars)
        aim_to_player = return_value(self.data[6], self.vars)
        stay_on_create = return_value(self.data[7], self.vars)
        destroyable = return_value(self.data[8], self.vars)
        out_of_wall = return_value(self.data[9], self.vars)
        maxFrame = return_value(self.data[10], self.vars)
        act_frame = return_value(self.data[11], self.vars)
        acceleration = return_value(self.data[12], self.vars)
        accel_angle = return_value(self.data[13], self.vars)
        max_v = return_value(self.data[14], self.vars)
        new_bullet.initial(pos[0], pos[1], stay_on_create, destroyable, out_of_wall, maxFrame, act_frame, acceleration, accel_angle, max_v)
        if aim_to_player:
            angle = get_target_angle(pos, (get_value('player').x,get_value('player').y))+angle
        new_bullet.setSpeed(speed, angle)
        new_bullet.nodes = self.func_dicts.copy()
        get_value("bullets").add(new_bullet)
        var['last'] = new_bullet
        self.state = 'wait_to_do'

class CreateEnemyNode(Node):
    def __init__(self, father, children, data):
        super().__init__('Enemy', father, children, data)
        self.name = data[0]
        self.nodes = replace_nodes(enemy_lists[self.name], self)
        self.parameter=data[1:]
    def update(self, var):
        for i in range(0, len(self.parameter), 2):
            if len(self.parameter)==1:
                break
            exec("result={}".format(self.parameter[i+1]), globals(), var)
            self.nodes.vars[self.parameter[i]]=var['result']
        self.nodes.update(var)
        
class CreateBulletNode(Node):
    def __init__(self, father, children, data):
        super().__init__('Create_Bullet', father, children, data)
        self.name = data[0]
        self.nodes = replace_nodes(bullet_lists[self.name], self)
        #self.name = data[0]
        self.parameter=data[1:]
    def update(self, var):
        for i in range(0, len(self.parameter), 2):
            if len(self.parameter)==1:
                break
            exec("result={}".format(self.parameter[i+1]), globals(), var)
            self.nodes.vars[self.parameter[i]]=var['result']
        self.nodes.update(var)
        
class BossClassNode(Node):
    def __init__(self, father, children, data):
        super().__init__('Boss_Class', father, children, data)
        self.name = data[0]
        
    def update(self, var):
        new_boss = boss.BOSS()
        new_boss.nodes = self.children
        cnt = 0
        for i in self.children:
            if i.type == 'SpellCard' and i.name != '':
                cnt += 1
            
        get_value('boss_effect').add(effect.BossName_Effect(self.data[0], cnt))
        exec("result={}".format(self.data[1]), globals(), var)
        pos = var['result']
        new_boss.x = pos[0]
        new_boss.y = pos[1]
        new_boss.sp_back = replace_nodes(background_lists[self.data[2]], new_boss)
        exec("result={}".format(self.data[7]), globals(), var)
        new_boss.animation_interval = var['result']
        new_boss.normal_back = replace_nodes(background_lists[self.data[8]], new_boss)
        new_boss.bgm = self.data[9]
        if self.data[3] == '':
            get_value('enemies').add(new_boss)
            return
        new_boss.default = False
        sprite_sheet = ImageManager.getImage('Mods', self.data[3])
        w, h = sprite_sheet.get_size()
        exec("result={}".format(self.data[4]), globals(), var)
        nCol = var['result']
        exec("result={}".format(self.data[5]), globals(), var)
        nRow = var['result']
        w/=nCol
        h/=nRow
        exec("result={}".format(self.data[10]), globals(), var)
        nImage = var['result']
        for i in range(len(nImage)):
            for j in range(nImage[i]):
                new_boss.idle_frame.append(i*nCol+j)
        img_lists = []
        for r in range(nRow):
            for c in range(nCol):
                img_lists.append(ImageManager.CropImage(sprite_sheet, (w, h), (w*c, h*r, w, h)))
        new_boss.image = img_lists
        
        sprite_sheet = ImageManager.getImage('Mods', self.data[11])
        w, h = sprite_sheet.get_size()
        exec("result={}".format(self.data[15]), globals(), var)
        isFlip = var['result']
        sprite_sheet = ImageManager.CropImage(sprite_sheet, (w, h), (0, 0, w, h), flip=isFlip)
        exec("result={}".format(self.data[12]), globals(), var)
        nCol = var['result']
        exec("result={}".format(self.data[13]), globals(), var)
        nRow = var['result']
        w/=nCol
        h/=nRow
        exec("result={}".format(self.data[14]), globals(), var)
        nImage = var['result']
        for i in range(len(nImage)):
            for j in range(nImage[i]):
                new_boss.left_frame.append(i*nCol+j)
        img_lists = []
        for r in range(nRow):
            for c in range(nCol):
                img_lists.append(ImageManager.CropImage(sprite_sheet, (w, h), (w*c, h*r, w, h)))
        new_boss.left_image = img_lists
        
        sprite_sheet = ImageManager.getImage('Mods', self.data[16])
        w, h = sprite_sheet.get_size()
        exec("result={}".format(self.data[20]), globals(), var)
        isFlip = var['result']
        sprite_sheet = ImageManager.CropImage(sprite_sheet, (w, h), (0, 0, w, h), flip=isFlip)
        exec("result={}".format(self.data[17]), globals(), var)
        nCol = var['result']
        exec("result={}".format(self.data[18]), globals(), var)
        nRow = var['result']
        w/=nCol
        h/=nRow
        exec("result={}".format(self.data[19]), globals(), var)
        nImage = var['result']
        for i in range(len(nImage)):
            for j in range(nImage[i]):
                new_boss.right_frame.append(i*nCol+j)
        img_lists = []
        for r in range(nRow):
            for c in range(nCol):
                img_lists.append(ImageManager.CropImage(sprite_sheet, (w, h), (w*c, h*r, w, h)))
        new_boss.right_image = img_lists
        
        
        get_value('enemies').add(new_boss)
        
class CallBossNode(Node):
    def __init__(self, father, children, data):
        super().__init__("CallBoss", father, children, data)
        self.name = data[0]
        self.nodes = replace_nodes(boss_lists[self.name], self)
        
    def update(self, var):
        self.nodes.update(var)
        
class MoveToNode(Node):
    def __init__(self, father, children, data):
        super().__init__("MoveTo", father, children, data)
        self.mode_dicts = {"LINEAR":0,"ACC":1, "DCC":2, "ACC_DCC":3}
        
    def update(self, var):
        var['self'].start_x = var['self'].x
        var['self'].start_y = var['self'].y
        exec("result={}".format(self.data[0]), globals(), var)
        var['self'].movingFrame = var['result']
        var['self'].maxMovingFrame = var['result']
        exec("result={}".format(self.data[1]), globals(), var)
        var['self'].target_x = var['result'][0]
        var['self'].target_y = var['result'][1]
        var['self'].moving_mode = self.mode_dicts[self.data[2]]
        
class SpellCardNode(Node):
    def __init__(self, father, children, data):
        super().__init__("SpellCard", father, children, data)
        self.name = self.data[0]
        self.total_time = self.data[1]
        self.hp = self.data[2]
        self.drop_power = self.data[3]
        self.drop_point = self.data[4]
        self.state = 'wait_to_do'
    
    def update(self, var):
        if self.state == 'wait_to_do':
            exec("result={}".format(self.hp), globals(), var)
            var['self'].hp = var['result']
            var['self'].maxHp = var['result']
            exec("result={}".format(self.total_time), globals(), var)
            self.time = var['result']
            var['self'].timer = self.time*60
            exec("result={}".format(self.drop_power), globals(), var)
            power = var['result']
            exec("result={}".format(self.drop_point), globals(), var)
            point = var['result']
            var['self'].drop_power = power
            var['self'].drop_point = point
            if var['self'].bgm != '':
                SoundManager.BGM_Play(var['self'].bgm, -1, 1.0)
                var['self'].bgm = ''
            sp = 0
            if self.name != '':
                for i in get_value('boss_effect'):
                    if i.__class__.__name__ == 'BossName_Effect':
                        i.nsp -= 1
                        break
                SoundManager.play('spell_sound', 1.0)
                get_value('boss_effect').add(effect.SpellCardName(self.name))
                get_value('boss_effect').add(effect.SpellCardBonus(4000000, 5, self.time))
                sp=1
                get_value('backgrounds').empty()
                var['self'].sp_back.update(var)
                get_value('backgrounds').add(background.SpellCardAttack())
                var['self'].isSpell = 1
            var['self'].immune = False
            get_value('boss_effect').add(effect.Timer(self.time, sp))
            self.time *= 60
        self.state = 'doing'
        self.time -= 1
        if self.time == -1:
            self.state = 'wait_to_do'
            return
        self.children[0].update(var)
        if self.children[0].state == 'wait_to_do':
            self.state = 'wait_to_do'
            
class BossSpellNode(Node):
    def __init__(self, father, children, data):
        super().__init__("Boss_Spell", father, children, data)
        self.pos = self.data[0]
        self.color = self.data[1]
        self.radius = self.data[2]
        self.time = self.data[3]
        self.mode = self.data[4]
        
    def update(self, var):
        exec("result={}".format(self.pos), globals(), var)
        pos = var['result']
        exec('result={}'.format(self.color), globals(), var)
        color = var['result']
        if self.mode == 'START':
            exec("result={}".format(self.radius), globals(), var)
            radius = var['result']
            exec('result={}'.format(self.time), globals(), var)
            time = var['result']
            get_value('effects').add(effect.MagicSpell(pos, radius, color, time))
        else:
            get_value('effects').add(effect.SpellMagic(pos, color))
            
class BossExplosionNode(Node):
    def __init__(self, father, children, data):
        super().__init__("Boss_Explosion", father, children, data)
        
    def update(self, var):
        exec('result=self.x,self.y', globals(), var)
        pos = var['result']
        get_value('effects').add(effect.BossExplosion(pos))
        
class DialogueNode(Node):
    def __init__(self, father, children, data):
        super().__init__("Dialogue", father, children, data)
        self.left = None
        self.right = None
        self.text = None
        self.d = 0
        self.vars = {"DialogGroup":self}
        
    def update(self, var):
        self.vars.update(var)
        self.d = 0
        self.state = 'doing'
        set_value('dialog', True)
        self.children[0].update(self.vars)
        if self.children[0].state == 'wait_to_do':
            set_value('dialog', False)
            self.state = 'wait_to_do'
        set_value('dialog_direction', self.d)
        set_value('dialog_text', self.text)
        set_value('left_portrait', self.left)
        set_value('right_portrait', self.right)
        
class SentenceNode(Node):
    def __init__(self, father, children, data):
        super().__init__("Sentence", father, children, data)
        img = ImageManager.getImage("Mods", self.data[0])
        self.direction = self.data[1]
        self.text = self.data[2].split('$')
        v = {}
        exec("result={}".format(self.data[3]),globals(),v)
        self.scale = v['result']
        self.img = pygame.transform.smoothscale(img, (img.get_size()[0]*self.scale, img.get_size()[1]*self.scale))
        self.state = 'wait_to_do'
        
    def update(self, var):
        if get_value("K_z"):
            set_value("K_z", False)
            self.state = 'wait_to_do'
            return
        if self.state == 'wait_to_do':
            v = []
            l = 0
            for i in range(len(self.text)):
                v.append(ImageManager.stot("Regular_font", 14, self.text[i], (0,0,0), (0,0,0), 0))
                l = max(ImageManager.get_font_size("Regular_font", 14, self.text[i])[0], l)
            t_s = pygame.Surface((l+10, len(self.text)*24)).convert_alpha()
            t_s.fill((0,0,0,0))
            pygame.draw.rect(t_s, (255,255,128), t_s.get_rect(), border_radius=10)
            pygame.draw.rect(t_s, (0,0,0), t_s.get_rect(), 2, 10)
            for i in range(len(v)):
                t_s.blit(v[i], (0, i*20))
            var['DialogGroup'].text = t_s
        self.state = 'doing'
        if self.direction == 'LEFT':
            var['DialogGroup'].left = self.img
            var["DialogGroup"].d = -1
        else:
            var['DialogGroup'].right = self.img
            var["DialogGroup"].d = 1
       
class TweeningNode(Node):
    def __init__(self, father, children, data):
        super().__init__("Tweening", father, children, data)
        self.end = self.data[2]
        self.frame = self.data[3]
        self.mode_dicts = {"LINEAR":0,"ACC":1, "DCC":2, "ACC_DCC":3}
        
    def update(self, var):
        exec("result={}.{}".format(self.data[0], self.data[1]), globals(), var)
        start = var['result']
        exec('result={}'.format(self.data[2]), globals(), var)
        end = var['result']
        exec('result={}'.format(self.data[3]), globals(), var)
        frame = var['result']
        mode = self.mode_dicts[self.data[4]]
        var[self.data[0]].tweening_nodes.append([start, end, 0, frame, mode, self.data[1]])
        
class BackgroundClassNode(Node):
    def __init__(self, father, children, data):
        super().__init__("Background_Class", father, children, data)
        self.name = self.data[0]
        
    def update(self, var):
        new_back = background.Background()
        for i in self.children:
            layer = replace_nodes(i, None)
            new_layer = background.Layer()
            exec("result={}".format(i.data[1]), globals(), var)
            istile = var['result']
            exec("result={}".format(i.data[2]), globals(), var)
            pos = var['result']
            exec("result={}".format(i.data[3]), globals(), var)
            speedx = var['result']
            exec("result={}".format(i.data[4]), globals(), var)
            speedy = var['result']
            new_layer.initial(i.data[0], istile, pos, (speedx, speedy))
            new_layer.nodes = layer.children
            new_back.layers.append(new_layer)
        get_value('backgrounds').add(new_back)
        
class CallBackgroundNode(Node):
    def __init__(self, father, children, data):
        super().__init__("Create_Background", father, children, data)
        self.name = self.data[0]
        self.nodes = replace_nodes(background_lists[self.name], self)
        
    def update(self, var):
        self.nodes.update(var)

class ClearBackgroundNode(Node):
    def __init__(self, father, children, data):
        super().__init__("Clear_Background", father, children, data)
        
    def update(self, var):
        get_value('backgrounds').empty()

class ClearBulletNode(Node):
    def __init__(self, father, children, data):
        super().__init__("Clear_Bullet", father, children, data)
        self.point = self.data[0]

    def update(self, var):
        for i in get_value('bullets'):
            if self.point == 'True':
                bullet.createItem(i.x,i.y)
                print(1)
            new_vanish = effect.bulletVanish(i.x,i.y,i.color)
            get_value('effects').add(new_vanish)
            i.kill()

class ClearEnemyNode(Node):
    def __init__(self, father, children, data):
        super().__init__('Clear_Enemy', father, children, data)

    def update(self, var):
        for i in get_value('enemies'):
            if not i.boss:
                i.killEffect()
                i.kill()

class ItemNode(Node):
    def __init__(self, father, children, data):
        super().__init__('Item', father, children, data)

    def update(self, var):
        type = return_value(self.data[0], var)
        pos = return_value(self.data[1], var)
        num = return_value(self.data[2], var)
        dropItem(pos[0],pos[1],type,num)
        #dropItem(pos[0], pos[1], randint(0, 9), num)

class DeleteNode(Node):
    def __init__(self, father, children, data):
        super().__init__("Delete", father, children, data)
        
    def update(self, var):
        var[self.data[0]].kill(0)
        
class IfNode(Node):
    def __init__(self, father, children, data):
        super().__init__("If", father, children, data)
        self.statement = self.data[0]
        self.state = 'wait_to_do'
        self.thread = []
        self.idx = 0
        
    def update(self, var):
        if self.state == 'wait_to_do':
            exec("result={}".format(self.statement), globals(), var)
            print(self.statement, var['result']==True)
            self.idx = not var['result']
        self.children[self.idx].update(var)
        if self.children[self.idx].state in ("repeating", 'doing', 'threading'):
            self.state = 'doing'
            return
        self.state = 'wait_to_do'
        self.idx=0

class TrueFalseNode(Node):
    def __init__(self, father, children, data):
        super().__init__("TrueFalse", father, children, data)
        self.state = 'wait_to_do'
        self.thread = []
        self.idx = 0

    def update(self, var):
        for i in self.thread:
            i.update(var)
            if i.state == 'wait_to_do':
                self.thread.remove(i)
        while self.idx < len(self.children):
            self.children[self.idx].update(var)
            if self.idx >= len(self.children):
                break
            if self.children[self.idx].state in ("repeating", 'doing'):
                self.state = 'doing'
                return
            elif self.children[self.idx].state == 'threading':
                self.thread.append(self.children[self.idx])
            self.idx += 1
        self.state = 'wait_to_do'
        self.idx=0

class RankNode(Node):
    def __init__(self, father, children, data):
        super().__init__('Rank', father, children, data)
        v = {}
        exec("result={}".format(self.data[1]), globals(), v)
        self.color = v['result']
        self.text = self.data[0]
        self.rank = ImageManager.stot('Rank_font', 32, self.text, WHITE, self.color, 2)
        self.idx = 0
        
    def update(self, var):
        for i in range(self.idx, len(self.children)):
            self.children[i].update(var)
            self.idx = i
        return None

class StageNode(Node):
    def __init__(self, father, children, data):
        super().__init__('Stage', father, children, data)
        self.frame = -1
        self.name = self.data[0]
        self.title = self.data[1]
        self.addition = self.data[2]
        n = ImageManager.stot("Regular_font", 24, self.name, WHITE, BLACK, 2)
        t = ImageManager.stot("Art_font", 32, self.title, WHITE, BLACK, 2)
        a = ImageManager.stot("Regular_font", 16, self.addition, WHITE, BLACK, 2)
        s1 = ImageManager.get_font_size("Regular_font", 24, self.name)
        s2 = ImageManager.get_font_size("Art_font", 32, self.title)
        s3 = ImageManager.get_font_size("Regular_font", 16, self.addition)
        w = max(s1[0], max(s2[0], s3[0]))
        h = s1[1]+s2[1]+s3[1]+30
        s = pygame.Surface((w+20, h)).convert_alpha()
        s.fill((0,0,0,0))
        s.blit(n, (0,0))
        s.blit(t, (0,s1[1]+5))
        s.blit(a, a.get_rect(topright=(w+20,s1[1]+s2[1]+10)))
        self.surf = s
        self.idx = 0
        self.var = {}
        self.thread = []
        self.state = 'doing'
        
    def update(self, var):
        set_value('stage', self.surf)
        self.children[0].update(var)
        if self.children[0].state == 'wait_to_do' and not len(get_value('enemies')) and not len(get_value('bullets')) and not len(get_value('effects')):
            self.state = 'wait_to_do'
class StageTitleNode(Node):
    def __init__(self, father, children, data):
        super().__init__('Stage_Title', father, children, data)
        
    def update(self, var):
        get_value('effects').add(effect.Stage_Begin_Surface())

class WaitNode(Node):
    def __init__(self, father, children, data):
        super().__init__('Wait', father, children, data)

    def update(self, var):
        if self.state == 'wait_to_do':
            self.state = 'doing'
            self.times = return_value(self.data[0], var)
        if not self.times:
            self.state = 'wait_to_do'
            return
        self.times -= 1
        
class VarNode(Node):
    def __init__(self, father, children, data):
        super().__init__('Var', father, children, data)
        
    def update(self, var):
        if var.get(self.data[0]) is not None:
            self.set_var(self.data[0], self.data[1], var)
        else:
            cmd = '{}={}'.format(self.data[0],self.data[1])
            exec(cmd, globals(), var)
            
class CodeNode(Node):
    def __init__(self, father, children, data):
        super().__init__("Code", father, children, data)
        self.code = ""
        for i in self.data:
            i=i.replace("$", " ")
            self.code+=i+"\n"
        
    def update(self, var):
        exec(self.code, globals(), var)

class ThreadNode(Node):
    def __init__(self, father, children, data):
        super().__init__('Thread', father, children, data)
        self.idx = 0
        self.frame = -1
        self.var = {}
        self.thread = []

    def update(self, var :dict):
        self.var.update(var)
        if self.state == 'wait_to_do':
            self.state = 'doing'
            self.frame = -1
        for i in self.thread:
            i.update(self.var)
            if i.state == 'wait_to_do':
                self.thread.remove(i)
        while self.idx<len(self.children):
            self.children[self.idx].update(self.var)
            if self.idx >= len(self.children):
                break
            if self.children[self.idx].type == 'Thread' or self.children[self.idx].state == 'threading':
                self.thread.append(self.children[self.idx])
                self.idx += 1
                continue
            if self.children[self.idx].state in ('doing','repeating','threading'):
                return
            self.idx += 1
        self.state = 'wait_to_do' if not self.thread else 'threading'

class BulletNode(Node):
    def __init__(self, father, children, data):
        super().__init__('Bullet', father, children, data)
        
    def update(self, var):
        new_bullet = bullet.Bullet()
        type :str = self.data[0]
        new_bullet.loadType(type.lower())
        new_bullet.loadColor(self.data[1])
        pos = return_value(self.data[2], var)
        speed = return_value(self.data[3], var)
        angle = return_value(self.data[4], var)
        aim_to_player = return_value(self.data[5], var)
        stay_on_create = return_value(self.data[6], var)
        destroyable = return_value(self.data[7], var)
        out_of_wall = return_value(self.data[8], var)
        maxFrame = return_value(self.data[9], var)
        act_frame = return_value(self.data[10], var)
        acceleration = return_value(self.data[11], var)
        accel_angle = return_value(self.data[12], var)
        max_v = return_value(self.data[13], var)
        new_bullet.initial(pos[0], pos[1], stay_on_create, destroyable, out_of_wall, maxFrame, act_frame, acceleration, accel_angle, max_v)
        if aim_to_player:
            angle = get_target_angle(pos, (get_value('player').x,get_value('player').y))+angle
        new_bullet.setSpeed(speed, angle)
        get_value("bullets").add(new_bullet)
        var['last'] = new_bullet
        self.state = 'wait_to_do'

class EnemyNode(Node):
    def __init__(self, father, children, data):
        super().__init__('Enemy', father, children, data)
        self.func_dicts = {}

    def update(self, var):
        new_enemy = enemy.Enemy()
        self.func_dicts['update'] = replace_nodes(self.children[0], new_enemy)
        type = return_value(self.data[0], var)
        pos = return_value(self.data[1], var)
        angle = return_value(self.data[2], var)
        speed = return_value(self.data[3], var)
        hp = return_value(self.data[4], var)
        new_enemy.power_num = return_value(self.data[5], var)
        new_enemy.point_num = return_value(self.data[6], var)
        new_enemy.initial(pos[0], pos[1], type, hp)
        new_enemy.setSpeed(speed, angle)
        new_enemy.nodes = self.func_dicts.copy()
        var['last'] = new_enemy
        get_value('enemies').add(new_enemy)
        
class VelocityNode(Node):
    def __init__(self, father, children, data):
        super().__init__('Velocity', father, children, data)
        
    def update(self, var):
        exec("result={}".format(self.data[1]), globals(), var)
        speed = var['result']
        exec("result={}".format(self.data[2]), globals(), var)
        angle = var['result']
        var[self.data[0]].setSpeed(speed, angle)

class SoundNode(Node):
    def __init__(self, father, children, data):
        super().__init__('Sound', father, children, data)
        
    def update(self, var):
        SoundManager.play(self.data[0], int(self.data[1][0:-1])/100, 1)

class MusicNode(Node):
    def __init__(self, father, children, data):
        super().__init__('Music', father, children, data)

    def update(self, var):
        exec("result={}".format(self.data[1]), globals(), var)
        time = var['result']
        exec("result={}".format(self.data[2]), globals(), var)
        volume = var['result']
        SoundManager.BGM_Play(self.data[0], time, volume)

class RepeatNode(Node):
    def __init__(self, father, children, data):
        super().__init__('Repeat', father, children, data)
        self.idx = 0
        self.times = data[0]
        self.interval = data[1]
        self.maxTimes = 0
        self.maxInterval = 0
        self.var = {}
        self.var_self = {}
        self.var_og = {}
        self.increment = {}
        for i in range(2, len(data), 3):
            self.var_self[str(data[i])]=data[i+1]
            self.var_og[str(data[i])]=data[i+1]
            self.increment[str(data[i])]=data[i+2]
    def update(self, var):
        self.var.update(var)
        self.var.update(self.var_self)
        if self.state == 'wait_to_do':
            exec(f"result = {self.data[0]}",globals(),self.var)
            self.times = self.var['result']
            exec(f"result = {self.data[1]}",globals(),self.var)
            self.maxInterval = self.var['result']
            for i in self.var_self:
                exec("result = "+str(self.var_self[i]),globals(),self.var)
                self.var_self[i] = self.var['result']
            self.state = 'doing'
            self.var.update(var)
            self.var.update(self.var_self)
        if self.times == 0:
            return
        if self.maxInterval == 0:
            for i in self.var_self:
                exec("result = "+str(self.var_self[i]),globals(),self.var)
                self.var_self[i] = self.var['result']
            self.var.update(self.var_self)
            for _ in range(self.times):
                while self.idx < len(self.children):
                    self.children[self.idx].update(self.var)
                    if self.times == 0:
                        self.state = 'wait_to_do'
                        return
                    if self.idx >= len(self.children):
                        break
                    if self.children[self.idx].state == 'doing':
                        return
                    self.idx += 1
                self.idx = 0
                for i in self.var_self:
                    exec("result = "+str(self.var_self[i])+'+'+str(self.increment[i]),globals(),self.var)
                    self.var_self[i] = self.var['result']
                self.var.update(self.var_self)
            for i in self.var_self:
                self.var_self[i] = self.var_og[i]
            self.var.update(self.var_self)
            self.state = 'wait_to_do'
            
        elif self.interval == self.maxInterval or self.state == 'repeating':
            self.state = 'repeating'
            while self.idx < len(self.children):
                self.children[self.idx].update(self.var)
                if self.times == 0:
                    self.state = 'wait_to_do'
                    return
                if self.idx >= len(self.children):
                    break
                if self.children[self.idx].state in ('doing','repeating'):
                    return
                self.idx += 1
            self.times -= 1
            self.state = 'doing'
            self.idx = 0
            self.interval = 0
            for i in self.var_self:
                exec("result = "+str(self.var_self[i])+'+'+str(self.increment[i]),globals(),self.var)
                self.var_self[i] = self.var['result']
            self.var.update(self.var_self)
            
        self.interval += 1
        if self.times == 0:
            self.state = 'wait_to_do'
            self.idx = 0
            for i in self.var_self:
                self.var_self[i] = self.var_og[i]

class BreakNode(Node):
    def __init__(self, father, children, data):
        super().__init__("Break", father, children, data)
        
    def update(self, var):
        self.break_repeat()
        
class ContinueNode(Node):
    def __init__(self, father, children, data):
        super().__init__("Continue", father, children, data)
        
    def update(self, var):
        self.continue_repeat()