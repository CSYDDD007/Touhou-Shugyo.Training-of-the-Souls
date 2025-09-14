import pygame
import functions
from PIL import Image, ImageTk
from const import *

def edit_mode_loadImage():
    name_lists=['folder','wait','repeat','var','bullet','rank','stage','thread','enemy','music'
                ,'sound','function','enemy_class','bullet_class','comment','code','velocity','create_bullet'
                ,'image_resource','sound_resource','boss_class','create_boss','spellcard','dialogue','sentence'
                ,'movement','tweening','object','background_class','music_resource','create_background','layer','clear_background'
                ,'delete','stage_title','if','continue','break','boss_explosion','boss_spell'
                ,'kill','clear_enemy','clear_bullet','create_enemy','item','true','false','setting','object_class','create_object']
    lists={}
    for i in range(len(name_lists)):
        img=Image.open('resource/icon/'+name_lists[i]+'.png')
        img=img.resize((40,40),Image.LANCZOS)
        img1=img.resize((20,20),Image.LANCZOS)
        img=ImageTk.PhotoImage(img)
        img1=ImageTk.PhotoImage(img1)
        lists[name_lists[i]]=img
        lists[name_lists[i]+'small']=img1
    return lists

def loadImage_by_rows(sprite_sheet : Image.Image , n, m, x_start, y_start, width, height, rw, rh) -> list :
    lists = []
    for i in range(m):
        for j in range(n):
            img = sprite_sheet.crop((x_start+j*width, y_start+i*height, x_start+j*width+width, y_start+i*height+height))
            img = img.resize((rw, rh), Image.LANCZOS)
            background = Image.new('RGBA', (64, 64), (0,0,0,255))
            bg_w, bg_h = background.size
            offset = ((bg_w - rw) // 2, (bg_h - rh) // 2)
            background.paste(img, offset)
            lists.append(ImageTk.PhotoImage(background))
    return lists

def editor_loadImage_bullet():
    sprite_sheet = Image.open('resource/bullet/bullet_all.png')
    type_lists = ["Scale", "Orb", "Small", "Rice", "Chain", "Pin", "Satsu", "Gun", "Bact", "Star", "Water", "Grape", "Dot",
                  "Big_Star", "Mid", "Butterfly", "Knife", "Ellipse", "Big", "Heart", "Arrow", "Light", "Fire", "Drop", "Double_Star", "Big_Light"]
    lists = {}
    for i in range(1,12):
        lists[type_lists[i-1]]=loadImage_by_rows(sprite_sheet, 16, 1, 0, i*16, 16, 16, 64, 64)
    lists["Grape"]=loadImage_by_rows(sprite_sheet, 8, 2, 0, 12*16, 8, 8, 64, 64)
    lists["Dot"]=loadImage_by_rows(sprite_sheet, 8, 2, 0, 13*16+32, 8, 8, 64, 64)
    sprite_sheet_2 = Image.open('resource/bullet/bullet_all_2.png')
    for i in range(13, 18):
        lists[type_lists[i]]=loadImage_by_rows(sprite_sheet_2, 8, 1, 0, (i-13)*32, 32, 32, 64, 64)
        for j in range(2, 9, 2):
            lists[type_lists[i]].insert(j, lists[type_lists[i]][j-1])
        for j in range(10, 14, 3):
            lists[type_lists[i]].insert(j, lists[type_lists[i]][j-1])
            lists[type_lists[i]].insert(j, lists[type_lists[i]][j-1])
        #lists[type_lists[i]].insert(4, lists[type_lists[i]][3])
    lists["Big"]=loadImage_by_rows(sprite_sheet_2, 4, 1, 0, 6*32, 64, 64, 64, 64)
    for _ in range(2):
        lists["Big"].insert(1, lists["Big"][0])
    for _ in range(5):
        lists["Big"].insert(4, lists["Big"][3])
    for _ in range(2):
        lists["Big"].insert(10, lists["Big"][9])
    for _ in range(3):
        lists["Big"].insert(13, lists["Big"][12])
    for i in range(19, 23):
        lists[type_lists[i]]=loadImage_by_rows(sprite_sheet_2, 8, 1, 0, (i-11)*32+8, 32, 32, 64, 64)
        for j in range(2, 9, 2):
            lists[type_lists[i]].insert(j, lists[type_lists[i]][j-1])
        for j in range(10, 14, 3):
            lists[type_lists[i]].insert(j, lists[type_lists[i]][j-1])
            lists[type_lists[i]].insert(j, lists[type_lists[i]][j-1])
    lists["Fire"]=loadImage_by_rows(sprite_sheet_2, 8, 2, 0, 392, 32, 32, 64, 64)
    lists["Drop"]=loadImage_by_rows(sprite_sheet_2, 16, 1, 0, 14*32+8, 16, 16, 64, 64)
    lists["Double_Star"]=loadImage_by_rows(sprite_sheet_2, 8, 1, 0, 15*32+8, 32, 32, 64, 64)
    for j in range(2, 9, 2):
        lists["Double_Star"].insert(j, lists["Double_Star"][j-1])
    for j in range(10, 14, 3):
        lists["Double_Star"].insert(j, lists["Double_Star"][j-1])
        lists["Double_Star"].insert(j, lists["Double_Star"][j-1])
    lists["Big_Light"]=loadImage_by_rows(sprite_sheet_2, 4, 2, 0, 16*32+16, 64, 64, 64, 64)
    for j in range(2, 9, 2):
        lists["Big_Light"].insert(j, lists["Big_Light"][j-1])
    for j in range(10, 14, 3):
        lists["Big_Light"].insert(j, lists["Big_Light"][j-1])
        lists["Big_Light"].insert(j, lists["Big_Light"][j-1])
    return lists

def editor_loadImage_enemy():
    sprite_sheet = Image.open('resource/enemy/All.png')
    lists=[]
    fairy = loadImage_by_rows(sprite_sheet, 1, 4, 0, 320, 32, 32, 64, 64)
    for i in fairy:
        lists.append(i)
    corrored_fairy = loadImage_by_rows(sprite_sheet, 1, 4, 0, 1608, 32, 32, 64, 64)
    for i in corrored_fairy:
        lists.append(i)
    lists.append(loadImage_by_rows(sprite_sheet, 1, 1, 0, 448, 64, 64, 64, 64))
    lists.append(loadImage_by_rows(sprite_sheet, 1, 1, 0, 1736, 64, 64, 64, 64))
    pale_sheet = Image.open('resource/enemy/paleflower_fairy.png')
    lists.append(loadImage_by_rows(pale_sheet, 1, 1, 0, 0, 64, 64, 64, 64))
    lists.append(loadImage_by_rows(sprite_sheet, 1, 1, 0, 0, 48, 32, 64, 43))
    lists.append(loadImage_by_rows(sprite_sheet, 1, 1, 0, 96, 48, 32, 64, 43))
    lists.append(loadImage_by_rows(sprite_sheet, 1, 1, 320, 0, 48, 48, 64, 64))
    lists.append(loadImage_by_rows(sprite_sheet, 1, 1, 320, 144, 48, 48, 64, 64))
    ghost = loadImage_by_rows(sprite_sheet, 1, 4, 0, 1802, 32, 32, 64, 64)
    for i in ghost:
        lists.append(i)
    yinyangyu = loadImage_by_rows(sprite_sheet, 8, 1, 0, 256, 32, 32, 64, 64)
    for i in yinyangyu:
        lists.append(i)
    ke_sheet = Image.open('resource/enemy/kedama.png')
    kedama = loadImage_by_rows(ke_sheet, 2, 2, 0, 0, 32, 32, 64, 64)
    for i in kedama:
        lists.append(i)
    return lists

def editor_loadImage_items():
    sprite_sheet = Image.open('resource/image/item.png')
    return loadImage_by_rows(sprite_sheet, 10, 1, 0, 0, 16, 16, 64, 64)
    

images = {
    'Menu':{},
    'BattleUI':{},
    'Pause':{},
    'Bullet':{},
    'Effect':{},
    'Background':{},
    'Player':{},
    'Enemy':{},
    'Boss':{},
    'Portrait':{},
    'Item':{},
    'Text':{},
    'Texture':{},
    'Other':{},
    'Mods':{}
}
fonts = {
    'Art_font': "resource/font/aayangexing.ttf",
    'Rank_font': "resource/font/RevueEF Regular.otf",
    'Regular_font': "resource/font/TT0246M_.ttf"
}
backs = {
    
}
def CropImage(sprite_sheet, size, crop_area=None, **kwargs):
    new_image = pygame.Surface(size).convert_alpha()
    new_image.fill((0,0,0,0))
    if crop_area is None:
        new_image.blit(sprite_sheet, (0,0))
    else:
        new_image.blit(sprite_sheet, (0,0), crop_area)
    if "resize" in kwargs:
        new_image = pygame.transform.smoothscale(new_image, kwargs["resize"]).convert_alpha()
    if "zoom" in kwargs:
        new_image = pygame.transform.smoothscale(new_image, (size[0]*kwargs["zoom"][0], size[1]*kwargs["zoom"][1])).convert_alpha()
    if "alpha" in kwargs:
        new_image.set_alpha(kwargs["alpha"])
    if "rotation" in kwargs:
        new_image = pygame.transform.rotate(new_image, kwargs["rotation"]).convert_alpha()
    if "flip" in kwargs:
        new_image = pygame.transform.flip(new_image, kwargs["flip"][0], kwargs["flip"][1]).convert_alpha()
    return new_image.convert_alpha()

def CropImage_In_RC(sprite_sheet, size, start_pos, nRow, nCol, **kwargs):
    lists = []
    for r in range(nRow):
        for c in range(nCol):
            lists.append(CropImage(sprite_sheet, size, (start_pos[0]+size[0]*c, start_pos[1]+size[1]*r, size[0], size[1]), **kwargs))
    #print(kwargs)
    return lists
    
def loadImage_Tkinter(path, crop_area=None):
    new_image = Image.open(path)
    size = new_image.size
    if crop_area:
        new_image = new_image.crop(crop_area)
        size = (crop_area[2], crop_area[3])
    img = Image.new('RGBA', size, (0,0,0,0))
    img.paste(new_image, (0,0))
    img=ImageTk.PhotoImage(img)
    return img

def loadImage():
    global red_effect, images
    red_effect = pygame.Surface((200, 200)).convert_alpha()
    red_effect.fill((255,0,0))
    addImage("Forest", pygame.image.load("mods/resource/forest_1.jpg").convert_alpha())
    Texture()
    Menu(images['Menu'])
    Portrait(images['Portrait'])
    BattleUI(images['BattleUI'])
    Pause(images['Pause'])
    Player(images['Player'])
    Bullet(images['Bullet'])
    Enemy(images["Enemy"])
    Boss()
    Item()
    
def addImage(key, image):
    global images
    images['Mods'][key] = image
    print(key, images['Mods'][key])
    
def addBack(key, back):
    global backs
    backs[key] = back

def getImage(type :str, name :str) -> pygame.Surface:
    global images
    if type in images and name in images[type]:
        return images.get(type).get(name)
    else:
        return None
    
def getBack(key, name):
    global backs
    if key in backs:
        return backs.copy().get(name)
    else:
        return None
    
def saveImage(name, path):
    global images
    images[name] = pygame.image.load(path).convert_alpha()

def stot(f, size, content, color, shadow_color, width, bold=0) -> pygame.Surface:
    font = pygame.font.Font(fonts[f], size)
    font.set_bold(bold)
    text = font.render(content, 1, color)
    text_shadow = font.render(content, 1, shadow_color)
    rect = text.get_rect()
    text_image = pygame.Surface((rect.w+10, rect.h+10)).convert_alpha()
    text_image.fill((0,0,0,0))
    if width:
        for i in range(-width, width+1):
            for j in range(-width, width+1):
                if not(i or j):
                    continue
                rect.center = ((rect.w+10)//2+j, (rect.h+10)//2+i)
                text_image.blit(text_shadow, rect)
    rect.center = ((rect.w+10)//2, (rect.h+10)//2)
    text_image.blit(text, rect)
    return text_image

def get_font_size(f, size, content):
    return pygame.font.Font(fonts[f], size).size(content)

def Texture():
    global images
    images["Texture"][0] = pygame.image.load("resource/image/texture.jpg").convert_alpha()
    images["Texture"][1] = pygame.image.load("resource/image/texture_1.jpg").convert_alpha()
    images["Texture"][2] = pygame.image.load("resource/image/texture.png").convert_alpha()
    
def Menu(images):
    images["Game"] = [stot("Rank_font", 32, "Game Start", WHITE, BLACK, 2), stot("Rank_font", 32, "Game Start", WHITE, BLACK, 2)]
    images["Practice"] = [stot("Rank_font", 32, "Practice Start", WHITE, BLACK, 2), stot("Rank_font", 32, "Practice Start", WHITE, BLACK, 2)]
    images["Mod"] = [stot("Rank_font", 32, "Mod Start", WHITE, BLACK, 2), stot("Rank_font", 32, "Mod Start", WHITE, BLACK, 2)]
    images["Option"] = [stot("Rank_font", 32, "Option", WHITE, BLACK, 2), stot("Rank_font", 32, "Option", WHITE, BLACK, 2)]
    images["BGM Volume"] = [stot("Rank_font", 32, "BGM Volume", WHITE, BLACK, 2), stot("Rank_font", 32, "BGM Volume", WHITE, BLACK, 2)]
    images["SE Volume"] = [stot("Rank_font", 32, "SE Volume", WHITE, BLACK, 2), stot("Rank_font", 32, "SE Volume", WHITE, BLACK, 2)]
    images["Default"] = [stot("Rank_font", 32, "Default", WHITE, BLACK, 2), stot("Rank_font", 32, "Default", WHITE, BLACK, 2)]
    images["Quit"] = [stot("Rank_font", 32, "Quit", WHITE, BLACK, 2), stot("Rank_font", 32, "Quit", WHITE, BLACK, 2)]
    
    images["Game"][0].blit(getImage("Texture", 1), (0,0), special_flags = 3)
    images["Practice"][0].blit(getImage("Texture", 1), (0,0), special_flags = 3)
    images["Mod"][0].blit(getImage("Texture", 1), (0,0), special_flags = 3)
    images["Option"][0].blit(getImage("Texture", 1), (0,0), special_flags = 3)
    images["BGM Volume"][0].blit(getImage("Texture", 1), (0,0), special_flags = 3)
    images["SE Volume"][0].blit(getImage("Texture", 1), (0,0), special_flags = 3)
    images["Default"][0].blit(getImage("Texture", 1), (0,0), special_flags = 3)
    images["Quit"][0].blit(getImage("Texture", 1), (0,0), special_flags = 3)
    
    images["Title_1"] = stot("Art_font", 48, "Touhou Shuygo", WHITE, BLACK, 2)
    images["Title_2"] = stot("Art_font", 48, "Training of the Souls", WHITE, BLACK, 2)
    
    images["Title_1"].blit(getImage("Texture", 0), (0,0), special_flags = 3)
    images["Title_1"].blit(getImage("Texture", 0), (233,0), special_flags = 3)
    images["Title_2"].blit(getImage("Texture", 2), (0,0), special_flags = 3)
    images["Title_2"].blit(getImage("Texture", 2), (240,0), special_flags = 3)
    images["Title_2"].blit(getImage("Texture", 2), (480,0), special_flags = 3)

    images['Player_Info_Reimu'] = pygame.transform.smoothscale(pygame.image.load('resource/font/PlayerInfo_Reimu.png'), (1130/2.2,761/2.2)).convert_alpha()
    images['Player_Info_Marisa'] = pygame.transform.smoothscale(pygame.image.load('resource/font/PlayerInfo_Marisa.png'), (1130/2.2,761/2.2)).convert_alpha()

def Portrait(images):
    images['Reimu'] = CropImage_In_RC(pygame.image.load('resource/NPC/Reimu Hakurei.png'), (4306/6, 1736/2), (0,0), 2, 6, zoom=(0.5,0.5))
    images['Marisa'] = CropImage_In_RC(pygame.image.load('resource/NPC/Marisa.png'), (1632/3, 2649/3), (0,0), 3, 3, zoom=(0.5,0.5))
    images['Cirno'] = CropImage_In_RC(pygame.image.load('resource/NPC/Cirno.png'), (1488/3, 1620/2), (0,0), 2, 3, zoom=(0.5,0.5))

def BattleUI(images):
    sprite_sheet = CropImage(pygame.image.load('resource/image/background.jpg'), (826,551), (0,0,826,551), resize=(640,480))
    lists = []#384 448
    lists.append(CropImage(sprite_sheet, (32,480), (0,0,32,480)))
    lists.append(CropImage(sprite_sheet, (384,16), (32,0,384,16)))
    lists.append(CropImage(sprite_sheet, (384,16), (32,464,384,16)))
    lists.append(CropImage(sprite_sheet, (224,480), (416,0,224,480)))
    images["Background"] = lists
    images["EASY"] = stot('Rank_font', 32, "EASY", WHITE, (0,144,44), 2)
    images["NORMAL"] = stot('Rank_font', 32, "NORMAL", WHITE, (0, 84, 178), 2)
    images["HARD"] = stot('Rank_font', 32, "HARD", WHITE, (0,9,197), 2)
    images["LUNATIC"] = stot('Rank_font', 32, "LUNATIC", WHITE, (151,0,160), 2)
    images["EXTRA"] = stot('Rank_font', 32, "EXTRA", WHITE, (189,0,0), 2)
    
    images["HiScore"] = stot('Regular_font', 20, "HiScore", GRAY, BLACK, 1)
    images["Score"] = stot('Regular_font', 20, "Score", WHITE, BLACK, 1)
    images["Player"] = stot('Regular_font', 20, "Player", PINK, BLACK, 2, 1)
    images["SpellCard"] = stot('Regular_font', 20, "SpellCard", GREEN, BLACK, 2, 1)
    images["Piece"] = stot('Regular_font', 16, "(pieces)", WHITE, BLACK, 2)
    images["Power"] = stot('Regular_font', 20, "Power", ORANGE, BLACK, 2, 1)
    images["Point"] = stot('Regular_font', 20, "Point", LIGHTBLUE, BLACK, 2, 1)
    images["Graze"] = stot('Regular_font', 20, "Graze", GRAY, BLACK, 2, 1)

    signs = CropImage_In_RC(pygame.image.load('resource/HUD/Sign.png').convert_alpha(), (32,40), (0,0), 2, 6, zoom=(0.5,0.5))

    images["LifeSign"] = signs[0:6]
    images['BoomSign'] = signs[6:]

    fuka = CropImage(pygame.image.load('resource/image/fuka.png'), (180, 492), (0,0,180,492), zoom=(0.2, 0.2))
    pygame.draw.rect(fuka, (0,0,0), fuka.get_rect(), 1)
    images["FUKA"] = fuka
    back = pygame.Surface((400, 350)).convert_alpha()
    back.fill((0,0,0,0))
    back.blit(stot('Art_font', 24, "TOUHOU SHUYGO", WHITE, BLACK, 2, 1), (0,0))
    back.blit(getImage("Texture", 0), (0,0), special_flags=3)
    back.blit(getImage("Texture", 0), (233,0), special_flags=3)
    back.blit(stot('Art_font', 24, "Training", WHITE, BLACK, 2), (0, 30))
    back.blit(stot('Art_font', 24, "of", WHITE, BLACK, 2), (0, 56))
    back.blit(stot('Art_font', 24, "the", WHITE, BLACK, 2), (0, 82))
    back.blit(stot('Art_font', 24, "Souls", WHITE, BLACK, 2), (0, 108))
    back.blit(getImage("Texture", 2), (0,30), special_flags=3)
    images["Title"] = back
    images["Get_Spell_Card"] = CropImage(pygame.image.load('resource/HUD/SpellCard_Bonus.png'), (450,56), (0,0,450,56), zoom=(0.7,0.7))
    images["Bonus_Failed"] = CropImage(pygame.image.load('resource/HUD/Bonus_Failed.png'), (300,59), (0,0,300,59))
    images["SpellCardAttack"] = CropImage(pygame.image.load('resource/image/spellcardAttack.png'), (128, 16), (0,0,128,16))
    images['Forest'] = pygame.image.load("mods/resource/forest_1.jpg").convert_alpha()

def Pause(images):
    images['Pause'] = stot("Art_font", 32, "Pause Menu", WHITE, BLACK, 2)
    images['Return'] = [stot("Art_font", 28, "Return to Game", WHITE, BLACK, 2),stot("Art_font", 28, "Return to Game", GRAY, BLACK, 2)]
    images['Back'] = [stot("Art_font", 28, "Back to Title", WHITE, BLACK, 2),stot("Art_font", 28, "Back to Title", GRAY, BLACK, 2)]
    images['Retry'] = [stot("Art_font", 28, "Retry", WHITE, BLACK, 2),stot("Art_font", 28, "Retry", GRAY, BLACK, 2)]
    images['Gameover'] = stot("Art_font", 32, "Gameover Menu", (240,0,0), BLACK, 2)
    images['GameEnd'] = stot("Art_font", 32, "GameEnd Menu", WHITE, BLACK, 2)
    


def Player(images):
    sprite_sheet = pygame.image.load('resource/player/P001/playerImage.png').convert_alpha()
    images['Reimu'] = CropImage_In_RC(sprite_sheet, (32,48), (0,0), 3, 8)
    sprite_sheet = pygame.image.load('resource/player/P001/Object_th16.png').convert_alpha()
    lists = CropImage_In_RC(sprite_sheet, (16,16), (0,0), 1, 4, rotation=90)
    lists.append(CropImage(sprite_sheet, (64,16), (256-64,0,64,16), rotation=90))
    images['Reimu_Main_Satsu'] = lists
    images['Reimu_Target_Satsu'] = CropImage_In_RC(sprite_sheet, (16,16), (0,16), 1, 4, rotation=90)
    images['Reimu_Shift_Bullet'] = CropImage_In_RC(sprite_sheet, (64,16), (0,32), 1, 2, rotation=90)
    images['Reimu_Floatgun'] = CropImage(sprite_sheet, (16,16), (64,0,16,16))

    sprite_sheet = pygame.image.load('resource/player/P002/playerImage.png').convert_alpha()
    images['Marisa'] = CropImage_In_RC(sprite_sheet, (32,48), (0,0), 3, 8)
    sprite_sheet = pygame.image.load('resource/player/P002/Object_th17.png').convert_alpha()
    images['Marisa_Main_Bullet'] = CropImage_In_RC(sprite_sheet, (32,16), (8,0), 1, 4, rotation=90)
    l1 = CropImage_In_RC(sprite_sheet, (48,16), (8,48), 2, 1, rotation=90)
    l1 += CropImage_In_RC(sprite_sheet, (32,32), (8,80), 1, 8, rotation=90)
    images['Marisa_Missile'] = l1
    images['Marisa_Laser'] = CropImage(sprite_sheet, (256,16), (8,32,256,16), rotation=90)
    images['Marisa_Floatgun'] = CropImage(sprite_sheet, (16,16), (64+8,16,16,16))
    sprite_sheet = pygame.image.load('resource/player/P002/All.png').convert_alpha()
    images['Master_Spark'] = CropImage(pygame.image.load('resource/player/P002/All.png').convert_alpha(), (256,144), (288,8,256,144), zoom=(4.0,4.0), rotation=-90)
    images['Master_Spark_Effect'] = CropImage(pygame.image.load('resource/player/P002/Wave.png').convert_alpha(), (84,245), (0,0,84,245), zoom=(2.5,2.5), rotation=-90, alpha=90)
    
def Bullet(images):
    sprite_sheet = pygame.image.load('resource/bullet/bullet_all.png').convert_alpha()
    images['scale'] = CropImage_In_RC(sprite_sheet, (16,16), (0,16), 1, 16)
    images['orb'] = CropImage_In_RC(sprite_sheet, (16,16), (0,32), 1, 16)
    images['small'] = CropImage_In_RC(sprite_sheet, (16,16), (0,48), 1, 16)
    images['rice'] = CropImage_In_RC(sprite_sheet, (16,16), (0,64), 1, 16)
    images['chain'] = CropImage_In_RC(sprite_sheet, (16,16), (0,80), 1, 16)
    images['pin'] = CropImage_In_RC(sprite_sheet, (16,16), (0,96), 1, 16)
    images['satsu'] = CropImage_In_RC(sprite_sheet, (16,16), (0,112), 1, 16)
    images['gun'] = CropImage_In_RC(sprite_sheet, (16,16), (0,128), 1, 16)
    images['bact'] = CropImage_In_RC(sprite_sheet, (16,16), (0,144), 1, 16)
    images['star'] = CropImage_In_RC(sprite_sheet, (16,16), (0,160), 1, 16)
    images['water'] = CropImage_In_RC(sprite_sheet, (16,16), (0,176), 1, 16)
    images['grape'] = CropImage_In_RC(sprite_sheet, (8,8), (0,192), 2, 8)
    images['create_effect'] = CropImage_In_RC(sprite_sheet, (32,32), (0,208), 1, 8)
    images['dot'] = CropImage_In_RC(sprite_sheet, (8,8), (0,240), 2, 8)
    sprite_sheet = pygame.image.load('resource/bullet/bullet_all_2.png').convert_alpha()
    images['big_star'] = CropImage_In_RC(sprite_sheet, (32,32), (0,0), 1, 8)
    images['mid'] = CropImage_In_RC(sprite_sheet, (32,32), (0,32), 1, 8)
    images['butterfly'] = CropImage_In_RC(sprite_sheet, (32,32), (0,64), 1, 8)
    images['knife'] = CropImage_In_RC(sprite_sheet, (32,32), (0,96), 1, 8)
    images['ellipse'] = CropImage_In_RC(sprite_sheet, (32,32), (0,128), 1, 8)
    images['big'] = CropImage_In_RC(sprite_sheet, (64,64), (0,192), 1, 4)
    images['heart'] = CropImage_In_RC(sprite_sheet, (32,32), (0,264), 1, 8)
    images['arrow'] = CropImage_In_RC(sprite_sheet, (32,32), (0,296), 1, 8)
    images['light'] = CropImage_In_RC(sprite_sheet, (32,32), (0,328), 1, 8)
    images['bullet_vanish'] = CropImage_In_RC(pygame.image.load('resource/bullet/bullet_vanish.png').convert_alpha(), (64,64), (0,0), 2, 4, alpha=200)
    #images['heart'] = CropImage_In_RC(sprite_sheet, (32,32), (0,264), 1, 8)

def Enemy(images):
    sprite_sheet = pygame.image.load('resource/enemy/All.png')
    #fairy 0-3
    for i in range(0, 4):
        image_list = []
        for k in range(0, 2):
            for j in range(0, 12):
                new_image = CropImage(sprite_sheet, (32, 32), (j*32, 320+i*32, 32, 32))
                if k:
                    new_image.blit(red_effect, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
                image_list.append(new_image)
        images[i] = image_list
    #corroded_fairy 4-7 
    for i in range(4, 8):
        image_list = []
        for k in range(0, 2):
            for j in range(0, 12):
                new_image = CropImage(sprite_sheet, (32, 32), (j*32, 1608+(i-4)*32, 32, 32))
                if k:
                    new_image.blit(red_effect, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
                image_list.append(new_image)
        images[i] = image_list
    #flower_fairy 8
    image_list = []
    for k in range(0, 2):
        for j in range(0, 8):
            new_image = CropImage(sprite_sheet, (64, 64), (j*64, 448, 64, 64))
            if k:
                new_image.blit(red_effect, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
            image_list.append(new_image)
        for i in range(0, 2):
            for j in range(0, 2):
                new_image = CropImage(sprite_sheet, (64, 64), (384+j*64, 320+i*64, 64, 64))
                if k:
                    new_image.blit(red_effect, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
                image_list.append(new_image)
    images[8] = image_list
    #corroded_flower_fairy 9
    image_list = []
    for k in range(0, 2):
        for j in range(0, 8):
            new_image = CropImage(sprite_sheet, (64, 64), (j*64, 1736, 64, 64))
            if k:
                new_image.blit(red_effect, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
            image_list.append(new_image)
        for i in range(0, 2):
            for j in range(0, 2):
                new_image = CropImage(sprite_sheet, (64, 64), (384+j*64, 1608+i*64, 64, 64))
                if k:
                    new_image.blit(red_effect, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
                image_list.append(new_image)
    images[9] = image_list
    #pale_flower_fairy 10
    sprite_sheet_1 = pygame.image.load("resource/enemy/paleflower_fairy.png")
    image_list = []
    for k in range(0, 2):
        for j in range(0, 8):
            new_image = CropImage(sprite_sheet_1, (64, 64), (j*64, 0, 64, 64))
            if k:
                new_image.blit(red_effect, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
            image_list.append(new_image)
        for i in range(0, 2):
            for j in range(0, 2):
                new_image = CropImage(sprite_sheet_1, (64, 64), (j*64, i*64, 64, 64))
                if k:
                    new_image.blit(red_effect, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
                image_list.append(new_image)
    images[10] = image_list
    #sp_fairy 11-12
    for i in range(11, 13):
        image_list = []
        for k in range(0, 2):
            for r in range(0, 3):
                for c in range(0, 4):
                    new_image = CropImage(sprite_sheet, (48, 32), (c*48, r*32+(i-11)*96, 48, 32))
                    if k:
                        new_image.blit(red_effect, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
                    image_list.append(new_image)
        images[i] = image_list
    #mid_fairy 13-14
    for i in range(13, 15):
        image_list = []
        for k in range(0, 2):
            for r in range(0, 3):
                for c in range(0, 4):
                    new_image = CropImage(sprite_sheet, (48, 48), (320+c*48, r*48+(i-13)*144, 48, 48))
                    if k:
                        new_image.blit(red_effect, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
                    image_list.append(new_image)
        images[i] = image_list
    #ghost 15-18
    for r in range(0, 4):
        image_list = []
        for k in range(0, 2):
            for c in range(0, 8):
                new_image = CropImage(sprite_sheet, (32, 32), (c*32, 1800+r*32, 32, 32))
                if k:
                    new_image.blit(red_effect, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
                image_list.append(new_image)
        images[r+15] = image_list
    images['death_effect'] = pygame.image.load('resource/enemy/enemy_death_effect.png').convert_alpha()
    lists = CropImage_In_RC(sprite_sheet, (32,32), (0,320-64), 2, 8)
    yinyangyu = lists[0:4]
    small_yinyangyu = lists[4:8]
    idx = 19
    for i in yinyangyu:
        new_image = i.copy()
        new_image.blit(red_effect, (0,0), special_flags=3)
        images[idx] = [i,new_image]
        idx+=1
    for i in small_yinyangyu:
        new_image = i.copy()
        new_image.blit(red_effect, (0,0), special_flags=3)
        images[idx] = [i,new_image]
        idx+=1
    nimbus = lists[8:12]
    balls = lists[12:16]
    for i in range(4):
        balls.append(CropImage(balls[i], (32,32), zoom=(1.5,1.5)))
    images['nimbus'] = nimbus
    images['balls'] = balls
    lists = CropImage_In_RC(pygame.image.load('resource/enemy/kedama.png').convert_alpha(), (32,32), (0,0), 2, 2)
    for i in lists:
        new_image = i.copy()
        new_image.blit(red_effect, (0,0), special_flags=3)
        images[idx] = [i,new_image]
        idx+=1
        
def Boss():
    global images
    images["Boss"]["Default"] = pygame.image.load("resource/enemy/boss.png").convert_alpha()
    images["Boss"]["Spellcard_Sign"] = pygame.image.load("resource/image/spellcard_sign.png").convert_alpha()
    images["Boss"]['boss_effect'] = pygame.image.load('resource/enemy/boss_effect.png').convert_alpha()
    images["Boss"]["boss_pos"] = pygame.image.load('resource/image/boss_pos.png').convert_alpha()
    images["Boss"]["boss_magic"] = CropImage(pygame.image.load('resource/enemy/boss_magic.png').convert_alpha(), (128,128), (0,0,128,128), zoom=(2.0,2.0))
    
def Item():
    global images
    new_image = pygame.image.load('resource/image/item.png').convert_alpha()
    item_list = []
    sign_list = []
    for i in range(0,10):
        item_list.append(CropImage(new_image, (16,16), (i*16,0,16,16)))
        sign_list.append(CropImage(new_image, (16,16), (i*16+10*16,0,16,16)))
    item_list[8].set_alpha(100)
    images['Item']['items'] = item_list
    images['Item']['signs'] = sign_list

        

                    
    
    