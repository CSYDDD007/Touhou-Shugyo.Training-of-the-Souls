import sys
import os
import webbrowser
import subprocess
from global_var import *
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import customtkinter as ctk
import datetime
import logging

from tkinter import *
from tkinter import colorchooser
from tkinter.filedialog import askopenfilename, asksaveasfile

import json
import SoundManager
import ImageManager
SoundManager.loadSound()
ctk.set_default_color_theme("dark-blue")
ctk.set_appearance_mode("light")

root = ctk.CTk()
root.title("sba_stg editor")
root.iconbitmap('resource/image/icon_aEm_icon.ico')
root.geometry("1600x900")

class MenuBar(Menu):
    def __init__(self, master):
        super().__init__(master, tearoff=False)
        self.master = master
        self.filemenu = Menu(self, tearoff=False)
        self.filemenu.add_command(label="New", command=lambda: self.new(False))
        self.filemenu.add_command(label="Open", command=self.load)
        self.filemenu.add_command(label="Save", command=self.save)
        self.add_cascade(label="File", menu=self.filemenu)
        self.Tutorial = Menu(self, tearoff=False)
        self.Tutorial.add_command(label="Introduction", command=lambda:webbrowser.open('file:///'+os.getcwd()+'/resource/introduction.html'))
        self.Tutorial.add_command(label="Basic", command=lambda:webbrowser.open('file:///'+os.getcwd()+'/resource/basic.html'))
        self.Tutorial.add_command(label="Advanced", command=lambda:webbrowser.open('file:///'+os.getcwd()+'/resource/advanced.html'))
        self.add_cascade(label="Help", menu=self.Tutorial)
        self.Test = Menu(self, tearoff=False)
        self.Test.add_command(label="Test", command=self.test)
        self.add_cascade(label="Test", menu=self.Test)

    def test(self):
        if messagebox.askyesno('Question','Do you need to save the current project?'):
            self.save()
        root.withdraw()
        p = subprocess.run("python th_SBA.py", shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(p.stdout)
        print(p.stderr)
        root.deiconify()
        root.update()
        
        
    def new(self, has):
        for widget in root.winfo_children():
            #print(widget.widgetName)
            if widget.widgetName == "menu":
                continue
            widget.destroy()
        global OB, A_F, DT_F, tree
        DT_F = DataTreeFrame(root)
        tree = DataTree(DT_F,has)
        OB = OverallBar(root)
        A_F = AttributeFrame(root)
        OB.pack(side=TOP,fill=X)
        A_F.pack(side=LEFT,fill=Y)
        DT_F.pack(side=LEFT,fill=BOTH,expand=True)
        tree.pack(fill=BOTH,expand=True)
        DT_F.debug()
        DT_F.config(bg="#ffffff")

    def load(self):
        filename = askopenfilename(filetypes=[("SBA STG Data", "*.sba_dat")] ,initialdir='resource/mods')
        if filename:
            with open(filename, 'r', encoding='utf-8') as f1:
                data = json.load(f1)
            self.new(True)
            self.my_iid=0
            self.loading(data,'')
            
    def loading(self,data,parent_id):
        global enemy_class_dicts, bullet_class_dicts, object_class_dicts
        if parent_id=='':
            length = len(data)
        else:
            length = len(data)-1
        for i in range(0,length):
            keys = str(i)
            tree.insert(parent_id, 'end', iid=str(self.my_iid), text=data[keys]['message']['text'], values=data[keys]['message']['values'], image=data[keys]['message']['image'], tags=data[keys]['message']['tags'])
            self.my_iid += 1
            if data[keys]['message']['tags'][0]=='Enemy_Class':
                enemy_class_dicts[data[keys]['message']['values'][0]] = data[keys]['message']['values'][8:]
            elif data[keys]['message']['tags'][0]=='Bullet_Class':
                bullet_class_dicts[data[keys]['message']['values'][0]] = data[keys]['message']['values'][15:]
            elif data[keys]['message']['tags'][0]=='Background_Class':
                background_class_dicts[data[keys]['message']['values'][0]] = 1
            elif data[keys]['message']['tags'][0]=='Boss_Class':
                boss_class_dicts[data[keys]['message']['values'][0]] = 1
            elif data[keys]['message']['tags'][0]=='Object_Class':
                object_class_dicts[data[keys]['message']['values'][0]] = data[keys]['message']['values'][14:]
            elif data[keys]['message']['tags'][0]=='Image_Resource':
                ImageManager.addImage(data[keys]['message']['values'][1], None)
            elif data[keys]['message']['tags'][0]=='Sound_Resource':
                SoundManager.addSound(data[keys]['message']['values'][1], data[keys]['message']['values'][0])
            elif data[keys]['message']['tags'][0]=='Music_Resource':
                SoundManager.addBGM(data[keys]['message']['values'][1], data[keys]['message']['values'][0])
            if len(data[keys])>1:
                self.loading(data[keys], self.my_iid-1)
            
    def save(self):
        files = [('SBA STG Data', '*.sba_dat')]
        filepath = asksaveasfile(filetypes = files, defaultextension = files ,initialdir='resource/mods')
        if filepath:
            try:
                self.check('',filepath)
            except IOError:
                print("Error writing to file.")
                
    def check(self, idx, filepath=None):
        a=0
        dicts={}
        if idx!='':
            dicts['message']=tree.item(idx)
        for i in tree.get_children(idx):
            dicts[a]=self.check(i)
            a+=1
        if idx=='':
            json.dump(dicts, filepath, ensure_ascii=False, indent=4)
        else:
            return dicts

button_choosed = StringVar()
insert_mode=0
class OverallBar(Frame):
    def __init__(self, master):
        super().__init__(master, width=1600, height=50)
        self.master = master
        ToolBar(self).pack(side=LEFT)
        Button(self,text="Copy",command=tree.copy_nodes,image=image_lists['object'],compound="top").pack(side=LEFT,padx=5)
        Button(self,text="Paste",command=tree.paste_nodes,image=image_lists['object'],compound="top").pack(side=LEFT,padx=5)
        Button(self,text="Delete",command=tree.remove,image=image_lists['object'],compound="top").pack(side=LEFT,padx=5)
        ttk.Radiobutton(self, text='Add_Up', style='Toolbutton', width=10,image=image_lists['object'],compound="top", value='Add_Up', variable=button_choosed, command=self.change_mode).pack(side=LEFT,padx=5)
        ttk.Radiobutton(self, text='Add_Inside', style='Toolbutton', width=10,image=image_lists['object'],compound="top", value='Add_Inside', variable=button_choosed, command=self.change_mode).pack(side=LEFT,padx=5)
        ttk.Radiobutton(self, text='Add_Down', style='Toolbutton', width=10,image=image_lists['object'],compound="top", value='Add_Down', variable=button_choosed, command=self.change_mode).pack(side=LEFT,padx=5)
        
    def change_mode(self):
        global insert_mode
        a = button_choosed.get()
        if a=='Add_Up':
            insert_mode=1
        elif a=='Add_Inside':
            insert_mode=2
        elif a=='Add_Down':
            insert_mode=3
                
class ToolBar(ttk.Notebook):
    def __init__(self, master):
        super().__init__(master, width=1000, height=50)
        self.master = master
        self.widgetName = 'ToolBar'
        self.add(GeneralFrame(), text='General')
        self.add(StageFrame(), text='Stage')
        self.add(TimesFrame(), text='Times')
        self.add(EnemyFrame(), text='Enemy')
        self.add(BossFrame(), text='Boss')
        self.add(BulletFrame(), text='Bullet')
        self.add(AudioFrame(), text='Audio')
        self.add(BackgroundFrame(), text='Background')
        self.add(ResourceFrame(), text='Resource')
        self.add(ObjectFrame(), text='Object')
        
        
class GeneralFrame(Frame):
    def __init__(self):
        super().__init__()
        Button(self,image=image_lists['folder'],command=lambda x='Folder': tree.checkInsert(x)).pack(side=LEFT)
        Button(self,image=image_lists['code'],command=lambda x='Code': tree.checkInsert(x)).pack(side=LEFT)
        Button(self,image=image_lists['comment'],command=lambda x='Comment': tree.checkInsert(x)).pack(side=LEFT)
        Button(self,image=image_lists['if'],command=lambda x='If': tree.checkInsert(x)).pack(side=LEFT)
        
        
class StageFrame(Frame):
    def __init__(self):
        super().__init__()
        Button(self,image=image_lists['rank'],command=lambda x='Rank': tree.checkInsert(x)).pack(side=LEFT)
        Button(self,image=image_lists['stage'],command=lambda x='Stage': tree.checkInsert(x)).pack(side=LEFT)
        Button(self,image=image_lists['stage_title'],command=lambda x='Stage_Title': tree.checkInsert(x)).pack(side=LEFT)
        
class TimesFrame(Frame):
    def __init__(self):
        super().__init__()
        Button(self,image=image_lists['thread'],command=lambda x='Thread': tree.checkInsert(x)).pack(side=LEFT)
        Button(self,image=image_lists['wait'],command=lambda x='Wait': tree.checkInsert(x)).pack(side=LEFT)
        Button(self,image=image_lists['repeat'],command=lambda x='Repeat': tree.checkInsert(x)).pack(side=LEFT)
        Button(self,image=image_lists['break'],command=lambda x='Break': tree.checkInsert(x)).pack(side=LEFT)
        Button(self,image=image_lists['continue'],command=lambda x='Continue': tree.checkInsert(x)).pack(side=LEFT)
        
class EnemyFrame(Frame):
    def __init__(self):
        super().__init__()
        Button(self,image=image_lists['enemy'],command=lambda x='Enemy': tree.checkInsert(x)).pack(side=LEFT)
        Button(self,image=image_lists['enemy_class'],command=lambda x='Enemy_Class': tree.checkInsert(x)).pack(side=LEFT)
        Button(self,image=image_lists['create_enemy'],command=lambda x='Create_Enemy': tree.checkInsert(x)).pack(side=LEFT)
        Button(self,image=image_lists['clear_enemy'],command=lambda x='Clear_Enemy': tree.checkInsert(x)).pack(side=LEFT)
        
class BossFrame(Frame):
    def __init__(self):
        super().__init__()
        Button(self, image=image_lists['create_boss'], command=lambda x='Create_Boss': tree.checkInsert(x)).pack(side=LEFT)
        Button(self, image=image_lists['boss_class'], command=lambda x='Boss_Class': tree.checkInsert(x)).pack(side=LEFT)
        Button(self, image=image_lists['spellcard'], command=lambda x='SpellCard': tree.checkInsert(x)).pack(side=LEFT)
        Button(self, image=image_lists['dialogue'], command=lambda x='Dialogue': tree.checkInsert(x)).pack(side=LEFT)
        Button(self, image=image_lists['sentence'], command=lambda x='Sentence': tree.checkInsert(x)).pack(side=LEFT)
        Button(self, image=image_lists['movement'], command=lambda x='Movement': tree.checkInsert(x)).pack(side=LEFT)
        Button(self, image=image_lists['boss_spell'], command=lambda x='Boss_Spell': tree.checkInsert(x)).pack(side=LEFT)
        Button(self, image=image_lists['boss_explosion'], command=lambda x='Boss_Explosion': tree.checkInsert(x)).pack(side=LEFT)
        
class BulletFrame(Frame):
    def __init__(self):
        super().__init__()
        Button(self,image=image_lists['bullet'],command=lambda x='Bullet': tree.checkInsert(x)).pack(side=LEFT)
        Button(self,image=image_lists['bullet_class'],command=lambda x='Bullet_Class': tree.checkInsert(x)).pack(side=LEFT)
        Button(self,image=image_lists['create_bullet'],command=lambda x='Create_Bullet': tree.checkInsert(x)).pack(side=LEFT)
        Button(self,image=image_lists['clear_bullet'],command=lambda x='Clear_Bullet': tree.checkInsert(x)).pack(side=LEFT)
        
class AudioFrame(Frame):
    def __init__(self):
        super().__init__()
        Button(self,image=image_lists['sound'],command=lambda x='Sound': tree.checkInsert(x)).pack(side=LEFT)
        Button(self,image=image_lists['music'],command=lambda x='Music': tree.checkInsert(x)).pack(side=LEFT)
        
class BackgroundFrame(Frame):
    def __init__(self):
        super().__init__()
        Button(self,image=image_lists['create_background'],command=lambda x='Create_Background': tree.checkInsert(x)).pack(side=LEFT)
        Button(self,image=image_lists['clear_background'],command=lambda x='Clear_Background':tree.checkInsert(x)).pack(side=LEFT)
        Button(self,image=image_lists['background_class'],command=lambda x='Background_Class': tree.checkInsert(x)).pack(side=LEFT)
        Button(self,image=image_lists['layer'],command=lambda x='Layer': tree.checkInsert(x)).pack(side=LEFT)
        
        
class ResourceFrame(Frame):
    def __init__(self):
        super().__init__()
        Button(self,image=image_lists['image_resource'],command=lambda x='Image_Resource': tree.checkInsert(x)).pack(side=LEFT)
        Button(self,image=image_lists['sound_resource'],command=lambda x='Sound_Resource': tree.checkInsert(x)).pack(side=LEFT)
        Button(self,image=image_lists['music_resource'],command=lambda x='Music_Resource': tree.checkInsert(x)).pack(side=LEFT)

class ObjectFrame(Frame):
    def __init__(self):
        super().__init__()
        Button(self,image=image_lists['object_class'],command=lambda x='Object_Class': tree.checkInsert(x)).pack(side=LEFT)
        Button(self,image=image_lists['create_object'],command=lambda x='Create_Object': tree.checkInsert(x)).pack(side=LEFT)
        Button(self,image=image_lists['var'],command=lambda x='Var': tree.checkInsert(x)).pack(side=LEFT)
        Button(self,image=image_lists['velocity'],command=lambda x='Velocity': tree.checkInsert(x)).pack(side=LEFT)
        Button(self,image=image_lists['tweening'],command=lambda x="Tweening": tree.checkInsert(x)).pack(side=LEFT)
        Button(self,image=image_lists['delete'],command=lambda x='Delete': tree.checkInsert(x)).pack(side=LEFT)
        Button(self,image=image_lists['item'],command=lambda x='Item': tree.checkInsert(x)).pack(side=LEFT)
        

class Redirect():
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        if text=='\n':
            return
        self.widget.write(text)

class LoggerBox(Text):
    def write(self, text):
        self.configure(state='normal')
        message = "{} {}\n".format(datetime.datetime.now(), text)
        self.insert('end', message)
        self.yview(tk.END)
        self.configure(state='disabled')

class AttributeFrame(Frame):
    def __init__(self, master):
        super().__init__(master,width=600, height=800,relief="groove", bd=2)
        self.master = master
        self.detail_frame = EditFrame(self)
        self.iid = None
        self.detail_frame.pack(side=TOP, fill=BOTH, expand=True)
  
    def details_identify(self, iid, tags):
        if iid==self.iid:
            return
        for widget in self.winfo_children():
            widget.destroy()
        # if self.detail_frame:
        #     self.detail_frame.destroy()
        if tags == 'Folder':
            self.detail_frame = FolderEditFrame(self)
        elif tags == 'Setting':
            self.detail_frame = SettingEditFrame(self)
        elif tags == 'Rank':
            self.detail_frame = RankEditFrame(self)
        elif tags == 'Stage':
            self.detail_frame = StageEditFrame(self)
        elif tags == 'Stage_Title':
            self.detail_frame = StageTitleEditFrame(self)
        elif tags == 'If':
            self.detail_frame = IfEditFrame(self, "If")
        elif tags == 'Bullet':
            self.detail_frame = BulletEditFrame(self)
        elif tags == 'Enemy':
            self.detail_frame = EnemyEditFrame(self)
        elif tags == 'Create_Bullet':
            self.detail_frame = CreateBulletFrame(self)
        elif tags == 'Clear_Bullet':
            self.detail_frame = ClearBulletFrame(self)
        elif tags == 'Wait':
            self.detail_frame = WaitEditFrame(self)
        elif tags == 'Repeat':
            self.detail_frame = RepeatEditFrame(self)
        elif tags == 'Break':
            self.detail_frame = BreakFrame(self)
        elif tags == 'Continue':
            self.detail_frame = ContinueFrame(self)
        elif tags == 'Var':
            self.detail_frame = VariableEditFrame(self)
        elif tags == 'Code':
            self.detail_frame = CodeEditFrame(self)
        elif tags == 'Comment':
            self.detail_frame = CommentEditFrame(self)
        elif tags == "Bullet_Class":
            self.detail_frame = BulletClassFrame(self)
        elif tags == "Enemy_Class":
            self.detail_frame = EnemyClassFrame(self)
        elif tags == "Create_Enemy":
            self.detail_frame = CreateEnemyFrame(self)
        elif tags == 'Velocity':
            self.detail_frame = VelocityEditFrame(self)
        elif tags == 'Image_Resource':
            self.detail_frame = ImageResourceEditFrame(self)
        elif tags == 'Sound_Resource':
            self.detail_frame = SoundResourceEditFrame(self)
        elif tags == 'Sound':
            self.detail_frame = SoundEditFrame(self)
        elif tags == 'Music_Resource':
            self.detail_frame = MusicResourceEditFrame(self)
        elif tags == 'Music':
            self.detail_frame = MusicEditFrame(self)
        elif tags == 'Boss_Class':
            self.detail_frame = BossClassFrame(self)
        elif tags == 'Create_Boss':
            self.detail_frame = CreateBossFrame(self)
        elif tags == 'Movement':
            self.detail_frame = MoveToFrame(self)
        elif tags == 'Sentence':
            self.detail_frame = SentenceFrame(self)
        elif tags == 'SpellCard':
            self.detail_frame = SpellCardFrame(self)
        elif tags == 'Boss_Spell':
            self.detail_frame = BossSpellFrame(self)
        elif tags == 'Tweening':
            self.detail_frame = TweeningFrame(self)
        elif tags == 'Background_Class':
            self.detail_frame = BackgroundClassFrame(self)
        elif tags == 'Create_Background':
            self.detail_frame = CreateBackgroundFrame(self)
        elif tags == 'Layer':
            self.detail_frame = LayerEditFrame(self)
        elif tags == 'Item':
            self.detail_frame = ItemEditFrame(self)
        elif tags == 'Object_Class':
            self.detail_frame = ObjectClassFrame(self)
        elif tags == 'Create_Object':
            self.detail_frame = CreateObjectFrame(self)
        elif tags == 'Delete':
            self.detail_frame = DeleteFrame(self)
        else:
            self.detail_frame = EditFrame(self)
        self.iid = iid
        self.detail_frame.pack(side=TOP, fill=BOTH, expand=True)

from CTkXYFrame import *
class EditFrame(CTkXYFrame):
    def __init__(self, master):
        super().__init__(master, width=500, height=800)
        self.master = master
        self.name_lists = []
        self.value_lists = []
        self.button_lists = []
        self.value_dicts = {}
            
    def get_all_data(self):
        self.value_dicts.clear()
        for i in range(1, len(self.value_lists)):
            if(self.name_lists[i].cget('text')=="                "):
                break
            self.value_dicts[self.name_lists[i].cget('text')]=self.value_lists[i].get()
        print("Saved")
        print(str(self.value_dicts))
        
    def Add_Row(self, n, name :str, type, values=None, init_state=None, lists=None, func=None):
        if type == 'Big_Button':
            self.button_lists.append(Button(self, text=name, font=("Arial", 16), command=func))
            self.button_lists[-1].grid(row=n, column=0, columnspan=3, ipadx=10, ipady=10, sticky='nswe')
            return
        self.name_lists.append(Label(self, text=name, font=("Arial", 16), relief='groove', bd=2, anchor="w"))
        self.name_lists[-1].grid(row=n, column=0, ipadx=10, ipady=10, sticky='nswe')
        if type == 'Label':
            self.value_lists.append(Label(self, text="                                                  ", font=("Arial", 16), relief='groove', bd=2, bg='#ffffff', anchor="w"))
        elif type == 'Entry':
            self.value_lists.append(Entry(self, font=("Arial", 16), relief='groove', bd=2, bg='#ffffff'))
            self.value_lists[-1].insert(0, values)
            if init_state in ("normal", "readonly", "disabled"):
                self.value_lists[-1].config(state=init_state)
        elif type == "ComboBox":
            self.value_lists.append(ttk.Combobox(self, values=lists, font=("Arial", 16)))
            self.value_lists[-1].insert(0, values)
            if init_state in ("normal", "readonly", "disabled"):
                self.value_lists[-1].config(state=init_state)
        self.value_lists[-1].grid(row=n, column=1, ipadx=10, ipady=10, sticky='nswe')
        self.button_lists.append(Button(self, text="...", command=func))
        self.button_lists[-1].grid(row=n, column=2, ipadx=10, ipady=10, sticky='nswe')
        
class EditToplevel(Toplevel):
    def __init__(self, master, size, title, res):
        super().__init__(master, bg="#ffffff")
        self.master = master
        root.attributes("-disabled", 1)
        self.geometry(size)
        self.title(title)
        self.protocol("WM_DELETE_WINDOW", self.t_close_handler)
        self.resizable(res[0], res[1])
        
    def t_close_handler(self):
        root.attributes("-disabled", 0)
        self.destroy()

#only for testing
class TestEditFrame(EditFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.name_lists.clear()
        self.value_lists.clear()
        self.button_lists.clear()
        self.Add_Row(0, "FolderName", 'Entry', tree.item(tree.selection())['text'])
        for i in range(1,16):
            self.Add_Row(i, "                ", 'Entry', "   ", init_state="disabled")
        self.Add_Row(16, " ", "Save", func=self.save)
        
    def save(self):
        name = self.value_lists[0].get()
        tree.item(tree.selection(), values=name, text = name)
        
class ObjectClassFrame(EditFrame):
    def __init__(self, master):
        super().__init__(master)
        self.data = tree.item(tree.selection())['values']
        self.p = self.data[14:]
        self.Add_Row(0, "Node Type", "Entry", "Object_Class", init_state='disabled')
        self.Add_Row(1, "Object Name", "Entry", self.data[0])
        self.Add_Row(2, "Parameters", "Big_Button", func=lambda:SetParameter(root, self.p, 'set'))
        self.Add_Row(3, "Object Type", "ComboBox", self.data[1], lists=["Enemy","Enemy_Bullet","Player_Bullet","Effect"], init_state='readonly')
        self.Add_Row(4, "Images", "ComboBox", self.data[2], lists=list(ImageManager.images['Mods'].keys())+[''], init_state='readonly')
        self.Add_Row(5, "Hitbox size", "Entry", self.data[3])
        self.Add_Row(6, "HP/Damage", "Entry", self.data[4])
        self.Add_Row(7, "Position", "Entry", self.data[5])
        self.Add_Row(8, "Speed", "Entry", self.data[6])
        self.Add_Row(9, "Angle", "Entry", self.data[7])
        self.Add_Row(10, "Rotation", "Entry", self.data[8])
        self.Add_Row(11, "Omiga", "Entry", self.data[9])
        self.Add_Row(12, "Out of Wall", "ComboBox", self.data[10], lists=["False","True"])
        self.Add_Row(13, "H_Scale", "Entry", self.data[11])
        self.Add_Row(14, "V_Scale", "Entry", self.data[12])
        self.Add_Row(15, "MaxFrame", "Entry", self.data[13])
        self.Add_Row(16, "Save", "Big_Button", func=self.save)

    def save(self):
        self.get_all_data()
        v = []
        for i in self.value_dicts:
            v.append(self.value_dicts[i])
        v+=self.p
        object_class_dicts.pop(self.data[0], None)
        name = v[0]
        object_class_dicts[name] = self.p
        n = "Object Class '{}'".format(name)
        tree.item(tree.selection(), values=v, text=n)

class CreateObjectFrame(EditFrame):
    def __init__(self, master):
        super().__init__(master)
        self.data = tree.item(tree.selection())['values']
        self.p = object_class_dicts.get(self.data[0],[]).copy()
        p = self.data[1:]
        print(self.p)
        print(p)
        for i in range(1, min(len(p), len(self.p)), 2):
            self.p[i]=p[i]
        self.Add_Row(0, "Node Type", "Entry", "CreateObject", init_state = "disabled")
        self.Add_Row(1, "Object Name", "ComboBox", self.data[0], lists=list(object_class_dicts.keys()), init_state='readonly')
        self.Add_Row(2, "Parameter", "Big_Button", func=lambda:SetParameter(root, self.p, 'input'))
        self.Add_Row(3, "Save", "Big_Button", func=self.save)
        
    def save(self):
        self.get_all_data()
        v = [self.value_dicts["Object Name"]]
        v += self.p
        tree.item(tree.selection(), text=f"Create Object '{self.value_dicts["Object Name"]}'", values=v)

class SettingEditFrame(EditFrame):
    def __init__(self, master):
        super().__init__(master)
        self.data = tree.item(tree.selection())['values']
        self.Add_Row(0, "Node Type", "Entry", "Setting", init_state='disabled')
        self.Add_Row(1, "Player_1_B1", "Entry", self.data[0])
        self.Add_Row(2, "Player_1_B2", "Entry", self.data[1])
        self.Add_Row(3, "Player_1_B3", "Entry", self.data[2])
        self.Add_Row(4, "Player_1_SP", "Entry", self.data[3])
        self.Add_Row(5, "Player_2_B1", "Entry", self.data[4])
        self.Add_Row(6, "Player_2_B2", "Entry", self.data[5])
        self.Add_Row(7, "Player_2_B3", "Entry", self.data[6])
        self.Add_Row(8, "Player_2_SP", "Entry", self.data[7])
        self.Add_Row(9, "Debug Mode", "ComboBox", self.data[8], lists=['False','True'], init_state='readonly')
        self.Add_Row(10, "Save", "Big_Button", func=self.save)
    
    def save(self):
        self.get_all_data()
        v = []
        for i in self.value_dicts:
            v.append(self.value_dicts[i])
        tree.item(tree.selection(), values=v)
        
class FolderEditFrame(EditFrame):
    def __init__(self, master):
        super().__init__(master)
        self.data = tree.item(tree.selection())['values']
        self.Add_Row(0, "Node Type: ", 'Entry', "Folder", init_state = "disabled")
        self.Add_Row(1, "FolderName", 'Entry', self.data[0])
        self.Add_Row(2, "Save", "Big_Button", func=self.save)
        
    def save(self):
        self.get_all_data()
        name = self.value_dicts["FolderName"]
        tree.item(tree.selection(), values=[name], text = name)

class RankEditFrame(EditFrame):
    def __init__(self, master):
        super().__init__(master)
        self.data = tree.item(tree.selection())['values']
        self.Add_Row(0, "Node Type", "Entry", "Rank", init_state = "disabled")
        self.Add_Row(1, "Rank Name", "Entry", self.data[0])
        self.Add_Row(2, "Color(r, g, b)", "Entry", self.data[1], init_state = 'readonly', func=lambda x=2:changecolor(self.data[1],x))
        self.Add_Row(3, "Save", "Big_Button", func=self.save)
        
    def save(self):
        self.get_all_data()
        v = []
        for i in self.value_dicts:
            v.append(self.value_dicts[i])
        name = "Rank '{}'; Color: {}".format(v[0], v[1])
        tree.item(tree.selection(), values=v, text=name)
        
class StageEditFrame(EditFrame):
    def __init__(self, master):
        super().__init__(master)
        self.data = tree.item(tree.selection())['values']
        self.Add_Row(0, "Node Type", "Entry", "Stage", init_state = "disabled")
        self.Add_Row(1, "Stage Name", "Entry", self.data[0])
        self.Add_Row(2, "Stage Title", "Entry", self.data[1])
        self.Add_Row(3, "Addition", "Entry", self.data[2])
        self.Add_Row(4, "Save", "Big_Button", func=self.save)
        
    def save(self):
        self.get_all_data()
        v = []
        for i in self.value_dicts:
            v.append(self.value_dicts[i])
        name = "Stage '{}'; Title: {}; Addition: {}".format(v[0], v[1], v[2])
        tree.item(tree.selection(), values=v, text=name)
        
class StageTitleEditFrame(EditFrame):
    def __init__(self, master):
        super().__init__(master)
        self.data = tree.item(tree.selection())['values']
        self.Add_Row(0, "Node Type", "Entry", "Stage", init_state = "disabled")

class WaitEditFrame(EditFrame):
    def __init__(self, master):
        super().__init__(master)
        self.values = tree.item(tree.selection())['values']
        self.Add_Row(0, "Node Type: ", 'Entry', "Wait", init_state = "disabled")
        self.Add_Row(1, "Wait Time", "Entry", self.values[0])
        self.Add_Row(2, "Save", "Big_Button", func=self.save)
        
    def save(self):
        self.get_all_data()
        times = self.value_dicts["Wait Time"]
        self.values = [times]
        tree.item(tree.selection(), values=self.values, text="Wait "+str(times)+" frame(s)")
        
class CodeEditFrame(EditFrame):
    def __init__(self, master):
        super().__init__(master)
        self.values = tree.item(tree.selection())['values']
        self.content = ""
        for i in self.values:
            i=i.replace("$", " ")
            self.content += i+"\n"
        self.Add_Row(0, "Node Type: ", 'Entry', "Code", init_state = "disabled")
        self.Add_Row(1, "Codes", "Entry", self.values[0], func=self.edit, init_state = 'disabled')
        self.Add_Row(2, "Save", "Big_Button", func=self.save)
        
    def edit(self):
        CodeEditTopLevel(root, self.content)
        
    def save(self):
        self.get_all_data()
        self.values[0]=self.values[0].replace(" ", "$")
        tree.item(tree.selection(), values=self.values[0])

class CodeEditTopLevel(EditToplevel):
    def __init__(self, master, content):
        super().__init__(master, '600x600', 'Code Frame', (True, True))
        self.text = Text(self, width=41,height=600, font=("Arial", 16), relief='groove', bd=2)
        self.text.insert(0.0, content)
        self.text.pack(side=TOP,fill=BOTH)
        
    def t_close_handler(self):
        root.attributes("-disabled", 0)
        A_F.detail_frame.values[0] = self.text.get(1.0, 'end-1c')
        print(self.text.get(1.0, 'end-1c'))
        changecontent(self.text.get(1.0, 'end-1c'), 1, 'readonly')
        self.destroy()

class CommentEditFrame(EditFrame):
    def __init__(self, master):
        super().__init__(master)
        self.data = tree.item(tree.selection())['values']
        self.Add_Row(0, "Node Type", "Entry", "Comment", init_state='disabled')
        self.Add_Row(1, "Comment", "Entry", self.data[0])
        self.Add_Row(2, "Save", "Big_Button", func=self.save)

    def save(self):
        self.get_all_data()
        tree.item(tree.selection(), values=[self.value_dicts["Comment"]], text=self.value_dicts["Comment"])
        
class IfEditFrame(EditFrame):
    def __init__(self, master, type):
        super().__init__(master)
        self.data = tree.item(tree.selection())['values']
        self.type = type
        self.Add_Row(0, "Node Type", "Entry", type, init_state = "disabled")
        self.Add_Row(1, "Statement", "Entry", self.data[0])
        self.Add_Row(2, "Save", "Big_Button", func=self.save)
        
    def save(self):
        self.get_all_data()
        v = []
        for i in self.value_dicts:
            v.append(self.value_dicts[i])
        name = "{} {}".format(self.type, v[0])
        tree.item(tree.selection(), values=v, text=name)

class RepeatEditFrame(EditFrame):
    def __init__(self, master):
        super().__init__(master)
        self.data = tree.item(tree.selection())['values']
        self.var_lists = self.data[2:]
        #print(self.data, self.var_lists)
        self.Add_Row(0, "Node Type: ", 'Entry', "Repeat", init_state = "disabled")
        self.Add_Row(1, "Number of loops", "Entry", self.data[0])
        self.Add_Row(2, "Interval(s)", "Entry", self.data[1])
        self.loc_y = 3
        self.no_of_var = len(self.var_lists)//3
        for i in range(self.no_of_var):
            self.Add_Row(self.loc_y, f"Var {i+1} Name", "Entry", self.var_lists[i*3])
            self.Add_Row(self.loc_y+1, f"Var {i+1} Value", "Entry", self.var_lists[i*3+1])
            self.Add_Row(self.loc_y+2, f"Var {i+1} Increment", "Entry", self.var_lists[i*3+2])
            self.loc_y += 3
        if self.no_of_var:
            self.Add_Row(self.loc_y, "Delete", "Big_Button", func=self.delete)
            self.loc_y += 1
        self.Add_Row(self.loc_y, "Add", "Big_Button", func=self.add)
        self.Add_Row(self.loc_y+1, "Save", "Big_Button", func=self.save)
        self.loc_y += 2

    def add(self):
        if self.no_of_var:
            self.button_lists[-1].destroy()
            del self.button_lists[-1]
            self.loc_y -= 1
        for _ in range(2):
            self.button_lists[-1].destroy()
            del self.button_lists[-1]
            self.loc_y -= 1
        self.no_of_var += 1
        self.Add_Row(self.loc_y, f"Var {self.no_of_var} Name", "Entry", "Default")
        self.Add_Row(self.loc_y+1, f"Var {self.no_of_var} Value", "Entry", "Default")
        self.Add_Row(self.loc_y+2, f"Var {self.no_of_var} Increment", "Entry", "Default")
        self.loc_y += 3
        self.Add_Row(self.loc_y, "Delete", "Big_Button", func=self.delete)
        self.Add_Row(self.loc_y+1, "Add", "Big_Button", func=self.add)
        self.Add_Row(self.loc_y+2, "Save", "Big_Button", func=self.save)
        self.loc_y += 3

    def delete(self):
        self.no_of_var -= 1
        self.loc_y -= 3
        for _ in range(3):
            self.name_lists[-1].destroy()
            del self.name_lists[-1]
            self.value_lists[-1].destroy()
            del self.value_lists[-1]
        for _ in range(6):
            self.button_lists[-1].destroy()
            del self.button_lists[-1]
        if self.no_of_var:
            self.Add_Row(self.loc_y, "Delete", "Big_Button", func=self.delete)
            self.loc_y += 1
        self.Add_Row(self.loc_y, "Add", "Big_Button", func=self.add)
        self.Add_Row(self.loc_y+1, "Save", "Big_Button", func=self.save)
        self.loc_y += 2

    def save(self):
        self.get_all_data()
        values = []
        for i in self.value_dicts:
            values.append(self.value_dicts[i])
        name = "repeat {} time(s); {} frame(s) interval".format(values[0] if int(values[0]) >= 0 else "infinite", values[1])
        vars = ""
        for i in range(2, len(values), 3):
            vars+="; {} = {}; {} += {}".format(values[i], values[i+1], values[i], values[i+2])
        tree.item(tree.selection(), values = values, text=name+vars)
        
class BreakFrame(EditFrame):
    def __init__(self, master):
        super().__init__(master)
        self.Add_Row(0, "Node Type", "Entry", "Break", init_state = 'disabled')
        
class ContinueFrame(EditFrame):
    def __init__(self, master):
        super().__init__(master)
        self.Add_Row(0, "Node Type", "Entry", "Continue", init_state = 'disabled')

class BulletEditFrame(EditFrame):
    def __init__(self, master):
        super().__init__(master)
        self.data = tree.item(tree.selection())['values']
        self.Add_Row(0, "Node Type: ", 'Entry', "Create Bullet", init_state = "disabled")
        self.Add_Row(1, "Bullet Type", "Entry", self.data[0], func=lambda:ChooseBulletType(root, self.value_lists[2].get(), 1), init_state = 'readonly')
        self.Add_Row(2, "Bullet Color", "Entry", self.data[1], func=lambda:ChooseBulletColor(root, self.value_lists[1].get(), 2), init_state = 'readonly')
        self.Add_Row(3, "Position", "Entry", self.data[2])
        self.Add_Row(4, "Speed", "Entry", self.data[3])
        self.Add_Row(5, "Angle", "Entry", self.data[4])
        self.Add_Row(6, "Aim to Player", "ComboBox", self.data[5], init_state="readonly", lists=["True", "False"])
        self.Add_Row(7, "Stay On Create", "ComboBox", self.data[6], init_state="readonly", lists=["True", "False"])
        self.Add_Row(8, "Destroyable", "ComboBox", self.data[7], init_state="readonly", lists=["True", "False"])
        self.Add_Row(9, "Out of Wall", "ComboBox", self.data[8], init_state="readonly", lists=["True", "False"])
        self.Add_Row(10, "MaxFrame", "Entry", self.data[9])

        self.Add_Row(11, "Frame", "Entry", self.data[10])
        self.Add_Row(12, "Acceleration", "Entry", self.data[11])
        self.Add_Row(13, "Accel Angle", "Entry", self.data[12])
        self.Add_Row(14, "Max Velocity", "Entry", self.data[13])
        self.Add_Row(15, "Save", "Big_Button", func=self.save)

    def save(self):
        self.get_all_data()
        data = []
        for i in self.value_dicts:
            data.append(self.value_dicts[i])
        tree.item(tree.selection(), values=data)

class ChooseBulletType(Toplevel):
    def __init__(self, master, color, n):
        super().__init__(master, bg="#ffffff")
        self.n=n
        self.master = master
        root.attributes("-disabled", 1)
        self.geometry("600x600")
        self.title("Bullet Type List")
        self.protocol("WM_DELETE_WINDOW", self.t_close_handler)
        self.resizable(False, False)
        idx=0
        self.lists = []
        self.color_dicts = {'grey':0,'red':1,'lightRed':2,'purple':3,'pink':4,'blue':5,'seaBlue':6,'skyBlue':7,'lightBlue':8,'darkGreen':9,'green':10,'lightGreen':11,'yellow':12,'lemonYellow':13,'orange':14,'white':15}
        self.type_lists = ["Scale", "Orb", "Small", "Rice", "Chain", "Pin", "Satsu", "Gun", "Bact", "Star", "Water", "Grape", "Dot",
                  "Big_Star", "Mid", "Butterfly", "Knife", "Ellipse", "Big", "Heart", "Arrow", "Light", "Fire", "Drop", "Double_Star", "Big_Light"]
        for i in range(0,5):
            for j in range(0,6):
                Button(self,image=bullet_image_lists[self.type_lists[idx]][self.color_dicts[color]],command=lambda x=self.type_lists[idx]:self.return_bullet_type(x),bg="black").grid(row=i, column=j, ipadx=10, ipady=10)
                idx+=1
                if(idx==26):
                    return
        
    def t_close_handler(self):
        root.attributes("-disabled", 0)
        self.destroy()
        
    def return_bullet_type(self, bullet_type):
        changecontent(bullet_type, self.n, 'readonly')
        self.t_close_handler()

class ChooseBulletColor(Toplevel):
    def __init__(self, master, type, n):
        super().__init__(master, bg="#ffffff")
        self.master = master
        self.n = n
        root.attributes("-disabled", 1)
        self.geometry("400x400")
        self.title("Bullet Color List")
        self.protocol("WM_DELETE_WINDOW", self.t_close_handler)
        self.resizable(False, False)
        idx=0
        self.lists = []
        self.type_dicts={
        'grape':0,'dot':1,
        'scale':2,'orb':3,'small':4,'rice':5,'chain':6,'pin':7,'satsu':8,'gun':9,'bact':10,'star':11,'water':12,'drop':13,
        'big_star':14,'mid':15,'butterfly':16,'knife':17,'ellipse':18,'heart':19,'arrow':20,'light':21,'fire':22,'double_star':23,
        'big':24,'big_light':25}
        self.color_dicts = ['grey','red','lightRed','purple','pink','blue','seaBlue','skyBlue','lightBlue','darkGreen','green','lightGreen','yellow','lemonYellow','orange','white']
        self.mid_bullet_lists = [0,1,3,5,7,9,12,15]
        self.mid_color_lists = ["grey", "red", "purple", "blue", "lightBlue", "green", "yellow", "white"]
        self.fire_color_lists = ["red", "purple", "blue", "orange"]
        self.big_color_lists = ["red", "blue", "green", "yellow"]
        self.big_bullet_lists = [0,3,9,12]
        self.type_idx = self.type_dicts[type.lower()]
        if self.type_idx <= 13:
            for i in range(0,4):
                for j in range(0,4):
                    Button(self ,command=lambda x=idx:self.return_bullet_color(x), image=bullet_image_lists[type][idx],bg="black").grid(row=i, column=j, ipadx=10, ipady=10)
                    idx+=1
        elif self.type_idx == 22:
            for i in range(4):
                Button(self ,command=lambda x=idx:self.return_bullet_color(x), image=bullet_image_lists[type][i*4],bg="black").grid(row=0, column=i, ipadx=10, ipady=10)
                idx += 1
        elif self.type_idx <= 23 or self.type_idx==25:
            for i in range(0,2):
                for j in range(0,4):
                    Button(self ,command=lambda x=idx:self.return_bullet_color(x), image=bullet_image_lists[type][self.mid_bullet_lists[idx]],bg="black").grid(row=i, column=j, ipadx=10, ipady=10)
                    idx += 1
        elif self.type_idx == 24:
            for i in range(4):
                Button(self ,command=lambda x=idx:self.return_bullet_color(x), image=bullet_image_lists[type][self.big_bullet_lists[idx]],bg="black").grid(row=0, column=i, ipadx=10, ipady=10)
                idx += 1
        
    def t_close_handler(self):
        root.attributes("-disabled", 0)
        self.destroy()
        
    def return_bullet_color(self, color_idx):
        if self.type_idx <= 13:
            color = self.color_dicts[color_idx]
        elif self.type_idx == 22:
            color = self.fire_color_lists[color_idx]
        elif self.type_idx <=23 or self.type_idx==25:
            color = self.mid_color_lists[color_idx]
        else:
            color = self.big_color_lists[color_idx]
        changecontent(color, self.n, 'readonly')
        self.t_close_handler()
        
class BulletClassFrame(EditFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.data = tree.item(tree.selection())['values']
        self.p = self.data[15:]
        self.Add_Row(0, "Node Type", "Entry", "BulletClass", init_state = "disabled")
        self.Add_Row(1, "Bullet Name", "Entry", self.data[0])
        self.Add_Row(2, "Parameters", "Big_Button", func=lambda:SetParameter(root, self.p, 'set'))
        self.Add_Row(3, "Bullet Type", "Entry", self.data[1], func=lambda:ChooseBulletType(root, self.value_lists[3].get(), 2), init_state = 'readonly')
        self.Add_Row(4, "Bullet Color", "Entry", self.data[2], func=lambda:ChooseBulletColor(root, self.value_lists[2].get(), 3), init_state = 'readonly')
        self.Add_Row(5, "Position", "Entry", self.data[3])
        self.Add_Row(6, "Speed", "Entry", self.data[4])
        self.Add_Row(7, "Angle", "Entry", self.data[5])
        self.Add_Row(8, "Aim to Player", "ComboBox", self.data[6], init_state="readonly", lists=["True", "False"])
        self.Add_Row(9, "Stay On Create", "ComboBox", self.data[7], init_state="readonly", lists=["True", "False"])
        self.Add_Row(10, "Destroyable", "ComboBox", self.data[8], init_state="readonly", lists=["True", "False"])
        self.Add_Row(11, "Out of Wall", "ComboBox", self.data[9], init_state="readonly", lists=["True", "False"])
        self.Add_Row(12, "MaxFrame", "Entry", self.data[10])

        self.Add_Row(13, "Frame", "Entry", self.data[11])
        self.Add_Row(14, "Acceleration", "Entry", self.data[12])
        self.Add_Row(15, "Accel Angle", "Entry", self.data[13])
        self.Add_Row(16, "Max Velocity", "Entry", self.data[14])
        self.Add_Row(17, "Save", "Big_Button", func=self.save)
        
    def save(self):
        self.get_all_data()
        v = []
        for i in self.value_dicts:
            v.append(self.value_dicts[i])
        v+=self.p
        bullet_class_dicts.pop(self.data[0], None)
        name = v[0]
        bullet_class_dicts[name] = self.p
        tree.item(tree.selection(), values=v, text="Bullet Class '{}'".format(name))

class CreateBulletFrame(EditFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.data = tree.item(tree.selection())['values']
        self.p = bullet_class_dicts.get(self.data[0],[]).copy()
        p = self.data[1:]
        print(self.p)
        print(p)
        for i in range(1, min(len(p), len(self.p)), 2):
            self.p[i]=p[i]
        self.Add_Row(0, "Node Type", "Entry", "CreateBullet", init_state = "disabled")
        self.Add_Row(1, "Bullet Name", "ComboBox", self.data[0], lists=list(bullet_class_dicts.keys()), init_state='readonly')
        self.Add_Row(2, "Parameter", "Big_Button", func=lambda:SetParameter(root, self.p, 'input'))
        self.Add_Row(3, "Save", "Big_Button", func=self.save)
        
    def save(self):
        self.get_all_data()
        v = [self.value_dicts["Bullet Name"]]
        v += self.p
        tree.item(tree.selection(), text=f"Create Bullet \'{self.value_dicts["Bullet Name"]}\'", values=v)

class ClearBulletFrame(EditFrame):
    def __init__(self, master):
        super().__init__(master)
        self.data = tree.item(tree.selection())["values"]
        self.Add_Row(0, "Node Type: ", 'Entry', "Clear Bullet", init_state = "disabled")
        self.Add_Row(1, "Drop Point", "ComboBox", self.data[0], lists=["True","False"], init_state='readonly')
        self.Add_Row(2, "Save", "Big_Button", func=self.save)
        
    def save(self):
        self.get_all_data()
        name = "Delete all bullet; drop point: {}".format(self.value_dicts['Drop Point'])
        tree.item(tree.selection(), values=[self.value_dicts["Drop Point"]], text=name)

class VariableEditFrame(EditFrame):
    def __init__(self, master):
        super().__init__(master)
        self.data = tree.item(tree.selection())["values"]
        self.Add_Row(0, "Node Type: ", 'Entry', "Set Variable", init_state = "disabled")
        self.Add_Row(1, "Var Name", "Entry", self.data[0])
        self.Add_Row(2, "Var Value", "Entry", self.data[1])
        self.Add_Row(3, "Save", "Big_Button", func=self.save)
        
    def save(self):
        self.get_all_data()
        name = "set {} = {}".format(self.value_dicts["Var Name"], self.value_dicts["Var Value"])
        tree.item(tree.selection(), values=[self.value_dicts["Var Name"], self.value_dicts["Var Value"]], text=name)
        
class VelocityEditFrame(EditFrame):
    def __init__(self, master):
        super().__init__(master)
        self.data = tree.item(tree.selection())["values"]
        self.Add_Row(0, "Node Type: ", "Entry", "Set Velocity".format(self.data[0]), init_state = "disabled")
        self.Add_Row(1, "Object", "ComboBox", self.data[0], init_state = "readonly", lists = ['self', 'last'])
        self.Add_Row(2, "Speed", "Entry", self.data[1])
        self.Add_Row(3, "Angle", "Entry", self.data[2])
        self.Add_Row(4, "Save", "Big_Button", func=self.save)
        
    def save(self):
        self.get_all_data()
        v = []
        for i in self.value_dicts:
            v.append(self.value_dicts[i])
        tree.item(tree.selection(), values=v, text = "Set {}'s Velocity: speed={}; angle={}".format(v[0], v[1], v[2]))

        
class EnemyClassFrame(EditFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.data = tree.item(tree.selection())['values']
        self.p = self.data[8:]
        self.Add_Row(0, "Node Type", "Entry", "EnemyClass", init_state = "disabled")
        self.Add_Row(1, "Enemy Name", "Entry", self.data[0])
        self.Add_Row(2, "Parameter", "Big_Button", func=lambda:SetParameter(root, self.p, 'set'))
        self.Add_Row(3, "Enemy Type", "Entry", self.data[1], func = lambda:ChooseEnemyTypeToplevel(root, 2), init_state='readonly')
        self.Add_Row(4, "Position", "Entry", self.data[2])
        self.Add_Row(5, "Angle", "Entry", self.data[3])
        self.Add_Row(6, "Speed", "Entry", self.data[4])
        self.Add_Row(7, "Hit Point", "Entry", self.data[5])
        self.Add_Row(8, "Drop Power", "Entry", self.data[6])
        self.Add_Row(9, "Drop Point", "Entry", self.data[7])
        self.Add_Row(10, "Save", "Big_Button", func=self.save)
        
    def save(self):
        self.get_all_data()
        v = []
        for i in self.value_dicts:
            v.append(self.value_dicts[i])
        v+=self.p
        enemy_class_dicts.pop(self.data[0], None)
        name = v[0]
        enemy_class_dicts[name] = self.p
        name = "Enemy Class '{}'".format(v[0])
        tree.item(tree.selection(), text=name, values=v)

class EnemyEditFrame(EditFrame):
    def __init__(self, master):
        super().__init__(master)
        self.data = tree.item(tree.selection())['values']
        self.Add_Row(0, "Node Type", "Entry", "EnemyClass", init_state = "disabled")
        self.Add_Row(1, "Enemy Type", "Entry", self.data[0], func = lambda:ChooseEnemyTypeToplevel(root, 1), init_state = 'readonly')
        self.Add_Row(2, "Position", "Entry", self.data[1])
        self.Add_Row(3, "Angle", "Entry", self.data[2])
        self.Add_Row(4, "Speed", "Entry", self.data[3])
        self.Add_Row(5, "Hit Point", "Entry", self.data[4])
        self.Add_Row(6, "Drop Power", "Entry", self.data[5])
        self.Add_Row(7, "Drop Point", "Entry", self.data[6])
        self.Add_Row(8, "Save", "Big_Button", func=self.save)

    def save(self):
        self.get_all_data()
        v = []
        for i in self.value_dicts:
            v.append(self.value_dicts[i])
        tree.item(tree.selection(), values=v)
        
class SetParameter(EditToplevel):
    def __init__(self, master, p, mode):
        super().__init__(master, '800x800', 'SetParameter Frame', (1,1))
        self.p_lists=[]
        idx = 0
        text = 'Value' if mode=='input' else 'Default Value'
        Label(self, text="Name", font=("Arial", 26), relief='groove', bd=2, bg='#ffffff').grid(row=0, column=0)
        Label(self, text=text, font=("Arial", 26), relief='groove', bd=2, bg='#ffffff').grid(row=0, column=1)
        for i in range(1, 16):
            for j in range(0, 2):
                self.p_lists.append(Entry(self, font=("Arial", 26), relief='groove', bd=2, bg='#ffffff'))
                if idx<len(p):
                    self.p_lists[-1].insert(0, p[idx])
                    if mode=='input' and idx%2==0:
                        self.p_lists[-1].config(state='disabled')
                    idx+=1
                elif mode=='input':
                    self.p_lists[-1].config(state='disabled') 
                self.p_lists[-1].grid(row=i, column=j)
        
    def t_close_handler(self):
        root.attributes("-disabled", 0)
        p = []
        for i in range(0, len(self.p_lists), 2):
            if self.p_lists[i].get() != '':
                p.append(self.p_lists[i].get())
                p.append(self.p_lists[i+1].get())
        #print(p)
        A_F.detail_frame.p=p
        self.destroy() 
        
class ChooseEnemyTypeToplevel(EditToplevel):
    def __init__(self, master, n):
        super().__init__(master, '400x800', 'Choose Enemy Frame', (0,0))
        self.n = n
        idx = 0
        for i in range(0,2):
            for j in range(0,4):
                Button(self, image=enemy_image_lists[idx], command=lambda x=idx:self.return_enemy_type(x) ,bg="black").grid(row=i, column=j, ipadx=10, ipady=10)
                idx += 1
        for j in range(0,3):
            Button(self, image=enemy_image_lists[idx], command=lambda x=idx:self.return_enemy_type(x) ,bg="black").grid(row=2, column=j, ipadx=10, ipady=10)
            idx += 1
        for i in range(3,7):
            for j in range(0,4):
                Button(self, image=enemy_image_lists[idx], command=lambda x=idx:self.return_enemy_type(x) ,bg="black").grid(row=i, column=j, ipadx=10, ipady=10)
                idx += 1
        for j in range(0, 4):
            Button(self, image=enemy_image_lists[idx], command=lambda x=idx:self.return_enemy_type(x) ,bg="black").grid(row=7, column=j, ipadx=10, ipady=10)
            idx += 1
        
    def t_close_handler(self):
        root.attributes("-disabled", 0)
        self.destroy()
        
    def return_enemy_type(self, enemy_type):
        changecontent(enemy_type, self.n, 'readonly')
        self.t_close_handler()
        
class CreateEnemyFrame(EditFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.data = tree.item(tree.selection())['values']
        self.p = enemy_class_dicts.get(self.data[0],[]).copy()
        p = self.data[1:]
        for i in range(1, min(len(p), len(self.p)), 2):
            self.p[i]=p[i]
        self.Add_Row(0, "Node Type", "Entry", "CreateEnemy", init_state = "disabled")
        self.Add_Row(1, "Enemy Name", "ComboBox", self.data[0], lists=list(enemy_class_dicts.keys()), init_state='readonly')
        self.Add_Row(2, "Parameter", "Big_Button", func=self.parameter)
        self.Add_Row(3, "Save", "Big_Button", func=self.save)
        
    def parameter(self):
        SetParameter(root, self.p, 'input')
        
    def save(self):
        self.get_all_data()
        v = [self.value_dicts["Enemy Name"]]
        v += self.p
        tree.item(tree.selection(), text=f"Create Enemy \'{self.value_dicts["Enemy Name"]}\'", values=v)
        
class BossClassFrame(EditFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.data = tree.item(tree.selection())['values']
        self.Add_Row(0, "Node Type", "Entry", "Boss_Class", init_state="disabled")
        self.Add_Row(1, "Boss Name", "Entry", self.data[0])
        self.Add_Row(2, "Position", "Entry", self.data[1])
        self.Add_Row(3, "SpellCard BG", "ComboBox", self.data[2], lists=list(background_class_dicts.keys())+[''], init_state='readonly')
        self.Add_Row(4, "Idle Images", "ComboBox", self.data[3], lists=list(ImageManager.images['Mods'].keys())+[''], init_state='readonly')
        self.Add_Row(5, "Idle nCol", "Entry", self.data[4])
        self.Add_Row(6, "Idle nRow", "Entry", self.data[5])
        self.Add_Row(7, "Hitbox size", "Entry", self.data[6])
        self.Add_Row(8, "Animation Interval", "Entry", self.data[7])
        self.Add_Row(9, "Background", "ComboBox", self.data[8], lists=list(background_class_dicts.keys())+[''], init_state='readonly')
        self.Add_Row(10, "BGM", "ComboBox", self.data[9], lists=list(SoundManager.bgm_lists.keys())+[''], init_state='readonly')
        self.Add_Row(11, "Number of images", "Entry", self.data[10])
        self.Add_Row(12, "Left Images", "ComboBox", self.data[11], lists=list(ImageManager.images['Mods'].keys()), init_state='readonly')
        self.Add_Row(13, "Left nCol", "Entry", self.data[12])
        self.Add_Row(14, "Left nRow", "Entry", self.data[13])
        self.Add_Row(15, "Left nImg", "Entry", self.data[14])
        self.Add_Row(16, "Left Flip", "Entry", self.data[15])
        self.Add_Row(17, "Right Images", "ComboBox", self.data[16], lists=list(ImageManager.images['Mods'].keys()), init_state='readonly')
        self.Add_Row(18, "Right nCol", "Entry", self.data[17])
        self.Add_Row(19, "Right nRow", "Entry", self.data[18])
        self.Add_Row(20, "Right nImg", "Entry", self.data[19])
        self.Add_Row(21, "Right Flip", "Entry", self.data[20])
        self.Add_Row(22, "Save", "Big_Button", func=self.save)
        
    def save(self):
        self.get_all_data()
        v = []
        for i in self.value_dicts:
            v.append(self.value_dicts[i])
        boss_class_dicts.pop(self.data[0], None)
        name = v[0]
        boss_class_dicts[name] = 1
        tree.item(tree.selection(), values=v, text = "Boss Class '{}'".format(self.value_dicts["Boss Name"]))
        
class CreateBossFrame(EditFrame):
    def __init__(self, master):
        super().__init__(master)
        self.data = tree.item(tree.selection())['values']
        self.Add_Row(0, "Node Type", "Entry", "Create_Boss", init_state="disabled")
        self.Add_Row(1, "Boss Name", "ComboBox", self.data[0], lists=list(boss_class_dicts.keys()), init_state='readonly')
        self.Add_Row(2, "Save", "Big_Button", func=self.save)
        
    def save(self):
        self.get_all_data()
        tree.item(tree.selection(), values=self.value_dicts["Boss Name"], text = "Create Boss '{}'".format(self.value_dicts["Boss Name"]))
        
class MoveToFrame(EditFrame):
    def __init__(self, master):
        super().__init__(master)
        self.data = tree.item(tree.selection())['values']
        self.Add_Row(0, "Node Type", "Entry", "MoveTo", init_state="disabled")
        self.Add_Row(1, "Moving Frame", "Entry", self.data[0])
        self.Add_Row(2, "Target Position", "Entry", self.data[1])
        self.Add_Row(3, "Mode", "ComboBox", self.data[2], lists=["LINEAR","ACC","DCC","ACC_DCC"], init_state='readonly')
        self.Add_Row(4, "Save", "Big_Button", func=self.save)
        
    def save(self):
        self.get_all_data()
        v = []
        for i in self.value_dicts:
            v.append(self.value_dicts[i])
        name = "move to ({}) in {} frame(s)".format(v[1], v[0])
        tree.item(tree.selection(), values=v, text=name)
           
class SentenceFrame(EditFrame):
    def __init__(self, master):
        super().__init__(master)
        self.data = tree.item(tree.selection())['values']
        self.Add_Row(0, "Node Type", "Entry", "Sentence", init_state = "disabled")
        self.Add_Row(1, "Image", "Entry", self.data[0])
        self.Add_Row(2, "Position", "ComboBox", self.data[1], lists=["LEFT", "RIGHT"], init_state = "readonly")
        self.Add_Row(3, "Text", "Entry", self.data[2])
        self.Add_Row(4, "Scale", "Entry", self.data[3])
        self.Add_Row(5, "Save", "Big_Button", func=self.save)
        
    def save(self):
        self.get_all_data()
        v = []
        for i in self.value_dicts:
            v.append(self.value_dicts[i])
        name = "image:{}; place:{}; text:'{}'".format(v[0],v[1],v[2])
        tree.item(tree.selection(), values=v, text=name)
        
class SpellCardFrame(EditFrame):
    def __init__(self, master):
        super().__init__(master)
        self.data = tree.item(tree.selection())['values']
        self.Add_Row(0, "Node Type", "Entry", "SpellCard", init_state = "disabled")
        self.Add_Row(1, "Spell Card Name", "Entry", self.data[0])
        self.Add_Row(2, "Total Time (seconds)", "Entry", self.data[1])
        self.Add_Row(3, "Hit Point", "Entry", self.data[2])
        self.Add_Row(4, "Drop Power", "Entry", self.data[3])
        self.Add_Row(5, "Drop Point", "Entry", self.data[4])
        self.Add_Row(6, "Save", "Big_Button", func=self.save)
        
    def save(self):
        self.get_all_data()
        v = []
        for i in self.value_dicts:
            v.append(self.value_dicts[i])
        name = "Non Spell Card" if self.value_dicts["Spell Card Name"]=='' else "Spell Card '{}'".format(self.value_dicts['Spell Card Name'])
        tree.item(tree.selection(), text=name ,values=v)

class BossSpellFrame(EditFrame):
    def __init__(self, master):
        super().__init__(master)
        self.data = tree.item(tree.selection())['values']
        self.Add_Row(0, "Node Type", "Entry", "Boss Spell", init_state = 'disabled')
        self.Add_Row(1, "Position", "Entry", self.data[0])
        self.Add_Row(2, "Color(r,g,b)", "Entry", self.data[1], func=lambda x=2:changecolor(self.data[1], x), init_state = 'readonly')
        self.Add_Row(3, "Radius", "Entry", self.data[2])
        self.Add_Row(4, "Time", "Entry", self.data[3])
        self.Add_Row(5, "Mode", "ComboBox", self.data[4], lists=['START',"END"], init_state = 'readonly')
        self.Add_Row(6, "Save", "Big_Button", func=self.save)
        
    def save(self):
        self.get_all_data()
        v = []
        for i in self.value_dicts:
            v.append(self.value_dicts[i])
        name = "Boss Spell in {} frame(s)".format(v[3])
        tree.item(tree.selection(), values=v, text=name)
        
        
class TweeningFrame(EditFrame):
    def __init__(self, master):
        super().__init__(master)
        self.data = tree.item(tree.selection())['values']
        self.Add_Row(0, "Node Type", "Entry", "Tweening", init_state = "disabled")
        self.Add_Row(1, "Target", "Entry", self.data[0])
        self.Add_Row(2, "ValueName", "Entry", self.data[1])
        self.Add_Row(3, "TargetValue", "Entry", self.data[2])
        self.Add_Row(4, "Frame", "Entry", self.data[3])
        self.Add_Row(5, "Mode", "ComboBox", self.data[4], lists=["LINEAR","ACC","DCC","ACC_DCC"], init_state='readonly')
        self.Add_Row(6, "Save", "Big_Button", func=self.save)
        
    def save(self):
        self.get_all_data()
        v = []
        for i in self.value_dicts:
            v.append(self.value_dicts[i])
        name = "Create tweening to {}.{} to {} in {} frame(s) and '{}' mode".format(v[0],v[1],v[2],v[3],v[4])
        tree.item(tree.selection(), values=v)
        
class DeleteFrame(EditFrame):
    def __init__(self, master):
        super().__init__(master)
        self.data = tree.item(tree.selection())['values']
        self.Add_Row(0, "Node Type", "Entry", "Delete", init_state='disabled')
        self.Add_Row(1, "Object", "ComboBox", self.data[0], lists=['self','last'], init_state='readonly')
        self.Add_Row(2, "Save", "Big_Button", func=self.save)
        
    def save(self):
        self.get_all_data()
        v = []
        for i in self.value_dicts:
            v.append(self.value_dicts[i])
        tree.item(tree.selection(), values=v)
        
class ImageResourceEditFrame(EditFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.data = tree.item(tree.selection())['values']
        self.Add_Row(0, "Node Type", "Entry", "LoadImage", init_state = "disabled")
        self.Add_Row(1, "Path", "Entry", self.data[0], func=self.load, init_state = 'readonly')
        self.Add_Row(2, "Image Name", "Entry", self.data[1])
        self.Add_Row(3, "Crop Area", "Entry", self.data[2])
        self.Add_Row(4, "Zoom", "Entry", self.data[3])
        self.Add_Row(5, "Alpha", "Entry", self.data[4])
        self.Add_Row(6, "Rotation", "Entry", self.data[5])
        self.Add_Row(7, "Flip", "Entry", self.data[6])
        self.Add_Row(8, "Show", "Big_Button", func=self.show)
        self.Add_Row(9, "Save", "Big_Button", func=self.save)
        
    def save(self):
        self.get_all_data()
        v = []
        for i in self.value_dicts:
            v.append(self.value_dicts[i])
        ImageManager.images['Mods'].pop(str(self.data[1]), None)
        ImageManager.addImage(v[1], None)
        name = "load '{}' from '{}'".format(v[1], v[0])
        tree.item(tree.selection(), values=v, text=name)

    def load(self):
        filename = askopenfilename(filetypes=[("BMP", "*bmp"),("GIF", "*gif"),("JEPG", "*jepg"),("PNG", "*.png"),("JPG", "*.jpg")])
        if filename:
            filename = os.path.relpath(filename, os.getcwd())
            self.value_lists[1].config(state='normal')
            self.value_lists[1].delete(0, "end")
            self.value_lists[1].insert(0, filename)
            self.value_lists[1].config(state='readonly')
        
    def show(self):
        self.get_all_data()
        vars = {}
        size=None
        if self.value_dicts["Crop Area"]!='':
            size = return_value(self.value_dicts["Crop Area"], {})
        exec('result={}'.format(self.data[3]),globals(),vars)
        zoom = vars['result']
        exec('result={}'.format(self.data[4]),globals(),vars)
        alpha = vars['result']
        exec('result={}'.format(self.data[5]),globals(),vars)
        rotation = vars['result']
        exec('result=({})'.format(self.data[6]),globals(),vars)
        flip = vars['result']
        self.img = ImageManager.loadImage_Tkinter(self.value_dicts['Path'], size)
        ShowImageToplevel(root, self.img)
        
class ShowImageToplevel(EditToplevel):
    def __init__(self, master, img):
        super().__init__(master, '600x600', 'Image', (True, True))
        Button(self, image=img).pack(expand=True)
        
    def t_close_handler(self):
        root.attributes("-disabled", 0)
        self.destroy()

class SoundResourceEditFrame(EditFrame):
    def __init__(self, master):
        super().__init__(master)
        self.data = tree.item(tree.selection())['values']
        self.Add_Row(0, "Node Type", "Entry", "LoadSound", init_state='disabled')
        self.Add_Row(1, "Path", "Entry", self.data[0], func=self.load, init_state = 'readonly')
        self.Add_Row(2, "Sound Name", "Entry", self.data[1])
        self.Add_Row(3, "Save", "Big_Button", func = self.save)

    def load(self):
        filename = askopenfilename(filetypes=[("WAV", "*.wav"),("OGG", "*.ogg")])
        if filename:
            filename = os.path.relpath(filename, os.getcwd())
            self.value_lists[1].config(state='normal')
            self.value_lists[1].delete(0, "end")
            self.value_lists[1].insert(0, filename)
            self.value_lists[1].config(state='readonly')
        
    def save(self):
        self.get_all_data()
        v = []
        for i in self.value_dicts:
            v.append(str(self.value_dicts[i]))
        name = "load '{}' from '{}'".format(v[1], v[0])
        SoundManager.sound_list.pop(str(self.data[1]), None)
        SoundManager.addSound(str(self.value_dicts['Sound Name']), self.value_dicts['Path'])
        tree.item(tree.selection(), values=v, text=name)

class SoundEditFrame(EditFrame):
    def __init__(self, master):
        super().__init__(master)
        self.data = tree.item(tree.selection())['values']
        self.Add_Row(0, "Node Type: ", 'Entry', "Play Sound", init_state = "disabled")
        self.Add_Row(1, "Sound Type", "Entry", self.data[0], init_state="readonly", func=lambda x=root: ChooseSoundFrame(x))
        self.Add_Row(2, "Sound Volume", "Entry", self.data[1], init_state="readonly")
        self.Add_Row(3, "Save", "Big_Button", func=self.save)
        
    def save(self):
        self.get_all_data()
        data = [self.value_dicts["Sound Type"], self.value_dicts["Sound Volume"]]
        tree.item(tree.selection(), values=data)
            
class ChooseSoundFrame(Toplevel):
    def __init__(self, master):
        super().__init__(master, bg="#ffffff")
        self.master = master
        root.attributes("-disabled", 1)
        self.geometry("280x200")
        self.title("Choose Bullet")
        self.protocol("WM_DELETE_WINDOW", self.t_close_handler)
        self.resizable(False, False)
        self.sound_lists = list(SoundManager.sound_list.keys())
        self.menu = ctk.CTkOptionMenu(self, values=self.sound_lists, command=self.play_sound)
        self.menu.set(A_F.detail_frame.data[0])
        self.menu.pack()
        self.slider_1 = ctk.CTkSlider(self, from_=0, to=100, number_of_steps=100,command=self.slider_event)
        self.slider_1.set(int(A_F.detail_frame.value_lists[2].get()[0:-1]))
        #self.slider_1.set(A_F.detail_frame.data[1]*100)
        self.slider_1.pack()
        self.label = Label(self, text=f"Volume: {A_F.detail_frame.value_lists[2].get()}", font=("Arial", 16), relief='groove', bd=2, anchor="w")
        self.label.pack()
        
    def t_close_handler(self):
        root.attributes("-disabled", 0)
        changecontent(self.menu.get(), 1, 'readonly')
        changecontent(f'{self.slider_1.get():g}%', 2, 'readonly')
        self.destroy()
        
    def play_sound(self,value):
        value = self.menu.get()
        #print(type(value))
        SoundManager.play(value,self.slider_1.get()/100,0)
        
    def slider_event(self,value):
        #print(type(value))
        self.label.config(text="Volume: "+str(int(value))+'%')

class MusicResourceEditFrame(EditFrame):
    def __init__(self, master):
        super().__init__(master)
        self.data = tree.item(tree.selection())['values']
        self.Add_Row(0, "Node Type", "Entry", "LoadMusic", init_state='disabled')
        self.Add_Row(1, "Path", "Entry", self.data[0], func=self.load, init_state='readonly')
        self.Add_Row(2, "BGM Name", "Entry", self.data[1])
        self.Add_Row(3, "Save", "Big_Button", func = self.save)

    def load(self):
        filename = askopenfilename(filetypes=[("MP3", "*.mp3"),("OGG", "*.ogg")])
        if filename:
            filename = os.path.relpath(filename, os.getcwd())
            self.value_lists[1].config(state='normal')
            self.value_lists[1].delete(0, "end")
            self.value_lists[1].insert(0, filename)
            self.value_lists[1].config(state='readonly')

    def save(self):
        self.get_all_data()
        v = []
        for i in self.value_dicts:
            v.append(self.value_dicts[i])
        SoundManager.bgm_lists.pop(str(self.data[1]), None)
        SoundManager.addBGM(str(self.value_dicts['BGM Name']), self.value_dicts['Path'])
        name = "load '{}' from '{}'".format(v[1], v[0])
        tree.item(tree.selection(), values=v, text=name)

class MusicEditFrame(EditFrame):
    def __init__(self, master):
        super().__init__(master)
        self.data = tree.item(tree.selection())['values']
        self.Add_Row(0, "Node Type", "Entry", "Play Music", init_state = 'disabled')
        self.Add_Row(1, "Music Name", "ComboBox", self.data[0], lists=list(SoundManager.bgm_lists.keys()), init_state='readonly')
        self.Add_Row(2, "Play times", "Entry", self.data[1])
        self.Add_Row(3, "Volume", "Entry", self.data[2])
        self.Add_Row(4, "Save", "Big_Button", func=self.save)

    def save(self):
        self.get_all_data()
        v = []
        for i in self.value_dicts:
            v.append(str(self.value_dicts[i]))
        name = "Play Music '{}'".format(v[0])
        tree.item(tree.selection(), values=v, text=name)

class ItemEditFrame(EditFrame):
    def __init__(self, master):
        super().__init__(master)
        self.data = tree.item(tree.selection())['values']
        self.Add_Row(0, "Node Type", "Entry", "Create Item", init_state = 'disabled')
        self.Add_Row(1, "Item Type", "Entry", self.data[0], init_state='readonly', func=lambda:ChooseItemToplevel(root))
        self.Add_Row(2, "Position", "Entry", self.data[1])
        self.Add_Row(3, "Number", "Entry", self.data[2])
        self.Add_Row(4, "Save", "Big_Button", func=self.save)

    def save(self):
        self.get_all_data()
        v = []
        for i in self.value_dicts:
            v.append(self.value_dicts[i])
        name = "Create {} Item '{}' at ({})".format(v[2],v[0],v[1])
        tree.item(tree.selection(), values=v, text=name)

class ChooseItemToplevel(EditToplevel):
    def __init__(self, master):
        super().__init__(master, "600x600", 'Choose Item Type', (0,0))
        idx = 0
        for i in range(0,2):
            for j in range(0,5):
                Button(self, image=item_image_lists[idx], command=lambda x=idx:self.return_item_type(x) ,bg="black").grid(row=i, column=j, ipadx=10, ipady=10)
                idx += 1
    def return_item_type(self, type):
        changecontent(str(type), 1, 'readonly')
        self.t_close_handler()
    
class BackgroundClassFrame(EditFrame):
    def __init__(self, master):
        super().__init__(master)
        self.data = tree.item(tree.selection())['values']
        self.Add_Row(0, "Node Type", "Entry", "BackgroundClass", init_state='disabled')
        self.Add_Row(1, "Background Name", "Entry", self.data[0])
        self.Add_Row(2, "Save", "Big_Button", func = self.save)
        
    def save(self):
        self.get_all_data()
        v = []
        for i in self.value_dicts:
            v.append(self.value_dicts[i])
        background_class_dicts.pop(self.data[0], None)
        background_class_dicts[v[0]] = 1
        name = "Background_Class '{}'".format(v[0])
        tree.item(tree.selection(), values=v, text=name)
        
class CreateBackgroundFrame(EditFrame):
    def __init__(self, master):
        super().__init__(master)
        self.data = tree.item(tree.selection())['values']
        self.Add_Row(0, "Node Type", "Entry", "CreateBackground", init_state='disabled')
        self.Add_Row(1, "Background Name", "ComboBox", self.data[0], lists=list(background_class_dicts.keys()), init_state='readonly')
        self.Add_Row(2, "Save", "Big_Button", func = self.save)
        
    def save(self):
        self.get_all_data()
        v = []
        for i in self.value_dicts:
            v.append(self.value_dicts[i])
        name = "Background Class '{}'".format(v[0])
        tree.item(tree.selection(), values=v, text=name)
        
class LayerEditFrame(EditFrame):
    def __init__(self, master):
        super().__init__(master)
        self.data = tree.item(tree.selection())['values']
        self.Add_Row(0, "Node Type", "Entry", "Layer", init_state='disabled')
        self.Add_Row(1, "Image", "ComboBox", self.data[0], lists=list(ImageManager.images['Mods'].keys()), init_state='readonly')
        self.Add_Row(2, "Is tile", "Entry", self.data[1])
        self.Add_Row(3, "Position", "Entry", self.data[2])
        self.Add_Row(4, "Speedx", "Entry", self.data[3])
        self.Add_Row(5, "Speedy", "Entry", self.data[4])
        self.Add_Row(6, "Save", "Big_Button", func=self.save)
        
    def save(self):
        self.get_all_data()
        v = []
        for i in self.value_dicts:
            v.append(self.value_dicts[i])
        name = "image'{}'".format(v[0])
        tree.item(tree.selection(), values=v, text=name)

class DataTreeFrame(Frame):
    def __init__(self, master):
        super().__init__(master, width=1400, height=800,relief="solid", bd=2)
        self.master = master
    
    def debug(self):
        self.streamHandlerBox = LoggerBox(self, width=50, height=12, font=("Arial", 16), relief='groove', bd=2)
        self.streamHandlerBox.pack(side=TOP,fill=X)
        self.log1=logging.getLogger('log1')
        self.log1.setLevel(logging.INFO)
        handler = logging.StreamHandler(self.streamHandlerBox)
        sys.stdout = Redirect(self.streamHandlerBox)
        sys.stderr = Redirect(self.streamHandlerBox)
        self.log1.addHandler(handler)
        self.streamHandlerBox.configure(state='disabled')

class DataTree(ttk.Treeview):
    def __init__(self, master, has):
        super().__init__(master)
        self.master = master
        self.copied_idx = 0
        self.copied_nodes = {}
        self.f_idx = 0
        self.heading("#0",text="Files")
        if not has:
            self.insert("", iid='0', index="end", image=image_lists['setting'+'small'], text="Setting", values=["50","30","60","1000","60","10","150","30","False"], tags='Setting', open=True)
            self.insert("0", iid='1', index="end", image=image_lists['folder'+'small'], text="Resources", values=["Resources"], tags='Folder')
            self.insert("0", iid='28', index="end", image=image_lists['folder'+'small'], text="Classes", values=["Classes"], tags='Folder')
            self.insert("0", iid='2', index="end", image=image_lists['folder'+'small'], text="Main", values=["Main"], tags='Folder', open=True)
            
            self.insert('2', iid='3', index="end", image=image_lists['rank'+'small'], text='Rank "Easy"', values=['Easy','0,144,44'], tags='Rank', open=0)
            self.insert('3', iid='4', index="end", image=image_lists['stage'+'small'], text='Stage "Stage1"', values=['Stage1','Work',''], tags='Stage', open=True)
            self.insert('4', iid='5', index="end", image=image_lists['thread'+'small'], text='Create Thread', tags='Thread', open=True)
            self.insert('5', iid='6', index="end", image=image_lists['stage_title'+'small'], text='Show Stage Title', values=['60'], tags='Stage_Title')
            self.insert('5', iid='7', index="end", image=image_lists['wait'+'small'], text='Wait 60 frame(s)', tags='Wait', values=[60])
            
            self.insert('2', iid='8', index="end", image=image_lists['rank'+'small'], text='Rank "Normal"', values=['Normal','0, 84, 178'], tags='Rank', open=0)
            self.insert('8', iid='9', index="end", image=image_lists['stage'+'small'], text='Stage "Stage1"', values=['Stage1','Work',''], tags='Stage', open=True)
            self.insert('9', iid='10', index="end", image=image_lists['thread'+'small'], text='Create Thread', tags='Thread', open=True)
            self.insert('10', iid='11', index="end", image=image_lists['stage_title'+'small'], text='Show Stage Title', values=['60'], tags='Stage_Title')
            self.insert('10', iid='12', index="end", image=image_lists['wait'+'small'], text='Wait 60 frame(s)', tags='Wait', values=[60])
            
            self.insert('2', iid='13', index="end", image=image_lists['rank'+'small'], text='Rank "Hard"', values=['Hard','0,9,197'], tags='Rank', open=0)
            self.insert('13', iid='14', index="end", image=image_lists['stage'+'small'], text='Stage "Stage1"', values=['Stage1','Work',''], tags='Stage', open=True)
            self.insert('14', iid='15', index="end", image=image_lists['thread'+'small'], text='Create Thread', tags='Thread', open=True)
            self.insert('15', iid='16', index="end", image=image_lists['stage_title'+'small'], text='Show Stage Title', values=['60'], tags='Stage_Title')
            self.insert('15', iid='17', index="end", image=image_lists['wait'+'small'], text='Wait 60 frame(s)', tags='Wait', values=[60])
            
            self.insert('2', iid='18', index="end", image=image_lists['rank'+'small'], text='Rank "Lunatic"', values=['Lunatic','151,0,160'], tags='Rank', open=0)
            self.insert('18', iid='19', index="end", image=image_lists['stage'+'small'], text='Stage "Stage1"', values=['Stage1','Work',''], tags='Stage', open=True)
            self.insert('19', iid='20', index="end", image=image_lists['thread'+'small'], text='Create Thread', tags='Thread', open=True)
            self.insert('20', iid='21', index="end", image=image_lists['stage_title'+'small'], text='Show Stage Title', values=['60'], tags='Stage_Title')
            self.insert('20', iid='22', index="end", image=image_lists['wait'+'small'], text='Wait 60 frame(s)', tags='Wait', values=[60])
            
            self.insert('2', iid='23', index="end", image=image_lists['rank'+'small'], text='Rank "Extra"', values=['Extra','189,0,0'], tags='Rank', open=0)
            self.insert('23', iid='24', index="end", image=image_lists['stage'+'small'], text='Stage "Stage1"', values=['Stage1','Work',''], tags='Stage', open=True)
            self.insert('24', iid='25', index="end", image=image_lists['thread'+'small'], text='Create Thread', tags='Thread', open=True)
            self.insert('25', iid='26', index="end", image=image_lists['stage_title'+'small'], text='Show Stage Title', values=['60'], tags='Stage_Title')
            self.insert('25', iid='27', index="end", image=image_lists['wait'+'small'], text='Wait 60 frame(s)', tags='Wait', values=[60])
        self.bind("<ButtonRelease-1>", self.show_details)
        self.bind("<Key-BackSpace>", self.remove)
        
    def show_details(self, event):
        item_iid = self.selection()[0]
        if item_iid:
            print("Selected Node: {}".format(self.item(item_iid)["tags"][0]))
            A_F.details_identify(item_iid, self.item(item_iid)["tags"][0])
            
    def copy_nodes(self):
        idx = self.selection()[0]
        self.copied_nodes = self.visit_nodes(idx, {})
        print("Copied")
    
    def visit_nodes(self, idx, nodes):
        tag = self.item(idx)['tags'][0]
        image = self.item(idx)['image'][0]
        text = self.item(idx)['text']
        value = self.item(idx)['values']
        nodes['message']=(image, text, value, tag)
        a = self.get_children(idx)
        idx = 0
        for i in a:
            nodes[idx]=self.visit_nodes(i, {})
            idx += 1
        return nodes
    
    def paste_nodes(self):
        item_iid = self.selection()[0]
        parent_iid = self.parent(item_iid)
        if insert_mode == 1:
            self.insert(parent_iid, iid='f'+str(self.f_idx), index=tree.index(self.selection()), text=self.copied_nodes['message'][1], image=self.copied_nodes['message'][0], tags=self.copied_nodes['message'][3], values=self.copied_nodes['message'][2])
        elif insert_mode == 2:
            if tree.item(tree.selection())['tags'][0] in ('Folder','Repeat','Rank','Stage','Thread','Enemy_Class','Bullet_Class','If','True','False'):
                self.insert(item_iid, iid='f'+str(self.f_idx), index='end', text=self.copied_nodes['message'][1], image=self.copied_nodes['message'][0], tags=self.copied_nodes['message'][3], values=self.copied_nodes['message'][2])
        elif insert_mode == 3:
            self.insert(parent_iid, iid='f'+str(self.f_idx), index=tree.index(self.selection())+1, text=self.copied_nodes['message'][1], image=self.copied_nodes['message'][0], tags=self.copied_nodes['message'][3], values=self.copied_nodes['message'][2])
        self.paste_nodes_children(self.copied_nodes)
        print("Pasted")

    def paste_nodes_children(self, nodes):
        now_idx = 'f'+str(self.f_idx)
        self.f_idx += 1
        for i in range(0, len(nodes)-1):
            self.insert(now_idx, iid='f'+str(self.f_idx), index='end', text=nodes[i]['message'][1], image=nodes[i]['message'][0], tags=nodes[i]['message'][3], values=nodes[i]['message'][2])
            self.paste_nodes_children(nodes[i])
            self.f_idx += 1
        
    def rename(self, name):
        self.item(self.selection(), text=name)
        
    def remove(self, event=None):
        des = self.selection()[0]
        if self.item(des)['tags'][0] in ('True','False'):
            return
        self.delete(des)
        print("Deleted")
        
    def checkInsert(self, type):
        pid = self.parent(self.selection())
        index = self.index(self.selection())
        if insert_mode == 1:
            self.AddData(pid, index, type)
            print("Inserted Up")
        elif insert_mode == 2:
            if tree.item(tree.selection())['tags'][0] in ('Folder','Repeat','Rank','Stage','Thread','Enemy','Enemy_Class','Bullet_Class','Boss_Class','SpellCard','Dialogue','Background_Class','Layer','Function','True','False'):
                self.AddData(self.selection(), 'end', type)
                print("Inserted Inside")
        elif insert_mode == 3:
            self.AddData(pid, index+1, type)
            print("Inserted Down")
    
    def AddData(self, parent_id, index, type, name=None, values=None):
        pid = 'f'+str(self.f_idx)
        self.insert(parent_id, iid=pid, index=index, text=insert_value_dicts[type]['name'] if name is None else name, image=image_lists[type.lower()+'small'], tags=type, values=insert_value_dicts[type]['values'] if values is None else values)
        self.f_idx += 1
        if type=='Boss_Class':
            self.AddData(pid, 'end', 'Movement')
            self.AddData(pid, 'end', 'Dialogue')
            self.AddData(pid, 'end', 'SpellCard')
        elif type in ('Enemy_Class', 'Bullet_Class', 'Object_Class'):
            self.AddData(pid, 'end', 'Function', 'update', ['update'])
            self.AddData(pid, 'end', 'Function', 'kill', ['kill'])
        elif type in ('SpellCard','Dialogue','Enemy','Stage'):
            self.AddData(pid, 'end', 'Thread')
        elif type=='Rank':
            self.AddData(pid, 'end', 'Stage')
        elif type=='Background_Class':
            self.AddData(pid, 'end', 'Layer')
        elif type=='If':
            self.AddData(pid, 'end', 'True')
            self.AddData(pid, 'end', "False")

image_lists = ImageManager.edit_mode_loadImage()
bullet_image_lists = ImageManager.editor_loadImage_bullet()
enemy_image_lists = ImageManager.editor_loadImage_enemy()
item_image_lists = ImageManager.editor_loadImage_items()
enemy_class_dicts = {}
boss_class_dicts = {}
bullet_class_dicts = {}
object_class_dicts = {}
background_class_dicts = {}
insert_value_dicts = {
    'Folder':{'name':'new_folder','values':['new_folder']},
    'Code':{'name':'code','values':['']},
    'Comment':{'name':'Comment','values':['']},
    'If':{'name':'If True==True','values':['True==True']},
    'True':{'name':'True','values':[]},
    'False':{'name':'False','values':[]},
    'Rank':{'name':"Rank 'Default'",'values':['Default','255,255,255']},
    'Stage':{'name':"Stage 'Default'",'values':['Default','Default','']},
    'Stage_Title':{'name':'Show Stage Title', 'values':[]},
    'Thread':{'name':'Thread','values':[]},
    'Wait':{'name':'Wait 60 frame(s)','values':['60']},
    'Repeat':{'name':'Repeat infinite time(s); 3 frame(s) interval','values':['-1','3','a','3','1']},
    'Break':{'name':'Break Current Repeat','values':[]},
    'Continue':{'name':'Continue Current Repeat','values':[]},
    'Enemy':{'name':'Create Simple Enemy','values':[0,'192,224','0','5','300','0','0']},
    'Enemy_Class':{'name':"Enemy Class 'Default'",'values':['Default', 0, '192,224', '0', '5', '300', '0', '0', []]},
    'Create_Enemy':{'name':"Create Enemy 'Default'",'values':['Default']},
    'Clear_Enemy':{'name':"Clear All Enemy",'values':[]},
    'Create_Boss':{'name':"Create Boss 'Default'",'values':['Default']},
    'Boss_Class':{'name':"Boss Class 'Default'",'values':['Default', "192,224", "Default", "Default", "1", "1", "128,128", "8", "Default", "Default", "1", "", "", "", "", "", "", "", "", "", ""]},
    'SpellCard':{'name':"Non Spellcard",'values':['','30','10000','0','0']},
    'Dialogue':{'name':"Dialogue",'values':[]},
    'Sentence':{'name':"Sentence (image:'Default'; pos:LEFT; text:'Test'; scale:1.0)", 'values':['Default','LEFT','Test','1.0']},
    'Movement':{'name':"Move to (192,140) in 60 frame(s) with 'LINEAR' mode", 'values':['60','192,140','LINEAR']},
    'Boss_Spell':{'name':"Boss Spell at (self.x,self.y); color:(255,0,0); radius:(500); frames:60; mode:START",'values':['self.x,self.y','255,0,0','500','60','START']},
    'Boss_Explosion':{'name':'Boss Explosion','values':[]},
    'Bullet':{'name':"Create Simple Bullet",'values':["Scale","white",'192,224','10','0',True,False,True,False,'-1','0','0','0','0']},
    'Bullet_Class':{'name':"Bullet Class 'Default'",'values':['Default',"Scale","white",'192,224','10','0',True,False,True,False,'-1','0','0','0','0',[]]},
    'Create_Bullet':{'name':"Create Bullet 'Default'",'values':['Default']},
    'Clear_Bullet':{'name':"Clear All Bullet",'values':['False']},
    'Sound':{'name':"Play sound 'pause_sound'; volume: 50%",'values':['pause_sound','50%']},
    'Music':{'name':"Play Music 'Sample'",'values':['Sample',-1,1.0]},
    'Create_Background':{'name':"Create Background 'Default'", 'values':['Default']},
    'Clear_Background':{'name':"Clear All Background", 'values':[]},
    'Background_Class':{'name':"Background Class 'Default'",'values':['Default']},
    'Layer':{'name':"Layer (image:''; istile:True; pos:(0,0); speedx:0; speedy:0)",'values':['','True','0,0','0','0']},
    'Image_Resource':{'name':"Load Image 'default' from 'mods/resource/'",'values':['mods/resource/', 'default', '', '1.0', '255', '0', 'False, False']},
    'Sound_Resource':{'name':"Load Sound 'default' from 'mods/resource/'",'values':['mods/resource/', 'default']},
    'Music_Resource':{'name':"Load Music 'default' from 'mods/resource/'",'values':['mods/resource/', 'default']},
    'Var':{'name':"Set a = None",'values':['a','None']},
    'Velocity':{'name':"Set last's velocity = (v:0; a:0)",'values':['last',0,0]},
    'Tweening':{'name':"Create tweening to self.a from 0 to 60 in 'LINEAR' mode", 'values':['self','a','0','60','LINEAR']},
    'Delete':{'name':"Delete Object 'last'",'values':['last']},
    'Item':{'name':"Create 1 Item '0' at (192,224)",'values':[0, '192,224', 1]},
    'Setting':{'name':"Setting",'values':['50','30','40','10','1000','60','10','150','30']},
    'Object_Class':{'name':"Object Class 'Default'", 'values':['Default','Enemy','Default','16,16','100','192,224','5','0','0','0','False','1.0','1.0','-1']},
    'Create_Object':{'name':"Create Object 'Default'", 'values':['Default']}
}
menubar = MenuBar(root)
root.config(menu=menubar)

def changecontent(content, n, state):
    A_F.detail_frame.value_lists[n].config(state='normal')
    A_F.detail_frame.value_lists[n].delete(0, 'end')
    A_F.detail_frame.value_lists[n].insert(0, content)
    A_F.detail_frame.value_lists[n].config(state=state)

def changecolor(color, n):
    e = color.split(',')
    cp = '#'
    for i in range(3):
        f = str(hex(int(e[i])))[2:]
        if len(f)==1:
            f='0'+f
        cp+=f
    choosecolor = colorchooser.askcolor(
        title="Choose Color",
        initialcolor=cp,
        parent=root
    )
    if choosecolor[1] is None:
        return
    r = choosecolor[1][1:3]
    g = choosecolor[1][3:5]
    b = choosecolor[1][5:7]
    r = int(r, 16)
    g = int(g, 16)
    b = int(b, 16)
    changecontent(str((r,g,b))[1:-1], n, 'readonly')

def return_value(statement, vars):
    exec('result={}'.format(statement), globals(), vars)
    return vars['result']

def main():
    menubar.new(0)
    root.mainloop()
    

if __name__ == '__main__':
    main()