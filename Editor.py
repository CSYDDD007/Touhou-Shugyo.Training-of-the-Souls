import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
from tkinter import *
from tkinter import font
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfile 

import json
import random
from database import edit_mode_loadImage
import SoundEffect
import pygame
from global_var import *
SoundEffect.loadSound()
ctk.set_default_color_theme("dark-blue")  
ctk.set_appearance_mode("light")
root = ctk.CTk()
root.title("sba_stg editor")
root.iconbitmap('resource/image/icon_aEm_icon.ico')
root.geometry("1600x900")
#root.resizable(False, False)

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
        self.Tutorial.add_command(label="Introduction", command=lambda:IntroductionFrame(root))
        self.Tutorial.add_command(label="Basic", command=lambda:BasicFrame(root))
        self.Tutorial.add_command(label="Advanced", command=lambda:AdvancedFrame(root))
        self.add_cascade(label="Help", menu=self.Tutorial)
        self.Test = Menu(self, tearoff=False)
        self.Test.add_command(label="Debug", command=self.debug)
        self.Test.add_command(label="Test", command=self.test)
        self.add_cascade(label="Test", menu=self.Test)
        
    def debug(self):
        import trick
        trick.main()
    
    def test(self):
        root.attributes("-disabled", 1)
        import th_SBA
        th_SBA.main()
        pygame.mixer.init()
        pygame.mixer.set_num_channels(60)
        SoundEffect.loadSound()
        root.attributes("-disabled", 0)
        
    def new(self, has):
        for widget in root.winfo_children():
            print(widget.widgetName)
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
        DT_F.config(bg="#ffffff")

    def load(self):
        filename = askopenfilename(filetypes=[("SBA STG Data", "*.sba_dat")])
        if filename:
            with open(filename, 'r', encoding='utf-8') as f1:
                data = json.load(f1)
            #print(len(data))
            self.new(True)
            self.my_iid=0
            self.loading(data,'')
            #print(data['0']['message'])
            
    def loading(self,data,parent_id):
        if parent_id=='':
            length = len(data)
        else:
            length = len(data)-1
        #tree.insert(parent_id, 'end', text=data[keys][], values=data)
        for i in range(0,length):
            keys = str(i)
            tree.insert(parent_id, 'end', text=data[keys]['message']['text'], values=data[keys]['message']['values'], image=data[keys]['message']['image'], tags=data[keys]['message']['tags'], iid=str(self.my_iid), open=True)
            self.my_iid += 1
            if len(data[keys])>1:
                self.loading(data[keys], self.my_iid-1)
            
    def save(self): 
        files = [('SBA STG Data', '*.sba_dat')]
        filepath = asksaveasfile(filetypes = files, defaultextension = files)
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
            print(dicts)
            json.dump(dicts, filepath, ensure_ascii=False, indent=4)
        else:
            return dicts
                
