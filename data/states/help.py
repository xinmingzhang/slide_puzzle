import pygame as pg
from .. import tools
from ..prepare import GFX, SCREEN_SIZE, FONTS
from ..components.animation import Animation, Task
from ..components.labels import Blinker


class Help(tools._State):
    def __init__(self):
        super(Help, self).__init__()



    def startup(self, persist):
        self.persist = persist
        self.bg = GFX['help_bg']
        self.labels = pg.sprite.Group()
        self.animations = pg.sprite.Group()
        midbottom = (SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] - 10)
        timespan = 1000
        self.hint = Blinker("Press key x to go back", {"midbottom": midbottom},
                            500, text_color='black', font_size=30, font_path=FONTS['ALGER'])

        task = Task(self.labels.add, timespan, args=(self.hint,))
        self.animations.add(task)

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_x:
                self.done = True
                self.next = 'MODE'


    def draw(self,surface):
        surface.blit(self.bg,(0,0))
        self.labels.draw(surface)

    def update(self,dt):
        self.animations.update(dt)
        self.labels.update(dt)