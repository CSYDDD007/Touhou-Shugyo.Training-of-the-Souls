import pygame

pygame.font.init()

SCREENWIDTH = 960
SCREENHEIGHT = 720
magnitude=1.5
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (140,217,143)
RED = (255,0,0)
BLUE = (0,0,255)
ORANGE = (252, 136, 3)
LIGHTBLUE = (3, 173, 252)
FUCHSIA = (255, 0, 255)
GRAY = (128, 128, 128)
LIME = (0, 128, 0)
MAROON = (128, 0, 0)
NAVYBLUE = (0, 0, 128)
OLIVE = (128, 128, 0)
PURPLE = (128, 0, 128)
TEAL = (0,128,128)
PINK = (241, 95, 229)

small_bullet_colorDict={'grey':0,'red':1,'lightRed':2,'purple':3,'pink':4,'blue':5,'seaBlue':6,'skyBlue':7,'lightBlue':8,'darkGreen':9,'green':10,'lightGreen':11,'yellow':12,'lemonYellow':13,'orange':14,'white':15}
mid_bullet_colorDict={'grey':0,'red':1,'purple':2,'blue':3,'lakeBlue':4,'green':5,'yellow':6,'white':7}
big_bullet_colorDict={'red':0,'blue':1,'green':2,'yellow':3}
fire_bullet_colorDict={'red':0,'purple':4,'blue':8,'orange':12}
small_createDict=[0,1,1,2,2,3,3,4,4,5,5,5,6,6,6,7]
big_createDict=[0,4,5,6]

path_menu_pos = ["resource/NPC/Reimu Hakurei.png", "resource/NPC/Marisa_0.png", "resource/NPC/Sanae_Kochiya_0.png", "resource/NPC/Reisen_Udongein_Inaba_0.png", "resource/NPC/Cirno_0.png", "resource/NPC/Sakuya_Izayoi_0.png", "resource/NPC/Flandre_Scarlet_0.png"]
menu_pos_size = [(413, 500), (308, 500), (418, 500), (303, 500), (306, 500), (277, 500), (341, 500)]
pos_name = ["博丽 灵梦", "雾雨 魔理沙", "东风谷 早苗", "铃仙", "琪露诺", "十六夜 咲夜", "芙兰朵露"]

smallfont = pygame.font.Font('resource/text/TT0246M_.ttf', int(6*magnitude))
middlefont = pygame.font.Font('resource/text/TT0246M_.ttf', int(12*magnitude))
numfont = pygame.font.Font('resource/text/TT0246M_.ttf', int(18*magnitude))


engtextfont = pygame.font.Font('resource/text/ARLRDBD.ttf', int(16*magnitude))
smalltextfont = pygame.font.Font('resource/text/chinese.ttf', int(8*magnitude))
midtextfont = pygame.font.Font('resource/text/chinese.ttf', int(12*magnitude))
textfont = pygame.font.Font('resource/text/chinese.ttf', int(16*magnitude))
titlefont = pygame.font.Font('resource/text/chinese.ttf', int(32*magnitude))

spellcardfont = pygame.font.Font('resource/text/Dengb.ttf', int(20*magnitude))
TitleFont = pygame.font.Font('resource/text/Dengb.ttf', int(30*magnitude))
scoreshowFont = pygame.font.Font('resource/text/Dengb.ttf', int(9*magnitude))