class IntroductionFrame(Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        root.attributes("-disabled", 1)
        self.geometry("1000x600")
        self.title("Introduction")
        self.protocol("WM_DELETE_WINDOW", self.t_close_handler)
        
    def t_close_handler(self):
        root.attributes("-disabled", 0)
        self.destroy()
        
class BasicFrame(Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        root.attributes("-disabled", 1)
        self.geometry("1000x600")
        self.title("Basic")
        self.protocol("WM_DELETE_WINDOW", self.t_close_handler)
        
    def t_close_handler(self):
        root.attributes("-disabled", 0)
        self.destroy()
        
class AdvancedFrame(Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        root.attributes("-disabled", 1)
        self.geometry("1000x600")
        self.title("Advanced")
        self.protocol("WM_DELETE_WINDOW", self.t_close_handler)
        
    def t_close_handler(self):
        root.attributes("-disabled", 0)
        self.destroy()

button_choosed = StringVar()
insert_mode=0
class OverallBar(Frame):
    def __init__(self, master):
        super().__init__(master, width=1600, height=50)
        self.master = master
        ToolBar(self).pack(side=LEFT)
        Button(self,text="Delete",command=tree.remove,image=image_lists['object'],compound="top").pack(side=LEFT,padx=5)
        a = ttk.Radiobutton(self, text='Add_Up', style='Toolbutton', width=10,image=image_lists['object'],compound="top", value='Add_Up', variable=button_choosed, command=self.change_mode)
        a.pack(side=LEFT,padx=5)
        b = ttk.Radiobutton(self, text='Add_Inside', style='Toolbutton', width=10,image=image_lists['object'],compound="top", value='Add_Inside', variable=button_choosed, command=self.change_mode)
        b.pack(side=LEFT,padx=5)
        c = ttk.Radiobutton(self, text='Add_Down', style='Toolbutton', width=10,image=image_lists['object'],compound="top", value='Add_Down', variable=button_choosed, command=self.change_mode)
        c.pack(side=LEFT,padx=5)
        
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
        self.GeneralFrame = GeneralFrame()
        self.StageFrame = StageFrame()
        self.TimesFrame = TimesFrame()
        self.EnemyFrame = EnemyFrame()
        self.BulletFrame = BulletFrame()
        self.AudioFrame = AudioFrame()
        self.BackgroundFrame = Frame()
        self.add(self.GeneralFrame, text='General')
        self.add(self.StageFrame, text='Stage')
        self.add(self.TimesFrame, text='Times')
        self.add(self.EnemyFrame, text='Enemy')
        self.add(self.BulletFrame, text='Bullet')
        self.add(self.AudioFrame, text='Audio')
        self.add(self.BackgroundFrame, text='Background')
        #self.pack(side=TOP, fill=BOTH, expand=True)
        #Button(self,text="print",command=print_selection).pack()
        self.btn=Button(self.EnemyFrame,text="print",command=print_selection)
        self.btn.pack(side=LEFT)
        self.ctn=Button(self.EnemyFrame,text="check",command=lambda x='':check(''))
        self.ctn.pack(side=LEFT)
        
class GeneralFrame(Frame):
    def __init__(self):
        super().__init__()
        self.ftn=Button(self,image=image_lists['folder'],command=lambda x='Folder': tree.checkInsert(x,['new_folder']))
        self.ftn.pack(side=LEFT)
        self.atn=Button(self,image=image_lists['action'],command=lambda x='Action': tree.checkInsert(x,[]))
        self.atn.pack(side=LEFT)
        
class StageFrame(Frame):
    def __init__(self):
        super().__init__()
        self.ftn=Button(self,image=image_lists['stagegroup'],command=lambda x='StageGroup': tree.checkInsert(x,['Default']))
        self.ftn.pack(side=LEFT)
        self.atn=Button(self,image=image_lists['stage'],command=lambda x='Stage': tree.checkInsert(x,[1]))
        self.atn.pack(side=LEFT)
        
class TimesFrame(Frame):
    def __init__(self):
        super().__init__()
        self.ftn=Button(self,image=image_lists['wait'],command=lambda x='Wait': tree.checkInsert(x,[60]))
        self.ftn.pack(side=LEFT)
        self.atn=Button(self,image=image_lists['repeat'],command=lambda x='Repeat': tree.checkInsert(x,[3,-1,{}]))
        self.atn.pack(side=LEFT)
        
class EnemyFrame(Frame):
    def __init__(self):
        super().__init__()
        self.ftn=Button(self,image=image_lists['enemy'],command=lambda x='Enemy': tree.checkInsert(x))
        self.ftn.pack(side=LEFT)
        
class BulletFrame(Frame):
    def __init__(self):
        super().__init__()
        self.ftn=Button(self,image=image_lists['bullet'],command=lambda x='Bullet': tree.checkInsert(x,[0,0,'0,0','10','0',True,False,True,'100',False,'0','0','0']))
        self.ftn.pack(side=LEFT)
        
class AudioFrame(Frame):
    def __init__(self):
        super().__init__()
        self.ftn=Button(self,image=image_lists['audio'],command=lambda x='Audio': tree.checkInsert(x,['Sample',-1]))
        self.ftn.pack(side=LEFT)
        self.atn=Button(self,image=image_lists['sound'],command=lambda x='Sound': tree.checkInsert(x,['pause_sound',50]))
        self.atn.pack(side=LEFT)
        
                
class AttributeFrame(Frame):
    def __init__(self, master):
        super().__init__(master,width=500, height=800,relief="groove", bd=2)
        self.master = master
        self.text = Text(self, width=41,height=5, font=("Arial", 16), relief='groove', bd=2)
        self.text.pack(side=TOP,fill=X)
        self.detail_frame = EmptyEditFrame(self)
        self.iid = None
        self.detail_frame.pack(side=TOP, fill=BOTH, expand=True)
        
    def details_identify(self, iid, tags):
        
        if iid==self.iid:
            return
        if self.detail_frame:
            self.detail_frame.pack_forget()
            print('destroy')
        
        if tags == 'new_object' or tags == None:
            self.detail_frame = EmptyEditFrame(self)
        elif tags == 'Folder':
            self.detail_frame = FolderEditFrame(self)
            print(0)
        elif tags == 'Bullet':
            self.detail_frame = BulletEditFrame(self)
            print(1)
        elif tags == 'Wait':
            self.detail_frame = WaitEditFrame(self)
            print(2)
        elif tags == 'Repeat':
            self.detail_frame = RepeatEditFrame(self)
            print(3)
        elif tags == 'Sound':
            self.detail_frame = SoundEditFrame(self)
        self.iid = iid
        self.detail_frame.pack(side=TOP, fill=BOTH, expand=True)
        
class EmptyEditFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, width=500, height=800, fg_color="transparent")
        self.master = master
        for i in range(16):
            Label(self, text="                ", font=("Arial", 16), relief='groove', bd=2, anchor="w").grid(row=i, column=0, ipadx=10, ipady=10, sticky='nswe')
            Label(self, text="                                                  ", font=("Arial", 16), relief='groove', bd=2, bg='#ffffff', anchor="w").grid(row=i, column=1, ipadx=10, ipady=10, sticky='nswe')
            Button(self, text="...").grid(row=i, column=2, ipadx=10, ipady=10, sticky='nswe')
        
    def gets(self):
        content = self.text.get("1.0", "end-1c")
        exec(content)
        
class FolderEditFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, width=500, height=800, fg_color="transparent")
        self.master = master
        Label(self, text="Filename", font=("Arial", 16), relief='groove', bd=2, anchor="w").grid(row=0, column=0, ipadx=10, ipady=10, sticky='nswe')
        self.name = Entry(self, font=("Arial", 16), relief='groove', bd=2, bg='#ffffff')
        self.name.grid(row=0, column=1, ipadx=10, ipady=10, sticky='nswe')
        self.name.insert(0,tree.item(tree.selection())['text'])
        Button(self, text="...").grid(row=0, column=2, ipadx=10, ipady=10, sticky='nswe')
        for i in range(1,16):
            Label(self, text="                ", font=("Arial", 16), relief='groove', bd=2, anchor="w").grid(row=i, column=0, ipadx=10, ipady=10, sticky='nswe')
            Label(self, text="                                                  ", font=("Arial", 16), relief='groove', bd=2, bg='#ffffff', anchor="w").grid(row=i, column=1, ipadx=10, ipady=10, sticky='nswe')
            Button(self, text="...").grid(row=i, column=2, ipadx=10, ipady=10, sticky='nswe')
            
class WaitEditFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, width=500, height=800, fg_color="transparent")
        self.master = master
        Label(self, text="Wait Time", font=("Arial", 16), relief='groove', bd=2, anchor="w").grid(row=0, column=0, ipadx=10, ipady=10, sticky='nswe')
        self.time = Entry(self, font=("Arial", 16), relief='groove', bd=2, bg='#ffffff')
        self.time.grid(row=0, column=1, ipadx=10, ipady=10, sticky='nswe')
        self.time.insert(0,tree.item(tree.selection())['values'][0])
        Button(self, text="...").grid(row=0, column=2, ipadx=10, ipady=10, sticky='nswe')
        for i in range(1,16):
            Label(self, text="                ", font=("Arial", 16), relief='groove', bd=2, anchor="w").grid(row=i, column=0, ipadx=10, ipady=10, sticky='nswe')
            Label(self, text="                                                  ", font=("Arial", 16), relief='groove', bd=2, bg='#ffffff', anchor="w").grid(row=i, column=1, ipadx=10, ipady=10, sticky='nswe')
            Button(self, text="...").grid(row=i, column=2, ipadx=10, ipady=10, sticky='nswe')
            
class RepeatEditFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, width=500, height=800, fg_color="transparent")
        self.master = master
        self.var_lists = []
        self.data = tree.item(tree.selection())['values']
        print(self.data)
        Label(self, text="Number of times", font=("Arial", 16), relief='groove', bd=2, anchor="w").grid(row=0, column=0, ipadx=10, ipady=10, sticky='nswe')
        self.time = Entry(self, font=("Arial", 16), relief='groove', bd=2, bg='#ffffff')
        self.time.grid(row=0, column=1, ipadx=10, ipady=10, sticky='nswe')
        self.time.insert(0,self.data[0])
        Button(self, text="...").grid(row=0, column=2, ipadx=10, ipady=10, sticky='nswe')
        Label(self, text="Interval (in frames)", font=("Arial", 16), relief='groove', bd=2, anchor="w").grid(row=1, column=0, ipadx=10, ipady=10, sticky='nswe')
        self.interval = Entry(self, font=("Arial", 16), relief='groove', bd=2, bg='#ffffff')
        self.interval.grid(row=1, column=1, ipadx=10, ipady=10, sticky='nswe')
        self.interval.insert(0,self.data[1])
        Button(self, text="...").grid(row=1, column=2, ipadx=10, ipady=10, sticky='nswe')
        
        self.var_lists.append(Button(self, text="Add Variable", font=("Arial", 16), command=self.Add_Variable))
        self.var_lists[-1].grid(row=2, column=0, columnspan=3, ipadx=10, ipady=10, sticky='nswe')
        self.data[2] = self.data[2].replace("'","\"")
        self.data[2] = json.loads(self.data[2])
        self.no_var = len(self.data[2])
        print(type(self.data[2]))
        for i in range(3,16):
            Label(self, text="                ", font=("Arial", 16), relief='groove', bd=2, anchor="w").grid(row=i, column=0, ipadx=10, ipady=10, sticky='nswe')
            Label(self, text="                           ", font=("Arial", 16), relief='groove', bd=2, bg='#ffffff', anchor="w").grid(row=i, column=1, ipadx=10, ipady=10, sticky='nswe')
            Button(self, text="...").grid(row=i, column=2, ipadx=10, ipady=10, sticky='nswe')
        self.var_lists.append(Button(self, text="Save", font=("Arial", 16), command=self.Save))
        self.var_lists[-1].grid(row=3, column=0, columnspan=3, ipadx=10, ipady=10, sticky='nswe')
            
    def Add_Variable(self):
        if self.no_var < 1:
            for i in range(2):
                self.var_lists[-1].destroy()
                del self.var_lists[-1]
        else:
            for i in range(3):
                self.var_lists[-1].destroy()
                del self.var_lists[-1]
        #return
        self.no_var+=1
        self.var_lists.append(Label(self, text=f"Var {self.no_var} Name", font=("Arial", 16), relief='groove', bd=2, anchor="w"))
        self.var_lists[-1].grid(row=3*(self.no_var-1)+2, column=0, ipadx=10, ipady=10, sticky='nswe')
        self.var_lists.append(Entry(self, font=("Arial", 16), relief='groove', bd=2, bg='#ffffff'))
        self.var_lists[-1].grid(row=3*(self.no_var-1)+2, column=1, ipadx=10, ipady=10, sticky='nswe')
        self.var_lists.append(Button(self, text="..."))
        self.var_lists[-1].grid(row=3*(self.no_var-1)+2, column=2, ipadx=10, ipady=10, sticky='nswe')
        print(self.no_var)
        self.var_lists.append(Label(self, text=f"Var {self.no_var} Value", font=("Arial", 16), relief='groove', bd=2, anchor="w"))
        self.var_lists[-1].grid(row=3*(self.no_var-1)+3, column=0, ipadx=10, ipady=10, sticky='nswe')
        self.var_lists.append(Entry(self, font=("Arial", 16), relief='groove', bd=2, bg='#ffffff'))
        self.var_lists[-1].grid(row=3*(self.no_var-1)+3, column=1, ipadx=10, ipady=10, sticky='nswe')
        self.var_lists.append(Button(self, text="..."))
        self.var_lists[-1].grid(row=3*(self.no_var-1)+3, column=2, ipadx=10, ipady=10, sticky='nswe')
        print(self.no_var)
        self.var_lists.append(Label(self, text=f"Var {self.no_var} Increment", font=("Arial", 16), relief='groove', bd=2, anchor="w"))
        self.var_lists[-1].grid(row=3*(self.no_var-1)+4, column=0, ipadx=10, ipady=10, sticky='nswe')
        self.var_lists.append(Entry(self, font=("Arial", 16), relief='groove', bd=2, bg='#ffffff'))
        self.var_lists[-1].grid(row=3*(self.no_var-1)+4, column=1, ipadx=10, ipady=10, sticky='nswe')
        self.var_lists.append(Button(self, text="..."))
        self.var_lists[-1].grid(row=3*(self.no_var-1)+4, column=2, ipadx=10, ipady=10, sticky='nswe')

        
        print(self.no_var)
        self.var_lists.append(Button(self, text="Add Variable", font=("Arial", 16), command=self.Add_Variable))
        self.var_lists[-1].grid(row=3*(self.no_var-1)+5, column=0, columnspan=3, ipadx=10, ipady=10, sticky='nswe')
        self.var_lists.append(Button(self, text="Delete Variable", font=("Arial", 16), command=self.Delete_Variable))
        self.var_lists[-1].grid(row=3*(self.no_var-1)+6, column=0, columnspan=3, ipadx=10, ipady=10, sticky='nswe')
        self.var_lists.append(Button(self, text="Save", font=("Arial", 16), command=self.Save))
        self.var_lists[-1].grid(row=3*(self.no_var-1)+7, column=0, columnspan=3, ipadx=10, ipady=10, sticky='nswe')
        
    def Delete_Variable(self):
        self.no_var -= 1
        for i in range(12):
            self.var_lists[-1].destroy()
            del self.var_lists[-1]
        self.var_lists.append(Button(self, text="Add Variable", font=("Arial", 16), command=self.Add_Variable))
        self.var_lists[-1].grid(row=3*(self.no_var-1)+5, column=0, columnspan=3, ipadx=10, ipady=10, sticky='nswe')
        if self.no_var:
            self.var_lists.append(Button(self, text="Delete Variable", font=("Arial", 16), command=self.Delete_Variable))
            self.var_lists[-1].grid(row=3*(self.no_var-1)+6, column=0, columnspan=3, ipadx=10, ipady=10, sticky='nswe')
            self.var_lists.append(Button(self, text="Save", font=("Arial", 16), command=self.Save))
            self.var_lists[-1].grid(row=3*(self.no_var-1)+7, column=0, columnspan=3, ipadx=10, ipady=10, sticky='nswe')
        else:
            self.var_lists.append(Button(self, text="Save", font=("Arial", 16), command=self.Save))
            self.var_lists[-1].grid(row=3, column=0, columnspan=3, ipadx=10, ipady=10, sticky='nswe')
            
    def Save(self):
        tree.item(tree.selection(), values=[int(self.time.get()), int(self.interval.get()), {}])
            
class BulletEditFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, width=500, height=800, fg_color="transparent")
        self.master = master
        self.values = tree.item(tree.selection())['values']
        Label(self, text="Bullet Type", font=("Arial", 16), relief='groove', bd=2, anchor="w").grid(row=0, column=0, ipadx=10, ipady=10, sticky='nswe')
        self.type = Label(self, text=self.values[0], font=("Arial", 16), relief='groove', bd=2, bg='#ffffff', anchor="w")
        self.type.grid(row=0, column=1, ipadx=10, ipady=10, sticky='nswe')
        Button(self, text="...", command=self.choose_bullet_type).grid(row=0, column=2, ipadx=10, ipady=10, sticky='nswe')

        Label(self, text="Bullet Color", font=("Arial", 16), relief='groove', bd=2, anchor="w").grid(row=1, column=0, ipadx=10, ipady=10, sticky='nswe')
        self.color = Label(self, text=self.values[1], font=("Arial", 16), relief='groove', bd=2, bg='#ffffff', anchor="w")
        self.color.grid(row=1, column=1, ipadx=10, ipady=10, sticky='nswe')
        Button(self, text="...", command=self.choose_bullet_color).grid(row=1, column=2, ipadx=10, ipady=10, sticky='nswe')

        Label(self, text="Position", font=("Arial", 16), relief='groove', bd=2, anchor="w").grid(row=2, column=0, ipadx=10, ipady=10, sticky='nswe')
        self.position = ttk.Combobox(self, values=("self.x,self.y", "0,0"), font=("Arial", 16))
        self.position.insert(0, self.values[2])
        self.position.grid(row=2, column=1, ipadx=10, ipady=10, sticky='nswe')
        Button(self, text="...").grid(row=2, column=2, ipadx=10, ipady=10, sticky='nswe')

        Label(self, text="Speed", font=("Arial", 16), relief='groove', bd=2, anchor="w").grid(row=3, column=0, ipadx=10, ipady=10, sticky='nswe')
        self.speed = Entry(self, font=('Arial', 16), relief='groove', bd=2, bg='#ffffff')
        self.speed.insert(0, self.values[3])
        self.speed.grid(row=3, column=1, ipadx=10, ipady=10, sticky='nswe')
        Button(self, text="...").grid(row=3, column=2, ipadx=10, ipady=10, sticky='nswe')

        Label(self, text="Angle", font=("Arial", 16), relief='groove', bd=2, anchor="w").grid(row=4, column=0, ipadx=10, ipady=10, sticky='nswe')
        self.angle = Entry(self, font=('Arial', 16), relief='groove', bd=2, bg='#ffffff')
        self.angle.insert(0, self.values[4])
        self.angle.grid(row=4, column=1, ipadx=10, ipady=10, sticky='nswe')
        Button(self, text="...").grid(row=4, column=2, ipadx=10, ipady=10, sticky='nswe')

        Label(self, text="Aim to Player", font=("Arial", 16), relief='groove', bd=2, anchor="w").grid(row=5, column=0, ipadx=10, ipady=10, sticky='nswe')
        self.aim = ttk.Combobox(self, values=("True", "False"), font=("Arial", 16))
        self.aim.insert(0, "True" if self.values[5] else "False")
        self.aim.config(state="readonly")
        self.aim.grid(row=5, column=1, ipadx=10, ipady=10, sticky='nswe')
        Button(self, text="...").grid(row=5, column=2, ipadx=10, ipady=10, sticky='nswe')

        Label(self, text="Stay On Create", font=("Arial", 16), relief='groove', bd=2, anchor="w").grid(row=6, column=0, ipadx=10, ipady=10, sticky='nswe')
        self.stay = ttk.Combobox(self, values=("True", "False"), font=("Arial", 16))
        self.stay.insert(0, "True" if self.values[6] else "False")
        self.stay.config(state="readonly")
        self.stay.grid(row=6, column=1, ipadx=10, ipady=10, sticky='nswe')
        Button(self, text="...").grid(row=6, column=2, ipadx=10, ipady=10, sticky='nswe')

        Label(self, text="Destroyable", font=("Arial", 16), relief='groove', bd=2, anchor="w").grid(row=7, column=0, ipadx=10, ipady=10, sticky='nswe')
        self.destroyable = ttk.Combobox(self, values=("True", "False"), font=("Arial", 16))
        self.destroyable.insert(0, "True" if self.values[7] else "False")
        self.destroyable.config(state="readonly")
        self.destroyable.grid(row=7, column=1, ipadx=10, ipady=10, sticky='nswe')
        Button(self, text="...").grid(row=7, column=2, ipadx=10, ipady=10, sticky='nswe')

        Label(self, text="ExistTimes", font=("Arial", 16), relief='groove', bd=2, anchor="w").grid(row=8, column=0, ipadx=10, ipady=10, sticky='nswe')
        self.existTime = Entry(self, font=('Arial', 16), relief='groove', bd=2, bg='#ffffff')
        self.existTime.insert(0, self.values[8])
        self.existTime.grid(row=8, column=1, ipadx=10, ipady=10, sticky='nswe')
        Button(self, text="...").grid(row=8, column=2, ipadx=10, ipady=10, sticky='nswe')

        Label(self, text="Rebound", font=("Arial", 16), relief='groove', bd=2, anchor="w").grid(row=9, column=0, ipadx=10, ipady=10, sticky='nswe')
        self.rebound = ttk.Combobox(self, values=("True", "False"), font=("Arial", 16))
        self.rebound.insert(0, "True" if self.values[9] else "False")
        self.rebound.config(state="readonly")
        self.rebound.grid(row=9, column=1, ipadx=10, ipady=10, sticky='nswe')
        Button(self, text="...").grid(row=9, column=2, ipadx=10, ipady=10, sticky='nswe')

        Label(self, text="Acceleration", font=("Arial", 16), relief='groove', bd=2, anchor="w").grid(row=10, column=0, ipadx=10, ipady=10, sticky='nswe')
        self.accel = Entry(self, font=('Arial', 16), relief='groove', bd=2, bg='#ffffff')
        self.accel.insert(0, self.values[10])
        self.accel.grid(row=10, column=1, ipadx=10, ipady=10, sticky='nswe')
        Button(self, text="...").grid(row=10, column=2, ipadx=10, ipady=10, sticky='nswe')

        Label(self, text="Accel Angle", font=("Arial", 16), relief='groove', bd=2, anchor="w").grid(row=11, column=0, ipadx=10, ipady=10, sticky='nswe')
        self.accelAngle = Entry(self, font=('Arial', 16), relief='groove', bd=2, bg='#ffffff')
        self.accelAngle.insert(0, self.values[11])
        self.accelAngle.grid(row=11, column=1, ipadx=10, ipady=10, sticky='nswe')
        Button(self, text="...").grid(row=11, column=2, ipadx=10, ipady=10, sticky='nswe')

        Label(self, text="Max Velocity", font=("Arial", 16), relief='groove', bd=2, anchor="w").grid(row=12, column=0, ipadx=10, ipady=10, sticky='nswe')
        self.maxV = Entry(self, font=('Arial', 16), relief='groove', bd=2, bg='#ffffff')
        self.maxV.insert(0, self.values[12])
        self.maxV.grid(row=12, column=1, ipadx=10, ipady=10, sticky='nswe')
        Button(self, text="...").grid(row=12, column=2, ipadx=10, ipady=10, sticky='nswe')

        Button(self, text="Save", command=self.save, font=("Arial", 20)).grid(row=13, column=0, columnspan=3, ipadx=10, ipady=10, sticky='nswe')
        
    def choose_bullet_type(self):
        ChooseBulletType(root)

    def choose_bullet_color(self):
        ChooseBulletColor(root)
        
    def save(self):
        self.values[2] = self.position.get()
        self.values[3] = self.speed.get()
        self.values[4] = self.angle.get()
        self.values[5] = True if self.aim.get()=='True' else False
        self.values[6] = True if self.stay.get()=='True' else False
        self.values[7] = True if self.destroyable.get()=='True' else False
        self.values[8] = self.existTime.get()
        self.values[9] = True if self.rebound.get()=='True' else False
        self.values[10] = self.accel.get()
        self.values[11] = self.accelAngle.get()
        self.values[12] = self.maxV.get()
        tree.item(tree.selection(), values=self.values)
        print(tree.item(tree.selection())['values'])
        

