import subprocess
import sys

def install(file):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r",file])
    
def upgrade():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

def install_packages():
    try:
        upgrade()
        install('requirements.txt')
    except:
        sys.exit()