import pygame
import threading
import LevelManager
import SoundManager
import ImageManager
import functions
import UI
import player
import Login_System


from pygame.locals import *
from const import *
import math
import sys
from random import *
from global_var import *


fullscreen = False
times = 0
fps_cnt = 0

def initialization():
    global loading
    try:
        pygame.init()
        ImageManager.loadImage()
        SoundManager.loadSound()
        loading = False
    except Exception as errors:
        print(errors)
        sys.exit()

def playing(screen, FPS, loadscreen, loadtext, fuka):
    global angle, loading
    while(loading):
        FPS.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit() 
        screen.blit(loadscreen, (0,0))
        screen.blit(loadtext, loadtext.get_rect(bottomright=(525, 470)))
        angle = (angle+5)%360
        img = pygame.transform.rotate(fuka, angle).convert_alpha()
        screen.blit(img, img.get_rect(center=(575, 430)))
        pygame.display.flip()
        
def countFPS(fps):
    global times, fps_cnt
    if times < 59:
        times += 1
        fps_cnt += fps
    if times == 59:
        fps_cnt /= 60
        times = 0
        set_value('fps', fps_cnt)

def Points_Update():
    global angle, point1, point2, shiftFrame
    if pressed_keys[K_LSHIFT] and not pressed_keys_last[K_LSHIFT]:
        angle=0
        shiftFrame=-1
    if pressed_keys[K_LSHIFT] and shiftFrame<20:
        shiftFrame+=1
        scale = functions.dcc(96, 64, shiftFrame, 20)
        point1=pygame.transform.smoothscale(p1, (scale, scale))
        point2=pygame.transform.smoothscale(p2, (scale, scale))
        point2.set_alpha(80)
    else:
        point1=pygame.transform.smoothscale(p1, (64,64))
        point2=pygame.transform.smoothscale(p2, (64,64))
        point2.set_alpha(80)

