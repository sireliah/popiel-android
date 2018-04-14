
from kivy.config import Config
Config.set('graphics', 'width', '1024')
Config.set('graphics', 'width', '768')
Config.set('graphics', 'fullscreen', '0')
Config.write()

DEBUG = True

LEVEL_WIDTH = 1000
LEVEL_HEIGHT = 600

GRAVITY = 0.5

JUMP_HEIGHT = 200.0

MOUSE_LIFESPAN = 10.0
MOUSE_SIGHT = 100.0
MAX_MICE_NUM = 12
