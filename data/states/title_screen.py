import pygame as pg
from .. import tools
from ..prepare import GFX, SCREEN_RECT, FONTS,MUSIC
from ..components.animation import Animation, Task
from ..components.labels import Blinker

song = MUSIC['bg']
pg.mixer.music.load(song)
pg.mixer.music.play(-1)


class TitleScreen(tools._State):
    def __init__(self):
        super(TitleScreen, self).__init__()
        self.animations = pg.sprite.Group()
        self.labels = pg.sprite.Group()
        self.bg = GFX['title_screen']
        midbottom = (SCREEN_RECT.centerx, SCREEN_RECT.bottom - 40)
        timespan = 1000
        self.hint = Blinker("Press any key to start", {"midbottom": midbottom},
                                        500, text_color='black', font_size = 40,font_path = FONTS['ALGER'])
        task = Task(self.labels.add, timespan, args=(self.hint,))
        self.animations.add(task)

    def startup(self, persist):
        self.persist = persist
        self.bg = GFX['title_screen']

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type ==pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.quit = True
            else:
                self.done = True
                self.next = 'MODE'
        elif event.type == pg.MOUSEBUTTONUP:
            self.done = True
            self.next = 'MODE'



                
    def update(self, dt):
        self.animations.update(dt)
        self.labels.update(dt)
        
    def draw(self, surface):
        surface.blit(self.bg, (0,0))
        self.labels.draw(surface)


