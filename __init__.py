import setting
setting.install_packages()
import Login_Platform
Login_Platform.main()
from global_var import *
import sys
if not get_value('Login_Valid'):
    sys.exit()
import pygame
import th_SBA
th_SBA.main()
pygame.init()
import Editor
Editor.main()