class ChooseBulletType(Toplevel):
    def __init__(self, master):
        super().__init__(master, bg="#ffffff")
        self.master = master
        root.attributes("-disabled", 1)
        self.geometry("280x600")
        self.title("Bullet Type List")
        self.protocol("WM_DELETE_WINDOW", self.t_close_handler)
        self.resizable(False, False)
        idx=0
        self.lists = []
        self.type_lists = ["Scale","Orb","Small","Rice","Chain","Pin","Satsu","Gun","Bact","Star","Grape","Dot"]
        for i in range(0,4):
            for j in range(0,3):
                self.lists.append(PhotoImage(file="resource/bullet/enlarged_sprite_{}_{}.png".format(idx+1,1)))
                Button(self, image=self.lists[idx],command=lambda x=idx:self.return_bullet_type(x)).grid(row=i, column=j, ipadx=10, ipady=10)
                idx+=1
        
    def t_close_handler(self):
        root.attributes("-disabled", 0)
        self.destroy()
        
    def return_bullet_type(self, bullet_type):
        A_F.detail_frame.type.config(text=self.type_lists[bullet_type])
        A_F.detail_frame.values[0]=self.type_lists[bullet_type]
        self.t_close_handler()

class ChooseBulletColor(Toplevel):
    def __init__(self, master):
        super().__init__(master, bg="#ffffff")
        self.master = master
        root.attributes("-disabled", 1)
        self.geometry("280x600")
        self.title("Bullet Color List")
        self.protocol("WM_DELETE_WINDOW", self.t_close_handler)
        self.resizable(False, False)
        idx=0
        self.lists = []
        for i in range(0,4):
            for j in range(0,3):
                self.lists.append(PhotoImage(file="resource/bullet/enlarged_sprite_{}_{}.png".format(idx+1,1)))
                Button(self, image=self.lists[idx],command=lambda x=idx:self.return_bullet_color(x)).grid(row=i, column=j, ipadx=10, ipady=10)
                idx+=1
        
    def t_close_handler(self):
        root.attributes("-disabled", 0)
        self.destroy()
        
    def return_bullet_color(self, bullet_color):
        A_F.detail_frame.color.config(text=str(bullet_color))
        A_F.detail_frame.values[1]=bullet_color
        self.t_close_handler()
        
class SoundEditFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, width=500, height=800, fg_color="transparent")
        self.master = master
        self.data = tree.item(tree.selection())['values']
        Label(self, text="Sound_Type", font=("Arial", 16), relief='groove', bd=2, anchor="w").grid(row=0, column=0, ipadx=10, ipady=10, sticky='nswe')
        self.l1 = Label(self, text=self.data[0], font=("Arial", 16), relief='groove', bd=2, bg='#ffffff', anchor="w")
        self.l1.grid(row=0, column=1, ipadx=10, ipady=10, sticky='nswe')
        Button(self, text="...", command = self.choose_sound_type).grid(row=0, column=2, ipadx=10, ipady=10, sticky='nswe')
        Label(self, text="Sound_Volume", font=("Arial", 16), relief='groove', bd=2, anchor="w").grid(row=1, column=0, ipadx=10, ipady=10, sticky='nswe')
        self.l2 = Label(self, text=str(self.data[1]), font=("Arial", 16), relief='groove', bd=2, bg='#ffffff', anchor="w")
        self.l2.grid(row=1, column=1, ipadx=10, ipady=10, sticky='nswe')
        Button(self, text="...").grid(row=1, column=2, ipadx=10, ipady=10, sticky='nswe')
        for i in range(2,16):
            Label(self, text="                ", font=("Arial", 16), relief='groove', bd=2, anchor="w").grid(row=i, column=0, ipadx=10, ipady=10, sticky='nswe')
            Label(self, text="                                            ", font=("Arial", 16), relief='groove', bd=2, bg='#ffffff', anchor="w").grid(row=i, column=1, ipadx=10, ipady=10, sticky='nswe')
            Button(self, text="...").grid(row=i, column=2, ipadx=10, ipady=10, sticky='nswe')
            
    def choose_sound_type(self):
        menu = ChooseSoundFrame(root)
            
