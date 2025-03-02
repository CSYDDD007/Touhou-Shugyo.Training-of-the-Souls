import pygame, sys
import threading
import Class_logic as level
import database
import functions
import UI
import player
import Plot
import Login_System
import time

from pygame.locals import *
from const import *
import math
from random import *
from global_var import *
import SoundEffect

def main():
    #basic initial
    pygame.init()
    pygame.event.set_allowed([QUIT])
    FPS = pygame.time.Clock()
    FPS.tick(60)
    magnitude=1.5
    global fullscreen
    fullscreen = False
    screen = pygame.display.set_mode((640*magnitude,480*magnitude), SCALED|DOUBLEBUF|HWSURFACE, 16)# (1280, 960) 960,720
    #screen = pygame.Surface((640*magnitude,480*magnitude), pygame.SRCALPHA).convert_alpha()
    pygame.mouse.set_visible(False)
    icon = pygame.image.load('resource/image/icon_aEm_icon.ico')
    pygame.display.set_icon(icon)
    pygame.display.set_caption("東方修行記")

    #initialize image
    loadscreen = pygame.transform.flip(pygame.image.load('resource/image/background.jpg'),True,False).convert_alpha()
    loadscreen = pygame.transform.smoothscale(loadscreen, (640*magnitude,480*magnitude)).convert_alpha()
    set_value('loadscreen', loadscreen)
    loadtext = pygame.image.load('resource/image/loading.png').convert_alpha()
    loadtext = pygame.transform.rotozoom(loadtext, 0, 1.5).convert_alpha()
    fuka = pygame.image.load('resource/image/fuka.png').convert_alpha()
    fuka = pygame.transform.rotozoom(fuka, 0, 0.3).convert_alpha()
    global angle, loading, error
    angle = 0
    loading = True
    error = False
    def initialization():
        global loading, error
        try:
            database.loadImage()
            SoundEffect.loadSound()
            database.loadText()
            loading = False
        except Exception as errors:
            print(errors)
            error = False
            
    def playing():
        global angle
        while(loading):
            FPS.tick(60)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            if error:
                sys.exit()            
            screen.blit(loadscreen, (0,0))
            screen.blit(loadtext, loadtext.get_rect(bottomright=(525*magnitude, 470*magnitude)))
            angle = (angle+5)%360
            img = pygame.transform.rotate(fuka, angle).convert_alpha()
            screen.blit(img, img.get_rect(center=(575*magnitude, 430*magnitude)))
            #DS.blit(pygame.transform.smoothscale(screen, (1280,960)), (0,0))
            pygame.display.flip()
    load_a = threading.Thread(target=initialization,daemon=True)
    load_a.start()
    playing()
    #db.INIT()

    PLAYER = player.Player()
    STAGE = pygame.Surface((384*magnitude, 448*magnitude), pygame.SRCALPHA).convert_alpha()
    STAGE.fill((0,0,0))
    mask = pygame.Surface((384*magnitude, 448*magnitude), pygame.SRCALPHA).convert_alpha()
    mask.fill((0,0,0,60))
    mask1=pygame.Surface((384*magnitude, 448*magnitude),pygame.SRCALPHA).convert_alpha()
    mask1.fill((0,0,0,128))
    mask2=pygame.Surface((384*magnitude, 448*magnitude),pygame.SRCALPHA).convert_alpha()
    mask2.fill((0,0,0,255))
    p1=pygame.image.load('resource/image/point1.png').convert_alpha()
    p2=pygame.image.load('resource/image/point2.png').convert_alpha()
    global point1, point2, shiftFrame
    point1=pygame.transform.smoothscale(p1, (64*magnitude,64*magnitude))
    point2=pygame.transform.smoothscale(p2, (64*magnitude,64*magnitude))
    point2.set_alpha(80)
    screen_rect = pygame.Rect((32-1)*magnitude,(16-1)*magnitude,(384+2)*magnitude,(448+2)*magnitude)
    grid_screen=pygame.Surface((390*magnitude,450*magnitude),pygame.SRCALPHA)
    grid_screen.fill((0,0,0,0))
    for i in range(0,25):
        pygame.draw.line(grid_screen, BLACK, (i*16*magnitude,0), (i*16*magnitude,448*magnitude))
        for j in range(0,29):
            pygame.draw.line(grid_screen, BLACK, (0,j*16*magnitude), (384*magnitude,j*16*magnitude))
    grid_screen_1=pygame.Surface((390*magnitude,450*magnitude),pygame.SRCALPHA)
    grid_screen_1.fill((0,0,0,0))
    for i in range(0,25):
        pygame.draw.line(grid_screen_1, WHITE, (i*16*magnitude,0), (i*16*magnitude,448*magnitude))
        for j in range(0,29):
            pygame.draw.line(grid_screen_1, WHITE, (0,j*16*magnitude), (384*magnitude,j*16*magnitude))


    set_value('running', True)
    set_value('player_num', 0)
    set_value('player_HP', 4)
    set_value('player_Boom', 2)
    set_value('shift_down', False)
    set_value('player_attack', False)
    set_value('player_cx', 384)
    set_value('player_cy', 800)
    set_value('score', 0)
    #set_value('hi_score', 1000000)
    set_value('immune', False)
    set_value('immune_time', 0)
    set_value('menu', True)
    set_value('replay', False)
    set_value('battle_music', False)
    set_value('menu_music', True)
    set_value('select', 1)
    set_value('pause', False)
    set_value('unPause', False)
    set_value('deadpause', False)
    set_value('player_firelevel', 1)
    set_value('player_power', 100)
    set_value('maximum_score', 10000)
    set_value('score_item_count', 0)
    set_value('score_item_bound', 10)
    set_value('player_alive', True)
    set_value('player_backing', False)
    set_value('enemypos', (0, 0, 10000))
    set_value('lastframe', 0)
    set_value('number of bullets', 0)
    set_value('fps', 60.0)
    set_value('grazeNum', 0)
    set_value('booming', False)
    set_value('screen_shaking', False)
    set_value('exit', False)
    set_value('waveNum',0)
    set_value('test_hitbox', False)
    set_value('gethit', False)
    set_value('plot', False)
    set_value('boss_alive',False)
    set_value('stage_Num',1)
    set_value('change',False)
    set_value('ifSpell',False)
    set_value('show_health', False)
    set_value('edit_mode',False)
    set_value('grid_open',False)
    set_value('edit_mode_back',False)
    set_value('create_player',False)
    set_value('testing',False)
    set_value('load_level',False)
    set_value('finish',0)

    global get_mark, shiftFrame, times, tempfps
    global pause_idx, LEVEL_CONTROLLER
    get_mark = 10
    
    shiftFrame=0
    times=0
    tempfps=0

    Menu = UI.MENU()
    LEVEL_CONTROLLER = level.stagecontroller_stage_2()
    
    PLAYER_BULLETS = pygame.sprite.Group()
    PLAYER_LASERS = pygame.sprite.Group()
    FLOATGUNS = pygame.sprite.Group()
    ENEMY_BULLETS = pygame.sprite.Group()
    ENEMY_LASERS = pygame.sprite.Group()
    ENEMIES = pygame.sprite.Group()
    ITEMS = pygame.sprite.Group()
    EFFECTS = pygame.sprite.Group()
    set_value('effects',EFFECTS)
    EFFECTS1 = pygame.sprite.Group()
    set_value('effects1',EFFECTS1)
    wave = pygame.sprite.Group()
    backgrounds = pygame.sprite.Group()
    set_value('backgroundsss',backgrounds)
    boss_effect = pygame.sprite.Group()
    set_value('boss_effect',boss_effect)

    global pressed_keys, pressed_keys_last, pressed_mouse, pressed_mouse_last, frame, pause_idx
    pressed_keys_last = pygame.key.get_pressed()
    pressed_mouse_last = pygame.mouse.get_pressed()
    frame = -100
    set_value('frame',-100)
    pause_idx = 0
    #playing screen
    
    def countFPS(fps):
        global times,tempfps
        if times < 59:
            times += 1
            tempfps += fps
        if times == 59:
            tempfps /= 60
            times = 0
            set_value('fps', tempfps)
            
    def Points_Update():
        global angle, point1, point2, shiftFrame
        if pressed_keys[K_LSHIFT] and not pressed_keys_last[K_LSHIFT]:
            angle=0
            shiftFrame=-1
        if pressed_keys[K_LSHIFT] and shiftFrame<20:
            shiftFrame+=1
            point1=pygame.transform.smoothscale(p1, ((94-shiftFrame*1.5)*magnitude,(94-shiftFrame*1.5)*magnitude))
            point2=pygame.transform.smoothscale(p2, ((94-shiftFrame*1.5)*magnitude,(94-shiftFrame*1.5)*magnitude))
            point2.set_alpha(80)
        else:
            point1=pygame.transform.smoothscale(p1, (64*magnitude,64*magnitude))
            point2=pygame.transform.smoothscale(p2, (64*magnitude,64*magnitude))
            point2.set_alpha(80)
    
    def Back_to_Menu():
        global LEVEL_CONTROLLER
        functions.EXIT(PLAYER_BULLETS, PLAYER_LASERS, ENEMY_BULLETS, ENEMY_LASERS, ENEMIES, FLOATGUNS, ITEMS, backgrounds, EFFECTS, wave, STAGE, screen, plot)
        plot.__init__(PLAYER.__class__.__name__)
        set_value('frame', 0)
        set_value('menu', True)
        Menu.__init__()
        set_value('pause', False)
        set_value('menu_music', True)
        set_value('battle_music', False)
        set_value('exit', True)
        set_value('player_num', 0)
        LEVEL_CONTROLLER = level.stagecontroller_stage_2()
        if get_value('username'):
            Login_System.Update_Highest_Score(get_value('username'), get_value('hi_score'))
            
    def Restart():
        global LEVEL_CONTROLLER
        LEVEL_CONTROLLER = level.stagecontroller_stage_2()
        functions.EXIT(PLAYER_BULLETS, PLAYER_LASERS, ENEMY_BULLETS, ENEMY_LASERS, ENEMIES, FLOATGUNS, ITEMS, backgrounds, EFFECTS, wave, STAGE, screen, plot)
        functions.initialize()
        PLAYER.__init__()
        plot.__init__(PLAYER.__class__.__name__)
        set_value('frame', -100)
        set_value('waveNum',0)
        set_value('unPause', True)


    def Pause_Update():
        global LEVEL_CONTROLLER, pause_idx
        #print(get_value('pause'))
        if not (get_value('menu') or get_value('pause') or get_value('edit_mode')) and pressed_keys[K_ESCAPE] and not pressed_keys_last[K_ESCAPE]:
            set_value('pause', True)
            set_value('unPause',False)
            ps = STAGE
            ps = pygame.transform.rotozoom(ps, 0, 0.5)
            ps = pygame.transform.rotozoom(ps, 0, 2).convert_alpha()
            ps.blit(mask1, (0,0))
            set_value('pause_screen', ps)
            SoundEffect.play('pause_sound',0.35,True)
            pygame.mixer.music.pause()
            
        elif get_value('pause'):
            if get_value('finish') and pause_idx==0:
                pause_idx = 1
            if pressed_keys[K_z] and not pressed_keys_last[K_z]:
                SoundEffect.play('ok_sound',0.35,True)
                if not pause_idx:
                    set_value('unPause', True)
                    if not get_value('player_alive'):
                        functions.RESET(PLAYER)
                    pygame.mixer.music.unpause()
                elif pause_idx == 1:
                    Back_to_Menu()
                elif pause_idx == 2:
                    Restart()
                pause_idx = 0
            if (pause_idx if not get_value('finish') else pause_idx==2) and pressed_keys[K_UP] and not pressed_keys_last[K_UP]:
                pause_idx -= 1
                SoundEffect.play('select_sound',0.35,True)
            if pause_idx<2 and pressed_keys[K_DOWN] and not pressed_keys_last[K_DOWN]:
                pause_idx += 1
                SoundEffect.play('select_sound',0.35,True)


    def Event_Detection():
        global fullscreen
        for event in pygame.event.get():
            if event.type == QUIT:
                set_value('running', False)
                
        if pressed_keys[K_F11] and not pressed_keys_last[K_F11]:
            if not fullscreen:
                pygame.display.set_mode((640*magnitude,480*magnitude), FULLSCREEN|SCALED|DOUBLEBUF|HWSURFACE, 16)
                fullscreen = True
            else:
                pygame.display.set_mode((640*magnitude,480*magnitude), SCALED|DOUBLEBUF|HWSURFACE, 16)
                fullscreen = False
            
    rainbow = 0
    img_idx = 0
    plot = 0
    while get_value('running'):
        try:
            screen.fill((255,255,255))
            FPS.tick(60)
            pressed_keys = pygame.key.get_pressed()
            pressed_mouse = pygame.mouse.get_pressed()
            rainbow += 0.02
            if rainbow >= 2 * math.pi:
                rainbow = 0

            Pause_Update()
            Event_Detection()
            #print(get_value('waveNum'))
            if get_value('menu'):
                screen.fill((0,0,0,0))
                Menu.update(screen, pressed_keys, pressed_keys_last)
                if get_value('player_id')==1:
                    PLAYER = player.REIMU()
                    set_value('player_id',0)
                    plot = Plot.Stage_2('REIMU')
                elif get_value('player_id')==2:
                    PLAYER = player.MARISA()
                    plot = Plot.Stage_2("MARISA")
                    set_value('player_id',0)
                if get_value('load_level'):
                    set_value('load_level',False)
                    LEVEL_CONTROLLER = level.stagecontroller_stage_editor()
                    LEVEL_CONTROLLER.__init__(node_lists=Menu.node_lists)

            elif get_value('pause'):
                if get_value('finish'):
                    score_get_text = textfont.render("Your Result is: "+str(get_value('hi_score')),True,WHITE)
                    score_get_text_shadow = textfont.render("Your Result is: "+str(get_value('hi_score')),True,BLACK)
                    new_surface = pygame.Surface((500,200)).convert_alpha()
                    new_surface.fill((0,0,0,0))
                    for i in range(-1,2):
                        for j in range(-1,2):
                            new_surface.blit(score_get_text_shadow,(10+i*2,20+j*2))
                    new_surface.blit(score_get_text,(10,20))
                    set_value('final_result',new_surface)
                if get_value('deadpause'):
                    ps = STAGE
                    ps = pygame.transform.rotozoom(ps, 0, 0.5)
                    ps = pygame.transform.rotozoom(ps, 0, 2).convert_alpha()
                    ps.blit(mask1, (0,0))
                    set_value('pause_screen', ps)
                    set_value('deadpause', False)
                    pygame.mixer.music.pause()
                if get_value('unPause'):
                    set_value('pause', False)
                    set_value('unPause',False)
                UI.pauseScreen(screen,pause_idx)
                UI.display_UI(screen, PLAYER)
                pygame.draw.rect(screen, functions.get_rainbow_color(rainbow), screen_rect, 3, 2)
        
            if not (get_value('menu') or get_value('pause') or get_value('edit_mode')):
                if get_value('stage_Num')==2 and get_value('change'):
                    LEVEL_CONTROLLER = level.stagecontroller_stage_2()
                    frame = -100
                    set_value('frame',-100)
                    set_value('waveNum',0)
                    set_value('change',False)
                frame = get_value('frame')+1
                set_value('frame', frame)
                set_value('grazing',False)
                set_value('item_getting',False)
                set_value('enemypos',(-100,-100,10000))
                if pressed_keys[K_z] and not get_value('plot'):
                    set_value('player_attack', True)
                else:
                    set_value('player_attack', False)
                
                Points_Update()
                
                if get_value('screen_shaking'):
                    speed = randint(-3, 3)
                else:
                    speed = 0
                backgrounds.update(STAGE, speed)
                    
                LEVEL_CONTROLLER.update(ENEMIES, ENEMY_BULLETS, EFFECTS, backgrounds, frame)
                ENEMIES.update(STAGE, ENEMY_BULLETS, ENEMY_LASERS, ITEMS, EFFECTS, backgrounds)
                FLOATGUNS.update(STAGE, PLAYER, PLAYER_BULLETS, PLAYER_LASERS, pressed_keys, pressed_keys_last)
                PLAYER.update(PLAYER_BULLETS,PLAYER_LASERS, frame, pressed_keys, pressed_keys_last, EFFECTS, ENEMY_BULLETS, ITEMS, FLOATGUNS)
                set_value('PLAYER_rect', pygame.Rect(PLAYER.rect.centerx-30, PLAYER.rect.centery-60, 60, 90))
                if EFFECTS1:
                    EFFECTS1.update(STAGE)
                PLAYER_BULLETS.update(STAGE)
                PLAYER_LASERS.update(STAGE,ENEMIES)
                ITEMS.update(STAGE, PLAYER, EFFECTS)

                if get_value('shift_down'):
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

                if get_value('shift_down'):
                    functions.drawImage(point1, PLAYER.rect.center, angle, STAGE)
                    
                functions.missDetect(PLAYER, PLAYER_LASERS, ENEMIES, ENEMY_BULLETS, EFFECTS, wave, ITEMS)
                functions.hitEnemy(ENEMIES, PLAYER, PLAYER_BULLETS, EFFECTS)
                functions.laser_collision(ENEMIES, PLAYER_LASERS, EFFECTS)
                set_value('number of bullets' ,len(ENEMY_BULLETS))
                countFPS(FPS.get_fps())
                
                EFFECTS.update(STAGE)
                if get_value('boss_effect'):
                    get_value('boss_effect').update(STAGE, PLAYER)
                if get_value('booming') or get_value('plot'):
                    STAGE.blit(mask, (0,0))
                if frame>-100 and frame < 0:
                    mask2.set_alpha(255-((frame+100)/100*255))
                    STAGE.blit(mask2, (0,0))
                if frame>0 and frame<380 and get_value('waveNum')==11:
                    mask2.set_alpha((frame)/280*255)
                    STAGE.blit(mask2, (0,0))
                screen.blit(STAGE, (32*magnitude, 16*magnitude))
                wave.update(screen, EFFECTS)
                UI.display_UI(screen, PLAYER)
                
                pygame.draw.rect(screen, functions.get_rainbow_color(rainbow), screen_rect, 5, 3)
                if get_value('plot'):
                    if pressed_keys[K_z] and not pressed_keys_last[K_z]:
                        plot.update()
                    if get_value('plot'):
                        plot.draw(screen)
            if pressed_keys[K_F10] and not pressed_keys_last[K_F10]:
                filename = 'capture'+str(img_idx)+'.png'
                img_idx+=1
                pygame.image.save(screen, filename)
            pressed_keys_last=pressed_keys
            pressed_mouse_last=pressed_mouse
            pygame.display.update()
        except Exception as e:
            print(e)
            set_value('running', False)

    if get_value('username'):
        Login_System.Update_Highest_Score(get_value('username'), get_value('hi_score'))
    #db.CLEAR()
    pygame.quit()

if __name__ == '__main__':
    main()