SCREENWIDTH = 640
SCREENHEIGHT = 480
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
bullet_colorDict={
    'grey':(95,95,95),
    'red':(187,31,31),
    'lightRed':(255,27,27),
    'purple':(207,58,214),
    'pink':(250,98,238),
    'blue':(22,30,255),
    'seaBlue':(19,66,255),
    'skyBlue':(22,255,255),
    'lightBlue':(113,255,255),
    'darkGreen':(13,149,230),
    'green':(49,255,156),
    'lightGreen':(177,255,81),
    'yellow':(255,255,92),
    'lemonYellow':(255,255,102),
    'orange':(231,170,31),
    'white':(255,255,255)
}
small_createDict=[0,1,1,2,2,3,3,4,4,5,5,5,6,6,6,7]
big_createDict=[0,4,5,6]

bullet_typeDict={
'grape':0,'dot':1,
'scale':2,'orb':3,'small':4,'rice':5,'chain':6,'pin':7,'satsu':8,'gun':9,'bact':10,'star':11,'water':12,'drop':13,
'big_star':14,'mid':15,'butterfly':16,'knife':17,'ellipse':18,'heart':19,'arrow':20,'light':21,'fire':22,'double_star':23,
'big':24,'big_light':25}

enemy_color_list=[
    (0,0,255),(255,0,0),(0,255,0),(255,255,0),
    (0,0,255),(255,0,0),(255,255,0),(207,58,214),
    (255,255,0),(255,0,0),(207,58,214),
    (0,0,255),(255,0,0),(255,128,0),(0,0,255),
    (255,0,0),(0,255,0),(0,0,255),(255,255,0),
    (255,0,0),(0,255,0),(0,0,255),(207,58,214),
    (255,0,0),(0,255,0),(0,0,255),(207,58,214),
    (0,0,255),(255,0,0),(0,255,0),(255,255,0)
]