class ChooseSoundFrame(Toplevel):
    def __init__(self, master):
        super().__init__(master, bg="#ffffff")
        self.master = master
        root.attributes("-disabled", 1)
        self.geometry("280x200")
        self.title("Choose Bullet")
        self.protocol("WM_DELETE_WINDOW", self.t_close_handler)
        self.resizable(False, False)
        self.sound_lists = ['pause_sound','select_sound','ok_sound','cancel_sound','invalid_sound','miss_sound','shoot_sound',
                            'hit_sound1','hit_sound2','enemyDead_sound','bossDead_sound','enemyShoot_sound1','enemyShoot_sound2','enemyShoot_sound3',
                            'item_get','kira_sound','kira_sound1','powerup_sound','timeout_sound','bonus_sound',
                            'spellStart_sound','spell_sound','graze_sound','spellEnd_sound']
        self.menu = ctk.CTkOptionMenu(self, values=self.sound_lists, command=self.play_sound)
        self.menu.set(A_F.detail_frame.data[0])
        self.menu.pack()
        self.slider_1 = ctk.CTkSlider(self, from_=0, to=100, number_of_steps=100,command=self.slider_event)
        #self.slider_1.set(A_F.detail_frame.data[1]*100)
        self.slider_1.pack()
        self.label = Label(self, text="Volume: 50%", font=("Arial", 16), relief='groove', bd=2, anchor="w")
        self.label.pack()
        
    def t_close_handler(self):
        root.attributes("-disabled", 0)
        A_F.detail_frame.data[0] = self.menu.get()
        A_F.detail_frame.data[1] = int(float(self.slider_1.get()))
        A_F.detail_frame.l1.config(text=self.menu.get())
        A_F.detail_frame.l2.config(text=str(float(self.slider_1.get())/100))
        tree.item(tree.selection(), values=A_F.detail_frame.data)
        self.destroy()
        
    def play_sound(self,value):
        value = self.menu.get()
        #print(type(value))
        SoundEffect.play(value,self.slider_1.get()/100,0)
        
    def slider_event(self,value):
        #print(type(value))
        self.label.config(text="Volume: "+str(int(value))+'%')
        

class DataTreeFrame(Frame):
    def __init__(self, master):
        super().__init__(master, width=1400, height=800,relief="solid", bd=2)
        self.master = master
        #self.pack(side=LEFT)



