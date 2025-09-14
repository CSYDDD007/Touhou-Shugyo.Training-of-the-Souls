ob = {
    'Login_Valid': False,
    'running': True,
    'Debug': False,
    'BGM_Volume': 100,
    'SE_Volume': 80,
    'state': 'menu',
    'enemy_draw_healthbar': True,
    'enemy_show_health_value': True,
    'damage_show': False,
    'enter_game_effect': None,
    'ranks':[],
    'stages':[]
}
def set_value(key, value):
    global ob
    ob[key] = value

def get_value(key):
    try:
        return ob[key]
    except:
        return None
        print('read '+key+' error\r\n')