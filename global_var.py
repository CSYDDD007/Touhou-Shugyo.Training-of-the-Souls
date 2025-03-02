ob = {}
def __init__():
    global ob

def set_value(key, value):
    ob[key] = value

def get_value(key):
    try:
        return ob[key]
    except:
        return None
        print('read '+key+' error\r\n')