class DataTree(ttk.Treeview):
    def __init__(self, master, has):
        super().__init__(master)
        self.master = master
        #style = ttk.Style()
        #style.configure('Treeview', rowheight=200)
        self.heading("#0",text="Files")
        if not has:
            self.insert("", iid='0', index="end", image=image_lists['folder'+'small'], text="Project", values=[1], tags='Folder', open=True)
            self.insert("0", iid='1', index="end", image=image_lists['folder'+'small'], text="Resources", values=[1], tags='Folder')
            self.insert("0", iid='2', index="end", image=image_lists['folder'+'small'], text="Classes", values=[1], tags='Folder', open=True)
            
            self.insert('2', iid='3', index="end", image=image_lists['stagegroup'+'small'], text='Stage Group "Easy"', values=['Easy'], tags='StageGroup', open=0)
            self.insert('3', iid='4', index="end", image=image_lists['stage'+'small'], text='Stage "Stage1"', values=['Stage1'], tags='Stage', open=True)
            self.insert('4', iid='5', index="end", image=image_lists['action'+'small'], text='Create Action', tags='Action', open=True)
            self.insert('5', iid='6', index="end", image=image_lists['folder'+'small'], text='Initialize', tags='Folder')
            self.insert('5', iid='7', index="end", image=image_lists['wait'+'small'], text='Wait 60 frame(s)', tags='Wait', values=[60])
            
            self.insert('2', iid='8', index="end", image=image_lists['stagegroup'+'small'], text='Stage Group "Normal"', values=['Normal'], tags='StageGroup', open=0)
            self.insert('8', iid='9', index="end", image=image_lists['stage'+'small'], text='Stage "Stage1"', values=['Stage1'], tags='Stage', open=True)
            self.insert('9', iid='10', index="end", image=image_lists['action'+'small'], text='Create Action', tags='Action', open=True)
            self.insert('10', iid='11', index="end", image=image_lists['folder'+'small'], text='Initialize', tags='Folder')
            self.insert('10', iid='12', index="end", image=image_lists['wait'+'small'], text='Wait 60 frame(s)', tags='Wait', values=[60])
            
            self.insert('2', iid='13', index="end", image=image_lists['stagegroup'+'small'], text='Stage Group "Hard"', values=['Hard'], tags='StageGroup', open=0)
            self.insert('13', iid='14', index="end", image=image_lists['stage'+'small'], text='Stage "Stage1"', values=['Stage1'], tags='Stage', open=True)
            self.insert('14', iid='15', index="end", image=image_lists['action'+'small'], text='Create Action', tags='Action', open=True)
            self.insert('15', iid='16', index="end", image=image_lists['folder'+'small'], text='Initialize', tags='Folder')
            self.insert('15', iid='17', index="end", image=image_lists['wait'+'small'], text='Wait 60 frame(s)', tags='Wait', values=[60])
            
            self.insert('2', iid='18', index="end", image=image_lists['stagegroup'+'small'], text='Stage Group "Lunatic"', values=['Lunatic'], tags='StageGroup', open=0)
            self.insert('18', iid='19', index="end", image=image_lists['stage'+'small'], text='Stage "Stage1"', values=['Stage1'], tags='Stage', open=True)
            self.insert('19', iid='20', index="end", image=image_lists['action'+'small'], text='Create Action', tags='Action', open=True)
            self.insert('20', iid='21', index="end", image=image_lists['folder'+'small'], text='Initialize', tags='Folder')
            self.insert('20', iid='22', index="end", image=image_lists['wait'+'small'], text='Wait 60 frame(s)', tags='Wait', values=[60])
            
            self.insert('2', iid='23', index="end", image=image_lists['stagegroup'+'small'], text='Stage Group "Extra"', values=['Extra'], tags='StageGroup', open=0)
            self.insert('23', iid='24', index="end", image=image_lists['stage'+'small'], text='Stage "Stage1"', values=['Stage1'], tags='Stage', open=True)
            self.insert('24', iid='25', index="end", image=image_lists['action'+'small'], text='Create Action', tags='Action', open=True)
            self.insert('25', iid='26', index="end", image=image_lists['folder'+'small'], text='Initialize', tags='Folder')
            self.insert('25', iid='27', index="end", image=image_lists['wait'+'small'], text='Wait 60 frame(s)', tags='Wait', values=[60])
            # print(self.item('I001')['image'])
        #self.pack(ipadx=460, ipady=280)
        self.bind("<ButtonRelease-1>", self.show_details)
        self.bind("<ButtonRelease-3>", self.showMenu)
        self.bind("<Key-BackSpace>", lambda x:self.remove())
        
    def show_details(self, event):
        item_iid = self.identify_row(event.y)
        if item_iid:
            print(self.item(item_iid))
            A_F.details_identify(item_iid, self.item(item_iid)["tags"][0])
        
    def rename(self, name):
        self.item(self.selection(), text=name)
        
    def remove(self):
        des = self.selection()[0]
        self.delete(des)
        
    def checkInsert(self,type,values):
        if insert_mode == 1:
            self.AddDataUp(type,values)
        elif insert_mode == 2:
            if tree.item(tree.selection())['tags'][0] in ('Folder','Repeat','StageGroup','Stage','Action'):
                self.AddDataInside(type,values)
        elif insert_mode == 3:
            self.AddDataDown(type,values)

    def AddDataUp(self,type,values):
        item_iid = self.selection()[0]
        parent_iid = self.parent(item_iid)
        if parent_iid:
            self.insert(parent_iid, index=tree.index(self.selection()), text=type, image=image_lists[type.lower()+'small'], tags=type, values=values)
        else:
            self.insert('',index=tree.index(self.selection()), text=type, image=image_lists[type.lower()+'small'], tags=type, values=values)
    
    def AddDataInside(self,type,values):
        item_iid = self.selection()[0]
        if item_iid:
            self.insert(item_iid, index="end", text=type, image=image_lists[type.lower()+'small'], tags=type, values=values)
            
    def AddDataDown(self,type,values):
        item_iid = self.selection()[0]
        parent_iid = self.parent(item_iid)
        if parent_iid:
            self.insert(parent_iid, index=tree.index(self.selection())+1, text=type, image=image_lists[type.lower()+'small'], tags=type, values=values)
        else:
            self.insert('',index=tree.index(self.selection())+1, text=type, image=image_lists[type.lower()+'small'], tags=type, values=values)
        
    def showMenu(self, event):
        menu = NodeMenu(self)
        menu.tk_popup(event.x_root, event.y_root)
        
class NodeMenu(Menu):
    def __init__(self, master):
        super().__init__(master, tearoff=False)
        self.master = master
        #self.add_command(label="Rename", command=self.rename)
        self.add_command(label="Delete", command=tree.remove)
        
    def rename(self):
        top = RenameFrame(root)
        
class RenameFrame(Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        root.attributes("-disabled", 1)
        self.geometry("300x100")
        self.title("Rename")
        self.protocol("WM_DELETE_WINDOW", self.t_close_handler)
        entry = Entry(self)
        entry.pack(pady=10)
        button = Button(self, text="Rename", command=lambda:self.rename_handler(entry.get()))
        button.pack(pady=10)
        
    def rename_handler(self, name):
        if name:
            tree.rename(name)
        self.t_close_handler()
        
    def t_close_handler(self):
        root.attributes("-disabled", 0)
        self.destroy()
        
        
        
image_lists=edit_mode_loadImage()
menubar = MenuBar(root)
root.config(menu=menubar)

def print_selection():
    A_F.detail_frame.gets()

dicts = {}
def check(idx):
    a=0
    dicts={}
    if idx!='':
        dicts['message']=tree.item(idx)
    for i in tree.get_children(idx):
        dicts[a]=check(i)
        a+=1
    if idx=='':
        print(dicts)
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(dicts, f, ensure_ascii=False, indent=4)
    else:
        return dicts

def printddd(event):
    item=tree.identify("item",event.x,event.y)
    if item:
        print(tree.item(item))
        #tree.item(tree.selection()[0], values=[1])
        #print(tree.item(item))

#image = PhotoImage(file="resource/NPC/Reimu_dairi_3.png")
#Label(root, image=image, text="It's a monster.", compound="top").pack()
root.mainloop()