def main():
    #basic initial
    pygame.init()
    pygame.event.set_allowed([QUIT])
    FPS = pygame.time.Clock()
    FPS.tick(60)
    global fullscreen
    screen = pygame.display.set_mode((640, 480), DOUBLEBUF|HWSURFACE, 16)
    pygame.mouse.set_visible(False)
    icon = pygame.image.load('resource/image/icon_aEm_icon.ico')
    pygame.display.set_icon(icon)
    pygame.display.set_caption("THSBA")

    #initialize image
    loadscreen = pygame.transform.flip(pygame.image.load('resource/image/background.jpg'),True,False).convert_alpha()
    loadscreen = pygame.transform.smoothscale(loadscreen, (640, 480)).convert_alpha()
    loadtext = pygame.image.load('resource/image/loading.png').convert_alpha()
    fuka = pygame.image.load('resource/image/fuka.png').convert_alpha()
    fuka = pygame.transform.rotozoom(fuka, 0, 0.2).convert_alpha()
    global angle, loading
    angle = 0
    loading = True
    
    load_a = threading.Thread(target=initialization,daemon=True)
    load_a.start()
    playing(screen, FPS, loadscreen, loadtext, fuka)

    PLAYER = player.Player()
    STAGE = pygame.Surface((384, 448), pygame.SRCALPHA).convert_alpha()
    STAGE.fill((0,0,0))
    mask = pygame.Surface((384, 448), pygame.SRCALPHA).convert_alpha()
    mask.fill((0,0,0,60))
    mask1=pygame.Surface((384, 448),pygame.SRCALPHA).convert_alpha()
    mask1.fill((0,0,0,128))
    mask2=pygame.Surface((384, 448),pygame.SRCALPHA).convert_alpha()
    mask2.fill((0,0,0,255))
    global p1, p2
    p1=pygame.image.load('resource/image/point1.png').convert_alpha()
    p2=pygame.image.load('resource/image/point2.png').convert_alpha()
    global point1, point2, shiftFrame
    point1=pygame.transform.smoothscale(p1, (64,64))
    point2=pygame.transform.smoothscale(p2, (64,64))
    point2.set_alpha(80)
    screen_rect = pygame.Rect((32-1),(16-1),(384+2),(448+2))

    set_value('score', 0)
    set_value('hi_score', 0)
    set_value('waveNum', 0)
    set_value('grazeNum', 0)
    set_value('draw_healthbar', True)

    global get_mark, shiftFrame, times, tempfps
    global pause_idx, LEVEL_CONTROLLER
    get_mark = 10
    
    shiftFrame=0

    Menu = UI.MENU()
    LEVEL_CONTROLLER = LevelManager.GameController([])
    
    PLAYER_BULLETS = pygame.sprite.Group()
    set_value('player_bullets', PLAYER_BULLETS)
    PLAYER_LASERS = pygame.sprite.Group()
    FLOATGUNS = pygame.sprite.Group()
    ENEMY_BULLETS = pygame.sprite.Group()
    set_value('bullets', ENEMY_BULLETS)
    ENEMY_LASERS = pygame.sprite.Group()
    ENEMIES = pygame.sprite.Group()
    set_value('enemies',ENEMIES)
    ITEMS = pygame.sprite.Group()
    set_value('items', ITEMS)
    EFFECTS = pygame.sprite.Group()
    set_value('effects',EFFECTS)
    EFFECTS1 = pygame.sprite.Group()
    set_value('effects1',EFFECTS1)
    wave = pygame.sprite.Group()
    backgrounds = pygame.sprite.Group()
    set_value('backgrounds', backgrounds)
    boss_effect = pygame.sprite.Group()
    set_value('boss_effect',boss_effect)

    global pressed_keys, pressed_keys_last, pressed_mouse, pressed_mouse_last, frame, pause_idx
    pressed_keys_last = pygame.key.get_pressed()
    pressed_mouse_last = pygame.mouse.get_pressed()
    frame = -100
    set_value('frame',-100)
    pause_idx = 0
    #playing screen
    
    def Back_to_Menu():
        global LEVEL_CONTROLLER
        functions.EXIT(PLAYER_BULLETS, PLAYER_LASERS, ENEMY_BULLETS, ENEMY_LASERS, ENEMIES, FLOATGUNS, ITEMS, backgrounds, EFFECTS, wave, STAGE, screen)
        set_value('state', 'menu')
        Menu.__init__(False)
        set_value('dialog', False)
        username = ''
        with open('tmp.txt', 'w+') as file:
            username = file.read()
            file.write('')
            print(username)
        if username != '':
            Login_System.Update_Highest_Score(get_value('username'), get_value('hi_score'))
            
    def Restart():
        global LEVEL_CONTROLLER
        functions.EXIT(PLAYER_BULLETS, PLAYER_LASERS, ENEMY_BULLETS, ENEMY_LASERS, ENEMIES, FLOATGUNS, ITEMS, backgrounds, EFFECTS, wave, STAGE, screen)
        functions.initialize()
        PLAYER.__init__()
        set_value('frame', -100)
        set_value('waveNum',0)


    def Pause_Update():
        global LEVEL_CONTROLLER, pause_idx 
        if get_value('state') == 'pause':
            if get_value('finish') and pause_idx==0:
                pause_idx = 1
            if pressed_keys[K_z] and not pressed_keys_last[K_z]:
                SoundManager.play('ok_sound',0.35,True)
                set_value('state', 'game')
                set_value('pause_screen', None)
                if not pause_idx:
                    if not PLAYER.isAlive:
                        functions.RESET(PLAYER)
                    pygame.mixer.music.unpause()
                elif pause_idx == 1:
                    Back_to_Menu()
                elif pause_idx == 2:
                    Restart()
                pause_idx = 0
                return
            if (pause_idx if not get_value('finish') else pause_idx==2) and pressed_keys[K_UP] and not pressed_keys_last[K_UP]:
                pause_idx -= 1
                SoundManager.play('select_sound',0.35,True)
                return
            if pause_idx<1 and pressed_keys[K_DOWN] and not pressed_keys_last[K_DOWN]:
                pause_idx += 1
                SoundManager.play('select_sound',0.35,True)
                return


    def Event_Detection():
        global fullscreen
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
                
        if pressed_keys[K_F11] and not pressed_keys_last[K_F11]:
            if not fullscreen:
                pygame.display.set_mode((640,480), FULLSCREEN|DOUBLEBUF|HWSURFACE, 16)
                fullscreen = True
            else:
                pygame.display.set_mode((640,480), DOUBLEBUF|HWSURFACE, 16)
                fullscreen = False
                
        if not get_value('entering_game') and get_value('state') == 'game' and pressed_keys[K_ESCAPE] and not pressed_keys_last[K_ESCAPE]:
            set_value('state', 'pause')
            SoundManager.play('pause_sound',0.35,True)
            
        if get_value('state') == 'game' and pressed_keys[K_i] and not pressed_keys_last[K_i]:
            set_value('enemy_draw_healthbar', not get_value('enemy_draw_healthbar'))
            
        if get_value('state') == 'game' and pressed_keys[K_o] and not pressed_keys_last[K_o]:
            set_value('enemy_show_health_value', not get_value('enemy_show_health_value'))
            
        if get_value('state') == 'game' and pressed_keys[K_p] and not pressed_keys_last[K_p]:
            set_value('damage_show', not get_value('damage_show'))
            
    rainbow = 0
    img_idx = 0
    while get_value('running'):
        screen.fill((255,255,255))
        FPS.tick(60)
        pressed_keys = pygame.key.get_pressed()
        pressed_mouse = pygame.mouse.get_pressed()
        rainbow += 0.02
        if rainbow >= 2 * math.pi:
            rainbow = 0

        Event_Detection()
        Pause_Update()
        
        if get_value('state') == 'menu':
            screen.fill((0,0,0,0))
            Menu.update(screen, pressed_keys, pressed_keys_last)
            if get_value('player_id')==1:
                PLAYER = player.REIMU()
                set_value('player_id',0)
            elif get_value('player_id')==2:
                PLAYER = player.MARISA()
                set_value('player_id',0)
            if get_value('load_level'):
                set_value('load_level',False)
                LEVEL_CONTROLLER = LevelManager.GameController(Menu.node_lists)
            if get_value('load_stage'):
                LEVEL_CONTROLLER = LevelManager.GameController([Menu.node_lists[get_value('load_stage')-1]])
                set_value('load_stage',False)
            if get_value('entering_game_effect'):
                get_value('entering_game_effect').update(screen)

        elif get_value('state') == 'pause':
            if get_value('pause_screen') is None:
                ps = STAGE
                ps = pygame.transform.rotozoom(ps, 0, 0.5)
                ps = pygame.transform.rotozoom(ps, 0, 2).convert_alpha()
                ps.blit(mask1, (0,0))
                set_value('pause_screen', ps)
                pygame.mixer.music.pause()
            UI.pauseScreen(screen, pause_idx, PLAYER)
            UI.display_UI(screen, PLAYER)
            pygame.draw.rect(screen, functions.get_rainbow_color(rainbow), screen_rect, 3, 2)
            
        elif get_value('entering_game'):
            screen.fill((0,0,0))
            UI.display_UI(screen, PLAYER)
            pygame.draw.rect(screen, functions.get_rainbow_color(rainbow), screen_rect, 5, 3)
            get_value('entering_game_effect').update(screen)

        elif get_value('state') == 'game':
            STAGE.fill((0,0,0,0))
            if not get_value('entering_game'):
                frame = get_value('frame')+1
                set_value('frame', frame)
            set_value('grazing',False)
            set_value('item_getting',False)
            set_value('enemypos',(-100,-100,10000))
            
            Points_Update()

            backgrounds.update(STAGE)

            LEVEL_CONTROLLER.update(ENEMIES, ENEMY_BULLETS, EFFECTS, backgrounds, frame, STAGE)
            if get_value('show_stage_title'):
                set_value('show_stage_title', get_value('show_stage_title')-1)
                STAGE.blit(get_value('stage'), (100, 100))
            ENEMIES.update(STAGE, ENEMY_BULLETS, ENEMY_LASERS, ITEMS, EFFECTS, backgrounds)
            FLOATGUNS.update(STAGE, PLAYER, PLAYER_BULLETS, PLAYER_LASERS, pressed_keys, pressed_keys_last)
            PLAYER.update(PLAYER_BULLETS,PLAYER_LASERS, frame, pressed_keys, pressed_keys_last, EFFECTS, ENEMY_BULLETS, ITEMS, FLOATGUNS)
            set_value('player', PLAYER)
            if EFFECTS1:
                EFFECTS1.update(STAGE)
            PLAYER_BULLETS.update(STAGE)
            if not pressed_keys[K_z] or PLAYER.backing:
                PLAYER_LASERS.empty()
            PLAYER_LASERS.update(STAGE)
            ITEMS.update(STAGE, PLAYER, EFFECTS)
            set_value('items',ITEMS)
            if pressed_keys[K_LSHIFT]:
                if shiftFrame>=10:
                    angle = (angle-2)%360
                functions.drawImage(point2, PLAYER.rect.center, -angle, STAGE)
            if not PLAYER.immuneFrame:
                PLAYER.draw(STAGE)
            elif PLAYER.immuneFrame%5<2:
                PLAYER.draw(STAGE)
            
            ENEMY_BULLETS.update(STAGE,ENEMY_BULLETS,EFFECTS)
            
            ENEMY_LASERS.update(STAGE,ENEMY_LASERS)
            
            if get_value('grazeNum')>=get_mark:
                set_value('maximum_score', get_value('maximum_score')+10)
                get_mark+=10

            if pressed_keys[K_LSHIFT]:
                functions.drawImage(point1, PLAYER.rect.center, angle, STAGE)
                
            functions.missDetect(PLAYER, PLAYER_LASERS, ENEMIES, ENEMY_BULLETS, EFFECTS, wave, ITEMS)
            functions.hitEnemy(ENEMIES, PLAYER, PLAYER_BULLETS, EFFECTS)
            functions.laser_collision(ENEMIES, PLAYER, PLAYER_LASERS, EFFECTS)
            set_value('number of bullets' ,len(ENEMY_BULLETS))
            countFPS(FPS.get_fps())
            #print(len(ENEMY_BULLETS),len(ENEMIES),len(PLAYER_BULLETS))
            EFFECTS.update(STAGE)
            if get_value('boss_effect'):
                boss_effect.update(STAGE, PLAYER)
            if PLAYER.booming:
                STAGE.blit(mask, (0,0))
            wave.update(STAGE, ENEMY_BULLETS, ENEMY_LASERS)
            screen.blit(STAGE, (32, 16))
            UI.display_UI(screen, PLAYER)
            
            pygame.draw.rect(screen, functions.get_rainbow_color(rainbow), screen_rect, 5, 3)

            if get_value('dialog'):
                set_value("K_z", False)
                b = pygame.Surface((1000,1000)).convert_alpha()
                b.fill((100,100,100))
                if get_value("dialog_direction")==-1:
                    if get_value('right_portrait'):
                        r = get_value('right_portrait').copy()
                        r.blit(b, (0,0), special_flags=3)
                        screen.blit(r, r.get_rect(center=(440, 350)))
                    screen.blit(get_value('left_portrait'), get_value('left_portrait').get_rect(center=(60, 300)))
                    screen.blit(get_value('dialog_text'), get_value('dialog_text').get_rect(midleft=(60,300)))
                elif get_value('dialog_direction')==1:
                    if get_value('left_portrait'):
                        l = get_value('left_portrait').copy()
                        l.blit(b, (0,0), special_flags=3)
                        screen.blit(l, l.get_rect(center=(40, 350)))
                    screen.blit(get_value('right_portrait'), get_value('right_portrait').get_rect(center=(400, 300)))
                    screen.blit(get_value('dialog_text'), get_value('dialog_text').get_rect(midright=(330,300)))
                else:
                    if get_value('left_portrait'):
                        l = get_value('left_portrait').copy()
                        l.blit(b, (0,0), special_flags=3)
                        screen.blit(l, l.get_rect(center=(40, 350)))
                    if get_value('right_portrait'):
                        r = get_value('right_portrait').copy()
                        r.blit(b, (0,0), special_flags=3)
                        screen.blit(r, r.get_rect(center=(440, 350)))
                if pressed_keys[K_z] and not pressed_keys_last[K_z]:
                    set_value('K_z', True)
        
        if pressed_keys[K_F10] and not pressed_keys_last[K_F10]:
            filename = 'capture'+str(img_idx)+'.png'
            img_idx+=1
            pygame.image.save(screen, filename)
        pressed_keys_last=pressed_keys
        pressed_mouse_last=pressed_mouse
        pygame.display.update()

    if get_value('username'):
        Login_System.Update_Highest_Score(get_value('username'), get_value('hi_score'))
    pygame.quit()

if __name__ == '__main__':
    main()