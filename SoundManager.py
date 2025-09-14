import pygame
pygame.mixer.init()
pygame.mixer.set_num_channels(60)
from global_var import *

sound_list = {}
bgm_lists = {
    'Menu':'resource/BGM/01 - Concentration.mp3',
    'Stage_1_Mid':'resource/BGM/02 - As a Normal Day.mp3',
    'Stage_1_Final':'resource/BGM/03 - Sweat for Peace.mp3'
}
def BGM_Play(bgm_name, times=1, volume=1.0):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(bgm_lists[bgm_name])
    pygame.mixer.music.set_volume(volume*get_value('BGM_Volume')/100)
    pygame.mixer.music.play(times)

def addBGM(bgm_name, path):
    global bgm_lists
    if bgm_name in list(bgm_lists.keys()):
        return
    bgm_lists[bgm_name]=path

def play(sound_name, volume=1.0,isStop=False):
    if isStop:
        stop(sound_name)
    sound_list[sound_name].set_volume(volume*get_value('SE_Volume')/100)
    sound_list[sound_name].play()

def stop(sound_name):
    sound_list[sound_name].stop()

def addSound(sound_name, path):
    global sound_list
    if sound_name in list(sound_list.keys()):
        return
    sound_list[sound_name]=pygame.mixer.Sound(path)

def loadSound():
    global sound_list
    sound_list['pause_sound']=pygame.mixer.Sound('resource/sound/se_pause.wav')
    sound_list['select_sound']=pygame.mixer.Sound('resource/sound/se_select00.wav')
    sound_list['ok_sound']=pygame.mixer.Sound('resource/sound/se_ok00.wav')
    sound_list['cancel_sound']=pygame.mixer.Sound('resource/sound/se_cancel00.wav')
    sound_list['invalid_sound']=pygame.mixer.Sound('resource/sound/se_invalid.wav')
    sound_list['miss_sound']=pygame.mixer.Sound('resource/sound/se_pldead00.wav')
    sound_list['shoot_sound']=pygame.mixer.Sound('resource/sound/se_plst00.wav')
    sound_list['hit_sound1']=pygame.mixer.Sound('resource/sound/se_damage00.wav')
    sound_list['hit_sound2']=pygame.mixer.Sound('resource/sound/se_damage01.wav')
    sound_list['enemyDead_sound']=pygame.mixer.Sound('resource/sound/se_enep00.wav')
    sound_list['bossDead_sound']=pygame.mixer.Sound('resource/sound/se_enep01.wav')
    sound_list['enemyShoot_sound1']=pygame.mixer.Sound('resource/sound/se_tan00.wav')
    sound_list['enemyShoot_sound2']=pygame.mixer.Sound('resource/sound/se_tan01.wav')
    sound_list['enemyShoot_sound3']=pygame.mixer.Sound('resource/sound/se_tan02.wav')
    sound_list['item_get']=pygame.mixer.Sound('resource/sound/se_item00.wav')
    sound_list['kira_sound']=pygame.mixer.Sound('resource/sound/se_kira00.wav')
    sound_list['kira_sound1']=pygame.mixer.Sound('resource/sound/se_kira01.wav')
    sound_list['powerup_sound']=pygame.mixer.Sound('resource/sound/se_powerup.wav')
    sound_list['timeout_sound1']=pygame.mixer.Sound('resource/sound/se_timeout.wav')
    sound_list['timeout_sound2']=pygame.mixer.Sound('resource/sound/se_timeout2.wav')
    sound_list['bonus_sound']=pygame.mixer.Sound('resource/sound/se_bonus.wav')
    sound_list['spellStart_sound']=pygame.mixer.Sound('resource/sound/se_ch02.wav')
    sound_list['spell_sound']=pygame.mixer.Sound('resource/sound/se_cat00.wav')
    sound_list['graze_sound']=pygame.mixer.Sound('resource/sound/se_graze.wav')
    sound_list['spellEnd_sound']=pygame.mixer.Sound('resource/sound/se_enep02.wav')
    sound_list['playerSpell_sound']=pygame.mixer.Sound('resource/sound/se_nep00.wav')
    sound_list['cardget_sound']=pygame.mixer.Sound('resource/sound/se_cardget.wav')