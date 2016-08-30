import os
import pygame as pg
from pygame.ftfont import Font

from . import tools


SCREEN_SIZE = (600, 800)
BOARD_RECT = pg.Rect(60,160,480,480)


ORIGINAL_CAPTION = "Sliding Square Character Puzzle"

pg.mixer.pre_init(44100, -16, 1, 512)

pg.init()
os.environ['SDL_VIDEO_CENTERED'] = "TRUE"
pg.display.set_caption(ORIGINAL_CAPTION)
SCREEN = pg.display.set_mode(SCREEN_SIZE)
SCREEN_RECT = SCREEN.get_rect()

CHARACTERS = {'\u70ce':'n. light ',
             '\u56e7':'adj. embarrassed',
             '\u69d1':'n. plum ',
             '\u52e5':'adj. stubborn',
             '\u5ded':'n. kung fu',
             '\u5ad1':'n. donot',
             '\u604f':'n. desire',
             '\u56cd':'double happiness ',
             '\u9750':'n. thunder',
             '\u8f5f':'vi. explode',
             '\u99ab':'strong and pervasive fragrance',
             '\u9f98':'many dragons',
             '\u7fb4':'the smell of mutton',
             '\u8219':'make mischief',
             '\u96e6':'n. set',
             '\u71da':'n. fire'}


GFX   = tools.load_all_gfx(os.path.join("resources", "graphics"))
FONTS = tools.load_all_fonts(os.path.join("resources", "fonts"))
SFX = tools.load_all_sfx(os.path.join("resources", "sound"))
MUSIC = tools.load_all_music(os.path.join("resources", "music"))

font = FONTS['simfang']
game_font = Font(font,BOARD_RECT.width)
